# GCP Document Processing APIs

Sistema completo de APIs para procesamiento de documentos en Google Cloud Platform que incluye:

## 🚀 Funcionalidades

- **OCR de Documentos**: Conversión de documentos escaneados a texto usando Google Cloud Vision API
- **Backup Automático**: Almacenamiento clasificado en Google Cloud Storage
- **Extracción de Información**: Análisis y extracción de datos importantes usando Google Cloud Document AI
- **Clasificación Automática**: Organización inteligente de documentos por tipo y contenido

## 🏗️ Arquitectura

- **Cloud Functions**: APIs serverless para procesamiento
- **Cloud Storage**: Almacenamiento de documentos y resultados
- **Cloud Vision API**: OCR y análisis de imágenes
- **Document AI**: Extracción estructurada de información
- **Cloud Run**: API REST para gestión de documentos
- **Pub/Sub**: Procesamiento asíncrono de documentos

## 📁 Estructura del Proyecto

```
├── functions/           # Cloud Functions
│   ├── ocr-processor/  # Procesador OCR
│   ├── backup-manager/ # Gestor de backup
│   └── info-extractor/ # Extractor de información
├── api/                # API REST principal
├── terraform/          # Infraestructura como código
├── scripts/            # Scripts de despliegue
└── docs/              # Documentación
```

## 🚀 Despliegue

1. Configurar variables de entorno
2. Desplegar infraestructura con Terraform
3. Desplegar Cloud Functions
4. Desplegar API principal

## 📚 Documentación

Ver carpeta `docs/` para guías detalladas de uso y configuración.
