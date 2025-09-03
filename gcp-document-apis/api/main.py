"""
API Principal para Procesamiento de Documentos
Orquesta todo el flujo de trabajo: OCR, Backup y Extracción de Información
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from google.cloud import storage
from google.cloud import pubsub_v1

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="GCP Document Processing API",
    description="API para procesamiento completo de documentos con OCR, backup y extracción de información",
    version="1.0.0"
)

# Inicializar clientes GCP
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

# Modelos Pydantic
class DocumentUploadResponse(BaseModel):
    message: str
    file_name: str
    upload_path: str
    status: str

class ProcessingStatus(BaseModel):
    file_name: str
    status: str
    ocr_completed: bool
    backup_completed: bool
    extraction_completed: bool
    timestamp: str

class DocumentInfo(BaseModel):
    file_name: str
    document_type: str
    ocr_text: Optional[str]
    extracted_info: Optional[Dict[str, Any]]
    backup_path: Optional[str]

# Configuración
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET_NAME', 'document-processing')
BACKUP_BUCKET = os.environ.get('BACKUP_BUCKET_NAME', 'document-backup')
RESULT_BUCKET = os.environ.get('RESULT_BUCKET_NAME', 'document-results')
PUBSUB_TOPIC = os.environ.get('PUBSUB_TOPIC_NAME', 'document-processing')

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "GCP Document Processing API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "upload": "/upload",
            "status": "/status/{file_name}",
            "info": "/info/{file_name}",
            "list": "/documents",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificación de salud de la API"""
    try:
        # Verificar conexión a GCP
        bucket = storage_client.bucket(STORAGE_BUCKET)
        bucket.reload()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "gcp_connection": "ok",
            "storage_bucket": STORAGE_BUCKET
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Sube un documento y inicia el procesamiento automático
    
    El documento se procesa en el siguiente orden:
    1. OCR usando Google Cloud Vision API
    2. Backup y clasificación en Google Cloud Storage
    3. Extracción de información usando Google Cloud Document AI
    """
    try:
        # Validar archivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nombre de archivo requerido")
        
        # Validar tipo de archivo
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado. Permitidos: {', '.join(allowed_extensions)}"
            )
        
        # Crear nombre único para el archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{file.filename}"
        
        # Subir archivo al bucket de procesamiento
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(unique_filename)
        
        # Leer contenido del archivo
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)
        
        logger.info(f"Documento subido exitosamente: {unique_filename}")
        
        # Iniciar procesamiento en background
        background_tasks.add_task(
            start_document_processing,
            unique_filename,
            file.content_type
        )
        
        return DocumentUploadResponse(
            message="Documento subido exitosamente. El procesamiento ha comenzado.",
            file_name=unique_filename,
            upload_path=f"gs://{STORAGE_BUCKET}/{unique_filename}",
            status="uploaded"
        )
        
    except Exception as e:
        logger.error(f"Error subiendo documento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error subiendo documento: {str(e)}")

async def start_document_processing(file_name: str, content_type: str):
    """
    Inicia el procesamiento del documento en el flujo de trabajo
    
    Args:
        file_name: Nombre del archivo a procesar
        content_type: Tipo de contenido del archivo
    """
    try:
        logger.info(f"Iniciando procesamiento para: {file_name}")
        
        # Publicar mensaje en Pub/Sub para iniciar OCR
        topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)
        
        message_data = {
            'file_name': file_name,
            'content_type': content_type,
            'timestamp': datetime.now().isoformat(),
            'action': 'start_ocr'
        }
        
        publisher.publish(topic_path, json.dumps(message_data).encode('utf-8'))
        logger.info(f"Mensaje publicado en Pub/Sub para: {file_name}")
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento para {file_name}: {str(e)}")

@app.get("/status/{file_name}", response_model=ProcessingStatus)
async def get_processing_status(file_name: str):
    """
    Obtiene el estado del procesamiento de un documento específico
    """
    try:
        # Verificar archivo original
        bucket = storage_client.bucket(STORAGE_BUCKET)
        original_blob = bucket.blob(file_name)
        
        if not original_blob.exists():
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        # Verificar estado de OCR
        ocr_bucket = storage_client.bucket(RESULT_BUCKET)
        ocr_blob = ocr_bucket.blob(f"ocr_results/{file_name.replace('.', '_')}_ocr.txt")
        ocr_completed = ocr_blob.exists()
        
        # Verificar estado de backup
        backup_bucket = storage_client.bucket(BACKUP_BUCKET)
        backup_exists = False
        backup_path = None
        
        # Buscar en diferentes tipos de documento
        for doc_type in ['invoice', 'contract', 'identification', 'report', 'general']:
            blobs = list(backup_bucket.list_blobs(prefix=f"{doc_type}/"))
            for blob in blobs:
                if file_name in blob.name:
                    backup_exists = True
                    backup_path = blob.name
                    break
            if backup_exists:
                break
        
        # Verificar estado de extracción
        extraction_blob = ocr_bucket.blob(f"extracted_info/{file_name.replace('.', '_')}_info.json")
        extraction_completed = extraction_blob.exists()
        
        return ProcessingStatus(
            file_name=file_name,
            status="completed" if all([ocr_completed, backup_exists, extraction_completed]) else "processing",
            ocr_completed=ocr_completed,
            backup_completed=backup_exists,
            extraction_completed=extraction_completed,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo estado para {file_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")

@app.get("/info/{file_name}", response_model=DocumentInfo)
async def get_document_info(file_name: str):
    """
    Obtiene toda la información extraída de un documento
    """
    try:
        # Verificar que el documento existe
        bucket = storage_client.bucket(STORAGE_BUCKET)
        original_blob = bucket.blob(file_name)
        
        if not original_blob.exists():
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        # Obtener texto OCR
        ocr_text = None
        ocr_bucket = storage_client.bucket(RESULT_BUCKET)
        ocr_blob = ocr_bucket.blob(f"ocr_results/{file_name.replace('.', '_')}_ocr.txt")
        
        if ocr_blob.exists():
            ocr_text = ocr_blob.download_as_text()
        
        # Obtener información extraída
        extracted_info = None
        extraction_blob = ocr_bucket.blob(f"extracted_info/{file_name.replace('.', '_')}_info.json")
        
        if extraction_blob.exists():
            extracted_info = json.loads(extraction_blob.download_as_text())
        
        # Determinar tipo de documento
        document_type = "general"
        if extracted_info and 'document_type' in extracted_info:
            document_type = extracted_info['document_type']
        
        # Obtener ruta de backup
        backup_path = None
        backup_bucket = storage_client.bucket(BACKUP_BUCKET)
        
        for doc_type in ['invoice', 'contract', 'identification', 'report', 'general']:
            blobs = list(backup_bucket.list_blobs(prefix=f"{doc_type}/"))
            for blob in blobs:
                if file_name in blob.name:
                    backup_path = blob.name
                    break
            if backup_path:
                break
        
        return DocumentInfo(
            file_name=file_name,
            document_type=document_type,
            ocr_text=ocr_text,
            extracted_info=extracted_info,
            backup_path=backup_path
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo información para {file_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo información: {str(e)}")

@app.get("/documents")
async def list_documents():
    """
    Lista todos los documentos procesados
    """
    try:
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blobs = list(bucket.list_blobs())
        
        documents = []
        for blob in blobs:
            # Obtener información básica del documento
            doc_info = {
                'file_name': blob.name,
                'size': blob.size,
                'created': blob.time_created.isoformat(),
                'content_type': blob.content_type
            }
            
            # Verificar estado de procesamiento
            status = await get_processing_status(blob.name)
            doc_info['status'] = status.status
            
            documents.append(doc_info)
        
        return {
            "total_documents": len(documents),
            "documents": documents
        }
        
    except Exception as e:
        logger.error(f"Error listando documentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listando documentos: {str(e)}")

@app.delete("/documents/{file_name}")
async def delete_document(file_name: str):
    """
    Elimina un documento y todos sus archivos relacionados
    """
    try:
        # Eliminar archivo original
        bucket = storage_client.bucket(STORAGE_BUCKET)
        original_blob = bucket.blob(file_name)
        
        if not original_blob.exists():
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        original_blob.delete()
        
        # Eliminar archivos de OCR
        ocr_bucket = storage_client.bucket(RESULT_BUCKET)
        ocr_blob = ocr_bucket.blob(f"ocr_results/{file_name.replace('.', '_')}_ocr.txt")
        if ocr_blob.exists():
            ocr_blob.delete()
        
        # Eliminar archivos de extracción
        extraction_blob = ocr_bucket.blob(f"extracted_info/{file_name.replace('.', '_')}_info.json")
        if extraction_blob.exists():
            extraction_blob.delete()
        
        # Eliminar archivos de backup
        backup_bucket = storage_client.bucket(BACKUP_BUCKET)
        for doc_type in ['invoice', 'contract', 'identification', 'report', 'general']:
            blobs = list(backup_bucket.list_blobs(prefix=f"{doc_type}/"))
            for blob in blobs:
                if file_name in blob.name:
                    blob.delete()
        
        return {"message": f"Documento {file_name} eliminado exitosamente"}
        
    except Exception as e:
        logger.error(f"Error eliminando documento {file_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error eliminando documento: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("API_PORT", 8000)),
        reload=os.environ.get("DEBUG_MODE", "false").lower() == "true"
    )
