#!/bin/bash

# Production deployment script
set -e

echo "🚀 Starting production deployment..."

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ Error: .env.prod file not found!"
    echo "Please copy env.prod.example to .env.prod and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env.prod | grep -v '^#' | xargs)

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p backup
mkdir -p nginx/ssl
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/provisioning/dashboards

# Generate SSL certificates (self-signed for development)
if [ ! -f nginx/ssl/cert.pem ]; then
    echo "🔐 Generating SSL certificates..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/key.pem \
        -out nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Test API endpoints
echo "🧪 Testing API endpoints..."
curl -f http://localhost/health || echo "❌ Health check failed"
curl -f http://localhost/api/auth/register -X POST \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","username":"testuser","password":"TestPass123!"}' \
    || echo "❌ API test failed"

echo "✅ Deployment completed successfully!"
echo "🌐 Application is available at: http://localhost"
echo "📊 Grafana dashboard: http://localhost:3000 (admin/${GRAFANA_PASSWORD:-admin})"
echo "📈 Prometheus metrics: http://localhost:9090"
echo "📋 API documentation: http://localhost/docs"
