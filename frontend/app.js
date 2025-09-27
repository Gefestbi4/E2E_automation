// Main Application
class App {
    constructor() {
        this.currentPage = 'dashboard';
        this.modules = {};
        this.isInitialized = false;
    }

    async init() {
        try {
            await this.initAuth();
            this.initNavigation();
            await this.initModules();
            this.initTheme();
            this.initDefaultAvatar();
            this.initEventListeners();
            this.isInitialized = true;
            this.hideLoading();
        } catch (error) {
            console.error('Application initialization failed:', error);
            this.showError('Failed to initialize application');
        }
    }

    async initAuth() {
        if (typeof window.AuthService === 'undefined' || !window.AuthService) {
            this.showError('AuthService not loaded');
            throw new Error('AuthService not loaded');
        }

        if (typeof window.AuthService.isAuthenticated !== 'function') {
            this.showError('AuthService.isAuthenticated is not a function');
            throw new Error('AuthService.isAuthenticated is not a function');
        }

        if (!window.AuthService.isAuthenticated()) {
            this.redirectToLogin();
            return;
        }

        try {
            const userData = await window.AuthService.getCurrentUser();
            if (userData) {
                this.updateUserUI(userData);
            } else {
                this.redirectToLogin();
            }
        } catch (error) {
            console.error('Auth verification failed:', error);
            this.redirectToLogin();
        }
    }

    initNavigation() {
        this.navigation = {
            goToPage: (pageName) => {
                console.log('Going to page:', pageName);
                this.currentPage = pageName;
                this.showPage(pageName);
                this.navigation.updateActiveNavItem(pageName);
            },

            updateActiveNavItem: (pageName) => {
                document.querySelectorAll('.navbar-item').forEach(item => {
                    item.classList.remove('active');
                });

                const activeItem = document.querySelector(`[data-page="${pageName}"]`);
                if (activeItem) {
                    activeItem.classList.add('active');
                }
            }
        };
    }

    async initModules() {
        console.log('Initializing modules...');

        this.modules.dashboard = new DashboardModule();
        await this.modules.dashboard.init();
        console.log('Dashboard module initialized');

        this.modules.ecommerce = new EcommerceModule();
        await this.modules.ecommerce.init();
        console.log('Ecommerce module initialized');

        this.modules.social = new SocialModule();
        await this.modules.social.init();
        console.log('Social module initialized');

        this.modules.tasks = new TasksModule();
        await this.modules.tasks.init();
        console.log('Tasks module initialized');

        this.modules.content = new ContentModule();
        await this.modules.content.init();
        console.log('Content module initialized');

        this.modules.analytics = new AnalyticsModule();
        await this.modules.analytics.init();
        console.log('Analytics module initialized');

        console.log('All modules initialized:', Object.keys(this.modules));
    }

    initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    initDefaultAvatar() {
        // Устанавливаем дефолтный аватар для гостя
        const userAvatar = document.getElementById('user-avatar');
        if (userAvatar && !userAvatar.src) {
            AvatarUtils.setDefaultAvatar(userAvatar);
        }
    }

