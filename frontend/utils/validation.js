// Validation utilities
class ValidationUtils {
    static EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    static PASSWORD_MIN_LENGTH = 8;

    static validateEmail(email) {
        if (!email) return 'Email is required';
        if (!this.EMAIL_REGEX.test(email)) return 'Invalid email format';
        return null;
    }

    static validatePassword(password) {
        if (!password) return 'Password is required';
        if (password.length < this.PASSWORD_MIN_LENGTH) {
            return `Password must be at least ${this.PASSWORD_MIN_LENGTH} characters long`;
        }
        return null;
    }

    static validateRequired(value, fieldName) {
        if (!value || value.trim() === '') {
            return `${fieldName} is required`;
        }
        return null;
    }

    static validateMinLength(value, minLength, fieldName) {
        if (value && value.length < minLength) {
            return `${fieldName} must be at least ${minLength} characters long`;
        }
        return null;
    }

    static validateMaxLength(value, maxLength, fieldName) {
        if (value && value.length > maxLength) {
            return `${fieldName} must not exceed ${maxLength} characters`;
        }
        return null;
    }

    static validateNumber(value, fieldName) {
        if (value && isNaN(Number(value))) {
            return `${fieldName} must be a valid number`;
        }
        return null;
    }

    static validatePositiveNumber(value, fieldName) {
        const numberError = this.validateNumber(value, fieldName);
        if (numberError) return numberError;

        if (value && Number(value) <= 0) {
            return `${fieldName} must be a positive number`;
        }
        return null;
    }

    static validateUrl(value, fieldName) {
        if (value) {
            try {
                new URL(value);
            } catch {
                return `${fieldName} must be a valid URL`;
            }
        }
        return null;
    }

    static validateForm(formData, rules) {
        const errors = {};

        for (const [field, validators] of Object.entries(rules)) {
            const value = formData[field];

            for (const validator of validators) {
                const error = validator(value, field);
                if (error) {
                    errors[field] = error;
                    break; // Stop at first error for this field
                }
            }
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    static showFieldError(fieldElement, error) {
        // Remove existing error
        const existingError = fieldElement.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        if (error) {
            fieldElement.classList.add('error');
            const errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            errorElement.textContent = error;
            fieldElement.parentNode.appendChild(errorElement);
        } else {
            fieldElement.classList.remove('error');
        }
    }

    static clearFieldError(fieldElement) {
        fieldElement.classList.remove('error');
        const existingError = fieldElement.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
}

// CSS for error states
const errorStyles = `
.field-error {
    color: var(--error-color);
    font-size: 0.875rem;
    margin-top: 0.25rem;
}

.form-group input.error,
.form-group select.error,
.form-group textarea.error {
    border-color: var(--error-color);
    box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}
`;

// Inject error styles
const styleSheet = document.createElement('style');
styleSheet.textContent = errorStyles;
document.head.appendChild(styleSheet);
