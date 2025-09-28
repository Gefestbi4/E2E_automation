/**
 * Продвинутая система валидации форм
 * Поддерживает различные типы валидации, асинхронную валидацию и кастомные правила
 */

class FormValidator {
    constructor(form, options = {}) {
        this.form = form;
        this.options = {
            validateOnChange: true,
            validateOnBlur: true,
            showErrorsInline: true,
            errorClass: 'error',
            successClass: 'success',
            ...options
        };

        this.rules = new Map();
        this.errors = new Map();
        this.isValid = true;

        this.init();
    }

    /**
     * Инициализация валидатора
     */
    init() {
        this.setupEventListeners();
        this.setupDefaultRules();
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        if (this.options.validateOnChange) {
            this.form.addEventListener('input', (e) => {
                if (e.target.matches('input, textarea, select')) {
                    this.validateField(e.target);
                }
            });
        }

        if (this.options.validateOnBlur) {
            this.form.addEventListener('blur', (e) => {
                if (e.target.matches('input, textarea, select')) {
                    this.validateField(e.target);
                }
            }, true);
        }

        this.form.addEventListener('submit', (e) => {
            if (!this.validateForm()) {
                e.preventDefault();
            }
        });
    }

    /**
     * Настройка правил валидации по умолчанию
     */
    setupDefaultRules() {
        // Email валидация
        this.addRule('email', {
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Введите корректный email адрес'
        });

        // Пароль валидация
        this.addRule('password', {
            minLength: 8,
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
            message: 'Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и специальные символы'
        });

        // Обязательные поля
        this.addRule('required', {
            required: true,
            message: 'Это поле обязательно для заполнения'
        });

        // Минимальная длина
        this.addRule('minLength', {
            minLength: 3,
            message: 'Минимальная длина: {minLength} символов'
        });

        // Максимальная длина
        this.addRule('maxLength', {
            maxLength: 255,
            message: 'Максимальная длина: {maxLength} символов'
        });

        // Числовые значения
        this.addRule('number', {
            pattern: /^\d+(\.\d+)?$/,
            message: 'Введите корректное число'
        });

        // Положительные числа
        this.addRule('positive', {
            pattern: /^\d+(\.\d+)?$/,
            min: 0,
            message: 'Введите положительное число'
        });

        // URL валидация
        this.addRule('url', {
            pattern: /^https?:\/\/.+/,
            message: 'Введите корректный URL (начинающийся с http:// или https://)'
        });

        // Телефон валидация
        this.addRule('phone', {
            pattern: /^[\+]?[1-9][\d]{0,15}$/,
            message: 'Введите корректный номер телефона'
        });
    }

    /**
     * Добавление правила валидации
     */
    addRule(name, rule) {
        this.rules.set(name, rule);
    }

    /**
     * Валидация поля
     */
    async validateField(field) {
        const fieldName = field.name || field.id;
        if (!fieldName) return true;

        const rules = this.getFieldRules(field);
        const value = field.value.trim();

        // Очищаем предыдущие ошибки
        this.clearFieldError(field);

        for (const rule of rules) {
            const error = await this.validateValue(value, rule, field);
            if (error) {
                this.setFieldError(field, error);
                return false;
            }
        }

        this.setFieldSuccess(field);
        return true;
    }

    /**
     * Получение правил для поля
     */
    getFieldRules(field) {
        const rules = [];
        const fieldRules = field.dataset.validate?.split(' ') || [];

        for (const ruleName of fieldRules) {
            const rule = this.rules.get(ruleName);
            if (rule) {
                rules.push({ ...rule, name: ruleName });
            }
        }

        // Добавляем правила на основе типа поля
        if (field.type === 'email') {
            rules.push(this.rules.get('email'));
        }

        if (field.required) {
            rules.push(this.rules.get('required'));
        }

        return rules.filter(Boolean);
    }

