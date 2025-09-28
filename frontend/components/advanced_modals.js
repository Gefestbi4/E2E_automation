/**
 * Продвинутая система модальных окон
 * Поддерживает различные типы, анимации, размеры, позиционирование
 */

class AdvancedModal {
    constructor(id, options = {}) {
        this.id = id;
        this.options = {
            closable: true,
            backdrop: true,
            keyboard: true,
            size: 'medium', // small, medium, large, xlarge, fullscreen
            position: 'center', // center, top, bottom, left, right
            animation: 'fade', // fade, slide, zoom, flip
            duration: 300,
            autoFocus: true,
            restoreFocus: true,
            trapFocus: true,
            ...options
        };
        this.element = null;
        this.isOpen = false;
        this.previousFocus = null;
        this.focusableElements = [];
        this.currentFocusIndex = 0;
    }

    /**
     * Создание модального окна
     */
    create(content) {
        const modal = document.createElement('div');
        modal.id = this.id;
        modal.className = `modal modal-${this.options.size} modal-${this.options.position} modal-${this.options.animation}`;
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', `${this.id}-title`);
        modal.setAttribute('aria-describedby', `${this.id}-description`);

        modal.innerHTML = `
            <div class="modal-backdrop" ${this.options.backdrop ? '' : 'style="display: none;"'}></div>
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="${this.id}-title">${content.title || 'Modal'}</h3>
                        ${this.options.closable ? `
                            <button class="modal-close" aria-label="Close modal" type="button">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        ` : ''}
                    </div>
                    <div class="modal-body" id="${this.id}-description">
                        ${content.body || ''}
                    </div>
                    ${content.footer ? `
                        <div class="modal-footer">
                            ${content.footer}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;

        this.element = modal;
        this.setupEventListeners();
        return modal;
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        if (!this.element) return;

        // Закрытие по клику на backdrop
        if (this.options.backdrop) {
            const backdrop = this.element.querySelector('.modal-backdrop');
            backdrop.addEventListener('click', () => {
                if (this.options.closable) {
                    this.close();
                }
            });
        }

        // Закрытие по клику на кнопку закрытия
        const closeBtn = this.element.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.close();
            });
        }

        // Закрытие по клавише Escape
        if (this.options.keyboard) {
            this.handleKeydown = (e) => {
                if (e.key === 'Escape' && this.isOpen) {
                    this.close();
                }
            };
            document.addEventListener('keydown', this.handleKeydown);
        }

        // Обработка фокуса для trap focus
        if (this.options.trapFocus) {
            this.handleTabKey = (e) => {
                if (e.key === 'Tab' && this.isOpen) {
                    this.trapFocus(e);
                }
            };
            this.element.addEventListener('keydown', this.handleTabKey);
        }
    }

    /**
     * Показ модального окна
     */
    show(content) {
        if (this.isOpen) return;

        // Создаем модальное окно если его нет
        if (!this.element) {
            this.create(content);
        } else {
            // Обновляем содержимое
            this.updateContent(content);
        }

        // Сохраняем текущий фокус
        this.previousFocus = document.activeElement;

        // Добавляем в DOM
        document.body.appendChild(this.element);
        document.body.classList.add('modal-open');

        // Находим фокусируемые элементы
        this.updateFocusableElements();

        // Анимация появления
        requestAnimationFrame(() => {
            this.element.classList.add('modal-show');
            this.isOpen = true;

            // Автофокус
            if (this.options.autoFocus) {
                this.focusFirstElement();
            }
        });

        // Закрытие по клику вне модального окна
        this.element.addEventListener('click', (e) => {
            if (e.target === this.element && this.options.closable) {
                this.close();
            }
        });
    }

    /**
     * Обновление содержимого модального окна
     */
    updateContent(content) {
        if (!this.element) return;

        const title = this.element.querySelector('.modal-title');
        const body = this.element.querySelector('.modal-body');
        const footer = this.element.querySelector('.modal-footer');

        if (title) title.textContent = content.title || 'Modal';
        if (body) body.innerHTML = content.body || '';
        if (footer) footer.innerHTML = content.footer || '';

        // Обновляем фокусируемые элементы
        this.updateFocusableElements();
    }

    /**
     * Закрытие модального окна
     */
    close() {
        if (!this.isOpen || !this.element) return;

        this.element.classList.remove('modal-show');
        this.isOpen = false;

        // Анимация исчезновения
        setTimeout(() => {
            if (this.element && this.element.parentNode) {
                this.element.parentNode.removeChild(this.element);
            }
            document.body.classList.remove('modal-open');

            // Восстанавливаем фокус
            if (this.options.restoreFocus && this.previousFocus) {
                this.previousFocus.focus();
            }
        }, this.options.duration);

        // Очищаем обработчики событий
        this.cleanup();
    }

    /**
     * Очистка обработчиков событий
     */
    cleanup() {
        if (this.handleKeydown) {
            document.removeEventListener('keydown', this.handleKeydown);
        }
        if (this.handleTabKey) {
            this.element.removeEventListener('keydown', this.handleTabKey);
        }
    }

    /**
     * Обновление списка фокусируемых элементов
     */
    updateFocusableElements() {
        if (!this.element) return;

        const focusableSelectors = [
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            'a[href]',
            '[tabindex]:not([tabindex="-1"])'
        ];

        this.focusableElements = Array.from(
            this.element.querySelectorAll(focusableSelectors.join(', '))
        ).filter(el => {
            return el.offsetParent !== null; // Видимые элементы
        });

        this.currentFocusIndex = 0;
    }

    /**
     * Фокус на первом элементе
     */
    focusFirstElement() {
        if (this.focusableElements.length > 0) {
            this.focusableElements[0].focus();
        }
    }

    /**
     * Обработка Tab для trap focus
     */
    trapFocus(e) {
        if (this.focusableElements.length === 0) return;

        if (e.shiftKey) {
            // Shift + Tab - назад
            if (this.currentFocusIndex === 0) {
                e.preventDefault();
                this.currentFocusIndex = this.focusableElements.length - 1;
                this.focusableElements[this.currentFocusIndex].focus();
            }
        } else {
            // Tab - вперед
            if (this.currentFocusIndex === this.focusableElements.length - 1) {
                e.preventDefault();
                this.currentFocusIndex = 0;
                this.focusableElements[this.currentFocusIndex].focus();
            }
        }
    }

    /**
     * Статический метод для закрытия модального окна
     */
    static close(id) {
        const modal = document.getElementById(id);
        if (modal && modal._modalInstance) {
            modal._modalInstance.close();
        }
    }

    /**
     * Статический метод для показа модального окна
     */
    static show(id, content, options = {}) {
        let modal = document.getElementById(id);
        if (!modal) {
            modal = new AdvancedModal(id, options);
            modal.create(content);
            modal.element._modalInstance = modal;
        }
        modal.show(content);
        return modal;
    }
}

// Создаем глобальный экземпляр для обратной совместимости
window.Modal = AdvancedModal;

// Экспорт для глобального доступа
window.AdvancedModal = AdvancedModal;
