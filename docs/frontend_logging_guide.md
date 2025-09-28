# 🔍 Руководство по логгированию фронтенда для автотестов

## Обзор

Система логгирования фронтенда предоставляет полный мониторинг всех событий, происходящих в браузере, что позволяет автотестам:

- **Перехватывать** все пользовательские действия
- **Мониторить** API запросы и ответы
- **Отслеживать** ошибки и исключения
- **Анализировать** производительность
- **Детектировать** изменения DOM

## Архитектура

### Основные компоненты:

1. **Logger** (`utils/logger.js`) - Основная система логгирования
2. **TestLogger** (`utils/test_logger.js`) - API для автотестов
3. **Backend API** (`/api/logs`) - Серверная часть для сбора логов

## Автоматическое логгирование

### Перехватываемые события:

#### 1. **Console методы**
```javascript
console.log('Test message') // → DEBUG: CONSOLE
console.error('Error message') // → ERROR: CONSOLE
```

#### 2. **Fetch запросы**
```javascript
fetch('/api/users') // → DEBUG: FETCH_REQUEST
// Response → INFO: FETCH_RESPONSE
// Error → ERROR: FETCH_ERROR
```

#### 3. **Пользовательские действия**
```javascript
// Клик по кнопке
button.click() // → DEBUG: USER_ACTION
// Ввод в поле
input.value = 'test' // → DEBUG: USER_ACTION
```

#### 4. **JavaScript ошибки**
```javascript
// Uncaught errors → ERROR: JAVASCRIPT_ERROR
// Promise rejections → ERROR: PROMISE_REJECTION
// Resource errors → ERROR: RESOURCE_ERROR
```

#### 5. **Изменения DOM**
```javascript
// Добавление элементов → DEBUG: DOM_CHANGE
// Изменение атрибутов → DEBUG: DOM_ATTR_CHANGE
```

#### 6. **Навигация**
```javascript
// History API → DEBUG: NAVIGATION
// Hash changes → DEBUG: NAVIGATION
```

## API для автотестов

### Глобальные функции:

```javascript
// Получение всех логов
const logs = getTestLogs();

// Фильтрация логов
const errorLogs = getTestLogs({ level: 'error' });
const apiLogs = getTestLogs({ category: 'FETCH_REQUEST' });
const recentLogs = getTestLogs({ since: '2024-01-01T00:00:00Z' });

// Очистка логов
clearTestLogs();

// Экспорт логов
const exportData = exportTestLogs();
```

### Расширенный API:

```javascript
// Ожидание конкретного лога
const log = await waitForLog({
    category: 'USER_ACTION',
    message: 'click'
}, 5000);

// Ожидание завершения асинхронных операций
await waitForAsyncOperations(3000);

// Получение статистики
const stats = TestLogger.getLogStats();

// Поиск по паттерну
const searchResults = TestLogger.searchLogs('error.*api');

// Логи для конкретного элемента
const elementLogs = TestLogger.getElementLogs('#submit-btn');

// API логи
const apiLogs = TestLogger.getApiLogs();

// Пользовательские действия
const userActions = TestLogger.getUserActionLogs();

// Ошибки
const errors = TestLogger.getErrorLogs();
```

## Структура лог-записи

```javascript
{
    timestamp: "2024-01-15T10:30:45.123Z",
    level: "debug|info|warn|error",
    category: "USER_ACTION|FETCH_REQUEST|API_ERROR|...",
    message: "Описание события",
    data: {
        // Дополнительные данные
        tagName: "BUTTON",
        id: "submit-btn",
        testId: "submit-button",
        xpath: "//button[@id='submit-btn']",
        value: "Submit",
        // ... другие поля
    },
    url: "http://localhost:8000/login.html",
    userAgent: "Mozilla/5.0...",
    sessionId: "session_1234567890_abc123"
}
```

## Категории логов

### Системные:
- `CONSOLE` - Console методы
- `JAVASCRIPT_ERROR` - JavaScript ошибки
- `PROMISE_REJECTION` - Необработанные Promise
- `RESOURCE_ERROR` - Ошибки загрузки ресурсов

### API:
- `FETCH_REQUEST` - Исходящие запросы
- `FETCH_RESPONSE` - Успешные ответы
- `FETCH_ERROR` - Ошибки запросов
- `API_REQUEST` - API запросы через ApiService
- `API_SUCCESS` - Успешные API ответы
- `API_ERROR` - Ошибки API
- `API_AUTH` - Аутентификация

### Пользовательские действия:
- `USER_ACTION` - Клики, ввод, изменения
- `NAVIGATION` - Переходы между страницами
- `DOM_CHANGE` - Изменения DOM
- `DOM_ATTR_CHANGE` - Изменения атрибутов

