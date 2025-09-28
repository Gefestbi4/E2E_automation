# Frontend Phase 1: Core Infrastructure & Authentication - Detailed Plan

## 🎯 Цели Phase 1

1. **Исправить критические проблемы с авторизацией**
2. **Обеспечить полную интеграцию с бекенд API**
3. **Создать систему валидации форм**
4. **Реализовать централизованную обработку ошибок**

## 📋 Детальные задачи

### 1.1 Исправление проблем с авторизацией

#### Задача 1.1.1: Исправить проблему с index.html
**Приоритет: CRITICAL | Время: 30 минут**

**Проблема:**
- Nginx ищет `index.html`, а у нас есть только `index_new.html`
- На порту 3000 отображается дефолтная страница Nginx

**Решение:**
```bash
# В директории frontend
mv index_new.html index.html
```

**Проверка:**
- Перезапустить frontend контейнер
- Убедиться, что на `http://localhost:3000` отображается приложение

#### Задача 1.1.2: Оптимизировать AuthService
**Приоритет: HIGH | Время: 2-3 часа**

**Текущие проблемы:**
- Fallback код для ошибок
- Неоптимальная обработка токенов
- Отсутствие автоматического обновления

**Улучшения:**
```javascript
// services/auth.js - оптимизированная версия
class AuthService {
    constructor() {
        this.apiBase = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
        this.refreshTimer = null;
        this.isRefreshing = false;
        this.pendingRequests = [];
    }

    // Улучшенная проверка токена
    isTokenValid(token) {
        if (!token) return false;
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const now = Date.now() / 1000;
            return payload.exp > now;
        } catch {
            return false;
        }
    }

    // Автоматическое обновление токена
    async refreshTokenIfNeeded() {
        const token = localStorage.getItem('auth_token');
        const expires = localStorage.getItem('token_expires');
        
        if (!token || !expires) return false;
        
        // Обновляем токен за 5 минут до истечения
        const refreshTime = parseInt(expires) - 300000;
        if (Date.now() > refreshTime && !this.isRefreshing) {
            return await this.refreshToken();
        }
        
        return true;
    }

    // Очередь запросов во время обновления токена
    async queueRequest(requestFn) {
        if (this.isRefreshing) {
            return new Promise((resolve) => {
                this.pendingRequests.push(resolve);
            }).then(() => requestFn());
        }
        return requestFn();
    }
}
```

#### Задача 1.1.3: Реализовать защиту маршрутов
**Приоритет: HIGH | Время: 1-2 часа**

**Создать Route Guard:**
```javascript
// utils/route-guard.js
class RouteGuard {
    static async checkAuth() {
        if (!window.AuthService.isAuthenticated()) {
            window.location.href = '/login_new.html';
            return false;
        }
        
        // Проверяем актуальность токена
        const isValid = await window.AuthService.refreshTokenIfNeeded();
        if (!isValid) {
            window.location.href = '/login_new.html';
            return false;
        }
        
        return true;
    }
    
    static async protectRoute(routeName) {
        const isAuthenticated = await this.checkAuth();
        if (!isAuthenticated) {
            return false;
        }
        
        // Дополнительные проверки по ролям (если нужно)
        return true;
    }
}
```

### 1.2 Улучшение API интеграции

#### Задача 1.2.1: Обновить API сервисы под новые бекенд схемы
**Приоритет: HIGH | Время: 4-5 часов**

**Обновить ApiService:**
```javascript
// services/api.js - улучшенная версия
class ApiService {
    constructor() {
        this.baseURL = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
        this.retryAttempts = 3;
        this.retryDelay = 1000;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        // Подготавливаем заголовки
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        // Добавляем авторизацию если нужно
        const token = localStorage.getItem('auth_token');
        if (token && !options.skipAuth) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const config = {
            ...options,
            headers
        };
        
        return this.makeRequestWithRetry(url, config);
    }
    
    async makeRequestWithRetry(url, config, attempt = 1) {
        try {
            const response = await fetch(url, config);
            
            // Если токен истек, пытаемся обновить
            if (response.status === 401 && attempt === 1) {
                const refreshed = await window.AuthService.refreshToken();
                if (refreshed) {
                    // Обновляем заголовок авторизации
                    config.headers['Authorization'] = `Bearer ${localStorage.getItem('auth_token')}`;
                    return this.makeRequestWithRetry(url, config, attempt + 1);
                }
            }
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new ApiError(response.status, errorData.detail || `HTTP ${response.status}`, errorData);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            if (attempt < this.retryAttempts && this.shouldRetry(error)) {
                await this.delay(this.retryDelay * attempt);
                return this.makeRequestWithRetry(url, config, attempt + 1);
            }
            throw error;
        }
    }
    
    shouldRetry(error) {
        return error instanceof TypeError || // Network error
               (error instanceof ApiError && error.status >= 500); // Server error
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Кастомный класс ошибок API
class ApiError extends Error {
    constructor(status, message, data = {}) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
        this.data = data;
    }
}
```

