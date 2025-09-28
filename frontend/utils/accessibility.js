/**
 * Accessibility utilities for enhanced user experience
 * Provides ARIA attributes, keyboard navigation, and screen reader support
 */

class AccessibilityManager {
    constructor() {
        this.focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        this.focusableElementsVisible = 'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
        this.currentFocusIndex = 0;
        this.focusableList = [];
        this.init();
    }

    /**
     * Initialize accessibility features
     */
    init() {
        this.setupKeyboardNavigation();
        this.setupARIA();
        this.setupFocusManagement();
        this.setupScreenReaderSupport();
        console.log('♿ Accessibility manager initialized');
    }

    /**
     * Setup keyboard navigation
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Tab navigation
            if (e.key === 'Tab') {
                this.handleTabNavigation(e);
            }

            // Arrow key navigation for custom components
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                this.handleArrowNavigation(e);
            }

            // Enter and Space for activation
            if (['Enter', ' '].includes(e.key)) {
                this.handleActivation(e);
            }

            // Escape for closing modals/overlays
            if (e.key === 'Escape') {
                this.handleEscape(e);
            }
        });
    }

    /**
     * Handle Tab navigation
     */
    handleTabNavigation(e) {
        const focusableElements = this.getFocusableElements();

        if (focusableElements.length === 0) return;

        if (e.shiftKey) {
            // Shift + Tab (backward)
            if (document.activeElement === focusableElements[0]) {
                e.preventDefault();
                focusableElements[focusableElements.length - 1].focus();
            }
        } else {
            // Tab (forward)
            if (document.activeElement === focusableElements[focusableElements.length - 1]) {
                e.preventDefault();
                focusableElements[0].focus();
            }
        }
    }

    /**
     * Handle arrow key navigation
     */
    handleArrowNavigation(e) {
        const activeElement = document.activeElement;
        const container = activeElement.closest('[role="menu"], [role="listbox"], [role="grid"], [role="tree"]');

        if (!container) return;

        e.preventDefault();
        const focusableElements = Array.from(container.querySelectorAll(this.focusableElementsVisible));
        const currentIndex = focusableElements.indexOf(activeElement);

        let nextIndex = currentIndex;

        switch (e.key) {
            case 'ArrowUp':
            case 'ArrowLeft':
                nextIndex = currentIndex > 0 ? currentIndex - 1 : focusableElements.length - 1;
                break;
            case 'ArrowDown':
            case 'ArrowRight':
                nextIndex = currentIndex < focusableElements.length - 1 ? currentIndex + 1 : 0;
                break;
        }

        if (nextIndex !== currentIndex) {
            focusableElements[nextIndex].focus();
        }
    }

    /**
     * Handle Enter and Space activation
     */
    handleActivation(e) {
        const activeElement = document.activeElement;

        // Don't activate if it's a form input
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(activeElement.tagName)) {
            return;
        }

        e.preventDefault();

        // Trigger click event
        if (activeElement.click) {
            activeElement.click();
        }

