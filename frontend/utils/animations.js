/**
 * Система анимаций и переходов
 * Поддерживает различные типы анимаций, переходы между страницами, loading состояния
 */

class AnimationManager {
    constructor() {
        this.animations = new Map();
        this.transitions = new Map();
        this.loadingStates = new Set();
        this.animationQueue = [];
        this.isProcessing = false;

        this.init();
    }

    /**
     * Инициализация системы анимаций
     */
    init() {
        this.setupCSSAnimations();
        this.setupIntersectionObserver();
        this.setupPageTransitions();
        this.setupLoadingStates();
    }

    /**
     * Настройка CSS анимаций
     */
    setupCSSAnimations() {
        // Добавляем CSS для анимаций в head
        const style = document.createElement('style');
        style.textContent = `
            /* Анимации появления */
            .animate-fade-in {
                animation: fadeIn 0.3s ease-in-out;
            }
            
            .animate-slide-in-up {
                animation: slideInUp 0.4s ease-out;
            }
            
            .animate-slide-in-down {
                animation: slideInDown 0.4s ease-out;
            }
            
            .animate-slide-in-left {
                animation: slideInLeft 0.4s ease-out;
            }
            
            .animate-slide-in-right {
                animation: slideInRight 0.4s ease-out;
            }
            
            .animate-scale-in {
                animation: scaleIn 0.3s ease-out;
            }
            
            .animate-bounce-in {
                animation: bounceIn 0.6s ease-out;
            }
            
            /* Анимации исчезновения */
            .animate-fade-out {
                animation: fadeOut 0.3s ease-in-out forwards;
            }
            
            .animate-slide-out-up {
                animation: slideOutUp 0.4s ease-in forwards;
            }
            
            .animate-slide-out-down {
                animation: slideOutDown 0.4s ease-in forwards;
            }
            
            .animate-scale-out {
                animation: scaleOut 0.3s ease-in forwards;
            }
            
            /* Hover анимации */
            .animate-hover-lift {
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            .animate-hover-lift:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            
            .animate-hover-scale {
                transition: transform 0.2s ease;
            }
            
            .animate-hover-scale:hover {
                transform: scale(1.05);
            }
            
            .animate-hover-rotate {
                transition: transform 0.3s ease;
            }
            
            .animate-hover-rotate:hover {
                transform: rotate(5deg);
            }
            
            /* Loading анимации */
            .animate-spin {
                animation: spin 1s linear infinite;
            }
            
            .animate-pulse {
                animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }
            
            .animate-bounce {
                animation: bounce 1s infinite;
            }
            
            .animate-ping {
                animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
            }
            
            /* Skeleton loading */
            .skeleton {
                background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                background-size: 200% 100%;
                animation: skeleton-loading 1.5s infinite;
            }
            
            /* Keyframes */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            
            @keyframes slideInUp {
                from {
                    transform: translateY(20px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideInDown {
                from {
                    transform: translateY(-20px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideInLeft {
                from {
                    transform: translateX(-20px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(20px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutUp {
                from {
                    transform: translateY(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(-20px);
                    opacity: 0;
                }
            }
            
            @keyframes slideOutDown {
                from {
                    transform: translateY(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(20px);
                    opacity: 0;
                }
            }
            
            @keyframes scaleIn {
                from {
                    transform: scale(0.9);
                    opacity: 0;
                }
                to {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            @keyframes scaleOut {
                from {
                    transform: scale(1);
                    opacity: 1;
                }
                to {
                    transform: scale(0.9);
                    opacity: 0;
                }
            }
            
            @keyframes bounceIn {
                0% {
                    transform: scale(0.3);
                    opacity: 0;
                }
                50% {
                    transform: scale(1.05);
                }
                70% {
                    transform: scale(0.9);
                }
                100% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes pulse {
                0%, 100% {
                    opacity: 1;
                }
                50% {
                    opacity: 0.5;
                }
            }
            
            @keyframes bounce {
                0%, 100% {
                    transform: translateY(-25%);
                    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
                }
                50% {
                    transform: translateY(0);
                    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
                }
            }
            
            @keyframes ping {
                75%, 100% {
                    transform: scale(2);
                    opacity: 0;
                }
            }
            
            @keyframes skeleton-loading {
                0% {
                    background-position: -200% 0;
                }
                100% {
                    background-position: 200% 0;
                }
            }
            
            /* Улучшенные переходы */
            .transition-all {
                transition: all 0.3s ease;
            }
            
            .transition-colors {
                transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
            }
            
            .transition-transform {
                transition: transform 0.2s ease;
            }
            
            .transition-opacity {
                transition: opacity 0.2s ease;
            }
            
            /* Focus состояния */
            .focus-ring {
                outline: 2px solid transparent;
                outline-offset: 2px;
            }
            
            .focus-ring:focus {
                outline: 2px solid #3b82f6;
                outline-offset: 2px;
            }
            
            /* Disabled состояния */
            .disabled {
                opacity: 0.6;
                cursor: not-allowed;
                pointer-events: none;
            }
        `;

        document.head.appendChild(style);
    }

