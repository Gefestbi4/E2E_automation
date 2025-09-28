# Production Deployment Guide

## 🚀 E2E Automation Production Deployment

This guide covers deploying the E2E Automation application to production using Docker Compose or Kubernetes.

## 📋 Prerequisites

### Required Software
- Docker 20.10+
- Docker Compose 2.0+
- Git
- curl (for health checks)

### Optional (for Kubernetes)
- kubectl
- Kubernetes cluster (1.20+)
- Helm 3.0+

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
POSTGRES_PASSWORD=your_secure_password_here
REDIS_PASSWORD=your_redis_password_here

# Security
SECRET_KEY=your_super_secret_key_here_change_in_production

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Frontend
REACT_APP_API_URL=https://yourdomain.com
REACT_APP_ENVIRONMENT=production

# Monitoring
GRAFANA_PASSWORD=your_grafana_password_here
```

### SSL Certificates

For HTTPS deployment, place your SSL certificates in:
- `nginx/ssl/cert.pem` (certificate)
- `nginx/ssl/key.pem` (private key)

## 🐳 Docker Compose Deployment

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd e2e-automation

# Make deployment script executable
chmod +x scripts/deploy.sh

# Deploy to production
./scripts/deploy.sh production
```

### Manual Deployment

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check service health
curl http://localhost:8000/health
curl http://localhost:3000/health

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Service URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
- **Kibana**: http://localhost:5601

## ☸️ Kubernetes Deployment

### Prerequisites

1. Kubernetes cluster (1.20+)
2. kubectl configured
3. Docker images pushed to registry

### Deploy

```bash
# Deploy with Kubernetes
./scripts/deploy.sh kubernetes

# Or manually
kubectl apply -f k8s/
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n e2e-automation

# Check services
kubectl get services -n e2e-automation

# Check ingress
kubectl get ingress -n e2e-automation
```

## 📊 Monitoring Setup

### Prometheus

Prometheus is automatically configured to scrape metrics from:
- Backend API (`/metrics`)
- Node exporter
- Nginx metrics
- PostgreSQL metrics
- Redis metrics

### Grafana

Access Grafana at http://localhost:3001
- Username: `admin`
- Password: Set in `GRAFANA_PASSWORD` environment variable

### Alerting

Alerts are configured for:
- High error rates
- High response times
- High CPU/memory usage
- Low disk space
- Service downtime

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Change all default passwords
- [ ] Use strong, unique SECRET_KEY
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS with valid certificates
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure security headers
- [ ] Set up log monitoring
- [ ] Enable database encryption
- [ ] Configure backup strategy

### Security Headers

The application includes security headers:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: no-referrer-when-downgrade
- Content-Security-Policy: configured

## 📈 Performance Optimization

### Backend Optimization

- **Workers**: 4 Gunicorn workers
- **Caching**: Redis for session and data caching
- **Database**: Connection pooling enabled
- **Static Files**: Served by Nginx with caching

### Frontend Optimization

- **Gzip**: Enabled for all text assets
- **Caching**: 1-year cache for static assets
- **CDN**: Ready for CDN integration
- **Compression**: Brotli/Gzip compression

### Database Optimization

- **Connection Pooling**: Configured
- **Query Optimization**: Implemented
- **Indexing**: Proper indexes on frequently queried columns
- **Backup**: Automated daily backups

## 🔄 Backup Strategy

### Database Backups

```bash
# Manual backup
docker-compose exec postgres pg_dump -U postgres e2e_automation_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker-compose exec -T postgres psql -U postgres e2e_automation_prod < backup_file.sql
```

### Automated Backups

Set up cron job for daily backups:

```bash
# Add to crontab
0 2 * * * /path/to/backup_script.sh
```

## 🚨 Troubleshooting

### Common Issues

#### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs service_name

# Check resource usage
docker stats

# Restart service
docker-compose -f docker-compose.prod.yml restart service_name
```

#### Database Connection Issues

```bash
# Check database status
docker-compose exec postgres pg_isready -U postgres

# Check database logs
docker-compose logs postgres

# Reset database (WARNING: Data loss)
docker-compose down -v
docker-compose up -d
```

#### High Memory Usage

```bash
# Check memory usage
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Scale down if needed
docker-compose -f docker-compose.prod.yml up -d --scale backend=2
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000/health

# Database health
docker-compose exec postgres pg_isready -U postgres

# Redis health
docker-compose exec redis redis-cli ping
```

## 📝 Maintenance

### Regular Maintenance Tasks

1. **Daily**
   - Check service health
   - Review error logs
   - Monitor resource usage

2. **Weekly**
   - Review security logs
   - Check backup integrity
   - Update dependencies

3. **Monthly**
   - Security updates
   - Performance review
   - Capacity planning

### Updates

```bash
# Update application
git pull origin main
./scripts/deploy.sh production

# Update dependencies
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Support

For production support:

1. Check logs first
2. Review monitoring dashboards
3. Check service health endpoints
4. Review this documentation
5. Contact development team

## 🔗 Useful Commands

```bash
# View all services
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Stop all services
docker-compose -f docker-compose.prod.yml down

# View resource usage
docker stats

# Access database
docker-compose exec postgres psql -U postgres e2e_automation_prod

# Access Redis
docker-compose exec redis redis-cli

# Run migrations
docker-compose exec backend alembic upgrade head

# Create superuser
docker-compose exec backend python -c "from auth import create_user; create_user('admin', 'admin@example.com', 'password', is_superuser=True)"
```
