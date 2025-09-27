// Modal component
class Modal {
    constructor(id, options = {}) {
        this.id = id;
        this.options = {
            closable: true,
            backdrop: true,
            keyboard: true,
            ...options
        };
        this.element = null;
    }

    create(content) {
        const modal = document.createElement('div');
        modal.id = this.id;
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-backdrop" ${this.options.backdrop ? '' : 'style="display: none;"'}></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">${content.title || 'Modal'}</h3>
                    ${this.options.closable ? '<button class="modal-close">&times;</button>' : ''}
                </div>
                <div class="modal-body">
                    ${content.body || ''}
                </div>
                <div class="modal-footer">
                    ${content.footer || ''}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.element = modal;
        this.bindEvents();
        return modal;
    }

    show() {
        if (this.element) {
            this.element.classList.add('show');
            document.body.classList.add('modal-open');
        }
    }

    hide() {
        if (this.element) {
            this.element.classList.remove('show');
            document.body.classList.remove('modal-open');
        }
    }

    destroy() {
        if (this.element) {
            this.element.remove();
            this.element = null;
        }
    }

    bindEvents() {
        if (!this.element) return;

        const closeBtn = this.element.querySelector('.modal-close');
        const backdrop = this.element.querySelector('.modal-backdrop');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hide());
        }

        if (backdrop && this.options.backdrop) {
            backdrop.addEventListener('click', () => this.hide());
        }

        if (this.options.keyboard) {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.element.classList.contains('show')) {
                    this.hide();
                }
            });
        }
    }
}

// Export for global access
window.Modal = Modal;