    /**
     * Настройка Intersection Observer для анимаций при скролле
     */
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateOnScroll(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Наблюдаем за элементами с классом animate-on-scroll
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });
        });
    }

    /**
     * Настройка переходов между страницами
     */
    setupPageTransitions() {
        // Переходы между модулями
        document.addEventListener('click', (e) => {
            const link = e.target.closest('[data-page]');
            if (link) {
                e.preventDefault();
                this.transitionToPage(link.dataset.page);
            }
        });
    }

    /**
     * Настройка состояний загрузки
     */
    setupLoadingStates() {
        // Глобальные индикаторы загрузки
        this.createGlobalLoadingIndicator();
    }

    /**
     * Создание глобального индикатора загрузки
     */
    createGlobalLoadingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'global-loading-indicator';
        indicator.className = 'global-loading-indicator';
        indicator.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <span class="loading-text">Загрузка...</span>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            .global-loading-indicator {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(2px);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            }
            
            .global-loading-indicator.show {
                display: flex;
            }
            
            .loading-spinner {
                text-align: center;
            }
            
            .spinner {
                width: 40px;
                height: 40px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3b82f6;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 16px;
            }
            
            .loading-text {
                color: #6b7280;
                font-size: 14px;
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(indicator);
    }

    /**
     * Анимация элемента при появлении в viewport
     */
    animateOnScroll(element) {
        const animationType = element.dataset.animation || 'fadeIn';
        const delay = parseInt(element.dataset.delay) || 0;

        setTimeout(() => {
            element.classList.add(`animate-${animationType}`);
            element.classList.remove('animate-on-scroll');
        }, delay);
    }

    /**
     * Переход между страницами
     */
    transitionToPage(pageName) {
        const currentPage = document.querySelector('.page.active');
        const targetPage = document.getElementById(`${pageName}-page`);

        if (!targetPage || currentPage === targetPage) return;

        // Анимация исчезновения текущей страницы
        if (currentPage) {
            currentPage.classList.add('animate-fade-out');

            setTimeout(() => {
                currentPage.classList.remove('active', 'animate-fade-out');

                // Анимация появления новой страницы
                targetPage.classList.add('active', 'animate-fade-in');

                setTimeout(() => {
                    targetPage.classList.remove('animate-fade-in');
                }, 300);
            }, 300);
        } else {
            targetPage.classList.add('active', 'animate-fade-in');
            setTimeout(() => {
                targetPage.classList.remove('animate-fade-in');
            }, 300);
        }
    }

    /**
     * Анимация элемента
     */
    animate(element, animationType, options = {}) {
        const {
            duration = 300,
            delay = 0,
            callback = null
        } = options;

        return new Promise((resolve) => {
            setTimeout(() => {
                element.classList.add(`animate-${animationType}`);

                setTimeout(() => {
                    element.classList.remove(`animate-${animationType}`);
                    if (callback) callback();
                    resolve();
                }, duration);
            }, delay);
        });
    }

    /**
     * Показать индикатор загрузки
     */
    showLoading(identifier = 'global') {
        if (identifier === 'global') {
            const indicator = document.getElementById('global-loading-indicator');
            if (indicator) {
                indicator.classList.add('show');
            }
        } else {
            this.loadingStates.add(identifier);
            this.updateLoadingStates();
        }
    }

    /**
     * Скрыть индикатор загрузки
     */
    hideLoading(identifier = 'global') {
        if (identifier === 'global') {
            const indicator = document.getElementById('global-loading-indicator');
            if (indicator) {
                indicator.classList.remove('show');
            }
        } else {
            this.loadingStates.delete(identifier);
            this.updateLoadingStates();
        }
    }

    /**
     * Обновление состояний загрузки
     */
    updateLoadingStates() {
        // Обновляем элементы с data-loading атрибутами
        document.querySelectorAll('[data-loading]').forEach(el => {
            const loadingId = el.dataset.loading;
            if (this.loadingStates.has(loadingId)) {
                el.classList.add('loading');
            } else {
                el.classList.remove('loading');
            }
        });
    }

    /**
     * Создание skeleton loader
     */
    createSkeleton(type = 'card', count = 1) {
        const skeletons = [];

        for (let i = 0; i < count; i++) {
            const skeleton = document.createElement('div');
            skeleton.className = `skeleton skeleton-${type}`;

            switch (type) {
                case 'card':
                    skeleton.innerHTML = `
                        <div class="skeleton-header"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                        </div>
                    `;
                    break;
                case 'list':
                    skeleton.innerHTML = `
                        <div class="skeleton-line"></div>
                        <div class="skeleton-line short"></div>
                    `;
                    break;
                case 'table':
                    skeleton.innerHTML = `
                        <div class="skeleton-table">
                            <div class="skeleton-row"></div>
                            <div class="skeleton-row"></div>
                            <div class="skeleton-row"></div>
                        </div>
                    `;
                    break;
            }

            skeletons.push(skeleton);
        }

        return skeletons;
    }

    /**
     * Анимация появления списка элементов
     */
    animateList(items, container, options = {}) {
        const {
            animationType = 'slideInUp',
            stagger = 100,
            delay = 0
        } = options;

        items.forEach((item, index) => {
            setTimeout(() => {
                this.animate(item, animationType, {
                    duration: 300,
                    callback: () => {
                        if (index === items.length - 1 && options.onComplete) {
                            options.onComplete();
                        }
                    }
                });
            }, delay + (index * stagger));
        });
    }

    /**
     * Анимация уведомления
     */
    animateNotification(element, type = 'success') {
        element.classList.add(`notification-${type}`, 'animate-slide-in-right');

        setTimeout(() => {
            element.classList.remove('animate-slide-in-right');
        }, 300);
    }

    /**
     * Анимация модального окна
     */
    animateModal(element, action = 'show') {
        if (action === 'show') {
            element.classList.add('animate-scale-in');
        } else {
            element.classList.add('animate-scale-out');
        }
    }

    /**
     * Анимация кнопки
     */
    animateButton(element, type = 'click') {
        switch (type) {
            case 'click':
                element.classList.add('animate-scale-out');
                setTimeout(() => {
                    element.classList.remove('animate-scale-out');
                    element.classList.add('animate-scale-in');
                    setTimeout(() => {
                        element.classList.remove('animate-scale-in');
                    }, 150);
                }, 150);
                break;
            case 'loading':
                element.classList.add('animate-pulse');
                break;
            case 'success':
                element.classList.add('animate-bounce-in');
                setTimeout(() => {
                    element.classList.remove('animate-bounce-in');
                }, 600);
                break;
        }
    }

    /**
     * Очистка анимаций
     */
    cleanup() {
        this.animations.clear();
        this.transitions.clear();
        this.loadingStates.clear();
        this.animationQueue = [];
    }
}

