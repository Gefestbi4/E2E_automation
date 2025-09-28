/**
 * Централизованная обработка ошибок
 */
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);

        // Определяем тип ошибки
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            return this.handleNetworkError();
        }

        if (error.message.includes('401')) {
            return this.handleAuthError();
        }

        if (error.message.includes('403')) {
            return this.handlePermissionError();
        }

        if (error.message.includes('404')) {
            return this.handleNotFoundError();
        }

        if (error.message.includes('422')) {
            return this.handleValidationError(error);
        }

        if (error.message.includes('429')) {
            return this.handleRateLimitError();
        }

        if (error.message.includes('500')) {
            return this.handleServerError();
        }

        // Общая ошибка
        return this.handleGenericError(error);
    }

    static handleNetworkError() {
        return {
            type: 'network',
            title: 'Ошибка сети',
            message: 'Проверьте подключение к интернету и попробуйте снова',
            action: 'retry'
        };
    }

    static handleAuthError() {
        return {
            type: 'auth',
            title: 'Ошибка авторизации',
            message: 'Необходимо войти в систему',
            action: 'redirect',
            redirectTo: '/login.html'
        };
    }

    static handlePermissionError() {
        return {
            type: 'permission',
            title: 'Доступ запрещен',
            message: 'У вас нет прав для выполнения этого действия',
            action: 'none'
        };
    }

    static handleNotFoundError() {
        return {
            type: 'not_found',
            title: 'Ресурс не найден',
            message: 'Запрашиваемый ресурс не существует',
            action: 'none'
        };
    }

    static handleValidationError(error) {
        return {
            type: 'validation',
            title: 'Ошибка валидации',
            message: error.message || 'Проверьте правильность введенных данных',
            action: 'none'
        };
    }

    static handleRateLimitError() {
        return {
            type: 'rate_limit',
            title: 'Слишком много запросов',
            message: 'Пожалуйста, подождите немного перед следующим запросом',
            action: 'wait'
        };
    }

    static handleServerError() {
        return {
            type: 'server',
            title: 'Ошибка сервера',
            message: 'Временные технические проблемы. Попробуйте позже',
            action: 'retry'
        };
    }

    static handleGenericError(error) {
        return {
            type: 'generic',
            title: 'Произошла ошибка',
            message: error.message || 'Неизвестная ошибка',
            action: 'none'
        };
    }

    static showError(errorInfo) {
        // Показываем уведомление
        if (window.Toast) {
            window.Toast.show(errorInfo.message, 'error');
        } else {
            alert(`${errorInfo.title}: ${errorInfo.message}`);
        }

        // Выполняем действие
        switch (errorInfo.action) {
            case 'redirect':
                if (errorInfo.redirectTo) {
                    window.location.href = errorInfo.redirectTo;
                }
                break;
            case 'retry':
                // Можно добавить кнопку повтора
                break;
            case 'wait':
                // Можно добавить таймер
                break;
        }
    }
}

// Экспорт для глобального доступа
window.ErrorHandler = ErrorHandler;