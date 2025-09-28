/**
 * Мобильная навигация и адаптивные компоненты
 * Поддерживает bottom navigation, hamburger menu, drawer navigation
 */

class MobileNavigationManager {
    constructor() {
        this.isMobile = false;
        this.isTablet = false;
        this.isDesktop = false;
        this.currentBreakpoint = 'mobile';
        this.navigationType = 'bottom'; // bottom, drawer, tabs
        this.isDrawerOpen = false;

        this.init();
    }

    /**
     * Инициализация мобильной навигации
     */
    init() {
        this.detectDevice();
        this.setupResponsiveNavigation();
        this.setupMobileMenu();
        this.setupDrawerNavigation();
        this.setupBottomNavigation();
        this.setupTouchOptimizations();
        this.setupViewportHandling();
    }

    /**
     * Определение типа устройства
     */
    detectDevice() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        const userAgent = navigator.userAgent.toLowerCase();

        this.isMobile = width < 768 || (userAgent.includes('mobile') && width < 1024);
        this.isTablet = width >= 768 && width < 1024;
        this.isDesktop = width >= 1024;

        if (this.isMobile) {
            this.currentBreakpoint = 'mobile';
            this.navigationType = 'bottom';
        } else if (this.isTablet) {
            this.currentBreakpoint = 'tablet';
            this.navigationType = 'tabs';
        } else {
            this.currentBreakpoint = 'desktop';
            this.navigationType = 'sidebar';
        }
    }

    /**
     * Настройка адаптивной навигации
     */
    setupResponsiveNavigation() {
        // Слушаем изменения размера окна
        window.addEventListener('resize', this.handleResize.bind(this));

        // Слушаем изменения ориентации
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleResize();
            }, 100);
        });
    }

    /**
     * Обработка изменения размера окна
     */
    handleResize() {
        const oldBreakpoint = this.currentBreakpoint;
        this.detectDevice();

        if (oldBreakpoint !== this.currentBreakpoint) {
            this.updateNavigation();
        }
    }

    /**
     * Обновление навигации при изменении breakpoint
     */
    updateNavigation() {
        // Удаляем старую навигацию
        this.removeCurrentNavigation();

        // Создаем новую навигацию
        this.createNavigation();

        // Обновляем стили
        this.updateStyles();
    }

    /**
     * Удаление текущей навигации
     */
    removeCurrentNavigation() {
        const oldNav = document.querySelector('.mobile-nav, .tablet-nav, .desktop-nav');
        if (oldNav) {
            oldNav.remove();
        }

        const oldDrawer = document.querySelector('.drawer');
        if (oldDrawer) {
            oldDrawer.remove();
        }
    }

    /**
     * Создание навигации
     */
    createNavigation() {
        switch (this.navigationType) {
            case 'bottom':
                this.createBottomNavigation();
                break;
            case 'tabs':
                this.createTabNavigation();
                break;
            case 'sidebar':
                this.createSidebarNavigation();
                break;
        }
    }

    /**
     * Создание bottom navigation для мобильных
     */
    createBottomNavigation() {
        const nav = document.createElement('nav');
        nav.className = 'mobile-nav';
        nav.innerHTML = `
            <div class="mobile-nav-item" data-page="dashboard">
                <i class="fas fa-home"></i>
                <span>Главная</span>
            </div>
            <div class="mobile-nav-item" data-page="ecommerce">
                <i class="fas fa-shopping-cart"></i>
                <span>Магазин</span>
            </div>
            <div class="mobile-nav-item" data-page="social">
                <i class="fas fa-users"></i>
                <span>Соцсеть</span>
            </div>
            <div class="mobile-nav-item" data-page="tasks">
                <i class="fas fa-tasks"></i>
                <span>Задачи</span>
            </div>
            <div class="mobile-nav-item" data-page="content">
                <i class="fas fa-file-alt"></i>
                <span>Контент</span>
            </div>
            <div class="mobile-nav-item" data-page="analytics">
                <i class="fas fa-chart-bar"></i>
                <span>Аналитика</span>
            </div>
        `;

        document.body.appendChild(nav);
        this.setupNavigationEvents(nav);
    }

    /**
     * Создание tab navigation для планшетов
     */
    createTabNavigation() {
        const nav = document.createElement('nav');
        nav.className = 'tablet-nav';
        nav.innerHTML = `
            <div class="tablet-nav-container">
                <div class="tablet-nav-item active" data-page="dashboard">
                    <i class="fas fa-home"></i>
                    <span>Главная</span>
                </div>
                <div class="tablet-nav-item" data-page="ecommerce">
                    <i class="fas fa-shopping-cart"></i>
                    <span>Магазин</span>
                </div>
                <div class="tablet-nav-item" data-page="social">
                    <i class="fas fa-users"></i>
                    <span>Соцсеть</span>
                </div>
                <div class="tablet-nav-item" data-page="tasks">
                    <i class="fas fa-tasks"></i>
                    <span>Задачи</span>
                </div>
                <div class="tablet-nav-item" data-page="content">
                    <i class="fas fa-file-alt"></i>
                    <span>Контент</span>
                </div>
                <div class="tablet-nav-item" data-page="analytics">
                    <i class="fas fa-chart-bar"></i>
                    <span>Аналитика</span>
                </div>
            </div>
        `;

        document.body.appendChild(nav);
        this.setupNavigationEvents(nav);
    }

    /**
     * Создание sidebar navigation для десктопа
     */
    createSidebarNavigation() {
        const nav = document.createElement('nav');
        nav.className = 'desktop-nav';
        nav.innerHTML = `
            <div class="desktop-nav-container">
                <div class="desktop-nav-header">
                    <h3>Меню</h3>
                </div>
                <div class="desktop-nav-items">
                    <div class="desktop-nav-item active" data-page="dashboard">
                        <i class="fas fa-home"></i>
                        <span>Главная</span>
                    </div>
                    <div class="desktop-nav-item" data-page="ecommerce">
                        <i class="fas fa-shopping-cart"></i>
                        <span>Магазин</span>
                    </div>
                    <div class="desktop-nav-item" data-page="social">
                        <i class="fas fa-users"></i>
                        <span>Соцсеть</span>
                    </div>
                    <div class="desktop-nav-item" data-page="tasks">
                        <i class="fas fa-tasks"></i>
                        <span>Задачи</span>
                    </div>
                    <div class="desktop-nav-item" data-page="content">
                        <i class="fas fa-file-alt"></i>
                        <span>Контент</span>
                    </div>
                    <div class="desktop-nav-item" data-page="analytics">
                        <i class="fas fa-chart-bar"></i>
                        <span>Аналитика</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(nav);
        this.setupNavigationEvents(nav);
    }

    /**
     * Настройка событий навигации
     */
    setupNavigationEvents(nav) {
        nav.addEventListener('click', (e) => {
            const navItem = e.target.closest('.mobile-nav-item, .tablet-nav-item, .desktop-nav-item');
            if (navItem) {
                const page = navItem.dataset.page;
                this.navigateToPage(page);
                this.setActiveNavItem(navItem);
            }
        });
    }

    /**
     * Навигация к странице
     */
    navigateToPage(pageName) {
        // Скрываем все страницы
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Показываем нужную страницу
        const targetPage = document.getElementById(`${pageName}-page`);
        if (targetPage) {
            targetPage.classList.add('active');

            // Анимация перехода
            if (window.Animations) {
                window.Animations.fadeIn(targetPage, { duration: 300 });
            }
        }

        // Закрываем drawer если открыт
        if (this.isDrawerOpen) {
            this.closeDrawer();
        }
    }

    /**
     * Установка активного элемента навигации
     */
    setActiveNavItem(activeItem) {
        const nav = activeItem.closest('.mobile-nav, .tablet-nav, .desktop-nav');
        if (nav) {
            nav.querySelectorAll('.mobile-nav-item, .tablet-nav-item, .desktop-nav-item').forEach(item => {
                item.classList.remove('active');
            });
            activeItem.classList.add('active');
        }
    }

    /**
     * Настройка мобильного меню
     */
    setupMobileMenu() {
        // Создаем hamburger menu для мобильных
        if (this.isMobile) {
            this.createHamburgerMenu();
        }
    }

    /**
     * Создание hamburger меню
     */
    createHamburgerMenu() {
        const hamburger = document.createElement('button');
        hamburger.className = 'hamburger-menu';
        hamburger.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;

        hamburger.addEventListener('click', () => {
            this.toggleDrawer();
        });

        // Добавляем в header если есть
        const header = document.querySelector('.navbar, .header');
        if (header) {
            header.appendChild(hamburger);
        }
    }

    /**
     * Настройка drawer навигации
     */
    setupDrawerNavigation() {
        this.createDrawer();
    }

    /**
     * Создание drawer
     */
    createDrawer() {
        const drawer = document.createElement('div');
        drawer.className = 'drawer';
        drawer.innerHTML = `
            <div class="drawer-overlay"></div>
            <div class="drawer-content">
                <div class="drawer-header">
                    <h3>Меню</h3>
                    <button class="drawer-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="drawer-body">
                    <div class="drawer-nav-item" data-page="dashboard">
                        <i class="fas fa-home"></i>
                        <span>Главная</span>
                    </div>
                    <div class="drawer-nav-item" data-page="ecommerce">
                        <i class="fas fa-shopping-cart"></i>
                        <span>Магазин</span>
                    </div>
                    <div class="drawer-nav-item" data-page="social">
                        <i class="fas fa-users"></i>
                        <span>Соцсеть</span>
                    </div>
                    <div class="drawer-nav-item" data-page="tasks">
                        <i class="fas fa-tasks"></i>
                        <span>Задачи</span>
                    </div>
                    <div class="drawer-nav-item" data-page="content">
                        <i class="fas fa-file-alt"></i>
                        <span>Контент</span>
                    </div>
                    <div class="drawer-nav-item" data-page="analytics">
                        <i class="fas fa-chart-bar"></i>
                        <span>Аналитика</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(drawer);

        // Обработка событий drawer
        drawer.addEventListener('click', (e) => {
            if (e.target.classList.contains('drawer-overlay') || e.target.closest('.drawer-close')) {
                this.closeDrawer();
            }

            const navItem = e.target.closest('.drawer-nav-item');
            if (navItem) {
                const page = navItem.dataset.page;
                this.navigateToPage(page);
            }
        });
    }

    /**
     * Открытие drawer
     */
    openDrawer() {
        const drawer = document.querySelector('.drawer');
        if (drawer) {
            drawer.classList.add('open');
            this.isDrawerOpen = true;

            // Блокируем скролл body
            document.body.style.overflow = 'hidden';
        }
    }

    /**
     * Закрытие drawer
     */
    closeDrawer() {
        const drawer = document.querySelector('.drawer');
        if (drawer) {
            drawer.classList.remove('open');
            this.isDrawerOpen = false;

            // Разблокируем скролл body
            document.body.style.overflow = '';
        }
    }

    /**
     * Переключение drawer
     */
    toggleDrawer() {
        if (this.isDrawerOpen) {
            this.closeDrawer();
        } else {
            this.openDrawer();
        }
    }

    /**
     * Настройка bottom navigation
     */
    setupBottomNavigation() {
        // Добавляем стили для bottom navigation
        this.addBottomNavigationStyles();
    }

    /**
     * Добавление стилей для bottom navigation
     */
    addBottomNavigationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .mobile-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: var(--navbar-bg, #ffffff);
                border-top: 1px solid var(--border-color, #e5e7eb);
                padding: var(--spacing-sm);
                display: flex;
                justify-content: space-around;
                z-index: 1000;
                padding-bottom: max(var(--spacing-sm), env(safe-area-inset-bottom));
            }
            
            .mobile-nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: var(--spacing-xs);
                padding: var(--spacing-xs);
                text-decoration: none;
                color: var(--text-secondary, #6b7280);
                font-size: var(--font-size-xs);
                font-weight: 500;
                transition: all 0.2s ease;
                min-height: var(--touch-target-comfortable);
                flex: 1;
                justify-content: center;
                border-radius: 6px;
            }
            
            .mobile-nav-item:hover,
            .mobile-nav-item.active {
                color: var(--primary-600, #2563eb);
                background: var(--primary-50, #eff6ff);
            }
            
            .mobile-nav-item i {
                font-size: var(--font-size-lg);
            }
            
            .tablet-nav {
                position: sticky;
                top: 0;
                background: var(--navbar-bg, #ffffff);
                border-bottom: 1px solid var(--border-color, #e5e7eb);
                z-index: 1000;
            }
            
            .tablet-nav-container {
                display: flex;
                justify-content: center;
                gap: var(--spacing-sm);
                padding: var(--spacing-sm) var(--spacing-md);
            }
            
            .tablet-nav-item {
                display: flex;
                align-items: center;
                gap: var(--spacing-xs);
                padding: var(--spacing-sm) var(--spacing-md);
                text-decoration: none;
                color: var(--text-secondary, #6b7280);
                font-size: var(--font-size-sm);
                font-weight: 500;
                transition: all 0.2s ease;
                min-height: var(--touch-target-min);
                border-radius: 6px;
            }
            
            .tablet-nav-item:hover,
            .tablet-nav-item.active {
                color: var(--primary-600, #2563eb);
                background: var(--primary-50, #eff6ff);
            }
            
            .desktop-nav {
                position: fixed;
                left: 0;
                top: 0;
                width: 250px;
                height: 100vh;
                background: var(--navbar-bg, #ffffff);
                border-right: 1px solid var(--border-color, #e5e7eb);
                z-index: 1000;
                overflow-y: auto;
            }
            
            .desktop-nav-container {
                padding: var(--spacing-lg);
            }
            
            .desktop-nav-header {
                margin-bottom: var(--spacing-lg);
                padding-bottom: var(--spacing-md);
                border-bottom: 1px solid var(--border-color, #e5e7eb);
            }
            
            .desktop-nav-header h3 {
                margin: 0;
                color: var(--text-primary, #111827);
                font-size: var(--font-size-lg);
            }
            
            .desktop-nav-items {
                display: flex;
                flex-direction: column;
                gap: var(--spacing-xs);
            }
            
            .desktop-nav-item {
                display: flex;
                align-items: center;
                gap: var(--spacing-sm);
                padding: var(--spacing-sm) var(--spacing-md);
                text-decoration: none;
                color: var(--text-secondary, #6b7280);
                font-size: var(--font-size-sm);
                font-weight: 500;
                transition: all 0.2s ease;
                min-height: var(--touch-target-min);
                border-radius: 6px;
            }
            
            .desktop-nav-item:hover,
            .desktop-nav-item.active {
                color: var(--primary-600, #2563eb);
                background: var(--primary-50, #eff6ff);
            }
            
            .drawer {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 2000;
                display: none;
            }
            
            .drawer.open {
                display: flex;
            }
            
            .drawer-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(2px);
            }
            
            .drawer-content {
                position: relative;
                width: 280px;
                height: 100%;
                background: var(--navbar-bg, #ffffff);
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                overflow-y: auto;
            }
            
            .drawer.open .drawer-content {
                transform: translateX(0);
            }
            
            .drawer-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: var(--spacing-lg);
                border-bottom: 1px solid var(--border-color, #e5e7eb);
            }
            
            .drawer-header h3 {
                margin: 0;
                color: var(--text-primary, #111827);
            }
            
            .drawer-close {
                background: none;
                border: none;
                font-size: var(--font-size-lg);
                color: var(--text-secondary, #6b7280);
                cursor: pointer;
                padding: var(--spacing-xs);
            }
            
            .drawer-body {
                padding: var(--spacing-lg);
            }
            
            .drawer-nav-item {
                display: flex;
                align-items: center;
                gap: var(--spacing-sm);
                padding: var(--spacing-sm) var(--spacing-md);
                text-decoration: none;
                color: var(--text-secondary, #6b7280);
                font-size: var(--font-size-sm);
                font-weight: 500;
                transition: all 0.2s ease;
                min-height: var(--touch-target-min);
                border-radius: 6px;
                margin-bottom: var(--spacing-xs);
            }
            
            .drawer-nav-item:hover,
            .drawer-nav-item.active {
                color: var(--primary-600, #2563eb);
                background: var(--primary-50, #eff6ff);
            }
            
            .hamburger-menu {
                display: none;
                flex-direction: column;
                justify-content: space-around;
                width: 30px;
                height: 30px;
                background: none;
                border: none;
                cursor: pointer;
                padding: 0;
            }
            
            .hamburger-menu span {
                width: 100%;
                height: 3px;
                background: var(--text-primary, #111827);
                border-radius: 2px;
                transition: all 0.3s ease;
            }
            
            .hamburger-menu.active span:nth-child(1) {
                transform: rotate(45deg) translate(5px, 5px);
            }
            
            .hamburger-menu.active span:nth-child(2) {
                opacity: 0;
            }
            
            .hamburger-menu.active span:nth-child(3) {
                transform: rotate(-45deg) translate(7px, -6px);
            }
            
            @media (max-width: 767.98px) {
                .hamburger-menu {
                    display: flex;
                }
                
                .desktop-nav {
                    display: none;
                }
            }
            
            @media (min-width: 768px) {
                .mobile-nav {
                    display: none;
                }
                
                .hamburger-menu {
                    display: none;
                }
            }
            
            @media (min-width: 1024px) {
                .tablet-nav {
                    display: none;
                }
                
                .desktop-nav {
                    display: block;
                }
                
                .main-content {
                    margin-left: 250px;
                }
            }
        `;

        document.head.appendChild(style);
    }

    /**
     * Настройка touch оптимизаций
     */
    setupTouchOptimizations() {
        // Улучшаем touch события
        document.addEventListener('touchstart', (e) => {
            // Добавляем класс для touch устройств
            document.body.classList.add('touch-device');
        }, { once: true });

        // Убираем hover эффекты на touch устройствах
        document.addEventListener('touchstart', () => {
            document.body.classList.add('no-hover');
        });

        document.addEventListener('touchend', () => {
            setTimeout(() => {
                document.body.classList.remove('no-hover');
            }, 300);
        });
    }

    /**
     * Настройка viewport handling
     */
    setupViewportHandling() {
        // Обработка изменения viewport
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover');
        }

        // Обработка safe areas
        this.setupSafeAreas();
    }

    /**
     * Настройка safe areas
     */
    setupSafeAreas() {
        const style = document.createElement('style');
        style.textContent = `
            @supports (padding: max(0px)) {
                .mobile-nav {
                    padding-bottom: max(var(--spacing-sm), env(safe-area-inset-bottom));
                }
                
                .navbar {
                    padding-top: max(var(--spacing-sm), env(safe-area-inset-top));
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Обновление стилей
     */
    updateStyles() {
        // Обновляем CSS переменные в зависимости от устройства
        const root = document.documentElement;

        if (this.isMobile) {
            root.style.setProperty('--touch-target-min', '44px');
            root.style.setProperty('--touch-target-comfortable', '48px');
        } else {
            root.style.setProperty('--touch-target-min', '32px');
            root.style.setProperty('--touch-target-comfortable', '36px');
        }
    }

    /**
     * Получение текущего breakpoint
     */
    getCurrentBreakpoint() {
        return this.currentBreakpoint;
    }

    /**
     * Проверка мобильного устройства
     */
    isMobileDevice() {
        return this.isMobile;
    }

    /**
     * Проверка планшета
     */
    isTabletDevice() {
        return this.isTablet;
    }

    /**
     * Проверка десктопа
     */
    isDesktopDevice() {
        return this.isDesktop;
    }

    /**
     * Очистка
     */
    cleanup() {
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('orientationchange', this.handleResize);

        this.removeCurrentNavigation();

        const drawer = document.querySelector('.drawer');
        if (drawer) {
            drawer.remove();
        }
    }
}

// Создаем глобальный экземпляр
window.MobileNavigationManager = new MobileNavigationManager();

// Экспорт для глобального доступа
window.MobileNav = {
    navigateTo: (page) => window.MobileNavigationManager.navigateToPage(page),
    openDrawer: () => window.MobileNavigationManager.openDrawer(),
    closeDrawer: () => window.MobileNavigationManager.closeDrawer(),
    toggleDrawer: () => window.MobileNavigationManager.toggleDrawer(),
    isMobile: () => window.MobileNavigationManager.isMobileDevice(),
    isTablet: () => window.MobileNavigationManager.isTabletDevice(),
    isDesktop: () => window.MobileNavigationManager.isDesktopDevice(),
    getBreakpoint: () => window.MobileNavigationManager.getCurrentBreakpoint()
};