    /**
     * Валидация значения по правилу
     */
    async validateValue(value, rule, field) {
        // Проверка обязательности
        if (rule.required && (!value || value.trim() === '')) {
            return rule.message;
        }

        // Если поле пустое и не обязательное, пропускаем валидацию
        if (!value && !rule.required) {
            return null;
        }

        // Проверка минимальной длины
        if (rule.minLength && value.length < rule.minLength) {
            return rule.message.replace('{minLength}', rule.minLength);
        }

        // Проверка максимальной длины
        if (rule.maxLength && value.length > rule.maxLength) {
            return rule.message.replace('{maxLength}', rule.maxLength);
        }

        // Проверка паттерна
        if (rule.pattern && !rule.pattern.test(value)) {
            return rule.message;
        }

        // Проверка минимального значения
        if (rule.min !== undefined && parseFloat(value) < rule.min) {
            return rule.message.replace('{min}', rule.min);
        }

        // Проверка максимального значения
        if (rule.max !== undefined && parseFloat(value) > rule.max) {
            return rule.message.replace('{max}', rule.max);
        }

        // Асинхронная валидация
        if (rule.async) {
            try {
                const result = await rule.async(value, field);
                if (result !== true) {
                    return result;
                }
            } catch (error) {
                return 'Ошибка валидации: ' + error.message;
            }
        }

        // Кастомная валидация
        if (rule.custom) {
            try {
                const result = rule.custom(value, field);
                if (result !== true) {
                    return result;
                }
            } catch (error) {
                return 'Ошибка валидации: ' + error.message;
            }
        }

        return null;
    }

    /**
     * Валидация всей формы
     */
    async validateForm() {
        this.isValid = true;
        this.errors.clear();

        const fields = this.form.querySelectorAll('input, textarea, select');
        const validationPromises = Array.from(fields).map(field => this.validateField(field));

        const results = await Promise.all(validationPromises);
        this.isValid = results.every(result => result);

        if (!this.isValid) {
            this.showFormErrors();
        }

        return this.isValid;
    }

    /**
     * Установка ошибки для поля
     */
    setFieldError(field, message) {
        this.errors.set(field.name || field.id, message);
        this.isValid = false;

        if (this.options.showErrorsInline) {
            field.classList.add(this.options.errorClass);
            field.classList.remove(this.options.successClass);

            // Показываем сообщение об ошибке
            this.showFieldError(field, message);
        }
    }

    /**
     * Установка успешной валидации для поля
     */
    setFieldSuccess(field) {
        field.classList.add(this.options.successClass);
        field.classList.remove(this.options.errorClass);
        this.clearFieldError(field);
    }

    /**
     * Очистка ошибки поля
     */
    clearFieldError(field) {
        field.classList.remove(this.options.errorClass);

        // Удаляем сообщение об ошибке
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    /**
     * Показ ошибки поля
     */
    showFieldError(field, message) {
        // Удаляем существующее сообщение об ошибке
        this.clearFieldError(field);

        // Создаем элемент ошибки
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        errorElement.style.color = '#e74c3c';
        errorElement.style.fontSize = '0.875rem';
        errorElement.style.marginTop = '0.25rem';

        // Вставляем после поля
        field.parentNode.insertBefore(errorElement, field.nextSibling);
    }

    /**
     * Показ ошибок формы
     */
    showFormErrors() {
        const errorSummary = document.createElement('div');
        errorSummary.className = 'form-errors';
        errorSummary.style.cssText = `
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border: 1px solid #f5c6cb;
            border-radius: 0.375rem;
            margin-bottom: 1rem;
        `;

        const errorTitle = document.createElement('h4');
        errorTitle.textContent = 'Исправьте следующие ошибки:';
        errorTitle.style.margin = '0 0 0.5rem 0';

        const errorList = document.createElement('ul');
        errorList.style.margin = '0';
        errorList.style.paddingLeft = '1.5rem';

        this.errors.forEach((message, fieldName) => {
            const errorItem = document.createElement('li');
            errorItem.textContent = `${fieldName}: ${message}`;
            errorList.appendChild(errorItem);
        });

        errorSummary.appendChild(errorTitle);
        errorSummary.appendChild(errorList);

        // Вставляем в начало формы
        this.form.insertBefore(errorSummary, this.form.firstChild);

        // Удаляем через 5 секунд
        setTimeout(() => {
            if (errorSummary.parentNode) {
                errorSummary.remove();
            }
        }, 5000);
    }

    /**
     * Получение данных формы
     */
    getFormData() {
        const formData = new FormData(this.form);
        const data = {};

        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }

        return data;
    }

    /**
     * Очистка формы
     */
    resetForm() {
        this.form.reset();
        this.errors.clear();
        this.isValid = true;

        // Очищаем все ошибки
        const fields = this.form.querySelectorAll('input, textarea, select');
        fields.forEach(field => {
            this.clearFieldError(field);
        });

        // Удаляем сводку ошибок
        const errorSummary = this.form.querySelector('.form-errors');
        if (errorSummary) {
            errorSummary.remove();
        }
    }

    /**
     * Установка значений формы
     */
    setFormData(data) {
        Object.keys(data).forEach(key => {
            const field = this.form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
}

// Экспорт для глобального доступа
window.FormValidator = FormValidator;
