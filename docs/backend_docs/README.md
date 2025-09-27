# Backend Documentation

## Обзор архитектуры

Backend приложения построен на FastAPI и предоставляет RESTful API для полноценного веб-приложения для обучения автоматизаторов. Архитектура включает модульную структуру с разделением по бизнес-доменам.

## Структура проекта

```
backend/
├── api/                    # API endpoints по модулям
│   ├── auth.py            # Аутентификация и авторизация
│   ├── ecommerce.py       # E-commerce модуль
│   ├── social.py          # Social Network модуль
│   ├── tasks.py           # Task Management модуль
│   ├── content.py         # Content Management модуль
│   └── analytics.py       # Dashboard & Analytics модуль
├── core/                  # Основная конфигурация
│   ├── config.py          # Настройки приложения
│   ├── security.py        # JWT и безопасность
│   └── database.py        # Подключение к БД
├── models/                # SQLAlchemy модели
│   ├── user.py           # Модели пользователей
│   ├── ecommerce.py      # Модели e-commerce
│   ├── social.py         # Модели социальной сети
│   ├── tasks.py          # Модели задач
│   ├── content.py        # Модели контента
│   └── analytics.py      # Модели аналитики
├── schemas/               # Pydantic схемы
│   ├── auth.py           # Схемы аутентификации
│   ├── ecommerce.py      # Схемы e-commerce
│   ├── social.py         # Схемы социальной сети
│   ├── tasks.py          # Схемы задач
│   ├── content.py        # Схемы контента
│   └── analytics.py      # Схемы аналитики
├── services/              # Бизнес-логика
│   ├── auth_service.py   # Сервис аутентификации
│   ├── ecommerce_service.py
│   ├── social_service.py
│   ├── tasks_service.py
│   ├── content_service.py
│   └── analytics_service.py
├── utils/                 # Утилиты
│   ├── dependencies.py   # FastAPI зависимости
│   ├── exceptions.py     # Кастомные исключения
│   └── helpers.py        # Вспомогательные функции
└── tests/                # Тесты
    ├── unit/             # Юнит тесты
    ├── integration/      # Интеграционные тесты
    └── conftest.py       # Конфигурация тестов
```

## Модули приложения

### 1. Authentication & Authorization
- JWT токены (access + refresh)
- Роли и права доступа
- OAuth2 интеграция
- 2FA поддержка

### 2. E-commerce модуль
- Управление товарами
- Корзина и заказы
- Платежи и доставка
- Отзывы и рейтинги

### 3. Social Network модуль
- Посты и комментарии
- Лайки и реакции
- Подписки и друзья
- Чаты и сообщения

### 4. Task Management модуль
- Kanban доски
- Проекты и команды
- Уведомления
- Отчеты

### 5. Content Management модуль
- Статьи и блоги
- Медиа файлы
- Категории и теги
- Модерация

### 6. Analytics & Dashboard модуль
- Метрики и KPI
- Интерактивные дашборды
- Экспорт данных
- Настройки виджетов

## Технологический стек

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - основная БД
- **Redis** - кэширование и сессии
- **JWT** - аутентификация
- **Pydantic** - валидация данных
- **Alembic** - миграции БД
- **pytest** - тестирование
- **Docker** - контейнеризация

## API Endpoints

### Authentication
- `POST /api/auth/login` - Вход в систему
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/refresh` - Обновление токена
- `POST /api/auth/logout` - Выход
- `POST /api/auth/forgot-password` - Восстановление пароля

### E-commerce
- `GET /api/ecommerce/products` - Список товаров
- `GET /api/ecommerce/products/{id}` - Детали товара
- `POST /api/ecommerce/cart` - Добавить в корзину
- `GET /api/ecommerce/cart` - Корзина
- `POST /api/ecommerce/orders` - Создать заказ
- `GET /api/ecommerce/orders` - История заказов

### Social Network
- `GET /api/social/posts` - Лента постов
- `POST /api/social/posts` - Создать пост
- `POST /api/social/posts/{id}/like` - Лайк поста
- `POST /api/social/posts/{id}/comment` - Комментарий
- `GET /api/social/users` - Пользователи
- `POST /api/social/users/{id}/follow` - Подписка

### Task Management
- `GET /api/tasks/boards` - Доски задач
- `POST /api/tasks/boards` - Создать доску
- `GET /api/tasks/boards/{id}/cards` - Задачи доски
- `POST /api/tasks/cards` - Создать задачу
- `PUT /api/tasks/cards/{id}` - Обновить задачу
- `POST /api/tasks/cards/{id}/assign` - Назначить задачу

### Content Management
- `GET /api/content/articles` - Статьи
- `POST /api/content/articles` - Создать статью
- `PUT /api/content/articles/{id}` - Редактировать статью
- `POST /api/content/upload` - Загрузка файлов
- `GET /api/content/categories` - Категории
- `POST /api/content/articles/{id}/publish` - Публикация

### Analytics
- `GET /api/analytics/dashboard` - Данные дашборда
- `GET /api/analytics/metrics` - Метрики
- `POST /api/analytics/reports` - Создать отчет
- `GET /api/analytics/export` - Экспорт данных

## Безопасность

- JWT токены с коротким временем жизни
- Refresh токены для продления сессии
- CORS настройки
- Rate limiting
- Валидация входных данных
- Хеширование паролей (bcrypt)
- Защита от SQL инъекций
- Логирование безопасности

## Тестирование

- Unit тесты для всех сервисов
- Integration тесты для API
- Тесты безопасности
- Performance тесты
- Coverage > 90%

## Развертывание

- Docker контейнеризация
- Docker Compose для разработки
- Миграции БД через Alembic
- Environment переменные
- Health checks
- Логирование в JSON формате

## Мониторинг

- Логирование запросов
- Метрики производительности
- Ошибки и исключения
- Health endpoints
- Prometheus метрики
