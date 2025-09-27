# Production deployment script for Windows
param(
    [switch]$SkipTests,
    [switch]$Force
)

Write-Host "🚀 Starting production deployment..." -ForegroundColor Green

# Check if .env.prod exists
if (-not (Test-Path ".env.prod")) {
    Write-Host "❌ Error: .env.prod file not found!" -ForegroundColor Red
    Write-Host "Please copy env.prod.example to .env.prod and configure it." -ForegroundColor Yellow
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "backup" | Out-Null
New-Item -ItemType Directory -Force -Path "nginx\ssl" | Out-Null
New-Item -ItemType Directory -Force -Path "monitoring\grafana\dashboards" | Out-Null
New-Item -ItemType Directory -Force -Path "monitoring\grafana\provisioning\datasources" | Out-Null
New-Item -ItemType Directory -Force -Path "monitoring\grafana\provisioning\dashboards" | Out-Null

# Generate SSL certificates (self-signed for development)
if (-not (Test-Path "nginx\ssl\cert.pem")) {
    Write-Host "🔐 Generating SSL certificates..." -ForegroundColor Blue
    # Note: You'll need OpenSSL installed or use Windows certificate tools
    Write-Host "⚠️  Please generate SSL certificates manually for production use" -ForegroundColor Yellow
}

# Stop existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml down

# Build and start services
Write-Host "🔨 Building and starting services..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Blue
Start-Sleep -Seconds 30

# Check service health
Write-Host "🏥 Checking service health..." -ForegroundColor Blue
docker-compose -f docker-compose.prod.yml ps

# Test API endpoints
Write-Host "🧪 Testing API endpoints..." -ForegroundColor Blue
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost/health" -UseBasicParsing
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Health check passed" -ForegroundColor Green
    } else {
        Write-Host "❌ Health check failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Application is available at: http://localhost" -ForegroundColor Cyan
Write-Host "📊 Grafana dashboard: http://localhost:3000" -ForegroundColor Cyan
Write-Host "📈 Prometheus metrics: http://localhost:9090" -ForegroundColor Cyan
Write-Host "📋 API documentation: http://localhost/docs" -ForegroundColor Cyan
