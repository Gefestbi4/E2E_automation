# E2E Automation Framework

Современный фреймворк для автоматизации тестирования с полнофункциональным API и веб-интерфейсом.

## 🚀 Возможности

### Backend API
- **Аутентификация и авторизация** с JWT токенами
- **E-commerce модуль** - управление товарами, корзиной, заказами
- **Социальная сеть** - посты, лайки, комментарии, подписки
- **Управление задачами** - Kanban доски, карточки, комментарии
- **Управление контентом** - статьи, категории, теги, медиа
- **Аналитика и дашборды** - метрики, отчеты, алерты
- **Мониторинг** - Prometheus метрики, health checks
- **Безопасность** - rate limiting, CSRF защита, валидация

### Frontend
- **Современный UI** с адаптивным дизайном
- **Модульная архитектура** - каждый модуль независим
- **Интеграция с API** - полная поддержка всех endpoints
- **Тестирование** - встроенные инструменты для E2E тестов

### DevOps
- **Docker** - контейнеризация для разработки и продакшена
- **Kubernetes** - манифесты для развертывания в кластере
- **Мониторинг** - Grafana дашборды, Prometheus метрики
- **CI/CD** - готовые конфигурации для автоматизации

## 📋 Требования

- Python 3.11+
- Node.js 18+
- Docker 20.10+
- PostgreSQL 15+
- Redis 7+ (опционально)

## 🛠 Установка и запуск

### Быстрый старт с Docker

```bash
# Клонирование репозитория
git clone <repository-url>
cd E2E_automation

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Разработка

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📚 Документация

- [API Reference](docs/API_REFERENCE.md) - Полная документация API
- [Deployment Guide](docs/DEPLOYMENT.md) - Руководство по развертыванию
- [User Cases](docs/user_cases/README.md) - Пользовательские сценарии
- [Architecture](docs/ARCHITECTURE.md) - Архитектура системы

## 🧪 Тестирование

### Backend тесты

```bash
cd backend
python -m pytest tests/ -v
python -m pytest tests/test_integration.py -v
python -m pytest tests/test_security.py -v
python -m pytest tests/test_monitoring.py -v
```

### Frontend тесты

```bash
cd frontend
npm test
npm run test:e2e
```

### E2E тесты

```bash
# Запуск всех E2E тестов
npm run test:e2e:all

# Запуск тестов конкретного модуля
npm run test:e2e:auth
npm run test:e2e:ecommerce
npm run test:e2e:social
```

## 🏗 Архитектура

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **JWT** - аутентификация
- **Prometheus** - метрики
- **Structured Logging** - структурированное логирование

### Frontend
- **Vanilla JavaScript** - без фреймворков
- **CSS Grid/Flexbox** - современная верстка
- **Web Components** - переиспользуемые компоненты
- **Service Workers** - кэширование и офлайн режим

### База данных
- **PostgreSQL** - основная БД
- **Redis** - кэширование (опционально)
- **Миграции** - автоматическое управление схемой

## 🔧 Конфигурация

### Переменные окружения

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: e2e_automation
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
```

## 📊 Мониторинг

### Доступные сервисы

- **API**: http://localhost:8000
- **Документация**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Метрики**: http://localhost:8000/metrics
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### Ключевые метрики

- HTTP запросы и время ответа
- Использование памяти и CPU
- Ошибки и исключения
- Бизнес-метрики (пользователи, товары, заказы)

## 🚀 Развертывание

### Docker Compose (Продакшен)

```bash
# Подготовка
cp env.prod.example .env.prod
# Отредактируйте .env.prod

# Развертывание
docker-compose -f docker-compose.prod.yml up -d

# Проверка
curl http://localhost/health
```

### Kubernetes

```bash
# Создание namespace
kubectl apply -f k8s/namespace.yaml

# Развертывание
kubectl apply -f k8s/
```

## 🔒 Безопасность

- **JWT токены** с коротким временем жизни
- **Rate limiting** для предотвращения атак
- **CSRF защита** для форм
- **Валидация входных данных** на всех уровнях
- **Хеширование паролей** с bcrypt
- **HTTPS** в продакшене

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

- **Документация**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

## 🎯 Roadmap

### v2.0.0
- [ ] GraphQL API
- [ ] Real-time уведомления (WebSocket)
- [ ] Мобильное приложение
- [ ] Микросервисная архитектура

### v1.1.0
- [ ] Расширенная аналитика
- [ ] Интеграции с внешними сервисами
- [ ] Автоматические тесты
- [ ] Performance оптимизации

## 📈 Статистика

- **Backend**: 15+ модулей, 50+ endpoints
- **Frontend**: 6 модулей, 20+ страниц
- **Тесты**: 100+ unit тестов, 50+ интеграционных тестов
- **Документация**: 10+ документов, 500+ строк

---

**Сделано с ❤️ командой E2E Automation**