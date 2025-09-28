/**
 * Менеджер безопасности фронтенда
 */

class SecurityManager {
    constructor() {
        this.isInitialized = false;
        this.securityConfig = {
            enableCSP: true,
            enableXSSProtection: true,
            enableCSRFProtection: true,
            enableInputSanitization: true,
            enableRateLimiting: true,
            enableSecureHeaders: true,
            maxRequestRetries: 3,
            requestTimeout: 30000,
            sessionTimeout: 3600000 // 1 час
        };

        this.securityMetrics = {
            blockedRequests: 0,
            sanitizedInputs: 0,
            csrfTokensGenerated: 0,
            xssAttemptsBlocked: 0,
            suspiciousActivities: 0
        };

        this.csrfToken = null;
        this.sessionStartTime = Date.now();
        this.lastActivityTime = Date.now();
    }

    /**
     * Инициализация системы безопасности
     */
    async init() {
        console.log('🔒 Initializing Security Manager...');

        try {
            // Инициализируем CSP
            this.initContentSecurityPolicy();

            // Инициализируем XSS защиту
            this.initXSSProtection();

            // Инициализируем CSRF защиту
            this.initCSRFProtection();

            // Инициализируем санитизацию ввода
            this.initInputSanitization();

            // Инициализируем мониторинг сессии
            this.initSessionMonitoring();

            // Инициализируем мониторинг безопасности
            this.initSecurityMonitoring();

            this.isInitialized = true;
            console.log('🔒 Security Manager initialized successfully');

        } catch (error) {
            console.error('🔒 Failed to initialize Security Manager:', error);
        }
    }

    /**
     * Инициализация Content Security Policy
     */
    initContentSecurityPolicy() {
        if (!this.securityConfig.enableCSP) return;

        try {
            // Создаем мета-тег CSP
            const cspMeta = document.createElement('meta');
            cspMeta.setAttribute('http-equiv', 'Content-Security-Policy');
            cspMeta.setAttribute('content', this.generateCSP());
            document.head.appendChild(cspMeta);

            console.log('🔒 Content Security Policy initialized');
        } catch (error) {
            console.error('🔒 Failed to initialize CSP:', error);
        }
    }

    /**
     * Генерация Content Security Policy
     */
    generateCSP() {
        return [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com",
            "img-src 'self' data: https: blob:",
            "connect-src 'self' ws: wss:",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "object-src 'none'",
            "media-src 'self'",
            "worker-src 'self' blob:",
            "child-src 'self' blob:"
        ].join('; ');
    }

    /**
     * Инициализация XSS защиты
     */
    initXSSProtection() {
        if (!this.securityConfig.enableXSSProtection) return;

        // Перехватываем innerHTML и outerHTML
        this.overrideInnerHTML();
        this.overrideOuterHTML();

        // Перехватываем document.write
        this.overrideDocumentWrite();

        // Перехватываем eval
        this.overrideEval();

        console.log('🔒 XSS Protection initialized');
    }

    /**
     * Переопределение innerHTML для защиты от XSS
     */
    overrideInnerHTML() {
        const originalInnerHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');

        Object.defineProperty(Element.prototype, 'innerHTML', {
            set: function (value) {
                const sanitizedValue = window.securityManager.sanitizeHTML(value);
                originalInnerHTML.set.call(this, sanitizedValue);
            },
            get: originalInnerHTML.get
        });
    }

    /**
     * Переопределение outerHTML для защиты от XSS
     */
    overrideOuterHTML() {
        const originalOuterHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'outerHTML');

