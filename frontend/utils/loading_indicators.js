/**
 * Система индикаторов загрузки
 * Поддерживает различные типы индикаторов: спиннеры, прогресс бары, скелетоны
 */

class LoadingIndicator {
    constructor(options = {}) {
        this.options = {
            type: 'spinner', // spinner, progress, skeleton, dots, pulse
            size: 'medium', // small, medium, large
            color: '#3b82f6',
            text: 'Загрузка...',
            showText: true,
            overlay: false,
            ...options
        };

        this.element = null;
        this.isVisible = false;
        this.progress = 0;
    }

    /**
     * Создание индикатора загрузки
     */
    create() {
        const container = document.createElement('div');
        container.className = `loading-indicator loading-${this.options.type} loading-${this.options.size}`;

        if (this.options.overlay) {
            container.classList.add('loading-overlay');
        }

        switch (this.options.type) {
            case 'spinner':
                container.innerHTML = this.createSpinner();
                break;
            case 'progress':
                container.innerHTML = this.createProgressBar();
                break;
            case 'skeleton':
                container.innerHTML = this.createSkeleton();
                break;
            case 'dots':
                container.innerHTML = this.createDots();
                break;
            case 'pulse':
                container.innerHTML = this.createPulse();
                break;
        }

        this.element = container;
        return container;
    }

    /**
     * Создание спиннера
     */
    createSpinner() {
        return `
            <div class="spinner-container">
                <div class="spinner" style="border-color: ${this.options.color}"></div>
                ${this.options.showText ? `<span class="loading-text">${this.options.text}</span>` : ''}
            </div>
        `;
    }

    /**
     * Создание прогресс бара
     */
    createProgressBar() {
        return `
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="background-color: ${this.options.color}"></div>
                </div>
                ${this.options.showText ? `<span class="loading-text">${this.options.text}</span>` : ''}
            </div>
        `;
    }

    /**
     * Создание скелетона
     */
    createSkeleton() {
        return `
            <div class="skeleton-container">
                <div class="skeleton-item"></div>
                <div class="skeleton-item short"></div>
                <div class="skeleton-item medium"></div>
            </div>
        `;
    }

    /**
     * Создание точек
     */
    createDots() {
        return `
            <div class="dots-container">
                <div class="dot" style="background-color: ${this.options.color}"></div>
                <div class="dot" style="background-color: ${this.options.color}"></div>
                <div class="dot" style="background-color: ${this.options.color}"></div>
                ${this.options.showText ? `<span class="loading-text">${this.options.text}</span>` : ''}
            </div>
        `;
    }

    /**
     * Создание пульса
     */
    createPulse() {
        return `
            <div class="pulse-container">
                <div class="pulse-circle" style="background-color: ${this.options.color}"></div>
                ${this.options.showText ? `<span class="loading-text">${this.options.text}</span>` : ''}
            </div>
        `;
    }

    /**
     * Показать индикатор
     */
    show(target = null) {
        if (this.isVisible) return;

        if (!this.element) {
            this.create();
        }

        if (target) {
            target.appendChild(this.element);
        } else {
            document.body.appendChild(this.element);
        }

        this.isVisible = true;
        this.element.classList.add('show');
    }

    /**
     * Скрыть индикатор
     */
    hide() {
        if (!this.isVisible || !this.element) return;

        this.element.classList.remove('show');

        setTimeout(() => {
            if (this.element && this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
            this.isVisible = false;
        }, 300);
    }

    /**
     * Обновить прогресс (только для progress типа)
     */
    updateProgress(progress) {
        if (this.options.type !== 'progress' || !this.element) return;

        this.progress = Math.max(0, Math.min(100, progress));
        const fill = this.element.querySelector('.progress-fill');
        if (fill) {
            fill.style.width = `${this.progress}%`;
        }

        const text = this.element.querySelector('.loading-text');
        if (text) {
            text.textContent = `${this.options.text} ${Math.round(this.progress)}%`;
        }
    }

    /**
     * Обновить текст
     */
    updateText(text) {
        this.options.text = text;
        const textElement = this.element?.querySelector('.loading-text');
        if (textElement) {
            textElement.textContent = text;
        }
    }
}

/**
 * Менеджер индикаторов загрузки
 */
class LoadingManager {
    constructor() {
        this.indicators = new Map();
        this.globalIndicator = null;
        this.setupStyles();
    }

