# API Reference

## Обзор

E2E Automation API предоставляет RESTful API для управления пользователями, e-commerce, социальными функциями, задачами, контентом и аналитикой.

**Base URL**: `http://localhost:8000/api`

## Аутентификация

API использует JWT токены для аутентификации. Включите токен в заголовок `Authorization`:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Аутентификация

#### POST /auth/register
Регистрация нового пользователя.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "full_name": "Full Name"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /auth/login
Вход в систему.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### GET /auth/me
Получение информации о текущем пользователе.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### E-commerce

#### GET /ecommerce/products
Получение списка товаров.

**Query Parameters:**
- `skip` (int): Количество пропускаемых записей (по умолчанию: 0)
- `limit` (int): Максимальное количество записей (по умолчанию: 100)
- `search` (string): Поисковый запрос
- `category` (string): Фильтр по категории
- `min_price` (float): Минимальная цена
- `max_price` (float): Максимальная цена

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Product Name",
      "description": "Product Description",
      "price": 99.99,
      "category": "Electronics",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### POST /ecommerce/products
Создание нового товара.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "New Product",
  "description": "Product Description",
  "price": 99.99,
  "category": "Electronics",
  "stock_quantity": 100
}
```

#### GET /ecommerce/products/{product_id}
Получение товара по ID.

**Response:**
```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product Description",
  "price": 99.99,
  "category": "Electronics",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Социальная сеть

#### GET /social/posts
Получение списка постов.

**Query Parameters:**
- `skip` (int): Количество пропускаемых записей
- `limit` (int): Максимальное количество записей
- `user_id` (int): Фильтр по пользователю

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "content": "Post content",
      "user": {
        "id": 1,
        "username": "username",
        "full_name": "Full Name"
      },
      "likes_count": 5,
      "comments_count": 3,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### POST /social/posts
Создание нового поста.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "content": "Post content"
}
```

### Управление задачами

#### GET /tasks/boards
Получение списка досок.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Project Board",
      "description": "Main project board",
      "is_public": false,
      "user": {
        "id": 1,
        "username": "username"
      },
      "cards_count": 5,
      "completed_cards": 2,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### POST /tasks/boards
Создание новой доски.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "New Board",
  "description": "Board description",
  "is_public": false
}
```

### Управление контентом

#### GET /content/articles
Получение списка статей.

**Query Parameters:**
- `skip` (int): Количество пропускаемых записей
- `limit` (int): Максимальное количество записей
- `status` (string): Фильтр по статусу (draft, published, archived)
- `category` (string): Фильтр по категории

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Article Title",
      "slug": "article-title",
      "content": "Article content",
      "status": "published",
      "author": {
        "id": 1,
        "username": "username",
        "full_name": "Full Name"
      },
      "views_count": 100,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### Аналитика

#### GET /analytics/dashboard
Получение данных дашборда.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "status": "success",
  "data": {
    "users": {
      "total": 100,
      "active": 85,
      "new_today": 5
    },
    "products": {
      "total": 50,
      "active": 45,
      "sold_today": 10
    },
    "revenue": {
      "today": 1000.00,
      "this_month": 25000.00,
      "growth": 15.5
    }
  }
}
```

## Коды ответов

- `200 OK` - Успешный запрос
- `201 Created` - Ресурс создан
- `400 Bad Request` - Неверный запрос
- `401 Unauthorized` - Требуется аутентификация
- `403 Forbidden` - Недостаточно прав
- `404 Not Found` - Ресурс не найден
- `422 Unprocessable Entity` - Ошибка валидации
- `429 Too Many Requests` - Превышен лимит запросов
- `500 Internal Server Error` - Внутренняя ошибка сервера

## Обработка ошибок

Все ошибки возвращаются в формате:

```json
{
  "status": "error",
  "message": "Error description",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

## Rate Limiting

API имеет ограничения на количество запросов:
- Общие endpoints: 100 запросов в минуту
- Аутентификация: 5 попыток входа в минуту

При превышении лимита возвращается код `429 Too Many Requests`.

## Пагинация

Все списковые endpoints поддерживают пагинацию:

- `skip` - количество пропускаемых записей
- `limit` - максимальное количество записей (максимум 100)

## Фильтрация и поиск

Многие endpoints поддерживают фильтрацию и поиск:

- `search` - поиск по текстовым полям
- `sort_by` - поле для сортировки
- `sort_order` - порядок сортировки (asc/desc)

## Webhooks

API поддерживает webhooks для уведомлений о событиях:

- `user.registered` - новый пользователь зарегистрирован
- `product.created` - создан новый товар
- `order.placed` - размещен новый заказ
- `post.created` - создан новый пост

## SDK и клиенты

### JavaScript/TypeScript
```javascript
const api = new E2EAutomationAPI('http://localhost:8000/api');
const token = await api.auth.login('user@example.com', 'password');
const products = await api.ecommerce.getProducts();
```

### Python
```python
from e2e_automation_api import E2EAutomationAPI

api = E2EAutomationAPI('http://localhost:8000/api')
token = api.auth.login('user@example.com', 'password')
products = api.ecommerce.get_products()
```

## Примеры использования

### Полный цикл работы с API

```bash
# 1. Регистрация
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123!","confirm_password":"Pass123!","full_name":"User Name"}'

# 2. Вход
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123!"}'

# 3. Создание товара
curl -X POST http://localhost:8000/api/ecommerce/products \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","description":"Description","price":99.99,"category":"Test"}'

# 4. Получение товаров
curl -X GET "http://localhost:8000/api/ecommerce/products?limit=10" \
  -H "Authorization: Bearer <token>"
```

## Поддержка

Для получения поддержки:
1. Проверьте документацию API: http://localhost:8000/docs
2. Изучите примеры в этом документе
3. Обратитесь к команде разработки
