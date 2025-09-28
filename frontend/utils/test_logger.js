/**
 * API для автотестов для работы с логами
 * Предоставляет методы для мониторинга и перехвата событий в браузере
 */

class TestLogger {
    constructor() {
        this.isTestMode = false;
        this.testLogs = [];
        this.eventListeners = [];

        // Проверяем, запущены ли автотесты
        this.detectTestMode();

        if (this.isTestMode) {
            this.setupTestMode();
        }
    }

    detectTestMode() {
        // Проверяем различные признаки автотестов
        const testIndicators = [
            // Selenium/WebDriver
            window.navigator.webdriver,
            window.document.documentElement.getAttribute('webdriver'),

            // Playwright
            window.navigator.userAgent.includes('Playwright'),

            // Puppeteer
            window.navigator.userAgent.includes('HeadlessChrome'),

            // Cypress
            window.Cypress,

            // Test environment variables
            window.location.search.includes('test=true'),
            window.location.search.includes('autotest=true'),

            // Custom test markers
            window.isTestEnvironment,
            window.__TEST_MODE__
        ];

        this.isTestMode = testIndicators.some(indicator => !!indicator);

        if (this.isTestMode) {
            console.log('🧪 Test mode detected - enabling enhanced logging');
        }
    }

    setupTestMode() {
        // Увеличиваем уровень логирования для тестов
        if (window.Logger) {
            window.Logger.setLogLevel('debug');
            window.Logger.setEnabled(true, true, true);
        }

        // Добавляем специальные обработчики для тестов
        this.addTestEventListeners();

        // Экспортируем API для тестов
        window.TestLogger = this;
        window.getTestLogs = () => this.getTestLogs();
        window.clearTestLogs = () => this.clearTestLogs();
        window.exportTestLogs = () => this.exportTestLogs();
        window.waitForLog = (filter, timeout = 5000) => this.waitForLog(filter, timeout);
    }

    addTestEventListeners() {
        // Слушаем все логи от основного логгера
        if (window.Logger) {
            const originalTriggerCustomHandlers = window.Logger.triggerCustomHandlers.bind(window.Logger);
            window.Logger.triggerCustomHandlers = (logEntry) => {
                // Вызываем оригинальный метод
                originalTriggerCustomHandlers(logEntry);

                // Добавляем в тестовые логи
                this.addTestLog(logEntry);
            };
        }

        // Слушаем специальные тестовые события
        window.addEventListener('test:start', (event) => {
            this.addTestLog({
                timestamp: new Date().toISOString(),
                level: 'info',
                category: 'TEST_START',
                message: 'Test started',
                data: event.detail
            });
        });

        window.addEventListener('test:end', (event) => {
            this.addTestLog({
                timestamp: new Date().toISOString(),
                level: 'info',
                category: 'TEST_END',
                message: 'Test ended',
                data: event.detail
            });
        });

        window.addEventListener('test:step', (event) => {
            this.addTestLog({
                timestamp: new Date().toISOString(),
                level: 'info',
                category: 'TEST_STEP',
                message: event.detail.message || 'Test step',
                data: event.detail
            });
        });
    }

    addTestLog(logEntry) {
        this.testLogs.push({
            ...logEntry,
            testMode: true,
            testTimestamp: Date.now()
        });

        // Ограничиваем размер массива
        if (this.testLogs.length > 2000) {
            this.testLogs.splice(0, this.testLogs.length - 2000);
        }
    }

    // API для автотестов
    getTestLogs(filter = {}) {
        let filteredLogs = this.testLogs;

        if (filter.level) {
            filteredLogs = filteredLogs.filter(log => log.level === filter.level);
        }

        if (filter.category) {
            filteredLogs = filteredLogs.filter(log => log.category === filter.category);
        }

        if (filter.since) {
            const sinceTime = new Date(filter.since).getTime();
            filteredLogs = filteredLogs.filter(log => new Date(log.timestamp).getTime() >= sinceTime);
        }

        if (filter.message) {
            filteredLogs = filteredLogs.filter(log =>
                log.message.toLowerCase().includes(filter.message.toLowerCase())
            );
        }

        if (filter.testId) {
            filteredLogs = filteredLogs.filter(log =>
                log.data && log.data.testId === filter.testId
            );
        }

        return filteredLogs;
    }

    clearTestLogs() {
        this.testLogs = [];
        if (window.Logger) {
            window.Logger.clearLogs();
        }
    }

