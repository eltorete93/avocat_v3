"""
Information Extractor Cloud Function
Extrae información estructurada de documentos usando Google Cloud Document AI
"""

import json
import logging
import os
from typing import Dict, Any, List

from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from google.cloud import pubsub_v1

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar clientes
documentai_client = documentai.DocumentProcessorServiceClient()
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

def extract_document_info(event: Dict[str, Any], context) -> str:
    """
    Función principal que extrae información estructurada de documentos
    
    Args:
        event: Evento de Pub/Sub con información del documento
        context: Contexto de la función
    
    Returns:
        str: Resultado de la extracción
    """
    try:
        # Decodificar mensaje de Pub/Sub
        if 'data' in event:
            message_data = json.loads(event['data'].decode('utf-8'))
        else:
            message_data = event
            
        file_name = message_data.get('file_name')
        document_type = message_data.get('document_type', 'general')
        
        logger.info(f"Extrayendo información de documento: {file_name}")
        
        # Configurar Document AI
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        location = os.environ.get('DOCUMENT_AI_LOCATION', 'us')
        processor_id = os.environ.get('DOCUMENT_AI_PROCESSOR_ID')
        
        if not processor_id:
            logger.warning("No se configuró PROCESSOR_ID, usando procesador general")
            processor_id = "general-processor"
        
        # Construir nombre del procesador
        processor_name = documentai_client.processor_path(project_id, location, processor_id)
        
        # Descargar documento del bucket
        bucket_name = os.environ.get('STORAGE_BUCKET_NAME', 'document-processing')
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        # Leer contenido del documento
        document_content = blob.download_as_bytes()
        
        # Configurar documento para Document AI
        raw_document = documentai.RawDocument(
            content=document_content,
            mime_type=blob.content_type or 'application/pdf'
        )
        
        # Procesar documento
        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document
        )
        
        result = documentai_client.process_document(request=request)
        document = result.document
        
        # Extraer información estructurada
        extracted_info = extract_structured_data(document, document_type)
        
        # Guardar información extraída
        result_bucket_name = os.environ.get('RESULT_BUCKET_NAME', 'extracted-info')
        result_bucket = storage_client.bucket(result_bucket_name)
        
        # Crear archivo de resultado
        result_file_name = f"extracted_info/{file_name.replace('.', '_')}_info.json"
        result_blob = result_bucket.blob(result_file_name)
        
        # Guardar información extraída como JSON
        result_blob.upload_from_string(
            json.dumps(extracted_info, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        logger.info(f"Información extraída exitosamente de {file_name}")
        
        # Publicar mensaje de extracción completada
        topic_name = os.environ.get('PUBSUB_TOPIC_NAME', 'document-processing')
        topic_path = publisher.topic_path(project_id, topic_name)
        
        extraction_message = {
            'file_name': file_name,
            'extracted_info_path': result_file_name,
            'document_type': document_type,
            'status': 'extraction_completed',
            'extracted_fields': list(extracted_info.keys())
        }
        
        publisher.publish(topic_path, json.dumps(extraction_message).encode('utf-8'))
        
        return f"Extracción completada exitosamente para {file_name}"
        
    except Exception as e:
        logger.error(f"Error extrayendo información de {file_name}: {str(e)}")
        raise e

def extract_structured_data(document: documentai.Document, document_type: str) -> Dict[str, Any]:
    """
    Extrae información estructurada del documento procesado
    
    Args:
        document: Documento procesado por Document AI
        document_type: Tipo de documento
    
    Returns:
        Dict: Información extraída estructurada
    """
    extracted_data = {
        'document_type': document_type,
        'text': document.text,
        'pages': len(document.pages),
        'entities': {},
        'key_value_pairs': {},
        'tables': []
    }
    
    # Extraer entidades
    for entity in document.entities:
        entity_type = entity.type_
        entity_text = entity.mention_text
        
        if entity_type not in extracted_data['entities']:
            extracted_data['entities'][entity_type] = []
        
        extracted_data['entities'][entity_type].append({
            'text': entity_text,
            'confidence': entity.confidence,
            'page_anchor': entity.page_anchor.page if entity.page_anchor else None
        })
    
    # Extraer pares clave-valor
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content
            field_value = form_field.field_value.text_anchor.content
            
            extracted_data['key_value_pairs'][field_name] = {
                'value': field_value,
                'confidence': form_field.field_name.confidence,
                'page': page.page_number
            }
    
    # Extraer tablas
    for page in document.pages:
        for table in page.tables:
            table_data = []
            for row in table.header_rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text_anchor.content)
                table_data.append(row_data)
            
            for row in table.body_rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text_anchor.content)
                table_data.append(row_data)
            
            extracted_data['tables'].append({
                'page': page.page_number,
                'data': table_data
            })
    
    # Extraer información específica por tipo de documento
    if document_type == 'invoice':
        extracted_data.update(extract_invoice_specific_data(document))
    elif document_type == 'contract':
        extracted_data.update(extract_contract_specific_data(document))
    elif document_type == 'identification':
        extracted_data.update(extract_id_specific_data(document))
    
    return extracted_data

def extract_invoice_specific_data(document: documentai.Document) -> Dict[str, Any]:
    """Extrae información específica de facturas"""
    invoice_data = {}
    
    # Buscar campos comunes en facturas
    common_fields = ['invoice_number', 'date', 'total_amount', 'vendor_name', 'customer_name']
    
    for entity in document.entities:
        entity_type = entity.type_.lower()
        if any(field in entity_type for field in common_fields):
            invoice_data[entity_type] = {
                'value': entity.mention_text,
                'confidence': entity.confidence
            }
    
    return {'invoice_specific': invoice_data}

def extract_contract_specific_data(document: documentai.Document) -> Dict[str, Any]:
    """Extrae información específica de contratos"""
    contract_data = {}
    
    # Buscar campos comunes en contratos
    common_fields = ['contract_number', 'start_date', 'end_date', 'parties', 'amount']
    
    for entity in document.entities:
        entity_type = entity.type_.lower()
        if any(field in entity_type for field in common_fields):
            contract_data[entity_type] = {
                'value': entity.mention_text,
                'confidence': entity.confidence
            }
    
    return {'contract_specific': contract_data}

def extract_id_specific_data(document: documentai.Document) -> Dict[str, Any]:
    """Extrae información específica de documentos de identificación"""
    id_data = {}
    
    # Buscar campos comunes en IDs
    common_fields = ['id_number', 'name', 'date_of_birth', 'expiry_date', 'nationality']
    
    for entity in document.entities:
        entity_type = entity.type_.lower()
        if any(field in entity_type for field in common_fields):
            id_data[entity_type] = {
                'value': entity.mention_text,
                'confidence': entity.confidence
            }
    
    return {'id_specific': id_data}
