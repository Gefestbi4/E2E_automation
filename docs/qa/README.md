# QA Documentation

## Обзор тестирования

Документация по тестированию для полноценного веб-приложения для обучения автоматизаторов. Включает E2E, API и Database тестирование с системой маркировки для отладки.

## Структура тестирования

```
tests/
├── e2e/                    # End-to-End тесты
│   ├── auth/              # Тесты авторизации
│   ├── ecommerce/         # Тесты e-commerce
│   ├── social/            # Тесты social network
│   ├── tasks/             # Тесты task management
│   ├── content/           # Тесты content management
│   ├── analytics/         # Тесты analytics
│   └── integration/       # Интеграционные тесты
├── api/                   # API тесты
│   ├── auth/              # API тесты авторизации
│   ├── ecommerce/         # API тесты e-commerce
│   ├── social/            # API тесты social network
│   ├── tasks/             # API тесты task management
│   ├── content/           # API тесты content management
│   └── analytics/         # API тесты analytics
├── database/              # Database тесты
│   ├── models/            # Тесты моделей
│   ├── migrations/        # Тесты миграций
│   └── performance/       # Тесты производительности
├── performance/           # Performance тесты
│   ├── load/              # Нагрузочные тесты
│   ├── stress/            # Стресс тесты
│   └── volume/            # Тесты объема данных
└── security/              # Security тесты
    ├── authentication/    # Тесты аутентификации
    ├── authorization/     # Тесты авторизации
    └── vulnerabilities/   # Тесты уязвимостей
```

## Система маркировки тестов

### Маркеры для отладки
- `@debug` - Тест требует отладки
- `@fixme` - Тест сломан и требует исправления
- `@skip` - Пропустить тест
- `@xfail` - Ожидается падение теста
- `@flaky` - Нестабильный тест

### Маркеры по приоритету
- `@critical` - Критический путь
- `@high` - Высокий приоритет
- `@medium` - Средний приоритет
- `@low` - Низкий приоритет

### Маркеры по типу
- `@smoke` - Smoke тесты
- `@regression` - Регрессионные тесты
- `@api` - API тесты
- `@ui` - UI тесты
- `@database` - Database тесты
- `@performance` - Performance тесты
- `@security` - Security тесты

## E2E Testing Framework

### Технологический стек
- **Selenium** - основной фреймворк
- **Pytest** - test runner
- **Allure** - отчетность
- **Page Object Model** - паттерн для страниц
- **Data-driven testing** - тестирование с данными

### Структура E2E тестов

#### Page Objects
```
pages/
├── base_page.py           # Базовый класс страницы
├── auth/
│   ├── login_page.py     # Страница входа
│   ├── register_page.py  # Страница регистрации
│   └── profile_page.py   # Страница профиля
├── ecommerce/
│   ├── shop_page.py      # Страница магазина
│   ├── product_page.py   # Страница товара
│   ├── cart_page.py      # Страница корзины
│   └── checkout_page.py  # Страница оформления заказа
├── social/
│   ├── feed_page.py      # Страница ленты
│   ├── post_page.py      # Страница поста
│   └── chat_page.py      # Страница чата
├── tasks/
│   ├── boards_page.py    # Страница досок
│   ├── board_page.py     # Страница доски
│   └── task_page.py      # Страница задачи
├── content/
│   ├── articles_page.py  # Страница статей
│   ├── editor_page.py    # Страница редактора
│   └── media_page.py     # Страница медиа
└── analytics/
    ├── dashboard_page.py # Страница дашборда
    └── reports_page.py   # Страница отчетов
```

#### Тестовые файлы
```
e2e/
├── test_auth_flow.py      # Полный флоу авторизации
├── test_ecommerce_flow.py # E-commerce пользовательский путь
├── test_social_flow.py    # Social network взаимодействие
├── test_tasks_flow.py     # Task management сценарии
├── test_content_flow.py   # Content management операции
└── test_analytics_flow.py # Analytics и отчеты
```

### Пример E2E теста
```python
import pytest
from pages.ecommerce.shop_page import ShopPage
from pages.ecommerce.product_page import ProductPage
from pages.ecommerce.cart_page import CartPage

@pytest.mark.critical
@pytest.mark.ecommerce
def test_complete_purchase_flow(browser, test_data):
    """Полный флоу покупки товара"""
    # Открываем магазин
    shop_page = ShopPage(browser)
    shop_page.open()
    
    # Ищем товар
    shop_page.search_product(test_data["product"]["name"])
    
    # Открываем товар
    product_page = ProductPage(browser)
    product_page.add_to_cart()
    
    # Переходим в корзину
    cart_page = CartPage(browser)
    cart_page.proceed_to_checkout()
    
    # Проверяем успешность
    assert cart_page.is_checkout_successful()
```

## API Testing Framework

### Технологический стек
- **pytest** - test runner
- **requests** - HTTP клиент
- **pydantic** - валидация данных
- **Allure** - отчетность

### Структура API тестов

