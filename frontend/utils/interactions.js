/**
 * Система интерактивных элементов
 * Поддерживает hover эффекты, focus состояния, feedback, жесты
 */

class InteractionManager {
    constructor() {
        this.hoverElements = new Set();
        this.focusElements = new Set();
        this.clickElements = new Set();
        this.gestureElements = new Set();

        this.init();
    }

    /**
     * Инициализация системы взаимодействий
     */
    init() {
        this.setupHoverEffects();
        this.setupFocusStates();
        this.setupClickEffects();
        this.setupGestureSupport();
        this.setupKeyboardNavigation();
    }

    /**
     * Настройка hover эффектов
     */
    setupHoverEffects() {
        // Автоматические hover эффекты для элементов с классами
        document.addEventListener('mouseover', (e) => {
            const element = e.target;

            if (element.classList.contains('hover-lift')) {
                this.addHoverEffect(element, 'lift');
            }

            if (element.classList.contains('hover-scale')) {
                this.addHoverEffect(element, 'scale');
            }

            if (element.classList.contains('hover-rotate')) {
                this.addHoverEffect(element, 'rotate');
            }

            if (element.classList.contains('hover-glow')) {
                this.addHoverEffect(element, 'glow');
            }
        });

        document.addEventListener('mouseout', (e) => {
            const element = e.target;

            if (element.classList.contains('hover-lift') ||
                element.classList.contains('hover-scale') ||
                element.classList.contains('hover-rotate') ||
                element.classList.contains('hover-glow')) {
                this.removeHoverEffect(element);
            }
        });
    }

    /**
     * Настройка focus состояний
     */
    setupFocusStates() {
        document.addEventListener('focusin', (e) => {
            const element = e.target;

            if (element.matches('input, textarea, select, button, [tabindex]')) {
                this.addFocusEffect(element);
            }
        });

        document.addEventListener('focusout', (e) => {
            const element = e.target;

            if (element.matches('input, textarea, select, button, [tabindex]')) {
                this.removeFocusEffect(element);
            }
        });
    }

    /**
     * Настройка click эффектов
     */
    setupClickEffects() {
        document.addEventListener('click', (e) => {
            const element = e.target;

            if (element.classList.contains('click-ripple')) {
                this.createRippleEffect(element, e);
            }

            if (element.classList.contains('click-bounce')) {
                this.createBounceEffect(element);
            }

            if (element.classList.contains('click-pulse')) {
                this.createPulseEffect(element);
            }
        });
    }