    /**
     * Настройка стилей
     */
    setupStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Базовые стили для индикаторов загрузки */
            .loading-indicator {
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .loading-indicator.show {
                opacity: 1;
            }
            
            .loading-indicator.loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(2px);
                z-index: 9999;
            }
            
            /* Размеры */
            .loading-small .spinner {
                width: 20px;
                height: 20px;
                border-width: 2px;
            }
            
            .loading-medium .spinner {
                width: 40px;
                height: 40px;
                border-width: 4px;
            }
            
            .loading-large .spinner {
                width: 60px;
                height: 60px;
                border-width: 6px;
            }
            
            /* Спиннер */
            .spinner-container {
                text-align: center;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3b82f6;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            .loading-text {
                display: block;
                margin-top: 12px;
                color: #6b7280;
                font-size: 14px;
            }
            
            /* Прогресс бар */
            .progress-container {
                width: 200px;
                text-align: center;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background-color: #e5e7eb;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                background-color: #3b82f6;
                border-radius: 4px;
                transition: width 0.3s ease;
                width: 0%;
            }
            
            /* Скелетон */
            .skeleton-container {
                width: 100%;
            }
            
            .skeleton-item {
                height: 12px;
                background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                background-size: 200% 100%;
                animation: skeleton-loading 1.5s infinite;
                border-radius: 4px;
                margin-bottom: 8px;
            }
            
            .skeleton-item.short {
                width: 60%;
            }
            
            .skeleton-item.medium {
                width: 80%;
            }
            
            /* Точки */
            .dots-container {
                display: flex;
                align-items: center;
                gap: 4px;
            }
            
            .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: #3b82f6;
                animation: dots-bounce 1.4s ease-in-out infinite both;
            }
            
            .dot:nth-child(1) { animation-delay: -0.32s; }
            .dot:nth-child(2) { animation-delay: -0.16s; }
            .dot:nth-child(3) { animation-delay: 0s; }
            
            /* Пульс */
            .pulse-container {
                text-align: center;
            }
            
            .pulse-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: #3b82f6;
                animation: pulse-scale 1.5s ease-in-out infinite;
            }
            
