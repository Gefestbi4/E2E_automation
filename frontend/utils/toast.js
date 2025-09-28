/**
 * Улучшенная система Toast уведомлений
 * Поддерживает различные типы, позиционирование, анимации и автоудаление
 */

class Toast {
    constructor() {
        this.container = null;
        this.toasts = new Map();
        this.defaultOptions = {
            type: 'info',
            duration: 5000,
            position: 'top-right',
            closable: true,
            animation: 'slide',
            maxToasts: 5
        };

        this.types = {
            success: { icon: '✓', color: '#27ae60', bgColor: '#d5f4e6' },
            error: { icon: '✕', color: '#e74c3c', bgColor: '#f8d7da' },
            warning: { icon: '⚠', color: '#f39c12', bgColor: '#fff3cd' },
            info: { icon: 'ℹ', color: '#3498db', bgColor: '#d1ecf1' }
        };

        this.init();
    }

    /**
     * Инициализация Toast системы
     */
    init() {
        this.createContainer();
        this.setupStyles();
    }

    /**
     * Создание контейнера для Toast
     */
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
        `;

        document.body.appendChild(this.container);
    }

    /**
     * Настройка стилей
     */
    setupStyles() {
        if (document.getElementById('toast-styles')) return;

        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            .toast {
                display: flex;
                align-items: center;
                padding: 12px 16px;
                margin-bottom: 8px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                line-height: 1.4;
                max-width: 400px;
                min-width: 300px;
                pointer-events: auto;
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .toast-content {
                display: flex;
                align-items: flex-start;
                flex: 1;
            }

            .toast-icon {
                font-size: 18px;
                margin-right: 12px;
                flex-shrink: 0;
                margin-top: 2px;
            }

            .toast-message {
                flex: 1;
                word-wrap: break-word;
            }

            .toast-title {
                font-weight: 600;
                margin-bottom: 4px;
            }

            .toast-description {
                opacity: 0.9;
                font-size: 13px;
            }

            .toast-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
                margin-left: 12px;
                opacity: 0.6;
                transition: opacity 0.2s;
                flex-shrink: 0;
            }

            .toast-close:hover {
                opacity: 1;
            }

            .toast-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: rgba(255, 255, 255, 0.3);
                transition: width linear;
            }

            /* Анимации */
            .toast-enter {
                transform: translateX(100%);
                opacity: 0;
            }

            .toast-enter-active {
                transform: translateX(0);
                opacity: 1;
                transition: transform 0.3s ease-out, opacity 0.3s ease-out;
            }

            .toast-exit {
                transform: translateX(0);
                opacity: 1;
            }

            .toast-exit-active {
                transform: translateX(100%);
                opacity: 0;
                transition: transform 0.3s ease-in, opacity 0.3s ease-in;
            }

            /* Позиционирование */
            .toast-container-top-left {
                top: 20px;
                left: 20px;
                right: auto;
            }

            .toast-container-top-center {
                top: 20px;
                left: 50%;
                right: auto;
                transform: translateX(-50%);
            }

            .toast-container-bottom-right {
                top: auto;
                bottom: 20px;
                right: 20px;
            }

            .toast-container-bottom-left {
                top: auto;
                bottom: 20px;
                left: 20px;
                right: auto;
            }

            .toast-container-bottom-center {
                top: auto;
                bottom: 20px;
                left: 50%;
                right: auto;
                transform: translateX(-50%);
            }

            /* Типы Toast */
            .toast-success {
                background: linear-gradient(135deg, #d5f4e6 0%, #c8e6c9 100%);
                color: #2e7d32;
            }

            .toast-error {
                background: linear-gradient(135deg, #f8d7da 0%, #ffcdd2 100%);
                color: #c62828;
            }

            .toast-warning {
                background: linear-gradient(135deg, #fff3cd 0%, #ffe0b2 100%);
                color: #ef6c00;
            }

            .toast-info {
                background: linear-gradient(135deg, #d1ecf1 0%, #b3e5fc 100%);
                color: #0277bd;
            }
        `;