    initEventListeners() {
        // Navigation click handlers
        const navItems = document.querySelectorAll('.navbar-item');
        console.log('Found navbar items:', navItems.length);

        navItems.forEach(item => {
            console.log('Adding click handler to:', item.dataset.page);
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                console.log('Navigation clicked:', page);
                if (page && this.navigation) {
                    this.navigation.goToPage(page);
                } else {
                    console.error('Navigation not available or page not set');
                }
            });
        });

        // User menu toggle
        const userMenu = document.getElementById('user-menu');
        if (userMenu) {
            userMenu.addEventListener('click', (e) => {
                e.stopPropagation();
                const dropdown = document.getElementById('user-dropdown');
                dropdown.classList.toggle('show');
            });
        }

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            const dropdown = document.getElementById('user-dropdown');
            if (dropdown) {
                dropdown.classList.remove('show');
            }
        });

        // Logout handler
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        // Navigation buttons (data-navigate)
        document.querySelectorAll('[data-navigate]').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const page = button.dataset.navigate;
                console.log('Navigation button clicked:', page);
                if (page && this.navigation) {
                    this.navigation.goToPage(page);
                }
            });
        });
    }

    showPage(pageName) {
        console.log('Showing page:', pageName);

        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(`${pageName}-page`);
        console.log('Target page element:', targetPage);

        if (targetPage) {
            targetPage.classList.add('active');
            console.log('Page activated:', pageName);

            // Initialize page if module exists
            if (this.modules[pageName]) {
                console.log('Calling onPageShow for:', pageName);
                this.modules[pageName].onPageShow();
            } else {
                console.log('Module not found for:', pageName);
            }
        } else {
            console.error('Page element not found:', `${pageName}-page`);
        }
    }

    updateUserUI(userData) {
        const userName = document.getElementById('user-name');
        const userAvatar = document.getElementById('user-avatar');

        if (userName) {
            userName.textContent = userData.full_name || userData.email || 'User';
        }

        if (userAvatar) {
            if (userData.avatar_url) {
                // Если есть URL аватара, загружаем его с fallback
                userAvatar.src = userData.avatar_url;
                userAvatar.onerror = () => {
                    AvatarUtils.handleAvatarError(userAvatar, userData.full_name || userData.email);
                };
            } else {
                // Если нет URL аватара, используем встроенный
                AvatarUtils.setInitialsAvatar(userAvatar, userData.full_name || userData.email || 'User');
            }
        }
    }

    redirectToLogin() {
        window.location.href = '/login_new.html';
    }

    async logout() {
        await AuthService.logout();
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Update theme toggle icon
        const themeIcon = document.querySelector('.theme-icon');
        if (themeIcon) {
            themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        }
    }

    showLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('show');
        }
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.remove('show');
        }
    }

    showError(message) {
        console.error('SHOW ERROR:', message);

        // Показываем ошибку в консоли и на странице
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 5px;
            z-index: 10000;
            max-width: 300px;
            font-family: Arial, sans-serif;
        `;
        errorDiv.innerHTML = `
            <strong>Ошибка инициализации:</strong><br>
            ${message}<br>
            <small>Проверьте консоль для подробностей</small>
            <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; color: white; cursor: pointer;">×</button>
        `;
        document.body.appendChild(errorDiv);

        // Автоматически убираем через 10 секунд
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 10000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {

    // Проверяем, что все необходимые скрипты загружены
    const requiredScripts = [
        { name: 'AuthService', check: () => typeof window.AuthService !== 'undefined' && typeof window.AuthService.isAuthenticated === 'function' },
        { name: 'ApiService', check: () => typeof window.ApiService !== 'undefined' },
        { name: 'DashboardModule', check: () => typeof window.DashboardModule !== 'undefined' },
        { name: 'EcommerceModule', check: () => typeof window.EcommerceModule !== 'undefined' },
        { name: 'SocialModule', check: () => typeof window.SocialModule !== 'undefined' },
        { name: 'TasksModule', check: () => typeof window.TasksModule !== 'undefined' },
        { name: 'ContentModule', check: () => typeof window.ContentModule !== 'undefined' },
        { name: 'AnalyticsModule', check: () => typeof window.AnalyticsModule !== 'undefined' }
    ];

    function checkScripts() {
        const missingScripts = requiredScripts.filter(script => !script.check());

        if (missingScripts.length > 0) {
            console.warn('Waiting for scripts:', missingScripts.map(s => s.name).join(', '));
            setTimeout(checkScripts, 100);
            return;
        }

        window.App = new App();
        window.App.init();
    }

    // Начинаем проверку через 100ms
    setTimeout(checkScripts, 100);
});

// Export for global access
window.App = App;