            /* Анимации */
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes skeleton-loading {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            
            @keyframes dots-bounce {
                0%, 80%, 100% {
                    transform: scale(0);
                }
                40% {
                    transform: scale(1);
                }
            }
            
            @keyframes pulse-scale {
                0% {
                    transform: scale(0);
                    opacity: 1;
                }
                100% {
                    transform: scale(1);
                    opacity: 0;
                }
            }
            
            /* Skeleton для карточек */
            .skeleton-card {
                background: white;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .skeleton-card .skeleton-item {
                margin-bottom: 12px;
            }
            
            .skeleton-card .skeleton-item:last-child {
                margin-bottom: 0;
            }
            
            /* Skeleton для списков */
            .skeleton-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .skeleton-list-item {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .skeleton-list-item .skeleton-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }
            
            .skeleton-list-item .skeleton-content {
                flex: 1;
            }
            
            /* Skeleton для таблиц */
            .skeleton-table {
                width: 100%;
            }
            
            .skeleton-table-row {
                display: flex;
                gap: 12px;
                margin-bottom: 8px;
            }
            
            .skeleton-table-cell {
                flex: 1;
                height: 16px;
            }
        `;

        document.head.appendChild(style);
    }

    /**
     * Создать индикатор загрузки
     */
    create(id, options = {}) {
        const indicator = new LoadingIndicator(options);
        this.indicators.set(id, indicator);
        return indicator;
    }

    /**
     * Показать индикатор
     */
    show(id, target = null) {
        let indicator = this.indicators.get(id);

        if (!indicator) {
            indicator = this.create(id);
        }

        indicator.show(target);
    }

    /**
     * Скрыть индикатор
     */
    hide(id) {
        const indicator = this.indicators.get(id);
        if (indicator) {
            indicator.hide();
        }
    }

    /**
     * Обновить прогресс
     */
    updateProgress(id, progress) {
        const indicator = this.indicators.get(id);
        if (indicator) {
            indicator.updateProgress(progress);
        }
    }

    /**
     * Обновить текст
     */
    updateText(id, text) {
        const indicator = this.indicators.get(id);
        if (indicator) {
            indicator.updateText(text);
        }
    }

    /**
     * Показать глобальный индикатор
     */
    showGlobal(options = {}) {
        if (this.globalIndicator) {
            this.hideGlobal();
        }

        this.globalIndicator = new LoadingIndicator({
            type: 'spinner',
            size: 'large',
            overlay: true,
            text: 'Загрузка...',
            ...options
        });

        this.globalIndicator.show();
    }

    /**
     * Скрыть глобальный индикатор
     */
    hideGlobal() {
        if (this.globalIndicator) {
            this.globalIndicator.hide();
            this.globalIndicator = null;
        }
    }

    /**
     * Создать skeleton loader для контента
     */
    createSkeletonLoader(type = 'card', count = 1) {
        const container = document.createElement('div');
        container.className = `skeleton-${type}`;

        for (let i = 0; i < count; i++) {
            const skeleton = document.createElement('div');
            skeleton.className = `skeleton-${type}-item`;

            switch (type) {
                case 'card':
                    skeleton.innerHTML = `
                        <div class="skeleton-item" style="height: 200px; margin-bottom: 12px;"></div>
                        <div class="skeleton-item" style="height: 16px; margin-bottom: 8px;"></div>
                        <div class="skeleton-item short" style="height: 14px; margin-bottom: 8px;"></div>
                        <div class="skeleton-item medium" style="height: 14px;"></div>
                    `;
                    break;
                case 'list':
                    skeleton.innerHTML = `
                        <div class="skeleton-list-item">
                            <div class="skeleton-avatar skeleton-item"></div>
                            <div class="skeleton-content">
                                <div class="skeleton-item" style="height: 16px; margin-bottom: 4px;"></div>
                                <div class="skeleton-item short" style="height: 14px;"></div>
                            </div>
                        </div>
                    `;
                    break;
                case 'table':
                    skeleton.innerHTML = `
                        <div class="skeleton-table-row">
                            <div class="skeleton-table-cell skeleton-item"></div>
                            <div class="skeleton-table-cell skeleton-item"></div>
                            <div class="skeleton-table-cell skeleton-item"></div>
                            <div class="skeleton-table-cell skeleton-item"></div>
                        </div>
                    `;
                    break;
            }

            container.appendChild(skeleton);
        }

        return container;
    }

    /**
     * Показать skeleton loader
     */
    showSkeleton(target, type = 'card', count = 1) {
        const skeleton = this.createSkeletonLoader(type, count);
        target.innerHTML = '';
        target.appendChild(skeleton);
    }

    /**
     * Скрыть skeleton loader
     */
    hideSkeleton(target) {
        const skeletons = target.querySelectorAll('[class*="skeleton-"]');
        skeletons.forEach(skeleton => {
            skeleton.remove();
        });
    }

    /**
     * Очистка всех индикаторов
     */
    cleanup() {
        this.indicators.forEach(indicator => indicator.hide());
        this.indicators.clear();
        this.hideGlobal();
    }
}

// Создаем глобальный экземпляр
window.LoadingManager = new LoadingManager();

// Экспорт для глобального доступа
window.Loading = {
    // Быстрые методы
    show: (id, target, options) => window.LoadingManager.show(id, target, options),
    hide: (id) => window.LoadingManager.hide(id),
    showGlobal: (options) => window.LoadingManager.showGlobal(options),
    hideGlobal: () => window.LoadingManager.hideGlobal(),
    updateProgress: (id, progress) => window.LoadingManager.updateProgress(id, progress),
    updateText: (id, text) => window.LoadingManager.updateText(id, text),

    // Skeleton loaders
    showSkeleton: (target, type, count) => window.LoadingManager.showSkeleton(target, type, count),
    hideSkeleton: (target) => window.LoadingManager.hideSkeleton(target),

    // Создание индикаторов
    create: (id, options) => window.LoadingManager.create(id, options)
};
