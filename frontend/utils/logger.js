/**
 * Централизованная система логгирования для фронтенда
 * Предназначена для мониторинга и перехвата событий в автотестах
 */

class Logger {
    constructor() {
        this.logs = [];
        this.maxLogs = 1000; // Максимальное количество логов в памяти
        this.logLevel = 'debug'; // debug, info, warn, error
        this.enableConsole = true;
        this.enableStorage = true;
        this.enableNetwork = true;

        // Уровни логирования
        this.levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };

        this.init();
    }

    init() {
        // Перехватываем console методы
        this.interceptConsole();

        // Перехватываем fetch запросы
        this.interceptFetch();

        // Перехватываем ошибки
        this.interceptErrors();

        // Перехватываем пользовательские действия
        this.interceptUserActions();

        // Перехватываем изменения DOM
        this.interceptDOMChanges();

        // Перехватываем навигацию
        this.interceptNavigation();

        console.log('🔍 Logger initialized');
    }

    log(level, category, message, data = null) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            category: category,
            message: message,
            data: data,
            url: window.location.href,
            userAgent: navigator.userAgent,
            sessionId: this.getSessionId()
        };

        // Добавляем в массив логов
        this.logs.push(logEntry);

        // Ограничиваем размер массива
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        // Выводим в консоль если включено
        if (this.enableConsole && this.levels[level] >= this.levels[this.logLevel]) {
            const consoleMethod = level === 'debug' ? 'log' : level;
            console[consoleMethod](`[${category}] ${message}`, data || '');
        }

        // Сохраняем в localStorage если включено
        if (this.enableStorage) {
            this.saveToStorage(logEntry);
        }

        // Отправляем на сервер если включено
        if (this.enableNetwork) {
            this.sendToServer(logEntry);
        }

        // Вызываем кастомные обработчики
        this.triggerCustomHandlers(logEntry);
    }

    debug(category, message, data = null) {
        this.log('debug', category, message, data);
    }

    info(category, message, data = null) {
        this.log('info', category, message, data);
    }

    warn(category, message, data = null) {
        this.log('warn', category, message, data);
    }

    error(category, message, data = null) {
        this.log('error', category, message, data);
    }

    // Перехват console методов
    interceptConsole() {
        const originalConsole = {
            log: console.log,
            info: console.info,
            warn: console.warn,
            error: console.error
        };

        console.log = (...args) => {
            this.debug('CONSOLE', args.join(' '), args);
            originalConsole.log.apply(console, args);
        };

        console.info = (...args) => {
            this.info('CONSOLE', args.join(' '), args);
            originalConsole.info.apply(console, args);
        };

        console.warn = (...args) => {
            this.warn('CONSOLE', args.join(' '), args);
            originalConsole.warn.apply(console, args);
        };

        console.error = (...args) => {
            this.error('CONSOLE', args.join(' '), args);
            originalConsole.error.apply(console, args);
        };
    }

    // Перехват fetch запросов
    interceptFetch() {
        const originalFetch = window.fetch;

        window.fetch = async (...args) => {
            const [url, options = {}] = args;

            this.debug('FETCH_REQUEST', `Request to ${url}`, {
                url: url,
                method: options.method || 'GET',
                headers: options.headers,
                body: options.body
            });

            const startTime = Date.now();

            try {
                const response = await originalFetch(...args);
                const endTime = Date.now();
                const duration = endTime - startTime;

                this.info('FETCH_RESPONSE', `Response from ${url}`, {
                    url: url,
                    status: response.status,
                    statusText: response.statusText,
                    duration: duration,
                    headers: Object.fromEntries(response.headers.entries())
                });

                return response;
            } catch (error) {
                const endTime = Date.now();
                const duration = endTime - startTime;

                this.error('FETCH_ERROR', `Error fetching ${url}`, {
                    url: url,
                    error: error.message,
                    duration: duration
                });

                throw error;
            }
        };
    }

    // Перехват ошибок
    interceptErrors() {
        // JavaScript ошибки
        window.addEventListener('error', (event) => {
            this.error('JAVASCRIPT_ERROR', 'Uncaught JavaScript error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
        });

        // Promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.error('PROMISE_REJECTION', 'Unhandled promise rejection', {
                reason: event.reason,
                promise: event.promise
            });
        });

        // Resource loading errors
        window.addEventListener('error', (event) => {
            if (event.target !== window) {
                this.error('RESOURCE_ERROR', 'Resource loading error', {
                    tagName: event.target.tagName,
                    src: event.target.src,
                    href: event.target.href
                });
            }
        }, true);
    }

    // Перехват пользовательских действий
    interceptUserActions() {
        const events = ['click', 'input', 'change', 'submit', 'focus', 'blur'];

        events.forEach(eventType => {
            document.addEventListener(eventType, (event) => {
                const target = event.target;

                // Игнорируем системные события
                if (target.tagName === 'SCRIPT' || target.tagName === 'STYLE') {
                    return;
                }

                this.debug('USER_ACTION', `${eventType} on ${target.tagName}`, {
                    eventType: eventType,
                    tagName: target.tagName,
                    id: target.id,
                    className: target.className,
                    value: target.value,
                    testId: target.getAttribute('test-id'),
                    xpath: this.getXPath(target)
                });
            }, true);
        });
    }

    // Перехват изменений DOM
    interceptDOMChanges() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    this.debug('DOM_CHANGE', 'DOM nodes added/removed', {
                        addedNodes: mutation.addedNodes.length,
                        removedNodes: mutation.removedNodes.length,
                        target: mutation.target.tagName
                    });
                } else if (mutation.type === 'attributes') {
                    this.debug('DOM_ATTR_CHANGE', 'DOM attribute changed', {
                        attributeName: mutation.attributeName,
                        target: mutation.target.tagName,
                        oldValue: mutation.oldValue,
                        newValue: mutation.target.getAttribute(mutation.attributeName)
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeOldValue: true
        });
    }

    // Перехват навигации
    interceptNavigation() {
        // History API
        const originalPushState = history.pushState;
        const originalReplaceState = history.replaceState;

        history.pushState = function (...args) {
            window.Logger?.debug('NAVIGATION', 'History pushState', {
                url: args[2],
                state: args[0]
            });
            return originalPushState.apply(history, args);
        };

        history.replaceState = function (...args) {
            window.Logger?.debug('NAVIGATION', 'History replaceState', {
                url: args[2],
                state: args[0]
            });
            return originalReplaceState.apply(history, args);
        };

        // Popstate event
        window.addEventListener('popstate', (event) => {
            this.debug('NAVIGATION', 'History popstate', {
                url: window.location.href,
                state: event.state
            });
        });

        // Hash change
        window.addEventListener('hashchange', (event) => {
            this.debug('NAVIGATION', 'Hash change', {
                oldURL: event.oldURL,
                newURL: event.newURL
            });
        });
    }

    // Получение XPath элемента
    getXPath(element) {
        if (element.id) {
            return `//*[@id="${element.id}"]`;
        }

        if (element === document.body) {
            return '/html/body';
        }

        let path = '';
        while (element && element.nodeType === Node.ELEMENT_NODE) {
            let selector = element.nodeName.toLowerCase();
            if (element.previousElementSibling) {
                let index = 1;
                let sibling = element.previousElementSibling;
                while (sibling) {
                    if (sibling.nodeName === element.nodeName) {
                        index++;
                    }
                    sibling = sibling.previousElementSibling;
                }
                selector += `[${index}]`;
            }
            path = '/' + selector + path;
            element = element.parentElement;
        }

        return path;
    }

    // Получение ID сессии
    getSessionId() {
        let sessionId = sessionStorage.getItem('logger_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('logger_session_id', sessionId);
        }
        return sessionId;
    }

    // Сохранение в localStorage
    saveToStorage(logEntry) {
        try {
            const logs = JSON.parse(localStorage.getItem('logger_logs') || '[]');
            logs.push(logEntry);

            // Ограничиваем размер в localStorage
            if (logs.length > 100) {
                logs.splice(0, logs.length - 100);
            }

            localStorage.setItem('logger_logs', JSON.stringify(logs));
        } catch (error) {
            console.error('Failed to save log to storage:', error);
        }
    }

    // Отправка на сервер
    async sendToServer(logEntry) {
        try {
            // Отправляем только важные логи
            if (['error', 'warn'].includes(logEntry.level)) {
                await fetch('/api/logs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(logEntry)
                });
            }
        } catch (error) {
            // Игнорируем ошибки отправки логов
        }
    }

    // Кастомные обработчики
    triggerCustomHandlers(logEntry) {
        // Вызываем глобальные обработчики
        if (window.onLoggerEvent) {
            window.onLoggerEvent(logEntry);
        }

        // Вызываем обработчики для автотестов
        if (window.onTestLoggerEvent) {
            window.onTestLoggerEvent(logEntry);
        }
    }

    // API для автотестов
    getLogs(filter = {}) {
        let filteredLogs = this.logs;

        if (filter.level) {
            filteredLogs = filteredLogs.filter(log => log.level === filter.level);
        }

        if (filter.category) {
            filteredLogs = filteredLogs.filter(log => log.category === filter.category);
        }

        if (filter.since) {
            filteredLogs = filteredLogs.filter(log => new Date(log.timestamp) >= new Date(filter.since));
        }

        return filteredLogs;
    }

    clearLogs() {
        this.logs = [];
        localStorage.removeItem('logger_logs');
    }

    exportLogs() {
        return {
            logs: this.logs,
            sessionId: this.getSessionId(),
            exportedAt: new Date().toISOString()
        };
    }

    // Настройки
    setLogLevel(level) {
        this.logLevel = level;
    }

    setEnabled(console = true, storage = true, network = true) {
        this.enableConsole = console;
        this.enableStorage = storage;
        this.enableNetwork = network;
    }
}

// Создаем глобальный экземпляр
window.Logger = new Logger();

// Экспорт для модулей
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Logger;
}