    /**
     * Настройка поддержки жестов
     */
    setupGestureSupport() {
        let startX, startY, startTime;

        document.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            startX = touch.clientX;
            startY = touch.clientY;
            startTime = Date.now();
        });

        document.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;

            const touch = e.changedTouches[0];
            const endX = touch.clientX;
            const endY = touch.clientY;
            const endTime = Date.now();

            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const deltaTime = endTime - startTime;

            const element = document.elementFromPoint(endX, endY);

            if (element && element.classList.contains('gesture-swipe')) {
                this.handleSwipeGesture(element, deltaX, deltaY, deltaTime);
            }

            startX = startY = startTime = null;
        });
    }

    /**
     * Настройка клавиатурной навигации
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Enter для кнопок и ссылок
            if (e.key === 'Enter') {
                const element = e.target;
                if (element.classList.contains('keyboard-activatable')) {
                    element.click();
                }
            }

            // Escape для закрытия модальных окон
            if (e.key === 'Escape') {
                const modal = document.querySelector('.modal.show');
                if (modal) {
                    const closeBtn = modal.querySelector('.modal-close');
                    if (closeBtn) {
                        closeBtn.click();
                    }
                }
            }

            // Стрелки для навигации по спискам
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                this.handleArrowNavigation(e);
            }
        });
    }

    /**
     * Добавление hover эффекта
     */
    addHoverEffect(element, type) {
        if (this.hoverElements.has(element)) return;

        this.hoverElements.add(element);

        switch (type) {
            case 'lift':
                element.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';
                element.style.transform = 'translateY(-2px)';
                element.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                break;
            case 'scale':
                element.style.transition = 'transform 0.2s ease';
                element.style.transform = 'scale(1.05)';
                break;
            case 'rotate':
                element.style.transition = 'transform 0.3s ease';
                element.style.transform = 'rotate(5deg)';
                break;
            case 'glow':
                element.style.transition = 'box-shadow 0.2s ease';
                element.style.boxShadow = '0 0 20px rgba(59, 130, 246, 0.5)';
                break;
        }
    }

    /**
     * Удаление hover эффекта
     */
    removeHoverEffect(element) {
        if (!this.hoverElements.has(element)) return;

        this.hoverElements.delete(element);
        element.style.transform = '';
        element.style.boxShadow = '';
    }

    /**
     * Добавление focus эффекта
     */
    addFocusEffect(element) {
        if (this.focusElements.has(element)) return;

        this.focusElements.add(element);
        element.classList.add('focus-ring');

        // Добавляем анимацию фокуса
        element.style.transition = 'all 0.2s ease';
        element.style.outline = '2px solid #3b82f6';
        element.style.outlineOffset = '2px';
    }

    /**
     * Удаление focus эффекта
     */
    removeFocusEffect(element) {
        if (!this.focusElements.has(element)) return;

        this.focusElements.delete(element);
        element.classList.remove('focus-ring');
        element.style.outline = '';
        element.style.outlineOffset = '';
    }

    /**
     * Создание ripple эффекта
     */
    createRippleEffect(element, event) {
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        const ripple = document.createElement('span');
        ripple.className = 'ripple-effect';
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;

        // Добавляем стили для анимации
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    /**
     * Создание bounce эффекта
     */
    createBounceEffect(element) {
        element.style.animation = 'bounce 0.6s ease';

        setTimeout(() => {
            element.style.animation = '';
        }, 600);
    }

    /**
     * Создание pulse эффекта
     */
    createPulseEffect(element) {
        element.style.animation = 'pulse 0.3s ease';

        setTimeout(() => {
            element.style.animation = '';
        }, 300);
    }

    /**
     * Обработка swipe жестов
     */
    handleSwipeGesture(element, deltaX, deltaY, deltaTime) {
        const minSwipeDistance = 50;
        const maxSwipeTime = 300;

        if (deltaTime > maxSwipeTime) return;

        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            // Горизонтальный swipe
            if (Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    this.triggerSwipeEvent(element, 'swipe-right', { deltaX, deltaY });
                } else {
                    this.triggerSwipeEvent(element, 'swipe-left', { deltaX, deltaY });
                }
            }
        } else {
            // Вертикальный swipe
            if (Math.abs(deltaY) > minSwipeDistance) {
                if (deltaY > 0) {
                    this.triggerSwipeEvent(element, 'swipe-down', { deltaX, deltaY });
                } else {
                    this.triggerSwipeEvent(element, 'swipe-up', { deltaX, deltaY });
                }
            }
        }
    }

    /**
     * Триггер swipe события
     */
    triggerSwipeEvent(element, direction, data) {
        const event = new CustomEvent('swipe', {
            detail: { direction, ...data }
        });
        element.dispatchEvent(event);
    }

    /**
     * Обработка навигации стрелками
     */
    handleArrowNavigation(event) {
        const currentElement = event.target;
        const parent = currentElement.closest('[role="listbox"], [role="menu"], .navigation-list');

        if (!parent) return;

        const items = Array.from(parent.querySelectorAll('[role="option"], [role="menuitem"], .navigation-item'));
        const currentIndex = items.indexOf(currentElement);

        if (currentIndex === -1) return;

        event.preventDefault();

        let nextIndex;
        if (event.key === 'ArrowDown') {
            nextIndex = (currentIndex + 1) % items.length;
        } else {
            nextIndex = (currentIndex - 1 + items.length) % items.length;
        }

        items[nextIndex].focus();
    }

    /**
     * Добавление интерактивных классов к элементу
     */
    enhanceElement(element, options = {}) {
        const {
            hover = 'lift',
            click = 'ripple',
            focus = true,
            keyboard = true
        } = options;

        if (hover) {
            element.classList.add(`hover-${hover}`);
        }

        if (click) {
            element.classList.add(`click-${click}`);
        }

        if (focus) {
            element.classList.add('focusable');
        }

        if (keyboard) {
            element.classList.add('keyboard-activatable');
        }
    }

    /**
     * Создание интерактивной кнопки
     */
    createInteractiveButton(text, options = {}) {
        const button = document.createElement('button');
        button.textContent = text;
        button.className = 'interactive-button';

        this.enhanceElement(button, {
            hover: 'lift',
            click: 'ripple',
            focus: true,
            keyboard: true,
            ...options
        });

        return button;
    }

    /**
     * Создание интерактивной карточки
     */
    createInteractiveCard(content, options = {}) {
        const card = document.createElement('div');
        card.className = 'interactive-card';
        card.innerHTML = content;

        this.enhanceElement(card, {
            hover: 'lift',
            click: 'bounce',
            focus: true,
            keyboard: true,
            ...options
        });

        return card;
    }

    /**
     * Добавление drag and drop функциональности
     */
    makeDraggable(element, options = {}) {
        const {
            onDragStart = null,
            onDragEnd = null,
            onDrop = null,
            dragData = null
        } = options;

        element.draggable = true;
        element.classList.add('draggable');

        element.addEventListener('dragstart', (e) => {
            element.classList.add('dragging');
            if (dragData) {
                e.dataTransfer.setData('application/json', JSON.stringify(dragData));
            }
            if (onDragStart) onDragStart(e);
        });

        element.addEventListener('dragend', (e) => {
            element.classList.remove('dragging');
            if (onDragEnd) onDragEnd(e);
        });

        element.addEventListener('dragover', (e) => {
            e.preventDefault();
            element.classList.add('drag-over');
        });

        element.addEventListener('dragleave', (e) => {
            element.classList.remove('drag-over');
        });

        element.addEventListener('drop', (e) => {
            e.preventDefault();
            element.classList.remove('drag-over');

            if (onDrop) {
                const data = e.dataTransfer.getData('application/json');
                onDrop(JSON.parse(data || '{}'), e);
            }
        });
    }

    /**
     * Очистка всех эффектов
     */
    cleanup() {
        this.hoverElements.forEach(element => this.removeHoverEffect(element));
        this.focusElements.forEach(element => this.removeFocusEffect(element));

        this.hoverElements.clear();
        this.focusElements.clear();
        this.clickElements.clear();
        this.gestureElements.clear();
    }
}

// Создаем глобальный экземпляр
window.InteractionManager = new InteractionManager();

// Экспорт для глобального доступа
window.Interactions = {
    // Быстрые методы
    enhance: (element, options) => window.InteractionManager.enhanceElement(element, options),
    createButton: (text, options) => window.InteractionManager.createInteractiveButton(text, options),
    createCard: (content, options) => window.InteractionManager.createInteractiveCard(content, options),
    makeDraggable: (element, options) => window.InteractionManager.makeDraggable(element, options),

    // Эффекты
    ripple: (element, event) => window.InteractionManager.createRippleEffect(element, event),
    bounce: (element) => window.InteractionManager.createBounceEffect(element),
    pulse: (element) => window.InteractionManager.createPulseEffect(element),

    // Hover эффекты
    addHover: (element, type) => window.InteractionManager.addHoverEffect(element, type),
    removeHover: (element) => window.InteractionManager.removeHoverEffect(element),

    // Focus эффекты
    addFocus: (element) => window.InteractionManager.addFocusEffect(element),
    removeFocus: (element) => window.InteractionManager.removeFocusEffect(element)
};