        document.head.appendChild(style);
    }

    /**
     * Показ Toast уведомления
     */
    show(message, options = {}) {
        const config = { ...this.defaultOptions, ...options };
        const toastId = this.generateId();

        // Ограничиваем количество Toast
        if (this.toasts.size >= config.maxToasts) {
            const oldestToast = this.toasts.keys().next().value;
            this.hide(oldestToast);
        }

        const toast = this.createToast(toastId, message, config);
        this.toasts.set(toastId, { element: toast, config, timer: null });

        this.container.appendChild(toast);
        this.animateIn(toast);

        // Автоудаление
        if (config.duration > 0) {
            const timer = setTimeout(() => {
                this.hide(toastId);
            }, config.duration);

            this.toasts.get(toastId).timer = timer;
        }

        return toastId;
    }

    /**
     * Создание элемента Toast
     */
    createToast(id, message, config) {
        const toast = document.createElement('div');
        toast.id = `toast-${id}`;
        toast.className = `toast toast-${config.type}`;

        const typeConfig = this.types[config.type] || this.types.info;

        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-icon" style="color: ${typeConfig.color}">
                    ${typeConfig.icon}
                </div>
                <div class="toast-message">
                    ${this.formatMessage(message)}
                </div>
                ${config.closable ? `
                    <button class="toast-close" onclick="Toast.hide('${id}')" aria-label="Закрыть">
                        ×
                    </button>
                ` : ''}
            </div>
            ${config.duration > 0 ? '<div class="toast-progress"></div>' : ''}
        `;

        // Обработчик клика для закрытия
        if (config.closable) {
            toast.addEventListener('click', (e) => {
                if (e.target.classList.contains('toast-close')) return;
                this.hide(id);
            });
        }

        return toast;
    }

    /**
     * Форматирование сообщения
     */
    formatMessage(message) {
        if (typeof message === 'string') {
            return `<div class="toast-description">${this.escapeHtml(message)}</div>`;
        } else if (typeof message === 'object' && message.title) {
            return `
                <div class="toast-title">${this.escapeHtml(message.title)}</div>
                <div class="toast-description">${this.escapeHtml(message.description || '')}</div>
            `;
        }
        return `<div class="toast-description">${this.escapeHtml(String(message))}</div>`;
    }

    /**
     * Экранирование HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Анимация появления
     */
    animateIn(toast) {
        toast.classList.add('toast-enter');
        requestAnimationFrame(() => {
            toast.classList.add('toast-enter-active');
            toast.classList.remove('toast-enter');
        });
    }

    /**
     * Анимация исчезновения
     */
    animateOut(toast, callback) {
        toast.classList.add('toast-exit');
        toast.classList.add('toast-exit-active');
        toast.classList.remove('toast-exit');

        setTimeout(() => {
            if (callback) callback();
        }, 300);
    }

    /**
     * Скрытие Toast
     */
    hide(id) {
        const toastData = this.toasts.get(id);
        if (!toastData) return;

        const { element, timer } = toastData;

        // Очищаем таймер
        if (timer) {
            clearTimeout(timer);
        }

        // Анимируем исчезновение
        this.animateOut(element, () => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
            this.toasts.delete(id);
        });
    }

    /**
     * Скрытие всех Toast
     */
    hideAll() {
        this.toasts.forEach((_, id) => {
            this.hide(id);
        });
    }

    /**
     * Обновление позиции контейнера
     */
    setPosition(position) {
        this.container.className = `toast-container-${position}`;
    }

    /**
     * Генерация уникального ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Статические методы для удобства
    static success(message, options = {}) {
        return window.Toast.show(message, { ...options, type: 'success' });
    }

    static error(message, options = {}) {
        return window.Toast.show(message, { ...options, type: 'error' });
    }

    static warning(message, options = {}) {
        return window.Toast.show(message, { ...options, type: 'warning' });
    }

    static info(message, options = {}) {
        return window.Toast.show(message, { ...options, type: 'info' });
    }

    static hide(id) {
        return window.Toast.hide(id);
    }

    static hideAll() {
        return window.Toast.hideAll();
    }
}

// Создаем глобальный экземпляр
window.Toast = new Toast();

// Экспорт для глобального доступа
window.ToastClass = Toast;