        // Trigger custom activation
        const customActivation = activeElement.getAttribute('data-activate');
        if (customActivation && window[customActivation]) {
            window[customActivation]();
        }
    }

    /**
     * Handle Escape key
     */
    handleEscape(e) {
        // Close any open modals
        const openModal = document.querySelector('.modal.show, .advanced-modal.show');
        if (openModal) {
            e.preventDefault();
            const closeBtn = openModal.querySelector('[data-dismiss="modal"], .close-btn');
            if (closeBtn) {
                closeBtn.click();
            }
        }

        // Close any open dropdowns
        const openDropdown = document.querySelector('.dropdown.show, .menu.show');
        if (openDropdown) {
            e.preventDefault();
            openDropdown.classList.remove('show');
        }
    }

    /**
     * Setup ARIA attributes
     */
    setupARIA() {
        // Add ARIA labels to buttons without text
        document.querySelectorAll('button:not([aria-label]):empty, button:not([aria-label]) img').forEach(button => {
            const img = button.querySelector('img');
            if (img) {
                button.setAttribute('aria-label', img.alt || 'Button');
            } else {
                button.setAttribute('aria-label', 'Button');
            }
        });

        // Add ARIA labels to form inputs
        document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])').forEach(input => {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) {
                input.setAttribute('aria-labelledby', label.id || `label-${input.id}`);
            }
        });

        // Add role attributes
        document.querySelectorAll('.nav-menu').forEach(menu => {
            menu.setAttribute('role', 'navigation');
            menu.setAttribute('aria-label', 'Main navigation');
        });

        document.querySelectorAll('.modal, .advanced-modal').forEach(modal => {
            modal.setAttribute('role', 'dialog');
            modal.setAttribute('aria-modal', 'true');
        });

        // Add live regions for dynamic content
        this.createLiveRegion('status', 'Status updates');
        this.createLiveRegion('alert', 'Important alerts');
    }

    /**
     * Create live region for screen readers
     */
    createLiveRegion(id, label) {
        if (!document.getElementById(id)) {
            const liveRegion = document.createElement('div');
            liveRegion.id = id;
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-label', label);
            liveRegion.className = 'sr-only';
            document.body.appendChild(liveRegion);
        }
    }

    /**
     * Announce message to screen readers
     */
    announce(message, type = 'status') {
        const liveRegion = document.getElementById(type);
        if (liveRegion) {
            liveRegion.textContent = message;
            // Clear after announcement
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Setup focus management
     */
    setupFocusManagement() {
        // Track focus changes
        document.addEventListener('focusin', (e) => {
            this.currentFocusIndex = this.getFocusableElements().indexOf(e.target);
        });

        // Trap focus in modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                const modal = document.querySelector('.modal.show, .advanced-modal.show');
                if (modal) {
                    this.trapFocusInModal(modal, e);
                }
            }
        });
    }

    /**
     * Trap focus within modal
     */
    trapFocusInModal(modal, e) {
        const focusableElements = modal.querySelectorAll(this.focusableElementsVisible);
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else {
            // Tab
            if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    }

    /**
     * Setup screen reader support
     */
    setupScreenReaderSupport() {
        // Add skip links
        this.addSkipLinks();

        // Add screen reader only text
        this.addScreenReaderText();

        // Setup landmarks
        this.setupLandmarks();
    }

    /**
     * Add skip links
     */
    addSkipLinks() {
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links';
        skipLinks.innerHTML = `
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <a href="#navigation" class="skip-link">Skip to navigation</a>
        `;
        document.body.insertBefore(skipLinks, document.body.firstChild);
    }

    /**
     * Add screen reader only text
     */
    addScreenReaderText() {
        const style = document.createElement('style');
        style.textContent = `
            .sr-only {
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0, 0, 0, 0);
                white-space: nowrap;
                border: 0;
            }
            
            .skip-links {
                position: absolute;
                top: -40px;
                left: 6px;
                z-index: 1000;
            }
            
            .skip-link {
                position: absolute;
                top: -40px;
                left: 6px;
                background: #000;
                color: #fff;
                padding: 8px;
                text-decoration: none;
                z-index: 1000;
                transition: top 0.3s;
            }
            
            .skip-link:focus {
                top: 6px;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Setup landmarks
     */
    setupLandmarks() {
        // Main content
        const mainContent = document.querySelector('.main-content, main, .content');
        if (mainContent) {
            mainContent.id = 'main-content';
            mainContent.setAttribute('role', 'main');
        }

        // Navigation
        const navigation = document.querySelector('.nav-menu, nav');
        if (navigation) {
            navigation.id = 'navigation';
            navigation.setAttribute('role', 'navigation');
        }

        // Sidebar
        const sidebar = document.querySelector('.sidebar, aside');
        if (sidebar) {
            sidebar.setAttribute('role', 'complementary');
        }
    }

    /**
     * Get focusable elements
     */
    getFocusableElements() {
        return Array.from(document.querySelectorAll(this.focusableElementsVisible));
    }

    /**
     * Focus first element
     */
    focusFirst() {
        const focusableElements = this.getFocusableElements();
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }

    /**
     * Focus last element
     */
    focusLast() {
        const focusableElements = this.getFocusableElements();
        if (focusableElements.length > 0) {
            focusableElements[focusableElements.length - 1].focus();
        }
    }

    /**
     * Focus next element
     */
    focusNext() {
        const focusableElements = this.getFocusableElements();
        if (focusableElements.length > 0) {
            const currentIndex = focusableElements.indexOf(document.activeElement);
            const nextIndex = currentIndex < focusableElements.length - 1 ? currentIndex + 1 : 0;
            focusableElements[nextIndex].focus();
        }
    }

    /**
     * Focus previous element
     */
    focusPrevious() {
        const focusableElements = this.getFocusableElements();
        if (focusableElements.length > 0) {
            const currentIndex = focusableElements.indexOf(document.activeElement);
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : focusableElements.length - 1;
            focusableElements[prevIndex].focus();
        }
    }

    /**
     * Add ARIA attributes to element
     */
    addARIA(element, attributes) {
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
    }

    /**
     * Remove ARIA attributes from element
     */
    removeARIA(element, attributes) {
        attributes.forEach(attr => {
            element.removeAttribute(attr);
        });
    }

    /**
     * Make element focusable
     */
    makeFocusable(element) {
        if (!element.hasAttribute('tabindex')) {
            element.setAttribute('tabindex', '0');
        }
    }

    /**
     * Make element not focusable
     */
    makeNotFocusable(element) {
        element.setAttribute('tabindex', '-1');
    }

    /**
     * Setup high contrast mode
     */
    setupHighContrast() {
        const style = document.createElement('style');
        style.id = 'high-contrast';
        style.textContent = `
            .high-contrast {
                filter: contrast(150%) brightness(1.2);
            }
            
            .high-contrast * {
                border-color: currentColor !important;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Toggle high contrast mode
     */
    toggleHighContrast() {
        document.body.classList.toggle('high-contrast');
        const isEnabled = document.body.classList.contains('high-contrast');
        this.announce(`High contrast mode ${isEnabled ? 'enabled' : 'disabled'}`);
        return isEnabled;
    }

    /**
     * Setup reduced motion
     */
    setupReducedMotion() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (prefersReducedMotion) {
            document.body.classList.add('reduced-motion');
        }

        // Listen for changes
        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            if (e.matches) {
                document.body.classList.add('reduced-motion');
            } else {
                document.body.classList.remove('reduced-motion');
            }
        });
    }
}

// Export for global access
window.AccessibilityManager = AccessibilityManager;
console.log('♿ Accessibility utilities loaded');
