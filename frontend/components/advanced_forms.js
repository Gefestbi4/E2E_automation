/**
 * Продвинутая система форм
 * Поддерживает различные типы полей, валидацию, автозаполнение, маски ввода
 */

class AdvancedForm {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.options = {
            validateOnChange: true,
            validateOnBlur: true,
            showErrorsInline: true,
            errorClass: 'error',
            successClass: 'success',
            loadingClass: 'loading',
            autoSave: false,
            autoSaveDelay: 2000,
            ...options
        };

        this.validator = null;
        this.isSubmitting = false;
        this.autoSaveTimer = null;
        this.fieldTypes = new Map();

        this.init();
    }

    /**
     * Инициализация формы
     */
    init() {
        this.setupValidator();
        this.setupFieldTypes();
        this.setupEventListeners();
        this.setupAutoSave();
        this.initializeFields();
    }

    /**
     * Настройка валидатора
     */
    setupValidator() {
        if (window.FormValidator) {
            this.validator = new FormValidator(this.form, {
                validateOnChange: this.options.validateOnChange,
                validateOnBlur: this.options.validateOnBlur,
                showErrorsInline: this.options.showErrorsInline,
                errorClass: this.options.errorClass,
                successClass: this.options.successClass
            });
        }
    }

    /**
     * Настройка типов полей
     */
    setupFieldTypes() {
        // Текстовые поля
        this.fieldTypes.set('text', {
            validate: (value) => this.validateText(value),
            format: (value) => this.formatText(value),
            mask: null
        });

        // Email поля
        this.fieldTypes.set('email', {
            validate: (value) => this.validateEmail(value),
            format: (value) => this.formatEmail(value),
            mask: null
        });

        // Пароли
        this.fieldTypes.set('password', {
            validate: (value) => this.validatePassword(value),
            format: (value) => value,
            mask: null
        });

        // Телефоны
        this.fieldTypes.set('tel', {
            validate: (value) => this.validatePhone(value),
            format: (value) => this.formatPhone(value),
            mask: this.createPhoneMask()
        });

        // Числа
        this.fieldTypes.set('number', {
            validate: (value) => this.validateNumber(value),
            format: (value) => this.formatNumber(value),
            mask: null
        });

        // URL
        this.fieldTypes.set('url', {
            validate: (value) => this.validateUrl(value),
            format: (value) => this.formatUrl(value),
            mask: null
        });

        // Дата
        this.fieldTypes.set('date', {
            validate: (value) => this.validateDate(value),
            format: (value) => this.formatDate(value),
            mask: null
        });
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Обработка отправки формы
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Обработка изменений полей
        if (this.options.validateOnChange) {
            this.form.addEventListener('input', (e) => {
                if (e.target.matches('input, textarea, select')) {
                    this.handleFieldChange(e.target);
                }
            });
        }

        // Обработка потери фокуса
        if (this.options.validateOnBlur) {
            this.form.addEventListener('blur', (e) => {
                if (e.target.matches('input, textarea, select')) {
                    this.handleFieldBlur(e.target);
                }
            }, true);
        }
    }

    /**
     * Настройка автосохранения
     */
    setupAutoSave() {
        if (!this.options.autoSave) return;

        this.form.addEventListener('input', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.scheduleAutoSave();
            }
        });
    }

    /**
     * Инициализация полей
     */
    initializeFields() {
        const fields = this.form.querySelectorAll('input, textarea, select');

        fields.forEach(field => {
            this.initializeField(field);
        });
    }

    /**
     * Инициализация отдельного поля
     */
    initializeField(field) {
        const type = field.type || 'text';
        const fieldConfig = this.fieldTypes.get(type);

        if (!fieldConfig) return;

        // Устанавливаем маску ввода
        if (fieldConfig.mask) {
            this.applyMask(field, fieldConfig.mask);
        }

        // Добавляем индикаторы валидации
        this.addValidationIndicators(field);

        // Настраиваем автозаполнение
        this.setupAutocomplete(field);
    }

    /**
     * Обработка изменения поля
     */
    handleFieldChange(field) {
        this.clearFieldError(field);
        this.formatFieldValue(field);
        this.validateField(field);
    }

    /**
     * Обработка потери фокуса поля
     */
    handleFieldBlur(field) {
        this.validateField(field);
    }

    /**
     * Валидация поля
     */
    validateField(field) {
        if (!this.validator) return true;

        const type = field.type || 'text';
        const fieldConfig = this.fieldTypes.get(type);

        if (fieldConfig) {
            const value = field.value.trim();
            const error = fieldConfig.validate(value);

            if (error) {
                this.setFieldError(field, error);
                return false;
            } else {
                this.setFieldSuccess(field);
                return true;
            }
        }

        return this.validator.validateField(field);
    }

    /**
     * Форматирование значения поля
     */
    formatFieldValue(field) {
        const type = field.type || 'text';
        const fieldConfig = this.fieldTypes.get(type);

        if (fieldConfig && fieldConfig.format) {
            const formatted = fieldConfig.format(field.value);
            if (formatted !== field.value) {
                field.value = formatted;
            }
        }
    }

    /**
     * Обработка отправки формы
     */
    async handleSubmit() {
        if (this.isSubmitting) return;

        this.isSubmitting = true;
        this.setFormLoading(true);

        try {
            // Валидация всей формы
            const isValid = await this.validateForm();

            if (!isValid) {
                this.setFormError('Пожалуйста, исправьте ошибки в форме');
                return;
            }

            // Получение данных формы
            const formData = this.getFormData();

            // Отправка данных
            const result = await this.submitForm(formData);

            // Обработка успешного результата
            this.handleSubmitSuccess(result);

        } catch (error) {
            this.handleSubmitError(error);
        } finally {
            this.isSubmitting = false;
            this.setFormLoading(false);
        }
    }

    /**
     * Валидация всей формы
     */
    async validateForm() {
        if (this.validator) {
            return await this.validator.validateForm();
        }

        const fields = this.form.querySelectorAll('input, textarea, select');
        let isValid = true;

        for (const field of fields) {
            if (!this.validateField(field)) {
                isValid = false;
            }
        }

        return isValid;
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
     * Отправка формы (переопределяется в наследниках)
     */
    async submitForm(data) {
        // Базовая реализация - можно переопределить
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ success: true, data });
            }, 1000);
        });
    }

    /**
     * Обработка успешной отправки
     */
    handleSubmitSuccess(result) {
        if (window.Toast) {
            window.Toast.success('Форма успешно отправлена!');
        }

        // Событие успешной отправки
        this.form.dispatchEvent(new CustomEvent('form:success', {
            detail: result
        }));
    }

    /**
     * Обработка ошибки отправки
     */
    handleSubmitError(error) {
        console.error('Form submission error:', error);

        if (window.Toast) {
            window.Toast.error('Ошибка при отправке формы: ' + error.message);
        }

        // Событие ошибки отправки
        this.form.dispatchEvent(new CustomEvent('form:error', {
            detail: error
        }));
    }

    /**
     * Установка состояния загрузки формы
     */
    setFormLoading(loading) {
        if (loading) {
            this.form.classList.add(this.options.loadingClass);
            this.form.querySelectorAll('button[type="submit"]').forEach(btn => {
                btn.disabled = true;
                btn.textContent = 'Отправка...';
            });
        } else {
            this.form.classList.remove(this.options.loadingClass);
            this.form.querySelectorAll('button[type="submit"]').forEach(btn => {
                btn.disabled = false;
                btn.textContent = btn.dataset.originalText || 'Отправить';
            });
        }
    }

    /**
     * Планирование автосохранения
     */
    scheduleAutoSave() {
        if (this.autoSaveTimer) {
            clearTimeout(this.autoSaveTimer);
        }

        this.autoSaveTimer = setTimeout(() => {
            this.performAutoSave();
        }, this.options.autoSaveDelay);
    }

    /**
     * Выполнение автосохранения
     */
    async performAutoSave() {
        try {
            const data = this.getFormData();
            // Здесь можно отправить данные на сервер
            console.log('Auto-saving form data:', data);
        } catch (error) {
            console.error('Auto-save failed:', error);
        }
    }

    // Методы валидации
    validateText(value) {
        if (!value || value.trim() === '') {
            return 'Это поле обязательно для заполнения';
        }
        return null;
    }

    validateEmail(value) {
        if (!value) return 'Email обязателен';
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            return 'Введите корректный email адрес';
        }
        return null;
    }

    validatePassword(value) {
        if (!value) return 'Пароль обязателен';
        if (value.length < 8) {
            return 'Пароль должен содержать минимум 8 символов';
        }
        return null;
    }

    validatePhone(value) {
        if (!value) return null; // Телефон не обязателен
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phoneRegex.test(value.replace(/\D/g, ''))) {
            return 'Введите корректный номер телефона';
        }
        return null;
    }

    validateNumber(value) {
        if (!value) return null;
        if (isNaN(value)) {
            return 'Введите корректное число';
        }
        return null;
    }

    validateUrl(value) {
        if (!value) return null;
        try {
            new URL(value);
            return null;
        } catch {
            return 'Введите корректный URL';
        }
    }

    validateDate(value) {
        if (!value) return null;
        const date = new Date(value);
        if (isNaN(date.getTime())) {
            return 'Введите корректную дату';
        }
        return null;
    }

    // Методы форматирования
    formatText(value) {
        return value.trim();
    }

    formatEmail(value) {
        return value.toLowerCase().trim();
    }

    formatPhone(value) {
        return value.replace(/\D/g, '');
    }

    formatNumber(value) {
        return parseFloat(value) || 0;
    }

    formatUrl(value) {
        if (!value.startsWith('http://') && !value.startsWith('https://')) {
            return 'https://' + value;
        }
        return value;
    }

    formatDate(value) {
        return value;
    }

    // Создание маски для телефона
    createPhoneMask() {
        return (value) => {
            const numbers = value.replace(/\D/g, '');
            if (numbers.length <= 3) {
                return numbers;
            } else if (numbers.length <= 6) {
                return `(${numbers.slice(0, 3)}) ${numbers.slice(3)}`;
            } else if (numbers.length <= 10) {
                return `(${numbers.slice(0, 3)}) ${numbers.slice(3, 6)}-${numbers.slice(6)}`;
            } else {
                return `+${numbers.slice(0, 1)} (${numbers.slice(1, 4)}) ${numbers.slice(4, 7)}-${numbers.slice(7, 9)}-${numbers.slice(9, 11)}`;
            }
        };
    }

    // Применение маски к полю
    applyMask(field, mask) {
        field.addEventListener('input', (e) => {
            const formatted = mask(e.target.value);
            if (formatted !== e.target.value) {
                e.target.value = formatted;
            }
        });
    }

    // Добавление индикаторов валидации
    addValidationIndicators(field) {
        const wrapper = field.closest('.form-group') || field.parentNode;
        wrapper.classList.add('form-field-wrapper');

        // Добавляем иконку валидации
        const icon = document.createElement('span');
        icon.className = 'field-validation-icon';
        wrapper.appendChild(icon);
    }

    // Настройка автозаполнения
    setupAutocomplete(field) {
        if (field.type === 'email') {
            field.setAttribute('autocomplete', 'email');
        } else if (field.type === 'password') {
            field.setAttribute('autocomplete', 'current-password');
        } else if (field.name === 'name' || field.name === 'full_name') {
            field.setAttribute('autocomplete', 'name');
        } else if (field.type === 'tel') {
            field.setAttribute('autocomplete', 'tel');
        }
    }

    // Установка ошибки поля
    setFieldError(field, message) {
        field.classList.add(this.options.errorClass);
        field.classList.remove(this.options.successClass);

        const wrapper = field.closest('.form-field-wrapper') || field.parentNode;
        const errorElement = wrapper.querySelector('.field-error');

        if (errorElement) {
            errorElement.textContent = message;
        } else {
            const error = document.createElement('div');
            error.className = 'field-error';
            error.textContent = message;
            wrapper.appendChild(error);
        }
    }

    // Установка успешной валидации поля
    setFieldSuccess(field) {
        field.classList.add(this.options.successClass);
        field.classList.remove(this.options.errorClass);
        this.clearFieldError(field);
    }

    // Очистка ошибки поля
    clearFieldError(field) {
        field.classList.remove(this.options.errorClass);

        const wrapper = field.closest('.form-field-wrapper') || field.parentNode;
        const errorElement = wrapper.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    // Установка ошибки формы
    setFormError(message) {
        const errorElement = this.form.querySelector('.form-error');
        if (errorElement) {
            errorElement.textContent = message;
        } else {
            const error = document.createElement('div');
            error.className = 'form-error';
            error.textContent = message;
            this.form.insertBefore(error, this.form.firstChild);
        }
    }

    // Очистка формы
    reset() {
        this.form.reset();
        this.form.querySelectorAll('.field-error, .form-error').forEach(el => el.remove());
        this.form.querySelectorAll('input, textarea, select').forEach(field => {
            field.classList.remove(this.options.errorClass, this.options.successClass);
        });
    }
}

// Экспорт для глобального доступа
window.AdvancedForm = AdvancedForm;
