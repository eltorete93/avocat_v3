"""
OCR Processor Cloud Function
Procesa documentos usando Google Cloud Vision API para extraer texto
"""

import base64
import json
import logging
import os
from typing import Dict, Any

from google.cloud import vision
from google.cloud import storage
from google.cloud import pubsub_v1

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar clientes
vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

def process_document(event: Dict[str, Any], context) -> str:
    """
    Función principal que procesa documentos para OCR
    
    Args:
        event: Evento de Cloud Storage
        context: Contexto de la función
    
    Returns:
        str: Resultado del procesamiento
    """
    try:
        # Extraer información del evento
        bucket_name = event['bucket']
        file_name = event['name']
        
        logger.info(f"Procesando documento: {file_name} en bucket: {bucket_name}")
        
        # Descargar archivo del bucket
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Leer contenido del archivo
        content = blob.download_as_bytes()
        
        # Crear imagen para Vision API
        image = vision.Image(content=content)
        
        # Realizar OCR
        response = vision_client.text_detection(image=image)
        
        if response.error.message:
            raise Exception(f"Error en Vision API: {response.error.message}")
        
        # Extraer texto
        texts = response.text_annotations
        if texts:
            extracted_text = texts[0].description
            logger.info(f"Texto extraído exitosamente de {file_name}")
            
            # Guardar resultado en bucket de resultados
            result_bucket_name = os.environ.get('RESULT_BUCKET_NAME', 'ocr-results')
            result_bucket = storage_client.bucket(result_bucket_name)
            
            # Crear nombre del archivo de resultado
            result_file_name = f"ocr_results/{file_name.replace('.', '_')}_ocr.txt"
            result_blob = result_bucket.blob(result_file_name)
            
            # Guardar texto extraído
            result_blob.upload_from_string(extracted_text, content_type='text/plain')
            
            # Publicar mensaje en Pub/Sub para procesamiento posterior
            topic_name = os.environ.get('PUBSUB_TOPIC_NAME', 'document-processing')
            topic_path = publisher.topic_path(os.environ.get('GOOGLE_CLOUD_PROJECT'), topic_name)
            
            message_data = {
                'file_name': file_name,
                'ocr_result_path': result_file_name,
                'extracted_text': extracted_text[:1000],  # Primeros 1000 caracteres
                'status': 'ocr_completed'
            }
            
            publisher.publish(topic_path, json.dumps(message_data).encode('utf-8'))
            
            return f"OCR completado exitosamente para {file_name}"
        else:
            logger.warning(f"No se encontró texto en {file_name}")
            return f"No se encontró texto en {file_name}"
            
    except Exception as e:
        logger.error(f"Error procesando documento {file_name}: {str(e)}")
        raise e

def classify_document_type(text: str) -> str:
    """
    Clasifica el tipo de documento basado en el contenido extraído
    
    Args:
        text: Texto extraído del documento
    
    Returns:
        str: Tipo de documento identificado
    """
    text_lower = text.lower()
    
    # Clasificación simple basada en palabras clave
    if any(word in text_lower for word in ['factura', 'invoice', 'bill', 'recibo']):
        return 'invoice'
    elif any(word in text_lower for word in ['contrato', 'contract', 'acuerdo']):
        return 'contract'
    elif any(word in text_lower for word in ['identificación', 'id', 'passport', 'dni']):
        return 'identification'
    elif any(word in text_lower for word in ['reporte', 'report', 'informe']):
        return 'report'
    else:
        return 'general'