        Object.defineProperty(Element.prototype, 'outerHTML', {
            set: function (value) {
                const sanitizedValue = window.securityManager.sanitizeHTML(value);
                originalOuterHTML.set.call(this, sanitizedValue);
            },
            get: originalOuterHTML.get
        });
    }

    /**
     * Переопределение document.write для защиты от XSS
     */
    overrideDocumentWrite() {
        const originalWrite = document.write;
        const self = this;

        document.write = function (content) {
            const sanitizedContent = self.sanitizeHTML(content);
            originalWrite.call(document, sanitizedContent);
        };
    }

    /**
     * Переопределение eval для защиты от XSS
     */
    overrideEval() {
        const originalEval = window.eval;
        const self = this;

        window.eval = function (code) {
            console.warn('🔒 eval() usage detected and blocked for security');
            self.securityMetrics.xssAttemptsBlocked++;
            throw new Error('eval() is disabled for security reasons');
        };
    }

    /**
     * Инициализация CSRF защиты
     */
    async initCSRFProtection() {
        if (!this.securityConfig.enableCSRFProtection) return;

        try {
            // Генерируем CSRF токен
            this.csrfToken = this.generateCSRFToken();
            this.securityMetrics.csrfTokensGenerated++;

            // Добавляем токен ко всем формам
            this.addCSRFTokenToForms();

            // Перехватываем fetch для добавления CSRF заголовка
            this.interceptFetch();

            console.log('🔒 CSRF Protection initialized');
        } catch (error) {
            console.error('🔒 Failed to initialize CSRF protection:', error);
        }
    }

    /**
     * Генерация CSRF токена
     */
    generateCSRFToken() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Добавление CSRF токена к формам
     */
    addCSRFTokenToForms() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            if (!form.querySelector('input[name="_csrf_token"]')) {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = '_csrf_token';
                csrfInput.value = this.csrfToken;
                form.appendChild(csrfInput);
            }
        });
    }

    /**
     * Перехват fetch для добавления CSRF заголовка
     */
    interceptFetch() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = function (url, options = {}) {
            // Добавляем CSRF заголовок
            if (self.csrfToken) {
                options.headers = {
                    ...options.headers,
                    'X-CSRF-Token': self.csrfToken
                };
            }

            return originalFetch.call(this, url, options);
        };
    }

    /**
     * Инициализация санитизации ввода
     */
    initInputSanitization() {
        if (!this.securityConfig.enableInputSanitization) return;

        // Перехватываем все input события
        document.addEventListener('input', (event) => {
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                this.sanitizeInput(event.target);
            }
        });

        console.log('🔒 Input Sanitization initialized');
    }

    /**
     * Санитизация HTML
     */
    sanitizeHTML(html) {
        if (typeof html !== 'string') return html;

        // Создаем временный элемент
        const temp = document.createElement('div');
        temp.textContent = html;
        return temp.innerHTML;
    }

    /**
     * Санитизация пользовательского ввода
     */
    sanitizeInput(inputElement) {
        if (!inputElement) return;

        const originalValue = inputElement.value;
        const sanitizedValue = this.sanitizeUserInput(originalValue);

        if (originalValue !== sanitizedValue) {
            inputElement.value = sanitizedValue;
            this.securityMetrics.sanitizedInputs++;

            // Показываем предупреждение пользователю
            this.showSecurityWarning('Potentially dangerous input was sanitized');
        }
    }

    /**
     * Санитизация пользовательского ввода
     */
    sanitizeUserInput(input) {
        if (typeof input !== 'string') return input;

        // Удаляем потенциально опасные символы и теги
        return input
            .replace(/<script[^>]*>.*?<\/script>/gi, '')
            .replace(/<iframe[^>]*>.*?<\/iframe>/gi, '')
            .replace(/<object[^>]*>.*?<\/object>/gi, '')
            .replace(/<embed[^>]*>.*?<\/embed>/gi, '')
            .replace(/javascript:/gi, '')
            .replace(/on\w+\s*=/gi, '')
            .replace(/<[^>]*>/g, '')
            .replace(/[<>]/g, '');
    }

    /**
     * Инициализация мониторинга сессии
     */
    initSessionMonitoring() {
        // Обновляем время последней активности
        document.addEventListener('click', () => this.updateLastActivity());
        document.addEventListener('keypress', () => this.updateLastActivity());
        document.addEventListener('scroll', () => this.updateLastActivity());

        // Проверяем таймаут сессии каждую минуту
        setInterval(() => this.checkSessionTimeout(), 60000);

        console.log('🔒 Session Monitoring initialized');
    }

    /**
     * Обновление времени последней активности
     */
    updateLastActivity() {
        this.lastActivityTime = Date.now();
    }

    /**
     * Проверка таймаута сессии
     */
    checkSessionTimeout() {
        const timeSinceLastActivity = Date.now() - this.lastActivityTime;
        const sessionDuration = Date.now() - this.sessionStartTime;

        if (timeSinceLastActivity > this.securityConfig.sessionTimeout) {
            this.handleSessionTimeout();
        }

        // Предупреждение за 5 минут до таймаута
        if (timeSinceLastActivity > this.securityConfig.sessionTimeout - 300000) {
            this.showSessionWarning();
        }
    }

    /**
     * Обработка таймаута сессии
     */
    handleSessionTimeout() {
        console.log('🔒 Session timeout detected');

        // Очищаем данные сессии
        localStorage.removeItem('auth_token');
        sessionStorage.clear();

        // Перенаправляем на страницу входа
        window.location.href = '/login.html';
    }

    /**
     * Показ предупреждения о сессии
     */
    showSessionWarning() {
        if (document.getElementById('session-warning')) return;

        const warning = document.createElement('div');
        warning.id = 'session-warning';
        warning.className = 'alert alert-warning position-fixed';
        warning.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        warning.innerHTML = `
            <h6>Session Warning</h6>
            <p>Your session will expire soon. Click anywhere to extend it.</p>
            <button class="btn btn-sm btn-primary" onclick="this.parentElement.remove()">OK</button>
        `;

        document.body.appendChild(warning);

        // Автоматически удаляем через 10 секунд
        setTimeout(() => {
            if (warning.parentElement) {
                warning.remove();
            }
        }, 10000);
    }

    /**
     * Инициализация мониторинга безопасности
     */
    initSecurityMonitoring() {
        // Мониторинг подозрительной активности
        this.monitorSuspiciousActivity();

        // Мониторинг сетевых запросов
        this.monitorNetworkRequests();

        // Мониторинг ошибок
        this.monitorErrors();

        console.log('🔒 Security Monitoring initialized');
    }

    /**
     * Мониторинг подозрительной активности
     */
    monitorSuspiciousActivity() {
        // Мониторинг попыток доступа к консоли
        const originalConsole = {
            log: console.log,
            warn: console.warn,
            error: console.error
        };

        ['log', 'warn', 'error'].forEach(method => {
            console[method] = function (...args) {
                // Проверяем на подозрительные команды
                const message = args.join(' ');
                if (message.includes('eval') || message.includes('Function') || message.includes('setTimeout')) {
                    window.securityManager.securityMetrics.suspiciousActivities++;
                    console.warn('🔒 Suspicious console activity detected');
                }

                originalConsole[method].apply(console, args);
            };
        });
    }

    /**
     * Мониторинг сетевых запросов
     */
    monitorNetworkRequests() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = function (url, options = {}) {
            // Проверяем URL на подозрительные паттерны
            if (self.isSuspiciousURL(url)) {
                self.securityMetrics.blockedRequests++;
                console.warn('🔒 Suspicious URL blocked:', url);
                return Promise.reject(new Error('Suspicious URL blocked'));
            }

            return originalFetch.call(this, url, options);
        };
    }

    /**
     * Проверка URL на подозрительные паттерны
     */
    isSuspiciousURL(url) {
        const suspiciousPatterns = [
            /javascript:/i,
            /data:text\/html/i,
            /vbscript:/i,
            /file:/i,
            /ftp:/i
        ];

        return suspiciousPatterns.some(pattern => pattern.test(url));
    }

    /**
     * Мониторинг ошибок
     */
    monitorErrors() {
        window.addEventListener('error', (event) => {
            this.securityMetrics.suspiciousActivities++;
            console.warn('🔒 Error detected:', event.error);
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.securityMetrics.suspiciousActivities++;
            console.warn('🔒 Unhandled promise rejection:', event.reason);
        });
    }

    /**
     * Показ предупреждения о безопасности
     */
    showSecurityWarning(message) {
        if (window.Toast && typeof window.Toast.warning === 'function') {
            window.Toast.warning(message);
        } else {
            console.warn('🔒 Security Warning:', message);
        }
    }

    /**
     * Получение отчета по безопасности
     */
    getSecurityReport() {
        return {
            isInitialized: this.isInitialized,
            securityConfig: this.securityConfig,
            securityMetrics: this.securityMetrics,
            sessionInfo: {
                startTime: this.sessionStartTime,
                lastActivity: this.lastActivityTime,
                duration: Date.now() - this.sessionStartTime,
                timeSinceLastActivity: Date.now() - this.lastActivityTime
            },
            csrfToken: this.csrfToken ? 'Present' : 'Not generated',
            recommendations: this.getSecurityRecommendations()
        };
    }

    /**
     * Получение рекомендаций по безопасности
     */
    getSecurityRecommendations() {
        const recommendations = [];

        if (this.securityMetrics.sanitizedInputs > 10) {
            recommendations.push('Consider implementing stricter input validation');
        }

        if (this.securityMetrics.xssAttemptsBlocked > 0) {
            recommendations.push('XSS attempts detected - review user inputs');
        }

        if (this.securityMetrics.blockedRequests > 0) {
            recommendations.push('Suspicious requests blocked - review network traffic');
        }

        if (this.securityMetrics.suspiciousActivities > 5) {
            recommendations.push('High suspicious activity - consider additional monitoring');
        }

        return recommendations;
    }

    /**
     * Очистка ресурсов
     */
    destroy() {
        this.isInitialized = false;
        this.csrfToken = null;
        console.log('🔒 Security Manager destroyed');
    }
}

// Создаем глобальный экземпляр
window.securityManager = new SecurityManager();
