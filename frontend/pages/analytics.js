// Analytics page module
class AnalyticsModule {
    constructor() {
        this.analyticsService = new AnalyticsService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Analytics module...');

        try {
            await this.loadAnalyticsData();
            this.bindEvents();
            this.isInitialized = true;
            console.log('Analytics module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Analytics module:', error);
            throw error;
        }
    }

    async loadAnalyticsData() {
        try {
            // Mock data for demo
            const analyticsData = {
                overview: {
                    totalUsers: 1250,
                    activeUsers: 890,
                    totalRevenue: 125000,
                    conversionRate: 3.2
                },
                charts: {
                    userGrowth: [100, 150, 200, 250, 300, 350, 400],
                    revenue: [12000, 15000, 18000, 22000, 25000, 28000, 30000],
                    pageViews: [5000, 5500, 6000, 6500, 7000, 7500, 8000]
                },
                topPages: [
                    { path: '/dashboard', views: 1250, uniqueViews: 890 },
                    { path: '/ecommerce', views: 980, uniqueViews: 650 },
                    { path: '/social', views: 750, uniqueViews: 520 },
                    { path: '/tasks', views: 620, uniqueViews: 450 }
                ],
                recentEvents: [
                    { type: 'user_registration', user: 'John Doe', timestamp: new Date().toISOString() },
                    { type: 'purchase', user: 'Jane Smith', amount: 299.99, timestamp: new Date(Date.now() - 3600000).toISOString() },
                    { type: 'page_view', user: 'Bob Johnson', page: '/ecommerce', timestamp: new Date(Date.now() - 7200000).toISOString() }
                ]
            };

            this.renderAnalytics(analyticsData);
        } catch (error) {
            console.error('Failed to load analytics data:', error);
            this.renderError('Failed to load analytics data');
        }
    }

    renderAnalytics(data) {
        const analyticsElement = document.getElementById('analytics-page');
        if (!analyticsElement) return;

        analyticsElement.innerHTML = `
            <div class="page-header">
                <h1>Analytics & Dashboard</h1>
                <p>Аналитика и отчеты системы</p>
            </div>

            <div class="analytics-content">
                <div class="analytics-overview">
                    <div class="overview-stats">
                        <div class="stat-card">
                            <div class="stat-icon">👥</div>
                            <div class="stat-content">
                                <h3>${data.overview.totalUsers.toLocaleString()}</h3>
                                <p>Всего пользователей</p>
                                <span class="stat-change positive">+12%</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">🟢</div>
                            <div class="stat-content">
                                <h3>${data.overview.activeUsers.toLocaleString()}</h3>
                                <p>Активных пользователей</p>
                                <span class="stat-change positive">+8%</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">💰</div>
                            <div class="stat-content">
                                <h3>$${data.overview.totalRevenue.toLocaleString()}</h3>
                                <p>Общий доход</p>
                                <span class="stat-change positive">+15%</span>
                            </div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon">📈</div>
                            <div class="stat-content">
                                <h3>${data.overview.conversionRate}%</h3>
                                <p>Конверсия</p>
                                <span class="stat-change negative">-2%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="analytics-charts">
                    <div class="chart-section">
                        <h2>Графики</h2>
                        <div class="charts-grid">
                            <div class="chart-card">
                                <h3>Рост пользователей</h3>
                                <div class="chart-placeholder">
                                    <canvas id="userGrowthChart" width="400" height="200"></canvas>
                                </div>
                            </div>
                            <div class="chart-card">
                                <h3>Доходы</h3>
                                <div class="chart-placeholder">
                                    <canvas id="revenueChart" width="400" height="200"></canvas>
                                </div>
                            </div>
                            <div class="chart-card">
                                <h3>Просмотры страниц</h3>
                                <div class="chart-placeholder">
                                    <canvas id="pageViewsChart" width="400" height="200"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="analytics-details">
                    <div class="details-grid">
                        <div class="detail-card">
                            <h3>Топ страницы</h3>
                            <div class="top-pages-list">
                                ${data.topPages.map((page, index) => `
                                    <div class="page-item">
                                        <div class="page-rank">${index + 1}</div>
                                        <div class="page-info">
                                            <div class="page-path">${page.path}</div>
                                            <div class="page-stats">
                                                <span>${page.views} просмотров</span>
                                                <span>${page.uniqueViews} уникальных</span>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <div class="detail-card">
                            <h3>Последние события</h3>
                            <div class="events-list">
                                ${data.recentEvents.map(event => `
                                    <div class="event-item">
                                        <div class="event-icon">${this.getEventIcon(event.type)}</div>
                                        <div class="event-content">
                                            <p>${this.formatEvent(event)}</p>
                                            <span class="event-time">${this.formatTime(event.timestamp)}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="analytics-actions">
                    <button class="btn btn-primary" id="generate-report-btn">Создать отчет</button>
                    <button class="btn btn-secondary" id="export-data-btn">Экспорт данных</button>
                    <button class="btn btn-secondary" id="configure-alerts-btn">Настроить уведомления</button>
                </div>
            </div>
        `;
    }

    getEventIcon(type) {
        const icons = {
            'user_registration': '👤',
            'purchase': '🛒',
            'page_view': '👁️',
            'default': '📝'
        };
        return icons[type] || icons.default;
    }

    formatEvent(event) {
        switch (event.type) {
            case 'user_registration':
                return `Новый пользователь: ${event.user}`;
            case 'purchase':
                return `Покупка от ${event.user}: $${event.amount}`;
            case 'page_view':
                return `${event.user} посетил ${event.page}`;
            default:
                return 'Неизвестное событие';
        }
    }

    formatTime(timestamp) {
        const now = new Date();
        const eventTime = new Date(timestamp);
        const diffInMinutes = Math.floor((now - eventTime) / (1000 * 60));

        if (diffInMinutes < 1) return 'только что';
        if (diffInMinutes < 60) return `${diffInMinutes} мин назад`;

        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours} ч назад`;

        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays} дн назад`;
    }

    renderError(message) {
        const analyticsElement = document.getElementById('analytics-page');
        if (!analyticsElement) return;

        analyticsElement.innerHTML = `
            <div class="page-header">
                <h1>Analytics & Dashboard</h1>
                <p>Аналитика и отчеты системы</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" data-action="retry-load">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Analytics actions
        document.addEventListener('click', (e) => {
            if (e.target.id === 'generate-report-btn') {
                this.generateReport();
            } else if (e.target.id === 'export-data-btn') {
                this.exportData();
            } else if (e.target.id === 'configure-alerts-btn') {
                this.configureAlerts();
            } else if (e.target.dataset.action === 'retry-load') {
                this.loadAnalyticsData();
            }
        });
    }

    generateReport() {
        console.log('Generating report...');
        Toast.info('Функция создания отчетов будет реализована в следующих версиях');
    }

    exportData() {
        console.log('Exporting data...');
        Toast.info('Функция экспорта данных будет реализована в следующих версиях');
    }

    configureAlerts() {
        console.log('Configuring alerts...');
        Toast.info('Функция настройки уведомлений будет реализована в следующих версиях');
    }

    onPageShow() {
        console.log('Analytics page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.AnalyticsModule = AnalyticsModule;