#### Задача 1.2.2: Добавить обработку ошибок API
**Приоритет: HIGH | Время: 2-3 часа**

**Создать ErrorHandler:**
```javascript
// utils/error-handler.js
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        if (error instanceof ApiError) {
            this.handleApiError(error, context);
        } else if (error instanceof TypeError) {
            this.handleNetworkError(error, context);
        } else {
            this.handleGenericError(error, context);
        }
    }
    
    static handleApiError(error, context) {
        switch (error.status) {
            case 401:
                this.showError('Сессия истекла. Пожалуйста, войдите заново.');
                window.AuthService.logout();
                break;
            case 403:
                this.showError('Недостаточно прав для выполнения этого действия.');
                break;
            case 404:
                this.showError('Запрашиваемый ресурс не найден.');
                break;
            case 422:
                this.showValidationErrors(error.data);
                break;
            case 429:
                this.showError('Слишком много запросов. Попробуйте позже.');
                break;
            case 500:
                this.showError('Внутренняя ошибка сервера. Попробуйте позже.');
                break;
            default:
                this.showError(error.message || 'Произошла ошибка при выполнении запроса.');
        }
    }
    
    static handleNetworkError(error, context) {
        this.showError('Ошибка сети. Проверьте подключение к интернету.');
    }
    
    static handleGenericError(error, context) {
        this.showError('Произошла неожиданная ошибка.');
    }
    
    static showValidationErrors(data) {
        if (data.errors && Array.isArray(data.errors)) {
            data.errors.forEach(error => {
                this.showError(`${error.field}: ${error.message}`);
            });
        } else {
            this.showError(data.detail || 'Ошибка валидации данных.');
        }
    }
    
    static showError(message) {
        if (window.ToastService) {
            window.ToastService.error(message);
        } else {
            alert(message);
        }
    }
}
```

#### Задача 1.2.3: Реализовать loading states
**Приоритет: MEDIUM | Время: 2-3 часа**

**Создать LoadingService:**
```javascript
// utils/loading-service.js
class LoadingService {
    constructor() {
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingStates = new Map();
    }
    
    show(identifier = 'global', message = 'Загрузка...') {
        if (identifier === 'global') {
            this.showGlobalLoading(message);
        } else {
            this.loadingStates.set(identifier, true);
            this.updateLoadingUI(identifier, message);
        }
    }
    
    hide(identifier = 'global') {
        if (identifier === 'global') {
            this.hideGlobalLoading();
        } else {
            this.loadingStates.delete(identifier);
            this.updateLoadingUI(identifier);
        }
    }
    
    showGlobalLoading(message) {
        if (this.loadingOverlay) {
            const spinner = this.loadingOverlay.querySelector('.loading-spinner span');
            if (spinner) spinner.textContent = message;
            this.loadingOverlay.style.display = 'flex';
        }
    }
    
    hideGlobalLoading() {
        if (this.loadingOverlay) {
            this.loadingOverlay.style.display = 'none';
        }
    }
    
    updateLoadingUI(identifier, message) {
        const element = document.querySelector(`[data-loading="${identifier}"]`);
        if (element) {
            if (message) {
                element.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
                element.disabled = true;
            } else {
                element.innerHTML = element.getAttribute('data-original-text') || 'Сохранить';
                element.disabled = false;
            }
        }
    }
    
    isLoading(identifier = 'global') {
        return this.loadingStates.has(identifier);
    }
}

// Создаем глобальный экземпляр
window.LoadingService = new LoadingService();
```

### 1.3 Валидация форм

#### Задача 1.3.1: Создать систему валидации форм
**Приоритет: HIGH | Время: 3-4 часа**

