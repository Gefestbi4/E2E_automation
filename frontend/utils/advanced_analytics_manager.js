/**
 * Advanced Analytics Manager
 * Расширенная аналитика, отчеты, метрики, дашборды
 */

class AdvancedAnalyticsManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.dashboardData = null;
        this.userAnalytics = null;
        this.reports = [];
        this.isLoading = false;
    }

    /**
     * Инициализация системы аналитики
     */
    init() {
        this.createAnalyticsUI();
        this.setupEventListeners();
        this.loadDashboardData();
        console.log('📊 Advanced Analytics Manager initialized');
    }

    /**
     * Создание UI для аналитики
     */
    createAnalyticsUI() {
        const analyticsContainer = document.createElement('div');
        analyticsContainer.className = 'advanced-analytics-container';
        analyticsContainer.innerHTML = `
            <div class="analytics-header">
                <h2><i class="fas fa-chart-line"></i> Расширенная Аналитика</h2>
                <div class="analytics-actions">
                    <button id="refresh-analytics-btn" class="btn btn-primary">
                        <i class="fas fa-sync"></i> Обновить
                    </button>
                    <button id="export-data-btn" class="btn btn-secondary">
                        <i class="fas fa-download"></i> Экспорт
                    </button>
                </div>
            </div>

            <div class="analytics-content">
                <div class="analytics-sidebar">
                    <div class="analytics-nav">
                        <button class="nav-btn active" data-tab="dashboard">
                            <i class="fas fa-tachometer-alt"></i> Дашборд
                        </button>
                        <button class="nav-btn" data-tab="user">
                            <i class="fas fa-user"></i> Пользователь
                        </button>
                        <button class="nav-btn" data-tab="content">
                            <i class="fas fa-file-alt"></i> Контент
                        </button>
                        <button class="nav-btn" data-tab="business">
                            <i class="fas fa-briefcase"></i> Бизнес
                        </button>
                        <button class="nav-btn" data-tab="performance">
                            <i class="fas fa-server"></i> Производительность
                        </button>
                        <button class="nav-btn" data-tab="reports">
                            <i class="fas fa-file-pdf"></i> Отчеты
                        </button>
                    </div>
                </div>

                <div class="analytics-main">
                    <!-- Дашборд -->
                    <div id="dashboard-tab" class="analytics-tab active">
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <h3>Пользователи</h3>
                                <div class="metric-value" id="total-users">--</div>
                                <div class="metric-change" id="users-change">--</div>
                            </div>
                            <div class="metric-card">
                                <h3>Контент</h3>
                                <div class="metric-value" id="total-posts">--</div>
                                <div class="metric-change" id="posts-change">--</div>
                            </div>
                            <div class="metric-card">
                                <h3>Выручка</h3>
                                <div class="metric-value" id="total-revenue">--</div>
                                <div class="metric-change" id="revenue-change">--</div>
                            </div>
                            <div class="metric-card">
                                <h3>Вовлеченность</h3>
                                <div class="metric-value" id="engagement-rate">--</div>
                                <div class="metric-change" id="engagement-change">--</div>
                            </div>
                        </div>
                        <div class="charts-container">
                            <div class="chart-card">
                                <h3>Активность пользователей</h3>
                                <canvas id="users-chart"></canvas>
                            </div>
                            <div class="chart-card">
                                <h3>Топ контент</h3>
                                <div id="top-content-list"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Пользовательская аналитика -->
                    <div id="user-tab" class="analytics-tab">
                        <div class="user-analytics-content">
                            <h3>Аналитика пользователя</h3>
                            <div class="user-metrics">
                                <div class="metric-item">
                                    <span class="metric-label">Просмотры профиля:</span>
                                    <span class="metric-value" id="profile-views">--</span>
                                </div>
                                <div class="metric-item">
                                    <span class="metric-label">Создано постов:</span>
                                    <span class="metric-value" id="posts-created">--</span>
                                </div>
                                <div class="metric-item">
                                    <span class="metric-label">Получено лайков:</span>
                                    <span class="metric-value" id="likes-received">--</span>
                                </div>
                                <div class="metric-item">
                                    <span class="metric-label">Социальный рейтинг:</span>
                                    <span class="metric-value" id="social-score">--</span>
                                </div>
                            </div>
                            <div class="behavior-patterns">
                                <h4>Поведенческие паттерны</h4>
                                <div id="behavior-chart"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Аналитика контента -->
                    <div id="content-tab" class="analytics-tab">
                        <div class="content-analytics-content">
                            <h3>Аналитика контента</h3>
                            <div class="content-selector">
                                <select id="content-select" class="form-control">
                                    <option value="1">Python Tutorial</option>
                                    <option value="2">React Guide</option>
                                    <option value="3">ML Basics</option>
                                </select>
                                <button id="load-content-analytics" class="btn btn-primary">Загрузить</button>
                            </div>
                            <div id="content-metrics" class="content-metrics">
                                <div class="loading">Выберите контент для анализа</div>
                            </div>
                        </div>
                    </div>

                    <!-- Бизнес аналитика -->
                    <div id="business-tab" class="analytics-tab">
                        <div class="business-analytics-content">
                            <h3>Бизнес аналитика</h3>
                            <div class="business-metrics">
                                <div class="metric-row">
                                    <div class="metric-item">
                                        <span class="metric-label">Общая выручка:</span>
                                        <span class="metric-value" id="total-revenue-business">--</span>
                                    </div>
                                    <div class="metric-item">
                                        <span class="metric-label">Клиенты:</span>
                                        <span class="metric-value" id="total-customers">--</span>
                                    </div>
                                </div>
                                <div class="metric-row">
                                    <div class="metric-item">
                                        <span class="metric-label">Конверсия:</span>
                                        <span class="metric-value" id="conversion-rate">--</span>
                                    </div>
                                    <div class="metric-item">
                                        <span class="metric-label">Средний чек:</span>
                                        <span class="metric-value" id="avg-order-value">--</span>
                                    </div>
                                </div>
                            </div>
                            <div class="revenue-chart">
                                <h4>Динамика выручки</h4>
                                <canvas id="revenue-chart"></canvas>
                            </div>
                        </div>
                    </div>

                    <!-- Производительность -->
                    <div id="performance-tab" class="analytics-tab">
                        <div class="performance-analytics-content">
                            <h3>Аналитика производительности</h3>
                            <div class="performance-metrics">
                                <div class="metric-card">
                                    <h4>Сервер</h4>
                                    <div class="metric-item">
                                        <span>CPU:</span>
                                        <span id="cpu-usage">--</span>
                                    </div>
                                    <div class="metric-item">
                                        <span>Память:</span>
                                        <span id="memory-usage">--</span>
                                    </div>
                                </div>
                                <div class="metric-card">
                                    <h4>API</h4>
                                    <div class="metric-item">
                                        <span>Время ответа:</span>
                                        <span id="api-response-time">--</span>
                                    </div>
                                    <div class="metric-item">
                                        <span>Ошибки:</span>
                                        <span id="error-rate">--</span>
                                    </div>
                                </div>
                                <div class="metric-card">
                                    <h4>Frontend</h4>
                                    <div class="metric-item">
                                        <span>Загрузка страницы:</span>
                                        <span id="page-load-time">--</span>
                                    </div>
                                    <div class="metric-item">
                                        <span>Отказы:</span>
                                        <span id="bounce-rate">--</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Отчеты -->
                    <div id="reports-tab" class="analytics-tab">
                        <div class="reports-content">
                            <h3>Отчеты</h3>
                            <div class="report-generator">
                                <div class="form-group">
                                    <label>Тип отчета:</label>
                                    <select id="report-type" class="form-control">
                                        <option value="user_activity">Активность пользователя</option>
                                        <option value="content_performance">Производительность контента</option>
                                        <option value="business_overview">Бизнес обзор</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Период:</label>
                                    <select id="report-period" class="form-control">
                                        <option value="7d">7 дней</option>
                                        <option value="30d">30 дней</option>
                                        <option value="90d">90 дней</option>
                                    </select>
                                </div>
                                <button id="generate-report-btn" class="btn btn-primary">Сгенерировать отчет</button>
                            </div>
                            <div id="report-results" class="report-results">
                                <div class="no-content">Выберите параметры и сгенерируйте отчет</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.addStyles();
        document.body.appendChild(analyticsContainer);
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .advanced-analytics-container {
                max-width: 1400px;
                margin: 20px auto;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .analytics-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }

            .analytics-content {
                display: grid;
                grid-template-columns: 200px 1fr;
                gap: 30px;
            }

            .analytics-sidebar {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
            }

            .analytics-nav {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .nav-btn {
                padding: 12px 16px;
                border: none;
                background: transparent;
                color: #666;
                cursor: pointer;
                border-radius: 6px;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                text-align: left;
            }

            .nav-btn:hover {
                background: #e9ecef;
                color: #333;
            }

            .nav-btn.active {
                background: #007bff;
                color: white;
            }

            .analytics-main {
                background: white;
                border-radius: 8px;
                padding: 30px;
            }

            .analytics-tab {
                display: none;
            }

            .analytics-tab.active {
                display: block;
            }

            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }

            .metric-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #007bff;
            }

            .metric-card h3 {
                margin: 0 0 10px 0;
                color: #333;
                font-size: 14px;
            }

            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
                margin-bottom: 5px;
            }

            .metric-change {
                font-size: 12px;
                color: #28a745;
            }

            .charts-container {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 20px;
            }

            .chart-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
            }

            .chart-card h3 {
                margin: 0 0 15px 0;
                color: #333;
            }

            .user-metrics, .business-metrics {
                display: grid;
                gap: 15px;
                margin-bottom: 30px;
            }

            .metric-item {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }

            .metric-label {
                color: #666;
            }

            .metric-value {
                font-weight: bold;
                color: #333;
            }

            .performance-metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }

            .report-generator {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }

            .report-results {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                min-height: 200px;
            }

            .btn {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }

            .btn-primary {
                background: #007bff;
                color: white;
            }

            .btn-primary:hover {
                background: #0056b3;
            }

            .btn-secondary {
                background: #6c757d;
                color: white;
            }

            .btn-secondary:hover {
                background: #545b62;
            }

            .form-control {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }

            .form-group {
                margin-bottom: 15px;
            }

            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #555;
            }

            .loading {
                text-align: center;
                color: #666;
                padding: 20px;
            }

            .no-content {
                text-align: center;
                color: #999;
                padding: 40px;
                font-style: italic;
            }

            @media (max-width: 768px) {
                .analytics-content {
                    grid-template-columns: 1fr;
                }
                
                .analytics-sidebar {
                    order: 2;
                }
                
                .analytics-nav {
                    flex-direction: row;
                    overflow-x: auto;
                }
                
                .charts-container {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Навигация по табам
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Обновление данных
        document.getElementById('refresh-analytics-btn').addEventListener('click', () => {
            this.loadDashboardData();
        });

        // Экспорт данных
        document.getElementById('export-data-btn').addEventListener('click', () => {
            this.exportData();
        });

        // Загрузка аналитики контента
        document.getElementById('load-content-analytics').addEventListener('click', () => {
            this.loadContentAnalytics();
        });

        // Генерация отчета
        document.getElementById('generate-report-btn').addEventListener('click', () => {
            this.generateReport();
        });
    }

    /**
     * Переключение табов
     */
    switchTab(tabName) {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.analytics-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Загружаем данные для активного таба
        if (tabName === 'user') {
            this.loadUserAnalytics();
        } else if (tabName === 'business') {
            this.loadBusinessAnalytics();
        } else if (tabName === 'performance') {
            this.loadPerformanceAnalytics();
        }
    }

    /**
     * Загрузка данных дашборда
     */
    async loadDashboardData() {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/analytics/advanced/dashboard`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.dashboardData = data.metrics;
            this.renderDashboardData();

        } catch (error) {
            this.showError(`Ошибка загрузки данных дашборда: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Отображение данных дашборда
     */
    renderDashboardData() {
        if (!this.dashboardData) return;

        const overview = this.dashboardData.overview;

        document.getElementById('total-users').textContent = overview.total_users.toLocaleString();
        document.getElementById('users-change').textContent = `+${overview.growth_rate}%`;

        document.getElementById('total-posts').textContent = overview.total_posts.toLocaleString();
        document.getElementById('posts-change').textContent = '+5.2%';

        document.getElementById('total-revenue').textContent = `$${overview.revenue.toLocaleString()}`;
        document.getElementById('revenue-change').textContent = `+${overview.growth_rate}%`;

        document.getElementById('engagement-rate').textContent = `${(overview.growth_rate * 0.1).toFixed(1)}%`;
        document.getElementById('engagement-change').textContent = '+2.1%';

        // Отображаем топ контент
        const topContent = this.dashboardData.content_performance.top_content;
        const topContentList = document.getElementById('top-content-list');
        topContentList.innerHTML = topContent.map(item => `
            <div class="content-item">
                <div class="content-title">${item.title}</div>
                <div class="content-stats">
                    <span>${item.views} просмотров</span>
                    <span>${(item.engagement * 100).toFixed(1)}% вовлеченность</span>
                </div>
            </div>
        `).join('');
    }

    /**
     * Загрузка пользовательской аналитики
     */
    async loadUserAnalytics() {
        try {
            const response = await fetch(`${this.apiBase}/api/analytics/advanced/user`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.userAnalytics = data.analytics;
            this.renderUserAnalytics();

        } catch (error) {
            this.showError(`Ошибка загрузки пользовательской аналитики: ${error.message}`);
        }
    }

    /**
     * Отображение пользовательской аналитики
     */
    renderUserAnalytics() {
        if (!this.userAnalytics) return;

        const profileViews = this.userAnalytics.profile_views;
        const contentActivity = this.userAnalytics.content_activity;
        const socialActivity = this.userAnalytics.social_activity;

        document.getElementById('profile-views').textContent = profileViews.total.toLocaleString();
        document.getElementById('posts-created').textContent = contentActivity.posts_created;
        document.getElementById('likes-received').textContent = contentActivity.posts_liked;
        document.getElementById('social-score').textContent = socialActivity.social_score;
    }

    /**
     * Загрузка аналитики контента
     */
    async loadContentAnalytics() {
        const contentId = document.getElementById('content-select').value;

        try {
            const response = await fetch(`${this.apiBase}/api/analytics/advanced/content/${contentId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderContentAnalytics(data.analytics);

        } catch (error) {
            this.showError(`Ошибка загрузки аналитики контента: ${error.message}`);
        }
    }

    /**
     * Отображение аналитики контента
     */
    renderContentAnalytics(analytics) {
        const container = document.getElementById('content-metrics');
        const performance = analytics.performance;

        container.innerHTML = `
            <div class="content-performance">
                <h4>Производительность</h4>
                <div class="metric-row">
                    <div class="metric-item">
                        <span>Просмотры:</span>
                        <span>${performance.views.toLocaleString()}</span>
                    </div>
                    <div class="metric-item">
                        <span>Лайки:</span>
                        <span>${performance.likes.toLocaleString()}</span>
                    </div>
                </div>
                <div class="metric-row">
                    <div class="metric-item">
                        <span>Комментарии:</span>
                        <span>${performance.comments.toLocaleString()}</span>
                    </div>
                    <div class="metric-item">
                        <span>Поделились:</span>
                        <span>${performance.shares.toLocaleString()}</span>
                    </div>
                </div>
                <div class="metric-item">
                    <span>Вовлеченность:</span>
                    <span>${(performance.engagement_rate * 100).toFixed(1)}%</span>
                </div>
            </div>
        `;
    }

    /**
     * Загрузка бизнес аналитики
     */
    async loadBusinessAnalytics() {
        try {
            const response = await fetch(`${this.apiBase}/api/analytics/advanced/business`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderBusinessAnalytics(data.analytics);

        } catch (error) {
            this.showError(`Ошибка загрузки бизнес аналитики: ${error.message}`);
        }
    }

    /**
     * Отображение бизнес аналитики
     */
    renderBusinessAnalytics(analytics) {
        const revenue = analytics.revenue;
        const customers = analytics.customers;

        document.getElementById('total-revenue-business').textContent = `$${revenue.total.toLocaleString()}`;
        document.getElementById('total-customers').textContent = customers.total_customers.toLocaleString();
        document.getElementById('conversion-rate').textContent = `${(analytics.ecommerce_metrics.conversion_rate * 100).toFixed(1)}%`;
        document.getElementById('avg-order-value').textContent = `$${analytics.ecommerce_metrics.average_order_value}`;
    }

    /**
     * Загрузка аналитики производительности
     */
    async loadPerformanceAnalytics() {
        try {
            const response = await fetch(`${this.apiBase}/api/analytics/advanced/performance`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderPerformanceAnalytics(data.analytics);

        } catch (error) {
            this.showError(`Ошибка загрузки аналитики производительности: ${error.message}`);
        }
    }

    /**
     * Отображение аналитики производительности
     */
    renderPerformanceAnalytics(analytics) {
        const server = analytics.server_performance;
        const api = analytics.api_performance;
        const frontend = analytics.frontend_performance;
        const ux = analytics.user_experience;

        document.getElementById('cpu-usage').textContent = `${server.cpu_usage}%`;
        document.getElementById('memory-usage').textContent = `${server.memory_usage}%`;
        document.getElementById('api-response-time').textContent = `${api.average_response_time}s`;
        document.getElementById('error-rate').textContent = `${(api.error_rate * 100).toFixed(2)}%`;
        document.getElementById('page-load-time').textContent = `${frontend.page_load_time}s`;
        document.getElementById('bounce-rate').textContent = `${(ux.bounce_rate * 100).toFixed(1)}%`;
    }

    /**
     * Генерация отчета
     */
    async generateReport() {
        const reportType = document.getElementById('report-type').value;
        const reportPeriod = document.getElementById('report-period').value;

        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/analytics/advanced/reports`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    report_type: reportType,
                    time_period: reportPeriod
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderReport(data);

        } catch (error) {
            this.showError(`Ошибка генерации отчета: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Отображение отчета
     */
    renderReport(report) {
        const container = document.getElementById('report-results');

        container.innerHTML = `
            <div class="report-header">
                <h4>${report.report_info.type}</h4>
                <p>Период: ${report.report_info.period}</p>
            </div>
            <div class="report-summary">
                <h5>Краткое резюме</h5>
                <pre>${JSON.stringify(report.summary, null, 2)}</pre>
            </div>
            <div class="report-insights">
                <h5>Инсайты</h5>
                <ul>
                    ${report.insights.map(insight => `<li>${insight}</li>`).join('')}
                </ul>
            </div>
            <div class="report-recommendations">
                <h5>Рекомендации</h5>
                <ul>
                    ${report.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    /**
     * Экспорт данных
     */
    async exportData() {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/analytics/advanced/export/user_activity`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            // Создаем и скачиваем файл
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `analytics_export_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.showSuccess('Данные экспортированы успешно');

        } catch (error) {
            this.showError(`Ошибка экспорта: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Показ загрузки
     */
    showLoading(show) {
        const container = document.querySelector('.advanced-analytics-container');
        if (show) {
            container.style.opacity = '0.6';
            container.style.pointerEvents = 'none';
        } else {
            container.style.opacity = '1';
            container.style.pointerEvents = 'auto';
        }
    }

    /**
     * Показ ошибки
     */
    showError(message) {
        if (window.Toast && typeof window.Toast.error === 'function') {
            window.Toast.error(message);
        } else {
            alert(`Ошибка: ${message}`);
        }
    }

    /**
     * Показ успеха
     */
    showSuccess(message) {
        if (window.Toast && typeof window.Toast.success === 'function') {
            window.Toast.success(message);
        } else {
            alert(`Успех: ${message}`);
        }
    }
}

// Экспорт для глобального доступа
console.log('📊 AdvancedAnalyticsManager class defined:', typeof AdvancedAnalyticsManager);
window.AdvancedAnalyticsManager = AdvancedAnalyticsManager;
window.advancedAnalyticsManager = new AdvancedAnalyticsManager();
console.log('📊 AdvancedAnalyticsManager exported to window:', typeof window.AdvancedAnalyticsManager);
