// Form utilities
class FormUtils {
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    static validatePassword(password) {
        return password.length >= 8;
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

// Export for global access
window.FormUtils = FormUtils;