// Создаем глобальный экземпляр
window.AnimationManager = new AnimationManager();

// Экспорт для глобального доступа
window.Animations = {
    // Быстрые методы
    fadeIn: (element, options) => window.AnimationManager.animate(element, 'fade-in', options),
    fadeOut: (element, options) => window.AnimationManager.animate(element, 'fade-out', options),
    slideIn: (element, options) => window.AnimationManager.animate(element, 'slide-in-up', options),
    slideOut: (element, options) => window.AnimationManager.animate(element, 'slide-out-up', options),
    scaleIn: (element, options) => window.AnimationManager.animate(element, 'scale-in', options),
    scaleOut: (element, options) => window.AnimationManager.animate(element, 'scale-out', options),
    bounceIn: (element, options) => window.AnimationManager.animate(element, 'bounce-in', options),

    // Утилиты
    showLoading: (id) => window.AnimationManager.showLoading(id),
    hideLoading: (id) => window.AnimationManager.hideLoading(id),
    createSkeleton: (type, count) => window.AnimationManager.createSkeleton(type, count),
    animateList: (items, container, options) => window.AnimationManager.animateList(items, container, options),
    animateButton: (element, type) => window.AnimationManager.animateButton(element, type),
    animateModal: (element, action) => window.AnimationManager.animateModal(element, action),
    animateNotification: (element, type) => window.AnimationManager.animateNotification(element, type)
};
