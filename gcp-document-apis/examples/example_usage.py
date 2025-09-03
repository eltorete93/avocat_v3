"""
Ejemplo de uso de las GCP Document Processing APIs
Este script demuestra cómo interactuar con la API para procesar documentos
"""

import requests
import json
import time
import os
from typing import Dict, Any

class DocumentProcessorClient:
    """Cliente para interactuar con la API de procesamiento de documentos"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """
        Sube un documento para procesamiento
        
        Args:
            file_path: Ruta al archivo a subir
            
        Returns:
            Dict con la respuesta de la API
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(f"{self.base_url}/upload", files=files)
            response.raise_for_status()
            
        return response.json()
    
    def get_processing_status(self, file_name: str) -> Dict[str, Any]:
        """
        Obtiene el estado del procesamiento de un documento
        
        Args:
            file_name: Nombre del archivo
            
        Returns:
            Dict con el estado del procesamiento
        """
        response = self.session.get(f"{self.base_url}/status/{file_name}")
        response.raise_for_status()
        
        return response.json()
    
    def get_document_info(self, file_name: str) -> Dict[str, Any]:
        """
        Obtiene toda la información extraída de un documento
        
        Args:
            file_name: Nombre del archivo
            
        Returns:
            Dict con toda la información del documento
        """
        response = self.session.get(f"{self.base_url}/info/{file_name}")
        response.raise_for_status()
        
        return response.json()
    
    def list_documents(self) -> Dict[str, Any]:
        """
        Lista todos los documentos procesados
        
        Returns:
            Dict con la lista de documentos
        """
        response = self.session.get(f"{self.base_url}/documents")
        response.raise_for_status()
        
        return response.json()
    
    def delete_document(self, file_name: str) -> Dict[str, Any]:
        """
        Elimina un documento y todos sus archivos relacionados
        
        Args:
            file_name: Nombre del archivo
            
        Returns:
            Dict con la confirmación de eliminación
        """
        response = self.session.delete(f"{self.base_url}/documents/{file_name}")
        response.raise_for_status()
        
        return response.json()
    
    def wait_for_completion(self, file_name: str, timeout: int = 300, check_interval: int = 10) -> Dict[str, Any]:
        """
        Espera a que el procesamiento de un documento se complete
        
        Args:
            file_name: Nombre del archivo
            timeout: Tiempo máximo de espera en segundos
            check_interval: Intervalo entre verificaciones en segundos
            
        Returns:
            Dict con el estado final del procesamiento
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_processing_status(file_name)
            
            if status['status'] == 'completed':
                print(f"✅ Procesamiento completado para {file_name}")
                return status
            
            print(f"⏳ Procesando {file_name}... OCR: {status['ocr_completed']}, "
                  f"Backup: {status['backup_completed']}, Extracción: {status['extraction_completed']}")
            
            time.sleep(check_interval)
        
        raise TimeoutError(f"Tiempo de espera agotado para {file_name}")

def main():
    """Función principal de ejemplo"""
    
    # Configurar cliente
    api_url = os.environ.get('API_URL', 'http://localhost:8000')
    client = DocumentProcessorClient(api_url)
    
    print("🚀 GCP Document Processing API - Ejemplo de Uso")
    print("=" * 50)
    
    try:
        # 1. Verificar estado de la API
        print("\n1. Verificando estado de la API...")
        health_response = client.session.get(f"{api_url}/health")
        if health_response.status_code == 200:
            print("✅ API funcionando correctamente")
        else:
            print("❌ API no disponible")
            return
        
        # 2. Listar documentos existentes
        print("\n2. Listando documentos existentes...")
        documents = client.list_documents()
        print(f"📄 Total de documentos: {documents['total_documents']}")
        
        for doc in documents['documents'][:5]:  # Mostrar solo los primeros 5
            print(f"   - {doc['file_name']} ({doc['status']})")
        
        # 3. Subir un documento de ejemplo (si existe)
        example_file = "example_document.pdf"
        if os.path.exists(example_file):
            print(f"\n3. Subiendo documento de ejemplo: {example_file}")
            
            upload_response = client.upload_document(example_file)
            file_name = upload_response['file_name']
            
            print(f"✅ Documento subido: {file_name}")
            print(f"   Ruta: {upload_response['upload_path']}")
            
            # 4. Esperar a que se complete el procesamiento
            print(f"\n4. Esperando procesamiento de {file_name}...")
            
            try:
                final_status = client.wait_for_completion(file_name, timeout=600)  # 10 minutos
                print(f"✅ Procesamiento completado en {final_status['timestamp']}")
                
                # 5. Obtener información completa del documento
                print(f"\n5. Obteniendo información de {file_name}...")
                
                document_info = client.get_document_info(file_name)
                
                print(f"📋 Tipo de documento: {document_info['document_type']}")
                print(f"📝 Texto OCR: {len(document_info.get('ocr_text', ''))} caracteres")
                
                if document_info.get('extracted_info'):
                    extracted = document_info['extracted_info']
                    print(f"🏷️  Entidades encontradas: {len(extracted.get('entities', {}))}")
                    print(f"🔑 Pares clave-valor: {len(extracted.get('key_value_pairs', {}))}")
                    print(f"📊 Tablas encontradas: {len(extracted.get('tables', []))}")
                
                print(f"💾 Ruta de backup: {document_info.get('backup_path', 'N/A')}")
                
            except TimeoutError as e:
                print(f"⏰ {e}")
                print("El procesamiento puede estar en curso. Verifica más tarde.")
            
        else:
            print(f"\n3. Archivo de ejemplo {example_file} no encontrado")
            print("   Crea un archivo PDF para probar la funcionalidad")
        
        # 6. Mostrar información de la API
        print(f"\n6. Información de la API:")
        print(f"   Base URL: {api_url}")
        print(f"   Endpoints disponibles:")
        print(f"   - POST /upload - Subir documentos")
        print(f"   - GET /status/{'{file_name}'} - Estado del procesamiento")
        print(f"   - GET /info/{'{file_name}'} - Información del documento")
        print(f"   - GET /documents - Listar documentos")
        print(f"   - DELETE /documents/{'{file_name}'} - Eliminar documento")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("   Verifica que la API esté ejecutándose y sea accesible")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def create_example_document():
    """Crea un documento de ejemplo para pruebas"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "example_document.pdf"
        
        # Crear PDF de ejemplo
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, "FACTURA DE EJEMPLO")
        c.drawString(100, 720, "Número: INV-001")
        c.drawString(100, 690, "Fecha: 2023-12-01")
        c.drawString(100, 660, "Cliente: Cliente Ejemplo")
        c.drawString(100, 630, "Total: $1,000.00")
        c.drawString(100, 600, "Descripción: Servicios de ejemplo")
        c.save()
        
        print(f"✅ Documento de ejemplo creado: {filename}")
        return filename
        
    except ImportError:
        print("⚠️  reportlab no está instalado. Instala con: pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Error creando documento de ejemplo: {e}")
        return None

if __name__ == "__main__":
    # Intentar crear documento de ejemplo si no existe
    if not os.path.exists("example_document.pdf"):
        create_example_document()
    
    # Ejecutar ejemplo principal
    main()
