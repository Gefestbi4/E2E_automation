/**
 * Централизованная система обработки ошибок
 * Обрабатывает API ошибки, валидацию и пользовательские уведомления
 */

class ErrorHandler {
    constructor() {
        this.errorTypes = {
            VALIDATION_ERROR: 'validation',
            NETWORK_ERROR: 'network',
            AUTH_ERROR: 'auth',
            SERVER_ERROR: 'server',
            CLIENT_ERROR: 'client',
            UNKNOWN_ERROR: 'unknown'
        };

        this.errorMessages = {
            [this.errorTypes.VALIDATION_ERROR]: 'Ошибка валидации данных',
            [this.errorTypes.NETWORK_ERROR]: 'Ошибка сети. Проверьте подключение к интернету',
            [this.errorTypes.AUTH_ERROR]: 'Ошибка авторизации. Войдите в систему заново',
            [this.errorTypes.SERVER_ERROR]: 'Ошибка сервера. Попробуйте позже',
            [this.errorTypes.CLIENT_ERROR]: 'Ошибка в запросе',
            [this.errorTypes.UNKNOWN_ERROR]: 'Произошла неизвестная ошибка'
        };

        this.setupGlobalErrorHandling();
    }

    /**
     * Настройка глобальной обработки ошибок
     */
    setupGlobalErrorHandling() {
        // Обработка необработанных ошибок JavaScript
        window.addEventListener('error', (event) => {
            console.error('Unhandled error:', event.error);
            this.handleError(event.error, {
                type: this.errorTypes.UNKNOWN_ERROR,
                context: 'global'
            });
        });

        // Обработка необработанных промисов
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.handleError(event.reason, {
                type: this.errorTypes.UNKNOWN_ERROR,
                context: 'promise'
            });
        });
    }

    /**
     * Обработка ошибки
     */
    handleError(error, options = {}) {
        const errorInfo = this.parseError(error, options);

        // Логируем ошибку
        this.logError(errorInfo);

        // Показываем пользователю
        this.showUserError(errorInfo);

        // Отправляем в аналитику (если есть)
        this.trackError(errorInfo);

        return errorInfo;
    }

    /**
     * Парсинг ошибки
     */
    parseError(error, options = {}) {
        let errorInfo = {
            message: 'Произошла неизвестная ошибка',
            type: this.errorTypes.UNKNOWN_ERROR,
            code: null,
            details: null,
            context: options.context || 'unknown',
            timestamp: new Date().toISOString(),
            stack: null
        };

        // Обработка различных типов ошибок
        if (error instanceof Error) {
            errorInfo.message = error.message;
            errorInfo.stack = error.stack;
        } else if (typeof error === 'string') {
            errorInfo.message = error;
        } else if (error && typeof error === 'object') {
            errorInfo.message = error.message || error.detail || 'Ошибка';
            errorInfo.code = error.code || error.status;
            errorInfo.details = error.details || error.errors;
        }

        // Определяем тип ошибки
        if (options.type) {
            errorInfo.type = options.type;
        } else if (errorInfo.code) {
            errorInfo.type = this.determineErrorType(errorInfo.code);
        } else if (errorInfo.message) {
            errorInfo.type = this.determineErrorTypeByMessage(errorInfo.message);
        }

        return errorInfo;
    }

    /**
     * Определение типа ошибки по коду
     */
    determineErrorType(code) {
        if (code >= 400 && code < 500) {
            if (code === 401 || code === 403) {
                return this.errorTypes.AUTH_ERROR;
            }
            return this.errorTypes.CLIENT_ERROR;
        } else if (code >= 500) {
            return this.errorTypes.SERVER_ERROR;
        } else if (code === 'NETWORK_ERROR' || code === 'FETCH_ERROR') {
            return this.errorTypes.NETWORK_ERROR;
        }
        return this.errorTypes.UNKNOWN_ERROR;
    }

    /**
     * Определение типа ошибки по сообщению
     */
    determineErrorTypeByMessage(message) {
        const lowerMessage = message.toLowerCase();

        if (lowerMessage.includes('validation') || lowerMessage.includes('валидация')) {
            return this.errorTypes.VALIDATION_ERROR;
        }
        if (lowerMessage.includes('network') || lowerMessage.includes('fetch') || lowerMessage.includes('сеть')) {
            return this.errorTypes.NETWORK_ERROR;
        }
        if (lowerMessage.includes('auth') || lowerMessage.includes('unauthorized') || lowerMessage.includes('авторизация')) {
            return this.errorTypes.AUTH_ERROR;
        }
        if (lowerMessage.includes('server') || lowerMessage.includes('сервер')) {
            return this.errorTypes.SERVER_ERROR;
        }

        return this.errorTypes.UNKNOWN_ERROR;
    }

    /**
     * Логирование ошибки
     */
    logError(errorInfo) {
        const logData = {
            level: 'error',
            message: errorInfo.message,
            type: errorInfo.type,
            code: errorInfo.code,
            context: errorInfo.context,
            timestamp: errorInfo.timestamp,
            stack: errorInfo.stack,
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        console.error('Error logged:', logData);

        // Здесь можно добавить отправку в систему логирования
        // this.sendToLoggingService(logData);
    }

    /**
     * Показ ошибки пользователю
     */
    showUserError(errorInfo) {
        const message = this.getUserFriendlyMessage(errorInfo);

        // Показываем Toast уведомление
        if (window.Toast && typeof window.Toast.error === 'function') {
            window.Toast.error(message);
        } else {
            // Fallback на alert
            alert(message);
        }

        // Для критических ошибок показываем модальное окно
        if (this.isCriticalError(errorInfo)) {
            this.showCriticalErrorModal(errorInfo);
        }
    }

    /**
     * Получение пользовательского сообщения
     */
    getUserFriendlyMessage(errorInfo) {
        // Если есть детали валидации, показываем их
        if (errorInfo.type === this.errorTypes.VALIDATION_ERROR && errorInfo.details) {
            if (Array.isArray(errorInfo.details)) {
                return errorInfo.details.map(detail => detail.msg || detail.message).join(', ');
            } else if (typeof errorInfo.details === 'object') {
                return Object.values(errorInfo.details).flat().join(', ');
            }
        }

        // Используем предопределенные сообщения
        const baseMessage = this.errorMessages[errorInfo.type] || errorInfo.message;

        // Добавляем код ошибки если есть
        if (errorInfo.code) {
            return `${baseMessage} (Код: ${errorInfo.code})`;
        }

        return baseMessage;
    }

    /**
     * Проверка критичности ошибки
     */
    isCriticalError(errorInfo) {
        return errorInfo.type === this.errorTypes.AUTH_ERROR ||
            errorInfo.type === this.errorTypes.SERVER_ERROR ||
            errorInfo.code >= 500;
    }

    /**
     * Показ модального окна критической ошибки
     */
    showCriticalErrorModal(errorInfo) {
        if (window.Modal) {
            const modal = new Modal('critical-error-modal', {
                closable: false,
                backdrop: true
            });

            const content = {
                title: 'Критическая ошибка',
                body: `
                    <div class="error-details">
                        <p><strong>Тип ошибки:</strong> ${errorInfo.type}</p>
                        <p><strong>Сообщение:</strong> ${errorInfo.message}</p>
                        ${errorInfo.code ? `<p><strong>Код:</strong> ${errorInfo.code}</p>` : ''}
                        <p><strong>Время:</strong> ${new Date(errorInfo.timestamp).toLocaleString()}</p>
                    </div>
                `,
                footer: `
                    <button type="button" class="btn btn-primary" onclick="location.reload()">
                        Перезагрузить страницу
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="Modal.close('critical-error-modal')">
                        Закрыть
                    </button>
                `
            };

            modal.show(content);
        }
    }

    /**
     * Отслеживание ошибки в аналитике
     */
    trackError(errorInfo) {
        if (window.AnalyticsService) {
            window.AnalyticsService.trackEvent('error', {
                error_type: errorInfo.type,
                error_code: errorInfo.code,
                error_message: errorInfo.message,
                context: errorInfo.context
            }).catch(err => {
                console.error('Failed to track error:', err);
            });
        }
    }

    /**
     * Обработка API ошибок
     */
    handleApiError(response, context = 'api') {
        const errorInfo = {
            message: 'Ошибка API',
            type: this.errorTypes.SERVER_ERROR,
            code: response.status,
            context: context,
            timestamp: new Date().toISOString()
        };

        // Пытаемся получить детали ошибки из ответа
        return response.json().then(data => {
            errorInfo.message = data.detail || data.message || errorInfo.message;
            errorInfo.details = data.details || data.errors;
            return this.handleError(errorInfo);
        }).catch(() => {
            // Если не удалось распарсить JSON, используем базовую информацию
            errorInfo.message = `HTTP ${response.status}: ${response.statusText}`;
            return this.handleError(errorInfo);
        });
    }

    /**
     * Обработка ошибок валидации
     */
    handleValidationError(errors, context = 'validation') {
        const errorInfo = {
            message: 'Ошибка валидации',
            type: this.errorTypes.VALIDATION_ERROR,
            details: errors,
            context: context,
            timestamp: new Date().toISOString()
        };

        return this.handleError(errorInfo);
    }

    /**
     * Обработка сетевых ошибок
     */
    handleNetworkError(error, context = 'network') {
        const errorInfo = {
            message: 'Ошибка сети',
            type: this.errorTypes.NETWORK_ERROR,
            context: context,
            timestamp: new Date().toISOString()
        };

        if (error.message) {
            errorInfo.message = error.message;
        }

        return this.handleError(errorInfo);
    }

    /**
     * Обработка ошибок авторизации
     */
    handleAuthError(error, context = 'auth') {
        const errorInfo = {
            message: 'Ошибка авторизации',
            type: this.errorTypes.AUTH_ERROR,
            context: context,
            timestamp: new Date().toISOString()
        };

        if (error.message) {
            errorInfo.message = error.message;
        }

        // При ошибке авторизации перенаправляем на логин
        setTimeout(() => {
            if (window.AuthService) {
                window.AuthService.logout();
            } else {
                window.location.href = '/login.html';
            }
        }, 2000);

        return this.handleError(errorInfo);
    }
}

// Создаем глобальный экземпляр
window.ErrorHandler = new ErrorHandler();

// Экспорт для глобального доступа
window.ErrorHandlerClass = ErrorHandler;
