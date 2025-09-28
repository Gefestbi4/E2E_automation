/**
 * Система touch жестов и мобильных взаимодействий
 * Поддерживает swipe, pinch, tap, long press, pull-to-refresh
 */

class TouchGestureManager {
    constructor() {
        this.gestures = new Map();
        this.touchState = {
            startX: 0,
            startY: 0,
            startTime: 0,
            currentX: 0,
            currentY: 0,
            touches: [],
            isTracking: false
        };

        this.config = {
            swipeThreshold: 50,
            swipeVelocity: 0.3,
            longPressDelay: 500,
            pinchThreshold: 0.1,
            pullToRefreshThreshold: 80
        };

        this.init();
    }

    /**
     * Инициализация touch жестов
     */
    init() {
        this.setupTouchEvents();
        this.setupPullToRefresh();
        this.setupSwipeNavigation();
        this.setupPinchZoom();
    }

    /**
     * Настройка touch событий
     */
    setupTouchEvents() {
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
        document.addEventListener('touchcancel', this.handleTouchCancel.bind(this), { passive: false });
    }

    /**
     * Обработка начала touch
     */
    handleTouchStart(event) {
        const touch = event.touches[0];
        this.touchState.startX = touch.clientX;
        this.touchState.startY = touch.clientY;
        this.touchState.startTime = Date.now();
        this.touchState.currentX = touch.clientX;
        this.touchState.currentY = touch.clientY;
        this.touchState.touches = Array.from(event.touches);
        this.touchState.isTracking = true;

        // Long press detection
        this.scheduleLongPress(event);
    }

    /**
     * Обработка движения touch
     */
    handleTouchMove(event) {
        if (!this.touchState.isTracking) return;

        const touch = event.touches[0];
        this.touchState.currentX = touch.clientX;
        this.touchState.currentY = touch.clientY;
        this.touchState.touches = Array.from(event.touches);

        // Отменяем long press если есть движение
        this.cancelLongPress();

        // Обрабатываем pull-to-refresh
        this.handlePullToRefresh(event);

        // Обрабатываем pinch zoom
        if (event.touches.length === 2) {
            this.handlePinchZoom(event);
        }
    }

    /**
     * Обработка окончания touch
     */
    handleTouchEnd(event) {
        if (!this.touchState.isTracking) return;

        const deltaX = this.touchState.currentX - this.touchState.startX;
        const deltaY = this.touchState.currentY - this.touchState.startY;
        const deltaTime = Date.now() - this.touchState.startTime;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        const velocity = distance / deltaTime;

        // Отменяем long press
        this.cancelLongPress();

        // Определяем тип жеста
        if (event.touches.length === 0) {
            if (distance < 10 && deltaTime < 300) {
                // Tap
                this.handleTap(event, deltaX, deltaY);
            } else if (distance > this.config.swipeThreshold && velocity > this.config.swipeVelocity) {
                // Swipe
                this.handleSwipe(event, deltaX, deltaY, velocity);
            }
        }

        this.touchState.isTracking = false;
    }

    /**
     * Обработка отмены touch
     */
    handleTouchCancel(event) {
        this.cancelLongPress();
        this.touchState.isTracking = false;
    }

    /**
     * Обработка tap
     */
    handleTap(event, deltaX, deltaY) {
        const element = document.elementFromPoint(this.touchState.currentX, this.touchState.currentY);
        if (!element) return;

        // Проверяем на double tap
        const now = Date.now();
        if (this.lastTapTime && now - this.lastTapTime < 300) {
            this.handleDoubleTap(event, element);
        } else {
            this.handleSingleTap(event, element);
        }
        this.lastTapTime = now;
    }

    /**
     * Обработка single tap
     */
    handleSingleTap(event, element) {
        const tapEvent = new CustomEvent('gesture-tap', {
            detail: { element, x: this.touchState.currentX, y: this.touchState.currentY }
        });
        element.dispatchEvent(tapEvent);

        // Если элемент кликабельный, эмулируем click
        if (element.matches('button, a, [onclick], .clickable')) {
            element.click();
        }
    }

    /**
     * Обработка double tap
     */
    handleDoubleTap(event, element) {
        const doubleTapEvent = new CustomEvent('gesture-double-tap', {
            detail: { element, x: this.touchState.currentX, y: this.touchState.currentY }
        });
        element.dispatchEvent(doubleTapEvent);
    }

    /**
     * Обработка swipe
     */
    handleSwipe(event, deltaX, deltaY, velocity) {
        const element = document.elementFromPoint(this.touchState.currentX, this.touchState.currentY);
        if (!element) return;

        const absX = Math.abs(deltaX);
        const absY = Math.abs(deltaY);
        let direction;

        if (absX > absY) {
            direction = deltaX > 0 ? 'right' : 'left';
        } else {
            direction = deltaY > 0 ? 'down' : 'up';
        }

        const swipeEvent = new CustomEvent('gesture-swipe', {
            detail: {
                element,
                direction,
                deltaX,
                deltaY,
                velocity,
                x: this.touchState.currentX,
                y: this.touchState.currentY
            }
        });
        element.dispatchEvent(swipeEvent);
    }