#### API клиенты
```
api_clients/
├── base_client.py         # Базовый API клиент
├── auth_client.py         # Клиент авторизации
├── ecommerce_client.py    # Клиент e-commerce
├── social_client.py       # Клиент social network
├── tasks_client.py        # Клиент task management
├── content_client.py      # Клиент content management
└── analytics_client.py    # Клиент analytics
```

#### Тестовые файлы
```
api/
├── test_auth_api.py       # API тесты авторизации
├── test_ecommerce_api.py  # API тесты e-commerce
├── test_social_api.py     # API тесты social network
├── test_tasks_api.py      # API тесты task management
├── test_content_api.py    # API тесты content management
└── test_analytics_api.py  # API тесты analytics
```

### Пример API теста
```python
import pytest
from api_clients.ecommerce_client import EcommerceClient
from schemas.ecommerce import ProductResponse

@pytest.mark.api
@pytest.mark.ecommerce
def test_create_product_api(ecommerce_client, product_data):
    """API тест создания товара"""
    response = ecommerce_client.create_product(product_data)
    
    assert response.status_code == 201
    product = ProductResponse(**response.json())
    assert product.name == product_data["name"]
    assert product.price == product_data["price"]
```

## Database Testing

### Технологический стек
- **pytest** - test runner
- **SQLAlchemy** - ORM
- **Factory Boy** - генерация тестовых данных
- **Alembic** - миграции

### Типы DB тестов

#### Unit тесты моделей
```python
@pytest.mark.database
@pytest.mark.models
def test_user_model_creation():
    """Тест создания пользователя"""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
```

#### Интеграционные тесты
```python
@pytest.mark.database
@pytest.mark.integration
def test_user_product_relationship():
    """Тест связи пользователь-товар"""
    user = create_test_user()
    product = create_test_product()
    
    # Создаем заказ
    order = Order(user_id=user.id, product_id=product.id)
    db.add(order)
    db.commit()
    
    assert order.user == user
    assert order.product == product
```

## Performance Testing

### Нагрузочные тесты
- **Locust** - нагрузочное тестирование
- **JMeter** - performance тестирование
- **K6** - современное нагрузочное тестирование

### Метрики производительности
- Response time < 200ms
- Throughput > 1000 RPS
- Error rate < 1%
- CPU usage < 80%
- Memory usage < 2GB

## Security Testing

### Типы security тестов
- Аутентификация и авторизация
- SQL инъекции
- XSS атаки
- CSRF защита
- Rate limiting
- JWT токены

### Инструменты
- **OWASP ZAP** - сканер уязвимостей
- **Burp Suite** - тестирование безопасности
- **Bandit** - статический анализ Python

## Отчетность

### Allure отчеты
- Детальные отчеты по тестам
- Скриншоты при падении
- Видео записи тестов
- Графики производительности
- История запусков

### Интеграция с CI/CD
- Автоматический запуск тестов
- Уведомления о результатах
- Блокировка деплоя при падении
- Артефакты тестирования

## Команды для запуска тестов

### Запуск всех тестов
```bash
pytest
```

### Запуск по маркерам
```bash
# Только smoke тесты
pytest -m smoke

# Только API тесты
pytest -m api

# Только тесты для отладки
pytest -m debug

# Критические тесты
pytest -m critical
```

### Запуск конкретного модуля
```bash
# E-commerce тесты
pytest tests/e2e/ecommerce/

# API тесты авторизации
pytest tests/api/auth/

# Database тесты
pytest tests/database/
```

### Генерация отчетов
```bash
# Allure отчет
pytest --alluredir=allure-results
allure serve allure-results

# HTML отчет
pytest --html=report.html
```

## Best Practices

### Написание тестов
1. Используйте Page Object Model
2. Применяйте data-driven подход
3. Делайте тесты независимыми
4. Используйте понятные имена
5. Добавляйте детальные описания

### Отладка тестов
1. Маркируйте проблемные тесты `@debug`
2. Запускайте только отмеченные тесты для отладки
3. Используйте скриншоты и логи
4. Проверяйте данные и окружение
5. Снимайте маркеры после исправления

### Поддержка тестов
1. Регулярно обновляйте селекторы
2. Следите за изменениями в приложении
3. Оптимизируйте медленные тесты
4. Удаляйте устаревшие тесты
5. Документируйте изменения

## Конфигурация

### pytest.ini
```ini
[pytest]
markers =
    critical: Critical path tests
    high: High priority tests
    medium: Medium priority tests
    low: Low priority tests
    smoke: Smoke tests
    regression: Regression tests
    api: API tests
    ui: UI tests
    database: Database tests
    performance: Performance tests
    security: Security tests
    debug: Tests requiring debugging
    fixme: Broken tests
    skip: Skipped tests
    xfail: Expected to fail
    flaky: Flaky tests
```

### Docker конфигурация
- Изолированная среда тестирования
- Автоматический запуск сервисов
- Настройка тестовых данных
- Очистка после тестов
