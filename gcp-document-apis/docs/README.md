# Documentación de GCP Document Processing APIs

## 📋 Descripción General

Este sistema proporciona APIs completas para el procesamiento de documentos en Google Cloud Platform, incluyendo:

1. **OCR (Reconocimiento Óptico de Caracteres)** usando Google Cloud Vision API
2. **Backup automático** con clasificación en Google Cloud Storage
3. **Extracción de información estructurada** usando Google Cloud Document AI

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API REST      │    │  Cloud Functions │    │  Google Cloud   │
│   (FastAPI)     │◄──►│                  │◄──►│  Services       │
│                 │    │  • OCR Processor │    │                 │
│                 │    │  • Backup Mgr    │    │ • Vision API    │
│                 │    │  • Info Extractor│    │ • Document AI   │
└─────────────────┘    └──────────────────┘    │ • Storage       │
                                               │ • Pub/Sub       │
                                               └─────────────────┘
```

## 🚀 Flujo de Trabajo

### 1. Subida de Documento
- El usuario sube un documento a través de la API REST
- El documento se almacena en Google Cloud Storage
- Se inicia el procesamiento automático

### 2. Procesamiento OCR
- Cloud Function se activa automáticamente
- Google Cloud Vision API extrae texto del documento
- El resultado se guarda en el bucket de resultados

### 3. Backup y Clasificación
- Cloud Function de backup se activa
- El documento se clasifica automáticamente por tipo
- Se crea una copia de seguridad organizada

### 4. Extracción de Información
- Cloud Function de extracción se activa
- Google Cloud Document AI analiza el documento
- Se extrae información estructurada (entidades, campos, tablas)

## 📚 Endpoints de la API

### POST /upload
Sube un documento y inicia el procesamiento automático.

**Parámetros:**
- `file`: Archivo a procesar (PDF, JPG, PNG, TIFF, BMP)

**Respuesta:**
```json
{
  "message": "Documento subido exitosamente. El procesamiento ha comenzado.",
  "file_name": "20231201_143022_documento.pdf",
  "upload_path": "gs://bucket/documento.pdf",
  "status": "uploaded"
}
```

### GET /status/{file_name}
Obtiene el estado del procesamiento de un documento.

**Respuesta:**
```json
{
  "file_name": "20231201_143022_documento.pdf",
  "status": "completed",
  "ocr_completed": true,
  "backup_completed": true,
  "extraction_completed": true,
  "timestamp": "2023-12-01T14:30:22"
}
```

### GET /info/{file_name}
Obtiene toda la información extraída de un documento.

**Respuesta:**
```json
{
  "file_name": "20231201_143022_documento.pdf",
  "document_type": "invoice",
  "ocr_text": "Texto extraído del documento...",
  "extracted_info": {
    "document_type": "invoice",
    "entities": {
      "invoice_number": [
        {
          "text": "INV-001",
          "confidence": 0.95
        }
      ]
    },
    "key_value_pairs": {
      "total_amount": {
        "value": "$1,000.00",
        "confidence": 0.92
      }
    }
  },
  "backup_path": "invoice/20231201_143022/documento.pdf"
}
```

### GET /documents
Lista todos los documentos procesados.

### DELETE /documents/{file_name}
Elimina un documento y todos sus archivos relacionados.

## 🔧 Configuración

### Variables de Entorno

```bash
# GCP Configuration
GOOGLE_CLOUD_PROJECT=tu-proyecto-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# Cloud Storage
STORAGE_BUCKET_NAME=document-processing-bucket
BACKUP_BUCKET_NAME=document-backup-bucket
RESULT_BUCKET_NAME=document-results-bucket

# Document AI
DOCUMENT_AI_LOCATION=us
DOCUMENT_AI_PROCESSOR_ID=tu-processor-id