    /**
     * Планирование long press
     */
    scheduleLongPress(event) {
        this.longPressTimer = setTimeout(() => {
            const element = document.elementFromPoint(this.touchState.currentX, this.touchState.currentY);
            if (element && this.touchState.isTracking) {
                this.handleLongPress(event, element);
            }
        }, this.config.longPressDelay);
    }

    /**
     * Отмена long press
     */
    cancelLongPress() {
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }
    }

    /**
     * Обработка long press
     */
    handleLongPress(event, element) {
        const longPressEvent = new CustomEvent('gesture-long-press', {
            detail: { element, x: this.touchState.currentX, y: this.touchState.currentY }
        });
        element.dispatchEvent(longPressEvent);

        // Показываем контекстное меню или haptic feedback
        this.showContextMenu(element, this.touchState.currentX, this.touchState.currentY);
    }

    /**
     * Обработка pinch zoom
     */
    handlePinchZoom(event) {
        if (event.touches.length !== 2) return;

        const touch1 = event.touches[0];
        const touch2 = event.touches[1];

        const currentDistance = Math.sqrt(
            Math.pow(touch2.clientX - touch1.clientX, 2) +
            Math.pow(touch2.clientY - touch1.clientY, 2)
        );

        if (this.lastPinchDistance) {
            const scale = currentDistance / this.lastPinchDistance;
            const centerX = (touch1.clientX + touch2.clientX) / 2;
            const centerY = (touch1.clientY + touch2.clientY) / 2;

            const pinchEvent = new CustomEvent('gesture-pinch', {
                detail: { scale, centerX, centerY, distance: currentDistance }
            });
            document.dispatchEvent(pinchEvent);
        }

        this.lastPinchDistance = currentDistance;
    }

    /**
     * Настройка pull-to-refresh
     */
    setupPullToRefresh() {
        let pullStartY = 0;
        let isPulling = false;
        let pullElement = null;

        document.addEventListener('touchstart', (event) => {
            if (window.scrollY === 0) {
                pullStartY = event.touches[0].clientY;
                isPulling = true;
                pullElement = event.target;
            }
        });

        document.addEventListener('touchmove', (event) => {
            if (!isPulling) return;

            const currentY = event.touches[0].clientY;
            const pullDistance = currentY - pullStartY;

            if (pullDistance > 0) {
                event.preventDefault();

                const pullProgress = Math.min(pullDistance / this.config.pullToRefreshThreshold, 1);

                const pullEvent = new CustomEvent('gesture-pull-to-refresh', {
                    detail: { distance: pullDistance, progress: pullProgress }
                });
                document.dispatchEvent(pullEvent);
            }
        });

        document.addEventListener('touchend', (event) => {
            if (!isPulling) return;

            const currentY = event.changedTouches[0].clientY;
            const pullDistance = currentY - pullStartY;

            if (pullDistance > this.config.pullToRefreshThreshold) {
                const refreshEvent = new CustomEvent('gesture-refresh', {
                    detail: { distance: pullDistance }
                });
                document.dispatchEvent(refreshEvent);
            }

            isPulling = false;
            pullElement = null;
        });
    }

    /**
     * Настройка swipe навигации
     */
    setupSwipeNavigation() {
        document.addEventListener('gesture-swipe', (event) => {
            const { direction, element } = event.detail;

            // Swipe для навигации между страницами
            if (element.closest('.swipe-navigation')) {
                this.handleSwipeNavigation(direction);
            }

            // Swipe для закрытия модальных окон
            if (element.closest('.modal') && direction === 'down') {
                this.closeModal(element.closest('.modal'));
            }

            // Swipe для карточек
            if (element.closest('.swipeable-card')) {
                this.handleSwipeCard(element.closest('.swipeable-card'), direction);
            }
        });
    }

    /**
     * Обработка swipe навигации
     */
    handleSwipeNavigation(direction) {
        const currentPage = document.querySelector('.page.active');
        if (!currentPage) return;

        const pages = ['dashboard', 'ecommerce', 'social', 'tasks', 'content', 'analytics'];
        const currentIndex = pages.indexOf(currentPage.id.replace('-page', ''));

        let nextIndex;
        if (direction === 'left' && currentIndex < pages.length - 1) {
            nextIndex = currentIndex + 1;
        } else if (direction === 'right' && currentIndex > 0) {
            nextIndex = currentIndex - 1;
        } else {
            return;
        }

        const nextPage = document.getElementById(`${pages[nextIndex]}-page`);
        if (nextPage) {
            this.switchPage(currentPage, nextPage, direction);
        }
    }

    /**
     * Переключение страниц с анимацией
     */
    switchPage(fromPage, toPage, direction) {
        const slideDistance = window.innerWidth;
        const slideDirection = direction === 'left' ? 1 : -1;

        // Анимация исчезновения текущей страницы
        fromPage.style.transform = `translateX(${-slideDirection * slideDistance}px)`;
        fromPage.style.transition = 'transform 0.3s ease';

        // Показываем новую страницу
        toPage.classList.add('active');
        toPage.style.transform = `translateX(${slideDirection * slideDistance}px)`;
        toPage.style.transition = 'transform 0.3s ease';

        // Анимация появления новой страницы
        setTimeout(() => {
            toPage.style.transform = 'translateX(0)';
        }, 50);

        // Очистка после анимации
        setTimeout(() => {
            fromPage.classList.remove('active');
            fromPage.style.transform = '';
            fromPage.style.transition = '';
            toPage.style.transform = '';
            toPage.style.transition = '';
        }, 300);
    }

    /**
     * Обработка swipe карточек
     */
    handleSwipeCard(card, direction) {
        const cardActions = card.querySelector('.card-actions');
        if (!cardActions) return;

        if (direction === 'left') {
            // Показываем действия
            cardActions.style.transform = 'translateX(0)';
            cardActions.style.transition = 'transform 0.3s ease';
        } else if (direction === 'right') {
            // Скрываем действия
            cardActions.style.transform = 'translateX(100%)';
            cardActions.style.transition = 'transform 0.3s ease';
        }
    }

    /**
     * Закрытие модального окна
     */
    closeModal(modal) {
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.click();
        }
    }

    /**
     * Показ контекстного меню
     */
    showContextMenu(element, x, y) {
        // Создаем контекстное меню
        const contextMenu = document.createElement('div');
        contextMenu.className = 'context-menu';
        contextMenu.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            min-width: 120px;
        `;

        contextMenu.innerHTML = `
            <div class="context-menu-item" data-action="copy">Копировать</div>
            <div class="context-menu-item" data-action="share">Поделиться</div>
            <div class="context-menu-item" data-action="delete">Удалить</div>
        `;

        document.body.appendChild(contextMenu);

        // Обработка кликов по меню
        contextMenu.addEventListener('click', (e) => {
            const action = e.target.dataset.action;
            if (action) {
                this.handleContextAction(element, action);
            }
            contextMenu.remove();
        });

        // Закрытие меню при клике вне его
        setTimeout(() => {
            document.addEventListener('click', () => {
                contextMenu.remove();
            }, { once: true });
        }, 100);
    }

    /**
     * Обработка действий контекстного меню
     */
    handleContextAction(element, action) {
        const actionEvent = new CustomEvent('context-action', {
            detail: { element, action }
        });
        element.dispatchEvent(actionEvent);
    }

    /**
     * Настройка pinch zoom
     */
    setupPinchZoom() {
        document.addEventListener('gesture-pinch', (event) => {
            const { scale, centerX, centerY } = event.detail;

            // Применяем zoom к элементу под курсором
            const element = document.elementFromPoint(centerX, centerY);
            if (element && element.closest('.zoomable')) {
                this.applyZoom(element, scale);
            }
        });
    }

    /**
     * Применение zoom
     */
    applyZoom(element, scale) {
        const currentScale = parseFloat(element.style.transform.match(/scale\(([^)]+)\)/) || [0, 1])[1];
        const newScale = Math.max(0.5, Math.min(3, currentScale * scale));

        element.style.transform = `scale(${newScale})`;
        element.style.transformOrigin = 'center';
    }

    /**
     * Регистрация жеста
     */
    registerGesture(element, gesture, handler) {
        if (!this.gestures.has(element)) {
            this.gestures.set(element, new Map());
        }
        this.gestures.get(element).set(gesture, handler);
    }

    /**
     * Отмена регистрации жеста
     */
    unregisterGesture(element, gesture) {
        if (this.gestures.has(element)) {
            this.gestures.get(element).delete(gesture);
        }
    }

    /**
     * Очистка
     */
    cleanup() {
        document.removeEventListener('touchstart', this.handleTouchStart);
        document.removeEventListener('touchmove', this.handleTouchMove);
        document.removeEventListener('touchend', this.handleTouchEnd);
        document.removeEventListener('touchcancel', this.handleTouchCancel);

        this.gestures.clear();
        this.cancelLongPress();
    }
}

// Создаем глобальный экземпляр
window.TouchGestureManager = new TouchGestureManager();

// Экспорт для глобального доступа
window.TouchGestures = {
    register: (element, gesture, handler) => window.TouchGestureManager.registerGesture(element, gesture, handler),
    unregister: (element, gesture) => window.TouchGestureManager.unregisterGesture(element, gesture),

    // Быстрые методы
    enableSwipeNavigation: (element) => {
        element.classList.add('swipe-navigation');
    },
    enableSwipeCard: (element) => {
        element.classList.add('swipeable-card');
    },
    enableZoom: (element) => {
        element.classList.add('zoomable');
    }
};