    exportTestLogs() {
        return {
            testLogs: this.testLogs,
            allLogs: window.Logger ? window.Logger.getLogs() : [],
            sessionId: window.Logger ? window.Logger.getSessionId() : 'unknown',
            exportedAt: new Date().toISOString(),
            testMode: this.isTestMode
        };
    }

    // Ожидание конкретного лога
    async waitForLog(filter, timeout = 5000) {
        return new Promise((resolve, reject) => {
            const startTime = Date.now();

            const checkLogs = () => {
                const logs = this.getTestLogs(filter);
                if (logs.length > 0) {
                    resolve(logs[logs.length - 1]);
                    return;
                }

                if (Date.now() - startTime > timeout) {
                    reject(new Error(`Timeout waiting for log: ${JSON.stringify(filter)}`));
                    return;
                }

                setTimeout(checkLogs, 100);
            };

            checkLogs();
        });
    }

    // Ожидание завершения всех асинхронных операций
    async waitForAsyncOperations(timeout = 5000) {
        return new Promise((resolve) => {
            const startTime = Date.now();

            const checkAsync = () => {
                // Проверяем, есть ли активные fetch запросы
                const activeRequests = this.getTestLogs({ category: 'FETCH_REQUEST' });
                const recentRequests = activeRequests.filter(log =>
                    Date.now() - new Date(log.timestamp).getTime() < 1000
                );

                if (recentRequests.length === 0 || Date.now() - startTime > timeout) {
                    resolve();
                    return;
                }

                setTimeout(checkAsync, 100);
            };

            checkAsync();
        });
    }

    // Получение статистики логов
    getLogStats() {
        const stats = {
            total: this.testLogs.length,
            byLevel: {},
            byCategory: {},
            byHour: {},
            errors: 0,
            warnings: 0,
            apiCalls: 0,
            userActions: 0
        };

        this.testLogs.forEach(log => {
            // По уровням
            stats.byLevel[log.level] = (stats.byLevel[log.level] || 0) + 1;

            // По категориям
            stats.byCategory[log.category] = (stats.byCategory[log.category] || 0) + 1;

            // По часам
            const hour = new Date(log.timestamp).getHours();
            stats.byHour[hour] = (stats.byHour[hour] || 0) + 1;

            // Специальные счетчики
            if (log.level === 'error') stats.errors++;
            if (log.level === 'warn') stats.warnings++;
            if (log.category === 'FETCH_REQUEST') stats.apiCalls++;
            if (log.category === 'USER_ACTION') stats.userActions++;
        });

        return stats;
    }

    // Поиск логов по паттерну
    searchLogs(pattern) {
        const regex = new RegExp(pattern, 'i');
        return this.testLogs.filter(log =>
            regex.test(log.message) ||
            (log.data && JSON.stringify(log.data).match(regex))
        );
    }

    // Получение логов для конкретного элемента
    getElementLogs(selector) {
        return this.testLogs.filter(log =>
            log.data &&
            (log.data.xpath === selector ||
                log.data.testId === selector ||
                log.data.id === selector)
        );
    }

    // Получение логов API запросов
    getApiLogs() {
        return this.testLogs.filter(log =>
            ['FETCH_REQUEST', 'FETCH_RESPONSE', 'FETCH_ERROR', 'API_REQUEST', 'API_SUCCESS', 'API_ERROR'].includes(log.category)
        );
    }

    // Получение логов пользовательских действий
    getUserActionLogs() {
        return this.testLogs.filter(log =>
            log.category === 'USER_ACTION'
        );
    }

    // Получение логов ошибок
    getErrorLogs() {
        return this.testLogs.filter(log =>
            log.level === 'error'
        );
    }

    // Создание тестового события
    emitTestEvent(eventType, data = {}) {
        const event = new CustomEvent(`test:${eventType}`, {
            detail: {
                timestamp: new Date().toISOString(),
                ...data
            }
        });

        window.dispatchEvent(event);
    }

    // Маркировка тестового шага
    markTestStep(stepName, data = {}) {
        this.emitTestEvent('step', {
            step: stepName,
            ...data
        });
    }

    // Начало теста
    startTest(testName, data = {}) {
        this.emitTestEvent('start', {
            testName: testName,
            ...data
        });
    }

    // Завершение теста
    endTest(testName, result = 'passed', data = {}) {
        this.emitTestEvent('end', {
            testName: testName,
            result: result,
            ...data
        });
    }
}

// Создаем экземпляр
new TestLogger();
