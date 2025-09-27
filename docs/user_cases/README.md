# Пользовательские сценарии (User Cases)

## Обзор

Данная документация содержит comprehensive описание всех возможных пользовательских сценариев для полноценного веб-приложения для обучения автоматизаторов. Документация структурирована по модулям и приоритетам для удобства тестирования и разработки.

## Структура документации

```
docs/user_cases/
├── README.md                    # Общий обзор и навигация
├── authentication/              # Сценарии авторизации
│   ├── registration.md         # Регистрация пользователей
│   ├── login.md               # Вход в систему
│   ├── profile_management.md  # Управление профилем
│   └── security.md            # Безопасность и восстановление
├── ecommerce/                  # E-commerce модуль
│   ├── product_catalog.md     # Каталог товаров
│   ├── shopping_cart.md       # Корзина покупок
│   ├── checkout.md            # Оформление заказа
│   └── order_management.md    # Управление заказами
├── social/                     # Social Network модуль
│   ├── posts.md               # Посты и лента
│   ├── interactions.md        # Лайки и комментарии
│   ├── user_connections.md    # Подписки и друзья
│   └── messaging.md           # Чаты и сообщения
├── tasks/                      # Task Management модуль
│   ├── project_management.md  # Управление проектами
│   ├── kanban_boards.md       # Kanban доски
│   ├── task_operations.md     # Операции с задачами
│   └── collaboration.md       # Совместная работа
├── content/                    # Content Management модуль
│   ├── article_management.md  # Управление статьями
│   ├── media_library.md       # Медиа библиотека
│   ├── content_creation.md    # Создание контента
│   └── content_moderation.md  # Модерация контента
├── analytics/                  # Analytics & Dashboard модуль
│   ├── dashboard.md           # Главная панель
│   ├── reporting.md           # Отчеты и аналитика
│   ├── metrics.md             # Метрики и KPI
│   └── data_export.md         # Экспорт данных
└── integration/                # Интеграционные сценарии
    ├── cross_module.md        # Межмодульные взаимодействия
    ├── api_integration.md     # API интеграции
    └── error_handling.md      # Обработка ошибок
```

## Классификация сценариев

### По приоритету
- **🔴 Critical** - Критически важные сценарии (основной функционал)
- **🟡 High** - Высокий приоритет (важные функции)
- **🟢 Medium** - Средний приоритет (дополнительные функции)
- **🔵 Low** - Низкий приоритет (nice-to-have функции)

### По типу пользователя
- **👤 Guest** - Неавторизованный пользователь
- **👤 User** - Обычный пользователь
- **👤 Admin** - Администратор
- **👤 Moderator** - Модератор

### По типу тестирования
- **🧪 Smoke** - Smoke тесты (базовая функциональность)
- **🔄 Regression** - Регрессионные тесты
- **⚡ Performance** - Тесты производительности
- **🔒 Security** - Тесты безопасности
- **📱 Mobile** - Мобильное тестирование

## Формат описания сценария

Каждый сценарий содержит:

```markdown
## [Название сценария]

**Приоритет:** 🔴 Critical | 🟡 High | 🟢 Medium | 🔵 Low  
**Тип пользователя:** 👤 Guest | 👤 User | 👤 Admin | 👤 Moderator  
**Модуль:** Authentication | E-commerce | Social | Tasks | Content | Analytics  
**Тип тестирования:** 🧪 Smoke | 🔄 Regression | ⚡ Performance | 🔒 Security | 📱 Mobile

### Описание
Краткое описание того, что делает пользователь в этом сценарии.

### Предусловия
- Условия, которые должны быть выполнены перед началом сценария
- Состояние системы
- Данные пользователя

### Шаги выполнения
1. **Шаг 1:** Действие пользователя
   - **Ожидаемый результат:** Что должно произойти
   - **Test ID:** `test-id="element-id"`

2. **Шаг 2:** Следующее действие
   - **Ожидаемый результат:** Результат действия
   - **Test ID:** `test-id="element-id"`

### Постусловия
- Состояние системы после выполнения сценария
- Созданные данные
- Изменения в системе

### Тестовые данные
```json
{
  "user": {
    "email": "test@example.com",
    "password": "testpassword123"
  },
  "product": {
    "name": "Test Product",
    "price": 99.99
  }
}
```

### API Endpoints
- `POST /api/auth/login` - Вход в систему
- `GET /api/ecommerce/products` - Получение товаров

### Обработка ошибок
- **400 Bad Request** - Неверные данные
- **401 Unauthorized** - Неавторизован
- **404 Not Found** - Ресурс не найден

### Связанные сценарии
- [Связанный сценарий 1](./related-scenario.md)
- [Связанный сценарий 2](./another-scenario.md)
```

