# Руководство по развертыванию

## Обзор

Этот документ описывает процесс развертывания E2E Automation API в продакшене с использованием Docker Compose и Kubernetes.

## Предварительные требования

### Для Docker Compose развертывания:
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM минимум
- 20GB свободного места на диске

### Для Kubernetes развертывания:
- Kubernetes 1.20+
- kubectl настроен
- Helm 3.0+ (опционально)
- 8GB RAM минимум
- 50GB свободного места на диске

## Развертывание с Docker Compose

### 1. Подготовка

```bash
# Клонирование репозитория
git clone <repository-url>
cd E2E_automation

# Создание файла конфигурации
cp env.prod.example .env.prod
# Отредактируйте .env.prod с вашими настройками
```

### 2. Настройка переменных окружения

Отредактируйте `.env.prod`:

```bash
# Обязательные настройки
POSTGRES_PASSWORD=your_secure_password_here
SECRET_KEY=your_very_secure_secret_key_here_at_least_32_characters
GRAFANA_PASSWORD=your_grafana_admin_password

# Опциональные настройки
LOG_LEVEL=INFO
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Запуск

#### Windows (PowerShell):
```powershell
.\scripts\deploy.ps1
```

#### Linux/macOS (Bash):
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 4. Проверка развертывания

```bash
# Проверка статуса сервисов
docker-compose -f docker-compose.prod.yml ps

# Проверка логов
docker-compose -f docker-compose.prod.yml logs backend

# Тестирование API
curl http://localhost/health
curl http://localhost/api/docs
```

## Развертывание с Kubernetes

### 1. Подготовка кластера

```bash
# Создание namespace
kubectl apply -f k8s/namespace.yaml

# Создание секретов
kubectl apply -f k8s/secret.yaml

# Создание конфигурации
kubectl apply -f k8s/configmap.yaml
```

### 2. Развертывание базы данных

```bash
# PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Ожидание готовности
kubectl wait --for=condition=ready pod -l app=postgres -n e2e-automation --timeout=300s
```

### 3. Развертывание приложения

```bash
# Backend
kubectl apply -f k8s/backend.yaml

# Ожидание готовности
kubectl wait --for=condition=ready pod -l app=backend -n e2e-automation --timeout=300s
```

### 4. Настройка Ingress

```bash
# Ingress (требует nginx-ingress-controller)
kubectl apply -f k8s/ingress.yaml
```

## Мониторинг

### Доступные сервисы:

- **Приложение**: http://localhost (или ваш домен)
- **API Документация**: http://localhost/docs
- **Grafana**: http://localhost:3000 (admin/your_password)
- **Prometheus**: http://localhost:9090
- **Health Check**: http://localhost/health

### Ключевые метрики:

- HTTP запросы: `http_requests_total`
- Время ответа: `http_request_duration_seconds`
- Использование памяти: `memory_usage_bytes`
- Использование CPU: `cpu_usage_percent`
- Ошибки: `http_errors_total`

## Безопасность

### Рекомендации для продакшена:

1. **SSL/TLS**: Настройте валидные SSL сертификаты
2. **Firewall**: Ограничьте доступ к портам мониторинга
3. **Secrets**: Используйте Kubernetes Secrets или внешние системы управления секретами
4. **Network Policies**: Настройте сетевые политики Kubernetes
5. **RBAC**: Настройте роли и права доступа

### Обновление секретов:

```bash
# Kubernetes
kubectl create secret generic app-secrets \
  --from-literal=SECRET_KEY=new_secret_key \
  --from-literal=POSTGRES_PASSWORD=new_password \
  --dry-run=client -o yaml | kubectl apply -f -

# Docker Compose
# Обновите .env.prod и перезапустите сервисы
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## Масштабирование

### Горизонтальное масштабирование (Kubernetes):

```bash
# Увеличение количества реплик
kubectl scale deployment backend --replicas=5 -n e2e-automation

# Автоматическое масштабирование уже настроено через HPA
```

### Вертикальное масштабирование:

Отредактируйте `k8s/backend.yaml` и измените ресурсы:

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

## Резервное копирование

### База данных:

```bash
# Создание бэкапа
kubectl exec -it postgres-pod -n e2e-automation -- pg_dump -U app_user e2e_automation_prod > backup.sql

# Восстановление
kubectl exec -i postgres-pod -n e2e-automation -- psql -U app_user e2e_automation_prod < backup.sql
```

### Конфигурация:

```bash
# Экспорт конфигурации
kubectl get configmap app-config -n e2e-automation -o yaml > config-backup.yaml
kubectl get secret app-secrets -n e2e-automation -o yaml > secrets-backup.yaml
```

## Устранение неполадок

### Проверка логов:

```bash
# Docker Compose
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs postgres

# Kubernetes
kubectl logs -l app=backend -n e2e-automation
kubectl logs -l app=postgres -n e2e-automation
```

### Проверка состояния:

```bash
# Docker Compose
docker-compose -f docker-compose.prod.yml ps

# Kubernetes
kubectl get pods -n e2e-automation
kubectl get services -n e2e-automation
kubectl get ingress -n e2e-automation
```

### Частые проблемы:

1. **База данных не запускается**: Проверьте пароли и доступность портов
2. **Backend не может подключиться к БД**: Проверьте URL подключения и сеть
3. **Высокое использование памяти**: Увеличьте лимиты ресурсов
4. **Медленные запросы**: Проверьте метрики и настройте мониторинг

## Обновление

### Обновление приложения:

```bash
# Docker Compose
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Kubernetes
kubectl set image deployment/backend backend=new-image:tag -n e2e-automation
kubectl rollout status deployment/backend -n e2e-automation
```

### Откат изменений:

```bash
# Kubernetes
kubectl rollout undo deployment/backend -n e2e-automation
kubectl rollout status deployment/backend -n e2e-automation
```

## Поддержка

Для получения поддержки:
1. Проверьте логи приложения
2. Изучите метрики в Grafana
3. Обратитесь к команде разработки с подробным описанием проблемы
