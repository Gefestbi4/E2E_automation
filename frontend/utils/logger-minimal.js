/**
 * Минимальная система логгирования для страницы авторизации
 * Оптимизирована для предотвращения out of memory
 */

class MinimalLogger {
    constructor() {
        this.logs = [];
        this.maxLogs = 50; // Очень маленький лимит
        this.logLevel = 'error'; // Только ошибки
        this.enableConsole = false;
        this.enableStorage = false;
        this.enableNetwork = false;

        this.levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };

        this.init();
    }

    init() {
        // Только перехватываем критические ошибки
        this.interceptErrors();
        console.log('🔍 Minimal Logger initialized');
    }

    log(level, category, message, data = null) {
        // Логируем только ошибки
        if (this.levels[level] < this.levels[this.logLevel]) {
            return;
        }

        const logEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            category: category,
            message: message,
            data: data,
            url: window.location.href
        };

        this.logs.push(logEntry);

        // Ограничиваем размер массива
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        // Выводим только критические ошибки в консоль
        if (this.enableConsole && level === 'error') {
            console.error(`[${category}] ${message}`, data || '');
        }
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

    // Перехват только критических ошибок
    interceptErrors() {
        // JavaScript ошибки
        window.addEventListener('error', (event) => {
            this.error('JAVASCRIPT_ERROR', 'Uncaught JavaScript error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno
            });
        });

        // Promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.error('PROMISE_REJECTION', 'Unhandled promise rejection', {
                reason: event.reason
            });
        });
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

        return filteredLogs;
    }

    clearLogs() {
        this.logs = [];
    }

    exportLogs() {
        return {
            logs: this.logs,
            exportedAt: new Date().toISOString()
        };
    }
}

// Создаем глобальный экземпляр
window.Logger = new MinimalLogger();

// Экспорт для модулей
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MinimalLogger;
}

