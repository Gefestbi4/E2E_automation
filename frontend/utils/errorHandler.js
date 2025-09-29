// Enhanced Error Handler
class ErrorHandler {
    constructor() {
        this.errorLog = [];
        this.maxLogSize = 100;
        this.init();
    }

    init() {
        // Global error handlers
        window.addEventListener('error', (event) => {
            this.handleError(event.error, 'JavaScript Error');
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.handleError(event.reason, 'Unhandled Promise Rejection');
        });

        // Network error monitoring
        this.setupNetworkMonitoring();
    }

    setupNetworkMonitoring() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = async function (...args) {
            try {
                const response = await originalFetch.apply(this, args);

                if (!response.ok) {
                    const error = new Error(`HTTP ${response.status}: ${response.statusText}`);
                    error.status = response.status;
                    error.url = args[0];
                    self.handleError(error, 'Network Error');
                }

                return response;
            } catch (error) {
                self.handleError(error, 'Network Error');
                throw error;
            }
        };
    }

    handleError(error, type = 'Application Error', context = {}) {
        const errorInfo = {
            id: this.generateErrorId(),
            timestamp: new Date().toISOString(),
            type: type,
            message: error.message || 'Unknown error',
            stack: error.stack,
            url: window.location.href,
            userAgent: navigator.userAgent,
            context: context,
            severity: this.determineSeverity(error, type)
        };

        // Add to error log
        this.addToLog(errorInfo);

        // Log to console in development
        if (this.isDevelopment()) {
            console.error(`[${type}]`, errorInfo);
        }

        // Send to monitoring service in production
        if (this.isProduction()) {
            this.sendToMonitoring(errorInfo);
        }

        // Show user notification if needed
        this.showUserNotification(errorInfo);

        return errorInfo;
    }

    determineSeverity(error, type) {
        // Determine error severity based on type and context
        if (type === 'Network Error') {
            if (error.status >= 500) return 'high';
            if (error.status >= 400) return 'medium';
            return 'low';
        }

        if (type === 'JavaScript Error') {
            // Check if it's a critical error
            if (error.message.includes('Cannot read property') ||
                error.message.includes('is not a function') ||
                error.message.includes('Cannot access')) {
                return 'high';
            }
            return 'medium';
        }

        return 'low';
    }

    addToLog(errorInfo) {
        this.errorLog.unshift(errorInfo);

        // Keep log size manageable
        if (this.errorLog.length > this.maxLogSize) {
            this.errorLog = this.errorLog.slice(0, this.maxLogSize);
        }

        // Store in localStorage for persistence
        try {
            localStorage.setItem('errorLog', JSON.stringify(this.errorLog));
        } catch (e) {
            // localStorage might be full or disabled
            console.warn('Could not store error log:', e);
        }
    }

    async sendToMonitoring(errorInfo) {
        try {
            // Send to external monitoring service
            await fetch('/api/monitoring/errors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(errorInfo)
            });
        } catch (e) {
            // Silently fail - don't create error loops
            console.warn('Could not send error to monitoring service:', e);
        }
    }

    showUserNotification(errorInfo) {
        // Only show notifications for high severity errors
        if (errorInfo.severity === 'high') {
            this.showErrorToast('Произошла критическая ошибка. Пожалуйста, обновите страницу.');
        }
    }

    showErrorToast(message, duration = 5000) {
        const toast = document.createElement('div');
        toast.className = 'error-toast';
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">⚠️</span>
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add styles if not already added
        this.addToastStyles();

        document.body.appendChild(toast);

        // Auto remove after duration
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, duration);
    }

    addToastStyles() {
        if (document.getElementById('error-toast-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'error-toast-styles';
        styles.textContent = `
            .error-toast {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #e74c3c;
                color: white;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                z-index: 10000;
                animation: slideInRight 0.3s ease;
                max-width: 400px;
            }

            .toast-content {
                display: flex;
                align-items: center;
                padding: 15px 20px;
                gap: 10px;
            }

            .toast-icon {
                font-size: 1.2rem;
            }

            .toast-message {
                flex: 1;
                font-weight: 500;
            }

            .toast-close {
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .toast-close:hover {
                opacity: 0.8;
            }

            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;

        document.head.appendChild(styles);
    }

    generateErrorId() {
        return 'err_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    isDevelopment() {
        return window.location.hostname === 'localhost' ||
            window.location.hostname === '127.0.0.1' ||
            window.location.protocol === 'file:';
    }

    isProduction() {
        return !this.isDevelopment();
    }

    // Public methods for manual error handling
    logError(error, context = {}) {
        return this.handleError(error, 'Manual Log', context);
    }

    logWarning(message, context = {}) {
        const warning = new Error(message);
        warning.isWarning = true;
        return this.handleError(warning, 'Warning', context);
    }

    logInfo(message, context = {}) {
        const info = new Error(message);
        info.isInfo = true;
        return this.handleError(info, 'Info', context);
    }

    getErrorLog() {
        return [...this.errorLog];
    }

    clearErrorLog() {
        this.errorLog = [];
        localStorage.removeItem('errorLog');
    }

    // Load error log from localStorage
    loadErrorLog() {
        try {
            const stored = localStorage.getItem('errorLog');
            if (stored) {
                this.errorLog = JSON.parse(stored);
            }
        } catch (e) {
            console.warn('Could not load error log from localStorage:', e);
        }
    }

    // Get error statistics
    getErrorStats() {
        const stats = {
            total: this.errorLog.length,
            byType: {},
            bySeverity: { high: 0, medium: 0, low: 0 },
            last24Hours: 0
        };

        const now = new Date();
        const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);

        this.errorLog.forEach(error => {
            // Count by type
            stats.byType[error.type] = (stats.byType[error.type] || 0) + 1;

            // Count by severity
            stats.bySeverity[error.severity]++;

            // Count last 24 hours
            const errorTime = new Date(error.timestamp);
            if (errorTime > yesterday) {
                stats.last24Hours++;
            }
        });

        return stats;
    }

    // Create error report for debugging
    createErrorReport() {
        const stats = this.getErrorStats();
        const recentErrors = this.errorLog.slice(0, 10);

        return {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            userAgent: navigator.userAgent,
            stats: stats,
            recentErrors: recentErrors,
            systemInfo: {
                screen: `${screen.width}x${screen.height}`,
                viewport: `${window.innerWidth}x${window.innerHeight}`,
                language: navigator.language,
                platform: navigator.platform,
                cookieEnabled: navigator.cookieEnabled,
                onLine: navigator.onLine
            }
        };
    }
}

// Initialize error handler
const errorHandler = new ErrorHandler();
errorHandler.loadErrorLog();

// Export for global access
window.ErrorHandler = errorHandler;

// Also export the class for testing
export { ErrorHandler };
