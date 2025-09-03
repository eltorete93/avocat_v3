#!/bin/bash

# Script de despliegue para GCP Document Processing APIs
# Este script despliega toda la infraestructura y aplicaciones

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar dependencias
check_dependencies() {
    log "Verificando dependencias..."
    
    if ! command -v gcloud &> /dev/null; then
        error "gcloud CLI no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    if ! command -v terraform &> /dev/null; then
        error "Terraform no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    success "Todas las dependencias están instaladas"
}

# Verificar autenticación de GCP
check_gcp_auth() {
    log "Verificando autenticación de GCP..."
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        error "No hay una cuenta activa de GCP. Por favor ejecuta 'gcloud auth login'"
        exit 1
    fi
    
    success "Autenticación de GCP verificada"
}

# Configurar proyecto
setup_project() {
    local project_id=$1
    
    log "Configurando proyecto: $project_id"
    
    # Verificar si el proyecto existe
    if ! gcloud projects describe "$project_id" &> /dev/null; then
        error "El proyecto $project_id no existe o no tienes acceso"
        exit 1
    fi
    
    # Configurar proyecto activo
    gcloud config set project "$project_id"
    
    # Habilitar facturación (requerido para algunas APIs)
    log "Verificando facturación..."
    if ! gcloud billing projects describe "$project_id" --format="value(billingAccountName)" | grep -q .; then
        warning "El proyecto no tiene facturación habilitada. Algunas APIs pueden no funcionar."
    fi
    
    success "Proyecto configurado correctamente"
}

# Desplegar infraestructura con Terraform
deploy_infrastructure() {
    log "Desplegando infraestructura con Terraform..."
    
    cd terraform
    
    # Inicializar Terraform
    log "Inicializando Terraform..."
    terraform init
    
    # Verificar plan
    log "Verificando plan de Terraform..."
    terraform plan -out=tfplan
    
    # Aplicar cambios
    log "Aplicando cambios de infraestructura..."
    terraform apply tfplan
    
    # Obtener outputs
    log "Obteniendo outputs de Terraform..."
    terraform output
    
    cd ..
    
    success "Infraestructura desplegada correctamente"
}

# Construir y desplegar API
deploy_api() {
    log "Construyendo y desplegando API..."
    
    # Obtener project ID del output de Terraform
    local project_id=$(cd terraform && terraform output -raw project_id)
    
    # Construir imagen Docker
    log "Construyendo imagen Docker..."
    docker build -t "gcr.io/$project_id/document-api:latest" ./api
    
    # Configurar Docker para usar gcloud
    gcloud auth configure-docker
    
    # Subir imagen a Container Registry
    log "Subiendo imagen a Container Registry..."
    docker push "gcr.io/$project_id/document-api:latest"
    
    # Desplegar en Cloud Run
    log "Desplegando en Cloud Run..."
    gcloud run deploy document-processing-api \
        --image "gcr.io/$project_id/document-api:latest" \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 1Gi \
        --cpu 1 \
        --max-instances 10
    
    success "API desplegada correctamente"
}

# Configurar Cloud Functions
setup_cloud_functions() {
    log "Configurando Cloud Functions..."
    
    # Las Cloud Functions se despliegan automáticamente con Terraform
    # Solo verificamos que estén funcionando
    
    local project_id=$(cd terraform && terraform output -raw project_id)
    
    log "Verificando estado de Cloud Functions..."
    gcloud functions list --project="$project_id"
    
    success "Cloud Functions configuradas correctamente"
}

# Configurar permisos IAM
setup_iam() {
    log "Configurando permisos IAM..."
    
    local project_id=$(cd terraform && terraform output -raw project_id)
    
    # Crear service account para las funciones
    log "Creando service account..."
    gcloud iam service-accounts create document-processor \
        --display-name="Document Processor Service Account" \
        --description="Service account para procesamiento de documentos" \
        --project="$project_id"
    
    # Asignar roles necesarios
    log "Asignando roles..."
    gcloud projects add-iam-policy-binding "$project_id" \
        --member="serviceAccount:document-processor@$project_id.iam.gserviceaccount.com" \
        --role="roles/storage.admin"
    
    gcloud projects add-iam-policy-binding "$project_id" \
        --member="serviceAccount:document-processor@$project_id.iam.gserviceaccount.com" \
        --role="roles/vision.admin"
    
    gcloud projects add-iam-policy-binding "$project_id" \
        --member="serviceAccount:document-processor@$project_id.iam.gserviceaccount.com" \
        --role="roles/documentai.admin"
    
    gcloud projects add-iam-policy-binding "$project_id" \
        --member="serviceAccount:document-processor@$project_id.iam.gserviceaccount.com" \
        --role="roles/pubsub.admin"
    
    success "Permisos IAM configurados correctamente"
}

# Función principal
main() {
    local project_id=$1
    
    if [ -z "$project_id" ]; then
        error "Uso: $0 <project-id>"
        exit 1
    fi
    
    log "Iniciando despliegue de GCP Document Processing APIs..."
    log "Proyecto: $project_id"
    
    # Verificaciones previas
    check_dependencies
    check_gcp_auth
    setup_project "$project_id"
    
    # Desplegar infraestructura
    deploy_infrastructure
    
    # Configurar permisos
    setup_iam
    
    # Desplegar API
    deploy_api
    
    # Configurar Cloud Functions
    setup_cloud_functions
    
    # Mostrar información final
    log "Despliegue completado exitosamente!"
    log "URL de la API: $(cd terraform && terraform output -raw api_url)"
    log "Bucket de procesamiento: $(cd terraform && terraform output -raw document_processing_bucket)"
    log "Bucket de backup: $(cd terraform && terraform output -raw document_backup_bucket)"
    
    success "🎉 ¡Sistema desplegado correctamente!"
}

# Ejecutar script
main "$@"
