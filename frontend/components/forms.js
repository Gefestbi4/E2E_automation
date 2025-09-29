// Form utilities
class FormUtils {
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    static validatePassword(password) {
        if (!password) return false;
        if (password.length < 8) return false;
        if (!/(?=.*[a-z])/.test(password)) return false;
        if (!/(?=.*[A-Z])/.test(password)) return false;
        if (!/(?=.*\d)/.test(password)) return false;
        if (!/(?=.*[@$!%*?&])/.test(password)) return false;
        return true;
    }

    static validateRequired(value) {
        return value && value.trim().length > 0;
    }

    static getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    }

    static clearForm(form) {
        form.reset();
        // Clear validation states
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        form.querySelectorAll('.invalid-feedback').forEach(feedback => {
            feedback.remove();
        });
    }

    static showFieldError(field, message) {
        field.classList.add('is-invalid');

        let feedback = field.parentElement.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentElement.appendChild(feedback);
        }
        feedback.textContent = message;
    }

    static clearFieldError(field) {
        field.classList.remove('is-invalid');
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    static validateForm(form, rules) {
        let isValid = true;

        for (const [fieldName, fieldRules] of Object.entries(rules)) {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (!field) continue;

            let fieldValid = true;

            for (const rule of fieldRules) {
                if (!rule.validator(field.value)) {
                    this.showFieldError(field, rule.message);
                    fieldValid = false;
                    isValid = false;
                    break;
                }
            }

            if (fieldValid) {
                this.clearFieldError(field);
            }
        }

        return isValid;
    }
}

// Form templates
FormUtils.createLoginForm = function () {
    return `
        <form id="loginForm" class="auth-form">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
                <div class="error-message" id="emailError"></div>
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" name="password" required>
                <div class="error-message" id="passwordError"></div>
            </div>
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="rememberMe" name="rememberMe">
                    Запомнить меня
                </label>
            </div>
            <button type="submit" class="btn btn-primary">Войти</button>
            <div class="form-links">
                <a href="#" id="forgotPasswordLink">Забыли пароль?</a>
                <a href="#" id="registerLink">Нет аккаунта? Зарегистрироваться</a>
            </div>
        </form>
    `;
};

FormUtils.createRegisterForm = function () {
    return `
        <form id="registerForm" class="auth-form">
            <div class="form-group">
                <label for="firstName">Имя</label>
                <input type="text" id="firstName" name="firstName" required>
                <div class="error-message" id="firstNameError"></div>
            </div>
            <div class="form-group">
                <label for="lastName">Фамилия</label>
                <input type="text" id="lastName" name="lastName" required>
                <div class="error-message" id="lastNameError"></div>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
                <div class="error-message" id="emailError"></div>
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" id="password" name="password" required>
                <div class="error-message" id="passwordError"></div>
            </div>
            <div class="form-group">
                <label for="confirmPassword">Подтвердите пароль</label>
                <input type="password" id="confirmPassword" name="confirmPassword" required>
                <div class="error-message" id="confirmPasswordError"></div>
            </div>
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="agreeTerms" name="agreeTerms" required>
                    Я согласен с <a href="#" id="termsLink">условиями использования</a>
                </label>
                <div class="error-message" id="agreeTermsError"></div>
            </div>
            <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
            <div class="form-links">
                <a href="#" id="loginLink">Уже есть аккаунт? Войти</a>
            </div>
        </form>
    `;
};

FormUtils.createForgotPasswordForm = function () {
    return `
        <form id="forgotPasswordForm" class="auth-form">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
                <div class="error-message" id="emailError"></div>
            </div>
            <button type="submit" class="btn btn-primary">Отправить ссылку для сброса</button>
            <div class="form-links">
                <a href="#" id="loginLink">Вернуться к входу</a>
            </div>
        </form>
    `;
};

FormUtils.createResetPasswordForm = function () {
    return `
        <form id="resetPasswordForm" class="auth-form">
            <div class="form-group">
                <label for="password">Новый пароль</label>
                <input type="password" id="password" name="password" required>
                <div class="error-message" id="passwordError"></div>
            </div>
            <div class="form-group">
                <label for="confirmPassword">Подтвердите новый пароль</label>
                <input type="password" id="confirmPassword" name="confirmPassword" required>
                <div class="error-message" id="confirmPasswordError"></div>
            </div>
            <button type="submit" class="btn btn-primary">Сбросить пароль</button>
            <div class="form-links">
                <a href="#" id="loginLink">Вернуться к входу</a>
            </div>
        </form>
    `;
};

// Export for global access
window.FormUtils = FormUtils;
