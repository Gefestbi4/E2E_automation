/**
 * Performance optimization utilities
 * Provides lazy loading, caching, debouncing, and rendering optimization
 */

class PerformanceManager {
    constructor() {
        this.cache = new Map();
        this.observers = new Map();
        this.debounceTimers = new Map();
        this.throttleTimers = new Map();
        this.lazyImages = new Set();
        this.virtualScroll = new Map();
        this.init();
    }

    /**
     * Initialize performance features
     */
    init() {
        this.setupLazyLoading();
        this.setupVirtualScrolling();
        this.setupImageOptimization();
        this.setupCaching();
        this.setupDebouncing();
        this.setupThrottling();
        this.setupMemoryManagement();
        console.log('⚡ Performance manager initialized');
    }

    /**
     * Setup lazy loading for images and content
     */
    setupLazyLoading() {
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            this.imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadLazyImage(entry.target);
                        this.imageObserver.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            // Observe all lazy images
            document.querySelectorAll('img[data-src]').forEach(img => {
                this.imageObserver.observe(img);
            });
        }
    }

    /**
     * Load lazy image
     */
    loadLazyImage(img) {
        const src = img.getAttribute('data-src');
        if (src) {
            img.src = src;
            img.removeAttribute('data-src');
            img.classList.add('loaded');

            // Add loading animation
            img.addEventListener('load', () => {
                img.classList.add('fade-in');
            });
        }
    }

    /**
     * Setup virtual scrolling for large lists
     */
    setupVirtualScrolling() {
        this.virtualScrollContainers = new Map();
    }

    /**
     * Create virtual scroll container
     */
    createVirtualScroll(container, items, itemHeight, renderItem) {
        const containerId = container.id || `virtual-${Date.now()}`;
        const virtualContainer = {
            container,
            items,
            itemHeight,
            renderItem,
            visibleStart: 0,
            visibleEnd: 0,
            scrollTop: 0,
            containerHeight: container.clientHeight,
            totalHeight: items.length * itemHeight
        };

        this.virtualScrollContainers.set(containerId, virtualContainer);
        this.updateVirtualScroll(containerId);

        // Add scroll listener
        container.addEventListener('scroll', () => {
            this.throttle(`virtual-scroll-${containerId}`, () => {
                this.updateVirtualScroll(containerId);
            }, 16); // 60fps
        });

        return containerId;
    }

    /**
     * Update virtual scroll
     */
    updateVirtualScroll(containerId) {
        const virtual = this.virtualScrollContainers.get(containerId);
        if (!virtual) return;

        const { container, items, itemHeight, renderItem, containerHeight } = virtual;
        const scrollTop = container.scrollTop;

        const visibleStart = Math.floor(scrollTop / itemHeight);
        const visibleEnd = Math.min(visibleStart + Math.ceil(containerHeight / itemHeight) + 1, items.length);

        virtual.visibleStart = visibleStart;
        virtual.visibleEnd = visibleEnd;
        virtual.scrollTop = scrollTop;

        // Render visible items
        this.renderVirtualItems(virtual);
    }

    /**
     * Render virtual items
     */
    renderVirtualItems(virtual) {
        const { container, items, itemHeight, renderItem, visibleStart, visibleEnd } = virtual;

        // Clear container
        container.innerHTML = '';

        // Add spacer for items before visible area
        if (visibleStart > 0) {
            const spacer = document.createElement('div');
            spacer.style.height = `${visibleStart * itemHeight}px`;
            container.appendChild(spacer);
        }

        // Render visible items
        for (let i = visibleStart; i < visibleEnd; i++) {
            const item = renderItem(items[i], i);
            container.appendChild(item);
        }

        // Add spacer for items after visible area
        if (visibleEnd < items.length) {
            const spacer = document.createElement('div');
            spacer.style.height = `${(items.length - visibleEnd) * itemHeight}px`;
            container.appendChild(spacer);
        }
    }

    /**
     * Setup image optimization
     */
    setupImageOptimization() {
        // WebP support detection
        this.supportsWebP = this.detectWebPSupport();

        // Image compression
        this.setupImageCompression();
    }

    /**
     * Detect WebP support
     */
    detectWebPSupport() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    /**
     * Optimize image URL
     */
    optimizeImageUrl(url, width, height, quality = 80) {
        if (!url) return url;

        // If it's a placeholder, return as is
        if (url.includes('placeholder.com') || url.includes('via.placeholder.com')) {
            return url;
        }

        // Add WebP support if available
        if (this.supportsWebP && !url.includes('.webp')) {
            const extension = url.split('.').pop();
            url = url.replace(`.${extension}`, '.webp');
        }

        // Add size parameters if provided
        if (width || height) {
            const params = new URLSearchParams();
            if (width) params.set('w', width);
            if (height) params.set('h', height);
            if (quality) params.set('q', quality);

            const separator = url.includes('?') ? '&' : '?';
            url += `${separator}${params.toString()}`;
        }

        return url;
    }

    /**
     * Setup image compression
     */
    setupImageCompression() {
        // Canvas-based image compression
        this.compressImage = (file, maxWidth = 800, maxHeight = 600, quality = 0.8) => {
            return new Promise((resolve) => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();

                img.onload = () => {
                    // Calculate new dimensions
                    let { width, height } = img;
                    if (width > maxWidth || height > maxHeight) {
                        const ratio = Math.min(maxWidth / width, maxHeight / height);
                        width *= ratio;
                        height *= ratio;
                    }

                    canvas.width = width;
                    canvas.height = height;

                    // Draw and compress
                    ctx.drawImage(img, 0, 0, width, height);
                    canvas.toBlob(resolve, 'image/jpeg', quality);
                };

                img.src = URL.createObjectURL(file);
            });
        };
    }

    /**
     * Setup caching system
     */
    setupCaching() {
        // Memory cache
        this.cache = new Map();

        // Local storage cache
        this.storageCache = {
            set: (key, value, ttl = 3600000) => { // 1 hour default
                const item = {
                    value,
                    expiry: Date.now() + ttl
                };
                localStorage.setItem(`cache_${key}`, JSON.stringify(item));
            },

            get: (key) => {
                const item = localStorage.getItem(`cache_${key}`);
                if (!item) return null;

                const parsed = JSON.parse(item);
                if (Date.now() > parsed.expiry) {
                    localStorage.removeItem(`cache_${key}`);
                    return null;
                }

                return parsed.value;
            },

            remove: (key) => {
                localStorage.removeItem(`cache_${key}`);
            },

            clear: () => {
                Object.keys(localStorage).forEach(key => {
                    if (key.startsWith('cache_')) {
                        localStorage.removeItem(key);
                    }
                });
            }
        };
    }

    /**
     * Cache data
     */
    cacheData(key, data, ttl = 3600000) {
        this.cache.set(key, {
            data,
            expiry: Date.now() + ttl
        });
    }

    /**
     * Get cached data
     */
    getCachedData(key) {
        const cached = this.cache.get(key);
        if (!cached) return null;

        if (Date.now() > cached.expiry) {
            this.cache.delete(key);
            return null;
        }

        return cached.data;
    }

    /**
     * Setup debouncing
     */
    setupDebouncing() {
        this.debounceTimers = new Map();
    }

    /**
     * Debounce function
     */
    debounce(key, func, delay = 300) {
        if (this.debounceTimers.has(key)) {
            clearTimeout(this.debounceTimers.get(key));
        }

        const timer = setTimeout(() => {
            func();
            this.debounceTimers.delete(key);
        }, delay);

        this.debounceTimers.set(key, timer);
    }

    /**
     * Setup throttling
     */
    setupThrottling() {
        this.throttleTimers = new Map();
    }

    /**
     * Throttle function
     */
    throttle(key, func, delay = 100) {
        if (this.throttleTimers.has(key)) {
            return;
        }

        func();

        const timer = setTimeout(() => {
            this.throttleTimers.delete(key);
        }, delay);

        this.throttleTimers.set(key, timer);
    }

    /**
     * Setup memory management
     */
    setupMemoryManagement() {
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });

        // Periodic cleanup
        setInterval(() => {
            this.cleanup();
        }, 300000); // 5 minutes
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        // Clear expired cache
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now > value.expiry) {
                this.cache.delete(key);
            }
        }

        // Clear timers
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();

        this.throttleTimers.forEach(timer => clearTimeout(timer));
        this.throttleTimers.clear();

        // Clear observers
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
    }

    /**
     * Optimize DOM operations
     */
    batchDOMUpdates(updates) {
        // Use DocumentFragment for batch updates
        const fragment = document.createDocumentFragment();

        updates.forEach(update => {
            if (typeof update === 'function') {
                update(fragment);
            }
        });

        return fragment;
    }

    /**
     * Optimize rendering with requestAnimationFrame
     */
    scheduleRender(callback) {
        if (this.renderScheduled) return;

        this.renderScheduled = true;
        requestAnimationFrame(() => {
            callback();
            this.renderScheduled = false;
        });
    }

    /**
     * Preload critical resources
     */
    preloadResource(url, type = 'image') {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = url;
        link.as = type;
        document.head.appendChild(link);
    }

    /**
     * Prefetch resources
     */
    prefetchResource(url) {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        document.head.appendChild(link);
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');

        return {
            // Page load metrics
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
            firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
            firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,

            // Memory usage
            memory: performance.memory ? {
                used: performance.memory.usedJSHeapSize,
                total: performance.memory.totalJSHeapSize,
                limit: performance.memory.jsHeapSizeLimit
            } : null,

            // Cache stats
            cacheSize: this.cache.size,
            cacheHitRate: this.calculateCacheHitRate()
        };
    }

    /**
     * Calculate cache hit rate
     */
    calculateCacheHitRate() {
        // This would need to be implemented with hit/miss tracking
        return 0;
    }

    /**
     * Optimize images in container
     */
    optimizeImagesInContainer(container) {
        const images = container.querySelectorAll('img');
        images.forEach(img => {
            if (img.src && !img.src.includes('placeholder.com')) {
                const optimizedSrc = this.optimizeImageUrl(img.src, img.width, img.height);
                if (optimizedSrc !== img.src) {
                    img.src = optimizedSrc;
                }
            }
        });
    }

    /**
     * Lazy load content
     */
    lazyLoadContent(container, loadFunction) {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        loadFunction(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            });

            observer.observe(container);
            this.observers.set(container, observer);
        } else {
            // Fallback for older browsers
            loadFunction(container);
        }
    }
}

// Export for global access
window.PerformanceManager = PerformanceManager;
console.log('⚡ Performance utilities loaded');
