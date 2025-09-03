# Variables para la configuración de Terraform

variable "project_id" {
  description = "ID del proyecto de Google Cloud"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud para los recursos"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zona de Google Cloud para los recursos"
  type        = string
  default     = "us-central1-a"
}

variable "force_destroy" {
  description = "Forzar eliminación de buckets al destruir infraestructura"
  type        = bool
  default     = false
}

variable "environment" {
  description = "Ambiente de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "El ambiente debe ser dev, staging o prod."
  }
}

variable "document_ai_processor_id" {
  description = "ID del procesador de Document AI"
  type        = string
  default     = ""
}

variable "vision_api_enabled" {
  description = "Habilitar Google Cloud Vision API"
  type        = bool
  default     = true
}

variable "backup_retention_days" {
  description = "Días de retención para backups"
  type        = number
  default     = 365
}

variable "ocr_result_retention_days" {
  description = "Días de retención para resultados de OCR"
  type        = number
  default     = 90
}

variable "processing_result_retention_days" {
  description = "Días de retención para resultados de procesamiento"
  type        = number
  default     = 30
}