**Создать FormValidator:**
```javascript
// utils/form-validator.js
class FormValidator {
    constructor(form) {
        this.form = form;
        this.rules = {};
        this.errors = {};
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadRules();
    }
    
    setupEventListeners() {
        // Real-time валидация
        this.form.addEventListener('input', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.validateField(e.target);
            }
        });
        
        // Валидация при потере фокуса
        this.form.addEventListener('blur', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.validateField(e.target);
            }
        }, true);
        
        // Валидация при отправке формы
        this.form.addEventListener('submit', (e) => {
            if (!this.validateForm()) {
                e.preventDefault();
            }
        });
    }
    
    loadRules() {
        // Правила валидации для разных полей
        this.rules = {
            email: {
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Введите корректный email адрес'
            },
            password: {
                required: true,
                minLength: 8,
                pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
                message: 'Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и специальные символы'
            },
            username: {
                required: true,
                minLength: 3,
                maxLength: 20,
                pattern: /^[a-zA-Z0-9_]+$/,
                message: 'Имя пользователя должно содержать 3-20 символов (только буквы, цифры и _)'
            },
            full_name: {
                maxLength: 100,
                message: 'Полное имя не должно превышать 100 символов'
            },
            phone: {
                pattern: /^\+?[1-9]\d{1,14}$/,
                message: 'Введите корректный номер телефона'
            }
        };
    }
    
    validateField(field) {
        const fieldName = field.name;
        const value = field.value.trim();
        const rules = this.getFieldRules(fieldName);
        
        if (!rules) return true;
        
        const errors = [];
        
        // Проверка обязательности
        if (rules.required && !value) {
            errors.push('Это поле обязательно для заполнения');
        }
        
        // Проверка минимальной длины
        if (value && rules.minLength && value.length < rules.minLength) {
            errors.push(`Минимальная длина: ${rules.minLength} символов`);
        }
        
        // Проверка максимальной длины
        if (value && rules.maxLength && value.length > rules.maxLength) {
            errors.push(`Максимальная длина: ${rules.maxLength} символов`);
        }
        
        // Проверка паттерна
        if (value && rules.pattern && !rules.pattern.test(value)) {
            errors.push(rules.message);
        }
        
        // Специальные проверки
        if (value && rules.custom && typeof rules.custom === 'function') {
            const customError = rules.custom(value, field);
            if (customError) errors.push(customError);
        }
        
        this.setFieldErrors(fieldName, errors);
        return errors.length === 0;
    }
    
    validateForm() {
        const fields = this.form.querySelectorAll('[data-validate]');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    getFieldRules(fieldName) {
        return this.rules[fieldName] || this.getCustomRules(fieldName);
    }
    
    getCustomRules(fieldName) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        if (!field) return null;
        
        const rules = {};
        
        // Читаем правила из data-атрибутов
        if (field.hasAttribute('data-required')) {
            rules.required = true;
        }
        
        if (field.hasAttribute('data-min-length')) {
            rules.minLength = parseInt(field.getAttribute('data-min-length'));
        }
        
        if (field.hasAttribute('data-max-length')) {
            rules.maxLength = parseInt(field.getAttribute('data-max-length'));
        }
        
        if (field.hasAttribute('data-pattern')) {
            const pattern = field.getAttribute('data-pattern');
            rules.pattern = new RegExp(pattern);
        }
        
        if (field.hasAttribute('data-message')) {
            rules.message = field.getAttribute('data-message');
        }
        
        return Object.keys(rules).length > 0 ? rules : null;
    }
    
    setFieldErrors(fieldName, errors) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        if (!field) return;
        
        // Удаляем старые ошибки
        this.clearFieldErrors(field);
        
        // Добавляем новые ошибки
        if (errors.length > 0) {
            field.classList.add('error');
            
            const errorContainer = document.createElement('div');
            errorContainer.className = 'field-error';
            errorContainer.innerHTML = errors.join('<br>');
            
            field.parentNode.appendChild(errorContainer);
            
            this.errors[fieldName] = errors;
        } else {
            field.classList.remove('error');
            field.classList.add('valid');
            delete this.errors[fieldName];
        }
    }
    
    clearFieldErrors(field) {
        field.classList.remove('error', 'valid');
        const errorContainer = field.parentNode.querySelector('.field-error');
        if (errorContainer) {
            errorContainer.remove();
        }
    }
    
    getFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    getErrors() {
        return this.errors;
    }
    
    hasErrors() {
        return Object.keys(this.errors).length > 0;
    }
}
```

#### Задача 1.3.2: Добавить валидацию для всех форм
**Приоритет: HIGH | Время: 2-3 часа**

