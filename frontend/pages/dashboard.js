// Dashboard page module
class DashboardModule {
    constructor() {
        this.analyticsService = new AnalyticsService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Dashboard module...');

        try {
            await this.loadDashboardData();
            this.bindEvents();
            this.isInitialized = true;
            console.log('Dashboard module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Dashboard module:', error);
            throw error;
        }
    }

    async loadDashboardData() {
        try {
            // Mock data for demo purposes
            const dashboardData = {
                stats: {
                    totalUsers: 1250,
                    totalProducts: 89,
                    totalOrders: 456,
                    totalRevenue: 125000
                },
                recentActivity: [
                    { type: 'user_registration', user: 'John Doe', time: '2 minutes ago' },
                    { type: 'order_placed', user: 'Jane Smith', amount: 299.99, time: '5 minutes ago' },
                    { type: 'product_added', user: 'Admin', product: 'New Product', time: '1 hour ago' }
                ],
                charts: {
                    revenue: [12000, 15000, 18000, 22000, 25000],
                    users: [100, 150, 200, 250, 300]
                }
            };

            this.renderDashboard(dashboardData);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.renderError('Failed to load dashboard data');
        }
    }

    renderDashboard(data) {
        const dashboardElement = document.getElementById('dashboard-page');
        if (!dashboardElement) return;

        dashboardElement.innerHTML = `
            <div class="page-header">
                <h1>Dashboard</h1>
                <p>Обзор всех модулей платформы</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-content">
                        <h3>${data.stats.totalUsers}</h3>
                        <p>Пользователи</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🛍️</div>
                    <div class="stat-content">
                        <h3>${data.stats.totalProducts}</h3>
                        <p>Товары</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📦</div>
                    <div class="stat-content">
                        <h3>${data.stats.totalOrders}</h3>
                        <p>Заказы</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">💰</div>
                    <div class="stat-content">
                        <h3>$${data.stats.totalRevenue.toLocaleString()}</h3>
                        <p>Доход</p>
                    </div>
                </div>
            </div>

            <div class="dashboard-content">
                <div class="dashboard-section">
                    <h2>Модули системы</h2>
                    <div class="modules-grid">
                        <div class="module-card" data-module="ecommerce">
                            <div class="module-icon">🛒</div>
                            <h3>E-commerce</h3>
                            <p>Интернет-магазин с полным функционалом</p>
                            <div class="module-stats">
                                <span>${data.stats.totalProducts} товаров</span>
                                <span>${data.stats.totalOrders} заказов</span>
                            </div>
                            <button class="btn btn-primary module-btn" data-module="ecommerce">Открыть</button>
                        </div>
                        
                        <div class="module-card" data-module="social">
                            <div class="module-icon">👥</div>
                            <h3>Social Network</h3>
                            <p>Социальная сеть с постами и чатами</p>
                            <div class="module-stats">
                                <span>${data.stats.totalUsers} пользователей</span>
                                <span>0 постов</span>
                            </div>
                            <button class="btn btn-primary module-btn" data-module="social">Открыть</button>
                        </div>
                        
                        <div class="module-card" data-module="tasks">
                            <div class="module-icon">✅</div>
                            <h3>Task Management</h3>
                            <p>Система управления задачами</p>
                            <div class="module-stats">
                                <span>0 проектов</span>
                                <span>0 выполнено</span>
                            </div>
                            <button class="btn btn-primary module-btn" data-module="tasks">Открыть</button>
                        </div>
                        
                        <div class="module-card" data-module="content">
                            <div class="module-icon">📝</div>
                            <h3>Content Management</h3>
                            <p>Система управления контентом</p>
                            <div class="module-stats">
                                <span>0 статей</span>
                                <span>0 просмотров</span>
                            </div>
                            <button class="btn btn-primary module-btn" data-module="content">Открыть</button>
                        </div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <h2>Последняя активность</h2>
                    <div class="activity-list">
                        ${data.recentActivity.map(activity => `
                            <div class="activity-item">
                                <div class="activity-icon">${this.getActivityIcon(activity.type)}</div>
                                <div class="activity-content">
                                    <p>${this.formatActivity(activity)}</p>
                                    <span class="activity-time">${activity.time}</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    getActivityIcon(type) {
        const icons = {
            'user_registration': '👤',
            'order_placed': '🛒',
            'product_added': '➕',
            'default': '📝'
        };
        return icons[type] || icons.default;
    }

    formatActivity(activity) {
        switch (activity.type) {
            case 'user_registration':
                return `Новый пользователь: ${activity.user}`;
            case 'order_placed':
                return `Заказ от ${activity.user}: $${activity.amount}`;
            case 'product_added':
                return `${activity.user} добавил товар: ${activity.product}`;
            default:
                return 'Неизвестная активность';
        }
    }

    renderError(message) {
        const dashboardElement = document.getElementById('dashboard-page');
        if (!dashboardElement) return;

        dashboardElement.innerHTML = `
            <div class="page-header">
                <h1>Dashboard</h1>
                <p>Обзор всех модулей платформы</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.App.modules.dashboard.loadDashboardData()">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Module navigation
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('module-btn')) {
                const module = e.target.dataset.module;
                this.navigateToModule(module);
            }
        });
    }

    navigateToModule(module) {
        if (window.App && window.App.navigation) {
            window.App.navigation.goToPage(module);
        }
    }

    onPageShow() {
        console.log('Dashboard page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.DashboardModule = DashboardModule;