# Pub/Sub
PUBSUB_TOPIC_NAME=document-processing-topic

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=false
```

### Service Account

El sistema requiere un service account con los siguientes roles:
- `roles/storage.admin`
- `roles/vision.admin`
- `roles/documentai.admin`
- `roles/pubsub.admin`

## 🚀 Despliegue

### 1. Preparación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar gcloud
gcloud auth login
gcloud config set project tu-proyecto-id
```

### 2. Despliegue Automático
```bash
# Ejecutar script de despliegue
chmod +x scripts/deploy.sh
./scripts/deploy.sh tu-proyecto-id
```

### 3. Despliegue Manual

#### Infraestructura
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

#### API
```bash
cd api
docker build -t gcr.io/tu-proyecto-id/document-api:latest .
docker push gcr.io/tu-proyecto-id/document-api:latest
gcloud run deploy document-processing-api --image gcr.io/tu-proyecto-id/document-api:latest
```

## 📊 Monitoreo y Logs

### Cloud Logging
Todas las funciones y la API generan logs estructurados en Google Cloud Logging.

### Métricas
- Tiempo de procesamiento por documento
- Tasa de éxito de OCR
- Uso de recursos de Cloud Functions
- Latencia de la API

## 🔒 Seguridad

### Autenticación
- La API principal es pública para facilitar pruebas
- En producción, configurar autenticación con IAM

### Autorización
- Las Cloud Functions usan service accounts con permisos mínimos
- Acceso a buckets restringido por políticas IAM

### Encriptación
- Todos los datos se encriptan en tránsito y en reposo
- Las claves de encriptación son gestionadas por Google Cloud

## 🧪 Testing

### Pruebas Locales
```bash
# Ejecutar API localmente
cd api
uvicorn main:app --reload

# Probar endpoints
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@documento.pdf"
```

### Pruebas de Integración
```bash
# Ejecutar tests
pytest tests/
```

## 📈 Escalabilidad

### Cloud Functions
- Escalado automático basado en demanda
- Límite configurable de instancias concurrentes

### Cloud Run
- Escalado a cero cuando no hay tráfico
- Escalado automático hasta 1000 instancias

### Storage
- Los buckets se escalan automáticamente
- Lifecycle policies para gestión de costos

## 💰 Costos

### Factores de Costo
- **Cloud Functions**: Por invocación y tiempo de ejecución
- **Vision API**: Por imagen procesada
- **Document AI**: Por página procesada
- **Storage**: Por GB almacenado
- **Pub/Sub**: Por mensaje

### Optimización de Costos
- Lifecycle policies para eliminar archivos antiguos
- Compresión de archivos grandes
- Procesamiento por lotes cuando sea posible

## 🐛 Troubleshooting

### Problemas Comunes

#### Error de autenticación
```bash
# Verificar service account
gcloud auth list
gcloud config get-value project
```

#### Cloud Function no se activa
```bash
# Verificar triggers
gcloud functions describe ocr-processor --region=us-central1
```

#### Error de permisos
```bash
# Verificar IAM
gcloud projects get-iam-policy tu-proyecto-id
```

### Logs de Debug
```bash
# Ver logs de Cloud Functions
gcloud functions logs read ocr-processor --region=us-central1

# Ver logs de Cloud Run
gcloud logging read "resource.type=cloud_run_revision"
```

## 📞 Soporte

Para soporte técnico o preguntas:
1. Revisar logs en Google Cloud Console
2. Verificar configuración de variables de entorno
3. Comprobar permisos de IAM
4. Revisar estado de las APIs habilitadas

## 🔄 Actualizaciones

### Actualizar Cloud Functions
```bash
# Recrear archivos ZIP
cd functions/ocr_processor
zip -r ocr-processor.zip .
gcloud functions deploy ocr-processor --source=ocr-processor.zip
```

### Actualizar API
```bash
# Reconstruir y desplegar
docker build -t gcr.io/tu-proyecto-id/document-api:latest .
docker push gcr.io/tu-proyecto-id/document-api:latest
gcloud run deploy document-processing-api --image gcr.io/tu-proyecto-id/document-api:latest
```