**Обновить формы:**
```html
<!-- Пример обновленной формы регистрации -->
<form id="register-form" data-validate>
    <div class="form-group">
        <label for="email">Email *</label>
        <input 
            type="email" 
            id="email" 
            name="email" 
            data-validate
            data-required
            data-pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$"
            data-message="Введите корректный email адрес"
            required
        >
    </div>
    
    <div class="form-group">
        <label for="username">Имя пользователя *</label>
        <input 
            type="text" 
            id="username" 
            name="username" 
            data-validate
            data-required
            data-min-length="3"
            data-max-length="20"
            data-pattern="^[a-zA-Z0-9_]+$"
            data-message="Имя пользователя должно содержать 3-20 символов (только буквы, цифры и _)"
            required
        >
    </div>
    
    <div class="form-group">
        <label for="password">Пароль *</label>
        <input 
            type="password" 
            id="password" 
            name="password" 
            data-validate
            data-required
            data-min-length="8"
            data-message="Пароль должен содержать минимум 8 символов"
            required
        >
    </div>
    
    <div class="form-group">
        <label for="confirm_password">Подтверждение пароля *</label>
        <input 
            type="password" 
            id="confirm_password" 
            name="confirm_password" 
            data-validate
            data-required
            data-message="Пароли должны совпадать"
            required
        >
    </div>
    
    <button type="submit" class="btn btn-primary">
        Зарегистрироваться
    </button>
</form>
```

**Инициализация валидации:**
```javascript
// В components/forms.js
document.addEventListener('DOMContentLoaded', () => {
    // Инициализируем валидацию для всех форм
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        new FormValidator(form);
    });
});
```

### 1.4 Централизованная обработка ошибок

#### Задача 1.4.1: Создать систему логирования
**Приоритет: MEDIUM | Время: 1-2 часа**

**Создать Logger:**
```javascript
// utils/logger.js
class Logger {
    constructor() {
        this.logs = [];
        this.maxLogs = 100;
    }
    
    log(level, message, data = {}) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level,
            message,
            data,
            url: window.location.href,
            userAgent: navigator.userAgent
        };
        
        this.logs.push(logEntry);
        
        // Ограничиваем количество логов
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }
        
        // Выводим в консоль
        console[level](`[${level.toUpperCase()}] ${message}`, data);
        
        // Отправляем критические ошибки на сервер
        if (level === 'error' || level === 'critical') {
            this.sendToServer(logEntry);
        }
    }
    
    info(message, data) {
        this.log('info', message, data);
    }
    
    warn(message, data) {
        this.log('warn', message, data);
    }
    
    error(message, data) {
        this.log('error', message, data);
    }
    
    critical(message, data) {
        this.log('critical', message, data);
    }
    
    async sendToServer(logEntry) {
        try {
            await fetch('/api/logs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify(logEntry)
            });
        } catch (error) {
            console.error('Failed to send log to server:', error);
        }
    }
    
    getLogs() {
        return [...this.logs];
    }
    
    clearLogs() {
        this.logs = [];
    }
}

// Создаем глобальный экземпляр
window.Logger = new Logger();

// Глобальная обработка ошибок
window.addEventListener('error', (event) => {
    window.Logger.error('Uncaught error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error?.stack
    });
});

window.addEventListener('unhandledrejection', (event) => {
    window.Logger.error('Unhandled promise rejection', {
        reason: event.reason,
        promise: event.promise
    });
});
```

## 🧪 Тестирование Phase 1

### Тест 1: Авторизация
- [ ] **Создать тестового пользователя** (если база очищена)
- [ ] Регистрация нового пользователя
- [ ] Вход в систему
- [ ] Автоматическое обновление токенов
- [ ] Выход из системы
- [ ] Защита маршрутов
- [ ] **Проверить все редиректы** после переименования файлов

### Тест 2: API интеграция
- [ ] Успешные запросы к API
- [ ] Обработка ошибок API
- [ ] Retry логика для failed запросов
- [ ] Loading states

### Тест 3: Валидация форм
- [ ] Real-time валидация
- [ ] Валидация при отправке
- [ ] Отображение ошибок
- [ ] Очистка ошибок

### Тест 4: Обработка ошибок
- [ ] Логирование ошибок
- [ ] Показ пользователю
- [ ] Отправка на сервер
- [ ] Глобальная обработка

## 📊 Метрики успеха Phase 1

- [ ] 100% успешная авторизация
- [ ] 0 критических ошибок в консоли
- [ ] Время загрузки < 2 секунд
- [ ] Все формы с валидацией работают
- [ ] API интеграция работает стабильно

## 🚀 Готовность к следующей фазе

После завершения Phase 1 система будет готова к:
- Полноценной работе с E-commerce модулем
- Стабильной авторизации пользователей
- Надежной интеграции с бекенд API
- Качественной валидации данных

**Время выполнения Phase 1: 3-5 дней**
**Приоритет: CRITICAL**
