/**
 * Система оптимизации производительности фронтенда
 */

class PerformanceOptimizer {
    constructor() {
        this.metrics = {
            pageLoadTime: 0,
            domContentLoaded: 0,
            firstContentfulPaint: 0,
            largestContentfulPaint: 0,
            firstInputDelay: 0,
            cumulativeLayoutShift: 0,
            memoryUsage: 0,
            networkRequests: 0,
            cacheHits: 0,
            cacheMisses: 0
        };

        this.observers = {
            performance: null,
            intersection: null,
            resize: null
        };

        this.isInitialized = false;
        this.debounceTimers = new Map();
        this.throttleTimers = new Map();

        // Настройки оптимизации
        this.config = {
            lazyLoadThreshold: 0.1,
            debounceDelay: 300,
            throttleDelay: 100,
            maxConcurrentRequests: 5,
            cacheSize: 100,
            enableVirtualScrolling: true,
            enableImageOptimization: true,
            enableCodeSplitting: true
        };
    }

    /**
     * Инициализация системы оптимизации
     */
    async init() {
        console.log('⚡ Initializing Performance Optimizer...');

        try {
            // Инициализируем метрики производительности
            this.initPerformanceMetrics();

            // Инициализируем ленивую загрузку
            this.initLazyLoading();

            // Инициализируем виртуальный скроллинг
            this.initVirtualScrolling();

            // Инициализируем оптимизацию изображений
            this.initImageOptimization();

            // Инициализируем кэширование
            this.initCaching();

            // Инициализируем мониторинг
            this.initMonitoring();

            this.isInitialized = true;
            console.log('⚡ Performance Optimizer initialized successfully');

        } catch (error) {
            console.error('⚡ Failed to initialize Performance Optimizer:', error);
        }
    }

