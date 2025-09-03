"""
Backup Manager Cloud Function
Gestiona el backup y clasificación automática de documentos en Google Cloud Storage
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any

from google.cloud import storage
from google.cloud import pubsub_v1

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar clientes
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

def backup_document(event: Dict[str, Any], context) -> str:
    """
    Función principal que gestiona el backup y clasificación de documentos
    
    Args:
        event: Evento de Pub/Sub con información del documento
        context: Contexto de la función
    
    Returns:
        str: Resultado del backup
    """
    try:
        # Decodificar mensaje de Pub/Sub
        if 'data' in event:
            message_data = json.loads(event['data'].decode('utf-8'))
        else:
            message_data = event
            
        file_name = message_data.get('file_name')
        ocr_result_path = message_data.get('ocr_result_path')
        document_type = message_data.get('document_type', 'general')
        
        logger.info(f"Procesando backup para documento: {file_name}")
        
        # Configurar buckets
        source_bucket_name = os.environ.get('STORAGE_BUCKET_NAME', 'document-processing')
        backup_bucket_name = os.environ.get('BACKUP_BUCKET_NAME', 'document-backup')
        
        source_bucket = storage_client.bucket(source_bucket_name)
        backup_bucket = storage_client.bucket(backup_bucket_name)
        
        # Crear estructura de directorios para backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{document_type}/{timestamp}/{file_name}"
        
        # Copiar documento original al bucket de backup
        source_blob = source_bucket.blob(file_name)
        backup_blob = backup_bucket.blob(backup_path)
        
        # Copiar archivo
        backup_bucket.copy_blob(source_blob, backup_bucket, backup_path)
        logger.info(f"Documento original copiado a: {backup_path}")
        
        # Si hay resultado de OCR, también hacer backup
        if ocr_result_path:
            ocr_backup_path = f"{document_type}/{timestamp}/{file_name.replace('.', '_')}_ocr.txt"
            ocr_source_blob = source_bucket.blob(ocr_result_path)
            ocr_backup_blob = backup_bucket.blob(ocr_backup_path)
            
            backup_bucket.copy_blob(ocr_source_blob, backup_bucket, ocr_backup_path)
            logger.info(f"Resultado OCR copiado a: {ocr_backup_path}")
        
        # Crear metadatos del backup
        metadata = {
            'original_file': file_name,
            'backup_timestamp': timestamp,
            'document_type': document_type,
            'backup_path': backup_path,
            'ocr_result_path': ocr_backup_path if ocr_result_path else None,
            'status': 'backup_completed'
        }
        
        # Guardar metadatos como archivo JSON
        metadata_path = f"{document_type}/{timestamp}/metadata.json"
        metadata_blob = backup_bucket.blob(metadata_path)
        metadata_blob.upload_from_string(
            json.dumps(metadata, indent=2),
            content_type='application/json'
        )
        
        # Publicar mensaje de backup completado
        topic_name = os.environ.get('PUBSUB_TOPIC_NAME', 'document-processing')
        topic_path = publisher.topic_path(os.environ.get('GOOGLE_CLOUD_PROJECT'), topic_name)
        
        backup_message = {
            'file_name': file_name,
            'backup_path': backup_path,
            'document_type': document_type,
            'timestamp': timestamp,
            'status': 'backup_completed'
        }
        
        publisher.publish(topic_path, json.dumps(backup_message).encode('utf-8'))
        
        logger.info(f"Backup completado exitosamente para {file_name}")
        return f"Backup completado para {file_name} en {backup_path}"
        
    except Exception as e:
        logger.error(f"Error en backup para {file_name}: {str(e)}")
        raise e

def organize_by_document_type(document_type: str, file_name: str) -> str:
    """
    Organiza documentos por tipo en el bucket de backup
    
    Args:
        document_type: Tipo de documento identificado
        file_name: Nombre del archivo
    
    Returns:
        str: Ruta organizada del documento
    """
    # Mapeo de tipos de documento a directorios
    type_mapping = {
        'invoice': 'facturas',
        'contract': 'contratos',
        'identification': 'identificaciones',
        'report': 'reportes',
        'general': 'general'
    }
    
    # Obtener directorio correspondiente
    directory = type_mapping.get(document_type, 'general')
    
    # Crear ruta organizada
    timestamp = datetime.now().strftime('%Y%m%d')
    organized_path = f"{directory}/{timestamp}/{file_name}"
    
    return organized_path

def cleanup_old_backups(bucket_name: str, days_to_keep: int = 30):
    """
    Limpia backups antiguos para ahorrar espacio
    
    Args:
        bucket_name: Nombre del bucket de backup
        days_to_keep: Días a mantener los backups
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        blobs = bucket.list_blobs()
        for blob in blobs:
            # Verificar fecha de creación
            if blob.time_created < cutoff_date:
                blob.delete()
                logger.info(f"Backup antiguo eliminado: {blob.name}")
                
    except Exception as e:
        logger.error(f"Error limpiando backups antiguos: {str(e)}")
