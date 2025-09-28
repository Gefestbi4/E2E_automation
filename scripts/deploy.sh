#!/bin/bash

# E2E Automation Production Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-production}
DOCKER_REGISTRY=${DOCKER_REGISTRY:-localhost:5000}
NAMESPACE=${NAMESPACE:-e2e-automation}

echo -e "${BLUE}🚀 Starting E2E Automation deployment to ${ENVIRONMENT}${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    print_status "All requirements satisfied"
}

# Build and push Docker images
build_images() {
    print_status "Building Docker images..."
    
    # Build backend image
    print_status "Building backend image..."
    docker build -f backend/Dockerfile.prod -t ${DOCKER_REGISTRY}/e2e-automation-backend:latest ./backend
    
    # Build frontend image
    print_status "Building frontend image..."
    docker build -f frontend/Dockerfile.prod -t ${DOCKER_REGISTRY}/e2e-automation-frontend:latest ./frontend
    
    # Push images to registry (if not localhost)
    if [ "$DOCKER_REGISTRY" != "localhost:5000" ]; then
        print_status "Pushing images to registry..."
        docker push ${DOCKER_REGISTRY}/e2e-automation-backend:latest
        docker push ${DOCKER_REGISTRY}/e2e-automation-frontend:latest
    fi
    
    print_status "Images built and pushed successfully"
}

# Deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying with Docker Compose..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning "Creating .env file with default values..."
        cat > .env << EOF
POSTGRES_PASSWORD=secure_password_123
REDIS_PASSWORD=redis_password_123
SECRET_KEY=your_super_secret_key_here_change_in_production
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=production
GRAFANA_PASSWORD=admin_password_123
EOF
    fi
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose -f docker-compose.prod.yml down || true
    
    # Start new containers
    print_status "Starting new containers..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    sleep 30
    
    # Check service health
    check_health
    
    print_status "Docker Compose deployment completed"
}

# Deploy with Kubernetes
deploy_kubernetes() {
    print_status "Deploying with Kubernetes..."
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed"
        exit 1
    fi
    
    # Create namespace
    print_status "Creating namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    # Apply configurations
    print_status "Applying configurations..."
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/secrets.yaml
    
    # Deploy services
    print_status "Deploying services..."
    kubectl apply -f k8s/postgres.yaml
    kubectl apply -f k8s/backend.yaml
    kubectl apply -f k8s/frontend.yaml
    kubectl apply -f k8s/ingress.yaml
    
    # Wait for deployments
    print_status "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/backend -n ${NAMESPACE}
    kubectl wait --for=condition=available --timeout=300s deployment/frontend -n ${NAMESPACE}
    
    print_status "Kubernetes deployment completed"
}

# Check service health
check_health() {
    print_status "Checking service health..."
    
    # Check backend health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend is healthy"
    else
        print_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000/health > /dev/null 2>&1; then
        print_status "Frontend is healthy"
    else
        print_warning "Frontend health check failed (this might be normal for some configurations)"
    fi
    
    print_status "Health checks completed"
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    # This would typically run Alembic migrations
    # For now, we'll just print a message
    print_warning "Database migrations should be run manually in production"
    print_status "To run migrations: docker-compose exec backend alembic upgrade head"
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Check if Prometheus is accessible
    if curl -f http://localhost:9090 > /dev/null 2>&1; then
        print_status "Prometheus is accessible"
    else
        print_warning "Prometheus is not accessible"
    fi
    
    # Check if Grafana is accessible
    if curl -f http://localhost:3001 > /dev/null 2>&1; then
        print_status "Grafana is accessible"
    else
        print_warning "Grafana is not accessible"
    fi
}

# Main deployment function
main() {
    echo -e "${BLUE}🎯 E2E Automation Deployment Script${NC}"
    echo -e "${BLUE}Environment: ${ENVIRONMENT}${NC}"
    echo -e "${BLUE}Docker Registry: ${DOCKER_REGISTRY}${NC}"
    echo -e "${BLUE}Namespace: ${NAMESPACE}${NC}"
    echo ""
    
    check_requirements
    build_images
    
    if [ "$ENVIRONMENT" = "kubernetes" ]; then
        deploy_kubernetes
    else
        deploy_docker_compose
    fi
    
    run_migrations
    setup_monitoring
    
    echo ""
    print_status "🎉 Deployment completed successfully!"
    echo ""
    echo -e "${BLUE}📋 Access URLs:${NC}"
    echo -e "  Frontend: http://localhost:3000"
    echo -e "  Backend API: http://localhost:8000"
    echo -e "  API Docs: http://localhost:8000/docs"
    echo -e "  Prometheus: http://localhost:9090"
    echo -e "  Grafana: http://localhost:3001"
    echo -e "  Kibana: http://localhost:5601"
    echo ""
    echo -e "${BLUE}🔧 Useful Commands:${NC}"
    echo -e "  View logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo -e "  Stop services: docker-compose -f docker-compose.prod.yml down"
    echo -e "  Restart services: docker-compose -f docker-compose.prod.yml restart"
    echo ""
}

# Run main function
main "$@"