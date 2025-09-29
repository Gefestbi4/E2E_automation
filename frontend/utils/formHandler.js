// Import validation functions from global scope

class FormHandler {
    constructor(formId, validationRules, submitCallback) {
        this.form = document.getElementById(formId);
        this.validationRules = validationRules;
        this.submitCallback = submitCallback;
        this.init();
    }

    init() {
        if (!this.form) return;

        // Real-time валидация
        this.form.addEventListener('input', (e) => {
            this.validateField(e.target);
        });

        // Обработка отправки формы
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
    }

    validateField(field) {
        const fieldName = field.name;
        const fieldValue = field.value;
        const errorElement = document.getElementById(`${fieldName}Error`);

        if (this.validationRules[fieldName]) {
            const error = this.validationRules[fieldName](fieldValue);

            if (errorElement) {
                errorElement.textContent = error || '';
                errorElement.style.display = error ? 'block' : 'none';
            }

            // Обновляем стиль поля
            field.classList.toggle('error', !!error);
            field.classList.toggle('valid', !error && fieldValue);
        }
    }

    async handleSubmit() {
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries());

        // Валидация всей формы
        const validation = window.validateForm(data, this.validationRules);

        if (!validation.isValid) {
            // Показываем все ошибки
            for (const [field, error] of Object.entries(validation.errors)) {
                const errorElement = document.getElementById(`${field}Error`);
                if (errorElement) {
                    errorElement.textContent = error;
                    errorElement.style.display = 'block';
                }
            }
            return;
        }

        // Показываем loading state
        const submitButton = this.form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Загрузка...';
        submitButton.disabled = true;

        try {
            await this.submitCallback(data);
        } catch (error) {
            console.error('Form submission error:', error);
            // Показываем общую ошибку
            this.showFormError(error.message || 'Произошла ошибка при отправке формы');
        } finally {
            // Восстанавливаем кнопку
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    }

    showFormError(message) {
        // Показываем общую ошибку формы
        let errorElement = document.getElementById('formError');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'formError';
            errorElement.className = 'error-message form-error';
            this.form.insertBefore(errorElement, this.form.firstChild);
        }
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

// Export for global access
window.FormHandler = FormHandler;
