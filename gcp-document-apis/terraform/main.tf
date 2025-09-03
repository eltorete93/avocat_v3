# Configuración principal de Terraform para GCP Document Processing APIs

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# Configurar proveedor de Google Cloud
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Habilitar APIs necesarias
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "storage.googleapis.com",
    "vision.googleapis.com",
    "documentai.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "logging.googleapis.com"
  ])
  
  service = each.value
  disable_dependent_services = false
  disable_on_destroy = false
}

# Bucket para procesamiento de documentos
resource "google_storage_bucket" "document_processing" {
  name          = "${var.project_id}-document-processing"
  location      = var.region
  force_destroy = var.force_destroy
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Bucket para backup de documentos
resource "google_storage_bucket" "document_backup" {
  name          = "${var.project_id}-document-backup"
  location      = var.region
  force_destroy = var.force_destroy
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Bucket para resultados de procesamiento
resource "google_storage_bucket" "document_results" {
  name          = "${var.project_id}-document-results"
  location      = var.region
  force_destroy = var.force_destroy
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Tópico de Pub/Sub para procesamiento de documentos
resource "google_pubsub_topic" "document_processing" {
  name = "document-processing"
  
  depends_on = [google_project_service.required_apis]
}

# Suscripción para OCR Processor
resource "google_pubsub_subscription" "ocr_processor" {
  name  = "ocr-processor-subscription"
  topic = google_pubsub_topic.document_processing.name
  
  ack_deadline_seconds = 20
  
  expiration_policy {
    ttl = "2678400s" # 31 días
  }
}

# Suscripción para Backup Manager
resource "google_pubsub_subscription" "backup_manager" {
  name  = "backup-manager-subscription"
  topic = google_pubsub_topic.document_processing.name
  
  ack_deadline_seconds = 20
  
  expiration_policy {
    ttl = "2678400s" # 31 días
  }
}

# Suscripción para Info Extractor
resource "google_pubsub_subscription" "info_extractor" {
  name  = "info-extractor-subscription"
  topic = google_pubsub_topic.document_processing.name
  
  ack_deadline_seconds = 20
  
  expiration_policy {
    ttl = "2678400s" # 31 días
  }
}

# Cloud Function para OCR Processor
resource "google_storage_bucket_object" "ocr_processor_zip" {
  name   = "ocr-processor-${data.archive_file.ocr_processor.output_md5}.zip"
  bucket = google_storage_bucket.document_processing.name
  source = data.archive_file.ocr_processor.output_path
}

data "archive_file" "ocr_processor" {
  type        = "zip"
  source_dir  = "../functions/ocr_processor"
  output_path = "/tmp/ocr-processor.zip"
}

resource "google_cloudfunctions_function" "ocr_processor" {
  name        = "ocr-processor"
  description = "Procesa documentos usando Google Cloud Vision API para OCR"
  runtime     = "python39"
  
  available_memory_mb   = 512
  source_archive_bucket = google_storage_bucket.document_processing.name
  source_archive_object = google_storage_bucket_object.ocr_processor_zip.name
 
  
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.document_processing.name
  }
  
  entry_point = "process_document"
  
  environment_variables = {
    RESULT_BUCKET_NAME = google_storage_bucket.document_results.name
    PUBSUB_TOPIC_NAME  = google_pubsub_topic.document_processing.name
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Function para Backup Manager
resource "google_storage_bucket_object" "backup_manager_zip" {
  name   = "backup-manager-${data.archive_file.backup_manager.output_md5}.zip"
  bucket = google_storage_bucket.document_processing.name
  source = data.archive_file.backup_manager.output_path
}

data "archive_file" "backup_manager" {
  type        = "zip"
  source_dir  = "../functions/backup_manager"
  output_path = "/tmp/backup-manager.zip"
}

resource "google_cloudfunctions_function" "backup_manager" {
  name        = "backup-manager"
  description = "Gestiona backup y clasificación de documentos"
  runtime     = "python39"
  
  available_memory_mb   = 512
  source_archive_bucket = google_storage_bucket.document_processing.name
  source_archive_object = google_storage_bucket_object.backup_manager_zip.name
  
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.document_processing.name
  }
  
  entry_point = "backup_document"
  
  environment_variables = {
    STORAGE_BUCKET_NAME = google_storage_bucket.document_processing.name
    BACKUP_BUCKET_NAME  = google_storage_bucket.document_backup.name
    PUBSUB_TOPIC_NAME   = google_pubsub_topic.document_processing.name
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Function para Info Extractor
resource "google_storage_bucket_object" "info_extractor_zip" {
  name   = "info-extractor-${data.archive_file.info_extractor.output_md5}.zip"
  bucket = google_storage_bucket.document_processing.name
  source = data.archive_file.info_extractor.output_path
}

data "archive_file" "info_extractor" {
  type        = "zip"
  source_dir  = "../functions/info_extractor"
  output_path = "/tmp/info-extractor.zip"
}

resource "google_cloudfunctions_function" "info_extractor" {
  name        = "info-extractor"
  description = "Extrae información estructurada usando Google Cloud Document AI"
  runtime     = "python39"
  
  available_memory_mb   = 1024
  source_archive_bucket = google_storage_bucket.document_processing.name
  source_archive_object = google_storage_bucket_object.info_extractor_zip.name
  
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.document_processing.name
  }
  
  entry_point = "extract_document_info"
  
  environment_variables = {
    STORAGE_BUCKET_NAME = google_storage_bucket.document_processing.name
    RESULT_BUCKET_NAME  = google_storage_bucket.document_results.name
    PUBSUB_TOPIC_NAME   = google_pubsub_topic.document_processing.name
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Run para API principal
resource "google_cloud_run_service" "document_api" {
  name     = "document-processing-api"
  location = var.region
  
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/document-api:latest"
        
        ports {
          container_port = 8000
        }
        
        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project_id
        }
        
        env {
          name  = "STORAGE_BUCKET_NAME"
          value = google_storage_bucket.document_processing.name
        }
        
        env {
          name  = "BACKUP_BUCKET_NAME"
          value = google_storage_bucket.document_backup.name
        }
        
        env {
          name  = "RESULT_BUCKET_NAME"
          value = google_storage_bucket.document_results.name
        }
        
        env {
          name  = "PUBSUB_TOPIC_NAME"
          value = google_pubsub_topic.document_processing.name
        }
      }
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# IAM para permitir acceso público a la API
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_service.document_api.location
  service  = google_cloud_run_service.document_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Outputs
output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "document_processing_bucket" {
  value = google_storage_bucket.document_processing.name
}

output "document_backup_bucket" {
  value = google_storage_bucket.document_backup.name
}

output "document_results_bucket" {
  value = google_storage_bucket.document_results.name
}

output "pubsub_topic" {
  value = google_pubsub_topic.document_processing.name
}

output "api_url" {
  value = google_cloud_run_service.document_api.status[0].url
}