### Тестовые:
- `TEST_START` - Начало теста
- `TEST_END` - Завершение теста
- `TEST_STEP` - Тестовый шаг

## Примеры использования в автотестах

### Selenium/WebDriver:

```python
# Python + Selenium
def test_login_with_logging(driver):
    # Включаем тестовый режим
    driver.execute_script("window.__TEST_MODE__ = true;")
    
    # Выполняем действия
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login-btn").click()
    
    # Получаем логи
    logs = driver.execute_script("return getTestLogs();")
    
    # Проверяем, что логин был залогирован
    login_logs = [log for log in logs if log['category'] == 'AUTH_LOGIN']
    assert len(login_logs) > 0
    assert login_logs[-1]['level'] == 'info'
    assert 'Login successful' in login_logs[-1]['message']
```

### Playwright:

```javascript
// JavaScript + Playwright
test('login with logging', async ({ page }) => {
    // Включаем тестовый режим
    await page.addInitScript(() => {
        window.__TEST_MODE__ = true;
    });
    
    await page.goto('http://localhost:8000/login.html');
    
    // Выполняем действия
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'password123');
    await page.click('#login-btn');
    
    // Получаем логи
    const logs = await page.evaluate(() => getTestLogs());
    
    // Проверяем логи
    const loginLogs = logs.filter(log => log.category === 'AUTH_LOGIN');
    expect(loginLogs.length).toBeGreaterThan(0);
    expect(loginLogs[loginLogs.length - 1].level).toBe('info');
    expect(loginLogs[loginLogs.length - 1].message).toContain('Login successful');
});
```

### Cypress:

```javascript
// JavaScript + Cypress
describe('Login with logging', () => {
    it('should log login process', () => {
        // Включаем тестовый режим
        cy.window().then((win) => {
            win.__TEST_MODE__ = true;
        });
        
        cy.visit('http://localhost:8000/login.html');
        
        // Выполняем действия
        cy.get('#email').type('test@example.com');
        cy.get('#password').type('password123');
        cy.get('#login-btn').click();
        
        // Получаем логи
        cy.window().then((win) => {
            const logs = win.getTestLogs();
            const loginLogs = logs.filter(log => log.category === 'AUTH_LOGIN');
            
            expect(loginLogs.length).to.be.greaterThan(0);
            expect(loginLogs[loginLogs.length - 1].level).to.equal('info');
            expect(loginLogs[loginLogs.length - 1].message).to.contain('Login successful');
        });
    });
});
```

## Настройка уровня логирования

```javascript
// В тестах можно настроить уровень логирования
window.Logger.setLogLevel('debug'); // debug, info, warn, error

// Включить/выключить различные типы логирования
window.Logger.setEnabled(
    console: true,    // Вывод в консоль
    storage: true,    // Сохранение в localStorage
    network: true     // Отправка на сервер
);
```

## Мониторинг производительности

```javascript
// Получение логов API запросов с временем выполнения
const apiLogs = TestLogger.getApiLogs();
const slowRequests = apiLogs.filter(log => 
    log.data && log.data.duration > 1000
);

// Статистика по категориям
const stats = TestLogger.getLogStats();
console.log('API calls:', stats.byCategory.FETCH_REQUEST);
console.log('User actions:', stats.byCategory.USER_ACTION);
console.log('Errors:', stats.errors);
```

## Отладка тестов

```javascript
// Поиск логов по паттерну
const errorLogs = TestLogger.searchLogs('error.*login');

// Логи для конкретного элемента
const buttonLogs = TestLogger.getElementLogs('#submit-btn');

// Экспорт всех логов для анализа
const exportData = TestLogger.exportTestLogs();
console.log(JSON.stringify(exportData, null, 2));
```

## Лучшие практики

1. **Включайте тестовый режим** в начале каждого теста
2. **Очищайте логи** между тестами для изоляции
3. **Используйте фильтры** для поиска конкретных событий
4. **Проверяйте логи** для валидации поведения приложения
5. **Экспортируйте логи** при падении тестов для анализа
6. **Мониторьте производительность** через логи API запросов

## Troubleshooting

### Логи не появляются:
- Проверьте, что `window.__TEST_MODE__ = true`
- Убедитесь, что `utils/logger.js` и `utils/test_logger.js` загружены
- Проверьте уровень логирования

### Слишком много логов:
- Увеличьте уровень логирования: `window.Logger.setLogLevel('warn')`
- Используйте фильтры для поиска нужных событий
- Очищайте логи между тестами

### Производительность:
- Логи сохраняются в памяти (максимум 1000-2000 записей)
- Старые логи автоматически удаляются
- Можно отключить отправку на сервер: `window.Logger.setEnabled(true, true, false)`