## Навигация по модулям

### 🔐 Authentication Module
- [Регистрация нового пользователя](./authentication/registration.md) ✅
- [Вход в систему](./authentication/login.md) ✅
- [Управление профилем](./authentication/profile_management.md) 📝
- [Безопасность и восстановление](./authentication/security.md) 📝

### 🛒 E-commerce Module
- [Просмотр каталога товаров](./ecommerce/product_catalog.md) ✅
- [Управление корзиной покупок](./ecommerce/shopping_cart.md) 📝
- [Оформление заказа](./ecommerce/checkout.md) 📝
- [Управление заказами](./ecommerce/order_management.md) 📝

### 👥 Social Network Module
- [Создание и просмотр постов](./social/posts.md) ✅
- [Взаимодействие с контентом](./social/interactions.md) 📝
- [Управление связями](./social/user_connections.md) 📝
- [Обмен сообщениями](./social/messaging.md) 📝

### 📋 Task Management Module
- [Управление проектами](./tasks/project_management.md) 📝
- [Работа с Kanban досками](./tasks/kanban_boards.md) ✅
- [Операции с задачами](./tasks/task_operations.md) 📝
- [Совместная работа](./tasks/collaboration.md) 📝

### 📝 Content Management Module
- [Управление статьями](./content/article_management.md) ✅
- [Медиа библиотека](./content/media_library.md) 📝
- [Создание контента](./content/content_creation.md) 📝
- [Модерация контента](./content/content_moderation.md) 📝

### 📊 Analytics & Dashboard Module
- [Главная панель](./analytics/dashboard.md) ✅
- [Отчеты и аналитика](./analytics/reporting.md) 📝
- [Метрики и KPI](./analytics/metrics.md) 📝
- [Экспорт данных](./analytics/data_export.md) 📝

### 🔗 Integration Scenarios
- [Межмодульные взаимодействия](./integration/cross_module.md) ✅
- [API интеграции](./integration/api_integration.md) 📝
- [Обработка ошибок](./integration/error_handling.md) 📝

### 📊 Дополнительные ресурсы
- [Тестовые данные](./test_data.json) ✅
- [Схемы API](./api_schemas.md) 📝
- [Конфигурация тестов](./test_config.md) 📝

**Легенда:**
- ✅ Завершено
- 📝 В разработке

## Тестовые данные

### Пользователи
```json
{
  "guest_user": {
    "type": "guest",
    "permissions": ["view_public_content"]
  },
  "regular_user": {
    "email": "user@example.com",
    "password": "userpassword123",
    "username": "user",
    "full_name": "Regular User",
    "permissions": ["full_access"]
  },
  "admin_user": {
    "email": "admin@example.com",
    "password": "adminpassword123",
    "username": "admin",
    "full_name": "Admin User",
    "permissions": ["admin_access", "moderation", "analytics"]
  }
}
```

### Продукты
```json
{
  "sample_products": [
    {
      "name": "Laptop Pro 15",
      "price": 1299.99,
      "category": "Electronics",
      "description": "High-performance laptop for professionals"
    },
    {
      "name": "Wireless Headphones",
      "price": 199.99,
      "category": "Audio",
      "description": "Premium wireless headphones with noise cancellation"
    }
  ]
}
```

## Метрики и KPI

### Критические метрики
- **Время загрузки страницы** < 2 секунд
- **Время отклика API** < 500ms
- **Успешность операций** > 99%
- **Покрытие тестами** > 90%

### Пользовательские метрики
- **Время регистрации** < 30 секунд
- **Время оформления заказа** < 5 минут
- **Время создания поста** < 10 секунд
- **Время загрузки дашборда** < 3 секунд

## Обновления документации

Документация обновляется при:
- Добавлении новых функций
- Изменении существующего функционала
- Обнаружении новых сценариев использования
- Изменении требований к тестированию

**Последнее обновление:** 2025-09-27  
**Версия:** 1.0.0  
**Автор:** Senior QA Automation Engineer