    /**
     * Инициализация метрик производительности
     */
    initPerformanceMetrics() {
        // Измеряем время загрузки страницы
        window.addEventListener('load', () => {
            this.metrics.pageLoadTime = performance.now();
            this.trackMetric('pageLoadTime', this.metrics.pageLoadTime);
        });

        // Измеряем DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {
            this.metrics.domContentLoaded = performance.now();
            this.trackMetric('domContentLoaded', this.metrics.domContentLoaded);
        });

        // Измеряем Core Web Vitals
        this.measureCoreWebVitals();

        // Измеряем использование памяти
        this.measureMemoryUsage();
    }

    /**
     * Измерение Core Web Vitals
     */
    measureCoreWebVitals() {
        // First Contentful Paint
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.name === 'first-contentful-paint') {
                        this.metrics.firstContentfulPaint = entry.startTime;
                        this.trackMetric('firstContentfulPaint', entry.startTime);
                    }
                }
            });
            observer.observe({ entryTypes: ['paint'] });
        }

        // Largest Contentful Paint
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.metrics.largestContentfulPaint = lastEntry.startTime;
                this.trackMetric('largestContentfulPaint', lastEntry.startTime);
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }

        // First Input Delay
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    this.metrics.firstInputDelay = entry.processingStart - entry.startTime;
                    this.trackMetric('firstInputDelay', this.metrics.firstInputDelay);
                }
            });
            observer.observe({ entryTypes: ['first-input'] });
        }

        // Cumulative Layout Shift
        if ('PerformanceObserver' in window) {
            let clsValue = 0;
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                }
                this.metrics.cumulativeLayoutShift = clsValue;
                this.trackMetric('cumulativeLayoutShift', clsValue);
            });
            observer.observe({ entryTypes: ['layout-shift'] });
        }
    }

    /**
     * Измерение использования памяти
     */
    measureMemoryUsage() {
        if ('memory' in performance) {
            setInterval(() => {
                this.metrics.memoryUsage = performance.memory.usedJSHeapSize / 1024 / 1024; // MB
                this.trackMetric('memoryUsage', this.metrics.memoryUsage);
            }, 5000);
        }
    }

    /**
     * Инициализация ленивой загрузки
     */
    initLazyLoading() {
        if ('IntersectionObserver' in window) {
            this.observers.intersection = new IntersectionObserver(
                (entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            this.loadLazyElement(entry.target);
                            this.observers.intersection.unobserve(entry.target);
                        }
                    });
                },
                { threshold: this.config.lazyLoadThreshold }
            );

            // Находим все элементы для ленивой загрузки
            document.querySelectorAll('[data-lazy]').forEach(element => {
                this.observers.intersection.observe(element);
            });
        }
    }

    /**
     * Загрузка ленивого элемента
     */
    loadLazyElement(element) {
        const src = element.dataset.lazy;
        if (src) {
            if (element.tagName === 'IMG') {
                element.src = src;
                element.classList.add('loaded');
            } else if (element.tagName === 'IFRAME') {
                element.src = src;
            }

            // Удаляем атрибут data-lazy
            element.removeAttribute('data-lazy');
        }
    }

    /**
     * Инициализация виртуального скроллинга
     */
    initVirtualScrolling() {
        if (!this.config.enableVirtualScrolling) return;

        // Находим контейнеры для виртуального скроллинга
        document.querySelectorAll('[data-virtual-scroll]').forEach(container => {
            this.setupVirtualScrolling(container);
        });
    }

    /**
     * Настройка виртуального скроллинга для контейнера
     */
    setupVirtualScrolling(container) {
        const itemHeight = parseInt(container.dataset.itemHeight) || 50;
        const visibleItems = Math.ceil(container.clientHeight / itemHeight) + 2;
        let scrollTop = 0;
        let totalItems = 0;

        // Создаем виртуальный контейнер
        const virtualContainer = document.createElement('div');
        virtualContainer.style.height = '100%';
        virtualContainer.style.overflow = 'auto';
        virtualContainer.style.position = 'relative';

        // Создаем видимую область
        const visibleArea = document.createElement('div');
        visibleArea.style.position = 'absolute';
        visibleArea.style.top = '0';
        visibleArea.style.left = '0';
        visibleArea.style.right = '0';

        virtualContainer.appendChild(visibleArea);
        container.appendChild(virtualContainer);

        // Обработчик скролла
        virtualContainer.addEventListener('scroll', this.throttle(() => {
            scrollTop = virtualContainer.scrollTop;
            this.updateVirtualItems(visibleArea, scrollTop, itemHeight, visibleItems, totalItems);
        }, this.config.throttleDelay));

        // Функция обновления видимых элементов
        this.updateVirtualItems = (area, scrollTop, itemHeight, visibleItems, totalItems) => {
            const startIndex = Math.floor(scrollTop / itemHeight);
            const endIndex = Math.min(startIndex + visibleItems, totalItems);

            // Очищаем область
            area.innerHTML = '';

            // Создаем видимые элементы
            for (let i = startIndex; i < endIndex; i++) {
                const item = document.createElement('div');
                item.style.height = `${itemHeight}px`;
                item.style.position = 'absolute';
                item.style.top = `${i * itemHeight}px`;
                item.style.left = '0';
                item.style.right = '0';
                item.textContent = `Item ${i + 1}`;
                area.appendChild(item);
            }

            // Обновляем высоту области
            area.style.height = `${totalItems * itemHeight}px`;
        };
    }

    /**
     * Инициализация оптимизации изображений
     */
    initImageOptimization() {
        if (!this.config.enableImageOptimization) return;

        // Находим все изображения
        document.querySelectorAll('img').forEach(img => {
            this.optimizeImage(img);
        });

        // Обработчик для новых изображений
        const imageObserver = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.tagName === 'IMG') {
                        this.optimizeImage(node);
                    }
                });
            });
        });

        imageObserver.observe(document.body, { childList: true, subtree: true });
    }

    /**
     * Оптимизация изображения
     */
    optimizeImage(img) {
        // Добавляем ленивую загрузку
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }

        // Добавляем атрибуты для оптимизации
        if (!img.hasAttribute('decoding')) {
            img.setAttribute('decoding', 'async');
        }

        // Обработчик загрузки
        img.addEventListener('load', () => {
            img.classList.add('loaded');
        });

        // Обработчик ошибки
        img.addEventListener('error', () => {
            img.classList.add('error');
            // Можно добавить placeholder изображение
        });
    }

    /**
     * Инициализация кэширования
     */
    initCaching() {
        this.cache = new Map();
        this.cacheOrder = [];
    }

    /**
     * Кэширование данных
     */
    cacheData(key, data, ttl = 300000) { // 5 минут по умолчанию
        const cacheItem = {
            data: data,
            timestamp: Date.now(),
            ttl: ttl
        };

        // Удаляем старые элементы если кэш переполнен
        if (this.cache.size >= this.config.cacheSize) {
            const oldestKey = this.cacheOrder.shift();
            this.cache.delete(oldestKey);
        }

        this.cache.set(key, cacheItem);
        this.cacheOrder.push(key);
    }

    /**
     * Получение данных из кэша
     */
    getCachedData(key) {
        const cacheItem = this.cache.get(key);

        if (!cacheItem) {
            this.metrics.cacheMisses++;
            return null;
        }

        // Проверяем срок действия
        if (Date.now() - cacheItem.timestamp > cacheItem.ttl) {
            this.cache.delete(key);
            this.metrics.cacheMisses++;
            return null;
        }

        this.metrics.cacheHits++;
        return cacheItem.data;
    }

    /**
     * Инициализация мониторинга
     */
    initMonitoring() {
        // Мониторинг сетевых запросов
        this.monitorNetworkRequests();

        // Мониторинг производительности
        this.monitorPerformance();

        // Мониторинг ошибок
        this.monitorErrors();
    }

    /**
     * Мониторинг сетевых запросов
     */
    monitorNetworkRequests() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = async function (...args) {
            self.metrics.networkRequests++;
            const startTime = performance.now();

            try {
                const response = await originalFetch.apply(this, args);
                const endTime = performance.now();

                // Логируем медленные запросы
                if (endTime - startTime > 1000) {
                    console.warn(`Slow network request: ${args[0]} took ${endTime - startTime}ms`);
                }

                return response;
            } catch (error) {
                console.error('Network request failed:', error);
                throw error;
            }
        };
    }

    /**
     * Мониторинг производительности
     */
    monitorPerformance() {
        setInterval(() => {
            this.collectPerformanceMetrics();
        }, 10000); // Каждые 10 секунд
    }

    /**
     * Сбор метрик производительности
     */
    collectPerformanceMetrics() {
        const metrics = {
            timestamp: Date.now(),
            memoryUsage: this.metrics.memoryUsage,
            networkRequests: this.metrics.networkRequests,
            cacheHitRate: this.calculateCacheHitRate(),
            performanceScore: this.calculatePerformanceScore()
        };

        // Отправляем метрики на сервер (если нужно)
        this.sendMetricsToServer(metrics);
    }

    /**
     * Мониторинг ошибок
     */
    monitorErrors() {
        window.addEventListener('error', (event) => {
            this.trackError('JavaScript Error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                stack: event.error?.stack
            });
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.trackError('Unhandled Promise Rejection', {
                reason: event.reason,
                stack: event.reason?.stack
            });
        });
    }

    /**
     * Дебаунс функция
     */
    debounce(func, delay = this.config.debounceDelay) {
        return (...args) => {
            const key = func.name || 'anonymous';
            clearTimeout(this.debounceTimers.get(key));
            this.debounceTimers.set(key, setTimeout(() => func.apply(this, args), delay));
        };
    }

    /**
     * Троттлинг функция
     */
    throttle(func, delay = this.config.throttleDelay) {
        return (...args) => {
            const key = func.name || 'anonymous';
            if (!this.throttleTimers.has(key)) {
                func.apply(this, args);
                this.throttleTimers.set(key, setTimeout(() => {
                    this.throttleTimers.delete(key);
                }, delay));
            }
        };
    }

    /**
     * Отслеживание метрики
     */
    trackMetric(name, value) {
        console.log(`📊 Metric: ${name} = ${value}`);

        // Можно отправить на сервер аналитики
        if (window.gtag) {
            gtag('event', 'performance_metric', {
                metric_name: name,
                metric_value: value
            });
        }
    }

    /**
     * Отслеживание ошибки
     */
    trackError(type, details) {
        console.error(`🚨 Error: ${type}`, details);

        // Можно отправить на сервер мониторинга
        if (window.ErrorHandler) {
            window.ErrorHandler.handleError(new Error(type), details);
        }
    }

    /**
     * Отправка метрик на сервер
     */
    async sendMetricsToServer(metrics) {
        try {
            await window.ApiService.post('/api/performance/metrics', metrics);
        } catch (error) {
            console.error('Failed to send metrics to server:', error);
        }
    }

    /**
     * Расчет процента попаданий в кэш
     */
    calculateCacheHitRate() {
        const total = this.metrics.cacheHits + this.metrics.cacheMisses;
        return total > 0 ? (this.metrics.cacheHits / total * 100).toFixed(2) : 0;
    }

    /**
     * Расчет оценки производительности
     */
    calculatePerformanceScore() {
        let score = 100;

        // Штрафы за медленную загрузку
        if (this.metrics.pageLoadTime > 3000) score -= 20;
        else if (this.metrics.pageLoadTime > 2000) score -= 10;

        // Штрафы за медленный FCP
        if (this.metrics.firstContentfulPaint > 1800) score -= 15;
        else if (this.metrics.firstContentfulPaint > 1200) score -= 8;

        // Штрафы за медленный LCP
        if (this.metrics.largestContentfulPaint > 2500) score -= 15;
        else if (this.metrics.largestContentfulPaint > 1800) score -= 8;

        // Штрафы за высокий CLS
        if (this.metrics.cumulativeLayoutShift > 0.25) score -= 20;
        else if (this.metrics.cumulativeLayoutShift > 0.1) score -= 10;

        // Штрафы за высокое использование памяти
        if (this.metrics.memoryUsage > 100) score -= 10;
        else if (this.metrics.memoryUsage > 50) score -= 5;

        return Math.max(0, Math.min(100, score));
    }

    /**
     * Получение отчета о производительности
     */
    getPerformanceReport() {
        return {
            metrics: this.metrics,
            cacheHitRate: this.calculateCacheHitRate(),
            performanceScore: this.calculatePerformanceScore(),
            recommendations: this.getPerformanceRecommendations()
        };
    }

    /**
     * Получение рекомендаций по производительности
     */
    getPerformanceRecommendations() {
        const recommendations = [];

        if (this.metrics.pageLoadTime > 3000) {
            recommendations.push('Consider implementing code splitting and lazy loading');
        }

        if (this.metrics.firstContentfulPaint > 1800) {
            recommendations.push('Optimize critical rendering path and reduce render-blocking resources');
        }

        if (this.metrics.largestContentfulPaint > 2500) {
            recommendations.push('Optimize images and largest content elements');
        }

        if (this.metrics.cumulativeLayoutShift > 0.1) {
            recommendations.push('Fix layout shifts by reserving space for dynamic content');
        }

        if (this.metrics.memoryUsage > 50) {
            recommendations.push('Implement memory management and cleanup unused objects');
        }

        if (this.calculateCacheHitRate() < 50) {
            recommendations.push('Improve caching strategy for better performance');
        }

        return recommendations;
    }

    /**
     * Очистка ресурсов
     */
    destroy() {
        // Очищаем наблюдатели
        Object.values(this.observers).forEach(observer => {
            if (observer) observer.disconnect();
        });

        // Очищаем таймеры
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.throttleTimers.forEach(timer => clearTimeout(timer));

        // Очищаем кэш
        this.cache.clear();

        this.isInitialized = false;
    }
}

// Создаем глобальный экземпляр
window.performanceOptimizer = new PerformanceOptimizer();
