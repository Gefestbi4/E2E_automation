# Система авторизации и регистрации

## Обзор

Классическая система авторизации с раздельными процессами регистрации и входа пользователей.

## Архитектура

### Backend (FastAPI)

#### Модели данных
```python
class User(Base):
    id: int (Primary Key)
    email: str (Unique, Index)
    username: str
    full_name: str (Optional)
    hashed_password: str
    is_active: bool (Default: True)
    is_verified: bool (Default: False)
    created_at: datetime
    updated_at: datetime
```

#### API Endpoints

**Регистрация:**
- `POST /api/auth/register` - Регистрация нового пользователя
- `POST /api/auth/verify-email` - Подтверждение email

**Авторизация:**
- `POST /api/auth/login` - Вход в систему
- `POST /api/auth/logout` - Выход из системы
- `POST /api/auth/refresh` - Обновление токена

**Управление профилем:**
- `GET /api/auth/me` - Получение информации о пользователе
- `PUT /api/auth/me` - Обновление профиля
- `POST /api/auth/change-password` - Смена пароля

### Frontend (HTML/JS)

#### Страницы
1. **`/login.html`** - Страница входа
2. **`/register.html`** - Страница регистрации
3. **`/verify-email.html`** - Подтверждение email
4. **`/tests.html`** - Защищенная страница (требует авторизации)

#### Компоненты
- `AuthManager` - Класс для управления авторизацией
- `FormValidator` - Валидация форм
- `TokenManager` - Управление JWT токенами

## Процесс регистрации

1. **Заполнение формы регистрации**
   - Email (уникальный)
   - Пароль (минимум 8 символов)
   - Подтверждение пароля
   - Полное имя (опционально)

2. **Валидация данных**
   - Проверка формата email
   - Проверка сложности пароля
   - Проверка уникальности email

3. **Создание пользователя**
   - Хеширование пароля (PBKDF2)
   - Сохранение в БД
   - Генерация токена подтверждения

4. **Подтверждение email**
   - Отправка письма с токеном
   - Переход на страницу подтверждения
   - Активация аккаунта

## Процесс авторизации

1. **Ввод данных**
   - Email
   - Пароль

2. **Проверка учетных данных**
   - Поиск пользователя по email
   - Проверка хеша пароля
   - Проверка статуса аккаунта

3. **Выдача токенов**
   - Access Token (15 минут)
   - Refresh Token (7 дней)

4. **Автоматическое обновление**
   - Проверка токена каждые 5 минут
   - Обновление за 5 минут до истечения

## Безопасность

### JWT Токены
- **Access Token**: Короткоживущий (15 минут)
- **Refresh Token**: Долгоживущий (7 дней)
- **Алгоритм**: HS256
- **Payload**: `{sub: email, type: "access/refresh", exp: timestamp}`

### Пароли
- **Хеширование**: PBKDF2-SHA256
- **Требования**: минимум 8 символов
- **Соль**: уникальная для каждого пароля

### Валидация
- **Email**: RFC 5322 формат
- **Пароль**: сложность, длина
- **Rate Limiting**: защита от брутфорса

## Схемы данных

### UserRegistration
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123",
  "full_name": "John Doe"
}
```

### UserLogin
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### TokenResponse
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### UserResponse
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Обработка ошибок

### HTTP Status Codes
- `200` - Успех
- `400` - Неверные данные
- `401` - Неавторизован
- `403` - Доступ запрещен
- `409` - Конфликт (email уже существует)
- `422` - Ошибка валидации
- `500` - Внутренняя ошибка

### Error Response Format
```json
{
  "detail": "Описание ошибки",
  "field": "email",
  "code": "VALIDATION_ERROR"
}
```

## Тестирование

### Тестовые пользователи
- `test@example.com` / `testpassword123` - активный пользователь
- `admin@example.com` / `adminpassword123` - администратор

### Тестовые сценарии
1. Регистрация нового пользователя
2. Вход с валидными данными
3. Вход с неверным паролем
4. Обновление токена
5. Выход из системы
6. Доступ к защищенным ресурсам

## Мониторинг

### Метрики
- Количество регистраций
- Количество успешных входов
- Количество неудачных попыток
- Время ответа API

### Логирование
- Все попытки авторизации
- Ошибки валидации
- Подозрительная активность
