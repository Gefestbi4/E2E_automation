# Руководство по тестированию

## Обзор

Данное руководство описывает процесс тестирования полноценного веб-приложения для обучения автоматизаторов. Включает E2E, API и Database тестирование с системой маркировки для эффективной отладки.

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
├── database/              # Database тесты
├── performance/           # Performance тесты
└── security/              # Security тесты
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

## Запуск тестов

### Базовые команды

```bash
# Запуск всех тестов
pytest

# Запуск только тестов для отладки
pytest --debug-only

# Запуск только сломанных тестов
pytest --fixme-only

# Запуск критических тестов
pytest -m critical

# Запуск тестов высокого приоритета
pytest -m high

# Запуск smoke тестов
pytest -m smoke

# Запуск тестов конкретного модуля
pytest -m ecommerce
```

### Интерактивный запуск

```bash
# Использование скрипта для интерактивного выбора
python run_debug_tests.py

# Показать сводку по тестам
python run_debug_tests.py --summary

# Очистить маркеры debug
python run_debug_tests.py --cleanup
```

### Параллельный запуск

```bash
# Запуск в автоматическом режиме (по количеству CPU)
pytest -n auto

# Запуск с указанным количеством процессов
pytest -n 4
```

## Отладка тестов

### Маркировка тестов для отладки

```python
from utils.test_markers import debug_test, fixme_test

@debug_test("Проблема с загрузкой страницы")
@pytest.mark.debug
def test_page_loading():
    """Тест, требующий отладки"""
    pass

@fixme_test("Тест падает из-за изменений в API")
@pytest.mark.fixme
def test_api_integration():
    """Сломанный тест"""
    pass
```

### Процесс отладки

1. **Маркировка проблемного теста**
   ```python
   @debug_test("Описание проблемы")
   @pytest.mark.debug
   def test_problematic():
       pass
   ```

2. **Запуск только отмеченных тестов**
   ```bash
   pytest --debug-only -v
   ```

3. **Анализ ошибок и исправление**

4. **Удаление маркера после исправления**
   ```python
   # Убираем @debug_test и @pytest.mark.debug
   def test_fixed():
       pass
   ```

### Автоматическое удаление маркеров

```bash
# Запуск с автоматическим удалением маркеров debug с прошедших тестов
pytest --debug-only --mark-fixed
```

## Генерация отчетов

### Allure отчеты

```bash
# Генерация результатов Allure
pytest --alluredir=allure-results

# Просмотр отчета
allure serve allure-results

# Генерация статического отчета
allure generate allure-results -o allure-report --clean
```

### HTML отчеты

```bash
# Генерация HTML отчета
pytest --html=report.html --self-contained-html

# Отчет с покрытием кода
pytest --cov=. --cov-report=html
```

### Скриншоты при падении

```bash
# Автоматические скриншоты при падении тестов
pytest --screenshot_path=screenshots --screenshot_on_failure
```

## Типы тестов

### E2E тесты

**Технологии:** Playwright, Pytest, Allure

**Структура:**
```python
@allure.feature("E-commerce")
@allure.story("Покупка товара")
@pytest.mark.critical
@pytest.mark.ecommerce
def test_complete_purchase():
    """Полный процесс покупки товара"""
    with allure.step("Добавление товара в корзину"):
        # Код теста
        pass
```

**Page Object Model:**
```python
class ShopPage(BasePage):
    def search_products(self, query):
        """Поиск товаров"""
        self.find_element(*ShopLocators.SEARCH_INPUT).send_keys(query)
        self.find_element(*ShopLocators.SEARCH_BUTTON).click()
```

### API тесты

**Технологии:** Requests, Pytest, Pydantic

```python
@pytest.mark.api
@pytest.mark.ecommerce
def test_create_product():
    """API тест создания товара"""
    response = api_client.post("/api/ecommerce/products", data=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
```

### Database тесты

**Технологии:** SQLAlchemy, Pytest

```python
@pytest.mark.database
@pytest.mark.models
def test_user_creation():
    """Тест создания пользователя в БД"""
    user = User(email="test@example.com", username="testuser")
    db.add(user)
    db.commit()
    assert user.id is not None
```

## Конфигурация

### pytest.ini

```ini
[tool:pytest]
markers =
    debug: Tests requiring debugging
    fixme: Broken tests
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

addopts = 
    --strict-markers
    --verbose
    --alluredir=allure-results
    --screenshot_path=screenshots
```

### Docker конфигурация

```yaml
services:
  e2e-tests:
    build: ./e2e-automation
    environment:
      - TEST_ENV=docker
      - API_BASE_URL=http://backend:5000
      - FRONTEND_URL=http://frontend:80
    volumes:
      - ./allure-results:/app/allure-results
      - ./screenshots:/app/screenshots
    command: pytest --alluredir=allure-results
```

## Best Practices

### Написание тестов

1. **Используйте Page Object Model**
2. **Применяйте data-driven подход**
3. **Делайте тесты независимыми**
4. **Используйте понятные имена**
5. **Добавляйте детальные описания**

### Отладка

1. **Маркируйте проблемные тесты `@debug`**
2. **Запускайте только отмеченные тесты**
3. **Используйте скриншоты и логи**
4. **Проверяйте данные и окружение**
5. **Снимайте маркеры после исправления**

### Поддержка

1. **Регулярно обновляйте селекторы**
2. **Следите за изменениями в приложении**
3. **Оптимизируйте медленные тесты**
4. **Удаляйте устаревшие тесты**
5. **Документируйте изменения**

## Мониторинг и метрики

### Ключевые метрики

- **Успешность тестов:** > 90%
- **Время выполнения:** < 30 минут для полного набора
- **Покрытие кода:** > 80%
- **Количество flaky тестов:** < 5%

### Отчеты

- **Allure отчеты** с детальной информацией
- **Screenshots** при падении тестов
- **Видео записи** для сложных тестов
- **Performance метрики** для медленных тестов

## Интеграция с CI/CD

### GitHub Actions

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run E2E tests
        run: |
          docker-compose up --build --abort-on-container-exit e2e-tests
      - name: Upload Allure results
        uses: actions/upload-artifact@v3
        with:
          name: allure-results
          path: allure-results/
```

### Уведомления

- **Slack уведомления** при падении критических тестов
- **Email отчеты** для заинтересованных лиц
- **Dashboard** с метриками тестирования

## Troubleshooting

### Частые проблемы

1. **TimeoutException** - увеличить время ожидания
2. **ElementNotInteractableException** - добавить ожидание загрузки
3. **NoSuchElementException** - проверить селекторы
4. **StaleElementReferenceException** - переполучить элемент

### Решения

```python
# Увеличение времени ожидания
@pytest.fixture
def browser():
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    yield browser
    browser.quit()

# Ожидание загрузки элемента
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(browser, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, "button")))
```

## Заключение

Система маркировки тестов позволяет эффективно отлаживать и поддерживать тесты. Регулярное использование маркеров `@debug` и `@fixme` помогает быстро находить и исправлять проблемные тесты, а автоматизация процесса упрощает работу команды.
