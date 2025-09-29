// Analytics page module
class AnalyticsPage {
    constructor() {
        this.currentFilters = {};
        this.charts = {};
        this.init();
    }

    async init() {
        await this.loadDashboard();
        this.setupEventListeners();
    }

    async loadDashboard() {
        try {
            this.showLoading();
            const data = await window.ApiService.getAnalyticsDashboard();
            this.renderDashboard(data);
        } catch (error) {
            console.error('Failed to load analytics dashboard:', error);
            this.showError('Не удалось загрузить данные аналитики');
        } finally {
            this.hideLoading();
        }
    }

    renderDashboard(data) {
        const container = document.getElementById('analytics-container');
        if (!container) return;

        container.innerHTML = `
            <div class="analytics-header">
                <h1>Аналитика</h1>
                <div class="analytics-filters">
                    <select id="timeRange" class="form-control">
                        <option value="7d">Последние 7 дней</option>
                        <option value="30d" selected>Последние 30 дней</option>
                        <option value="90d">Последние 90 дней</option>
                        <option value="1y">Последний год</option>
                    </select>
                    <select id="metricType" class="form-control">
                        <option value="all" selected>Все метрики</option>
                        <option value="users">Пользователи</option>
                        <option value="revenue">Доходы</option>
                        <option value="conversion">Конверсия</option>
                    </select>
                </div>
            </div>

            <div class="analytics-grid">
                <div class="metric-card">
                    <div class="metric-icon">👥</div>
                    <div class="metric-content">
                        <h3>Всего пользователей</h3>
                        <div class="metric-value">${data.totalUsers || 0}</div>
                        <div class="metric-change ${data.usersChange >= 0 ? 'positive' : 'negative'}">
                            ${data.usersChange >= 0 ? '+' : ''}${data.usersChange || 0}%
                        </div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-icon">💰</div>
                    <div class="metric-content">
                        <h3>Общий доход</h3>
                        <div class="metric-value">$${data.totalRevenue || 0}</div>
                        <div class="metric-change ${data.revenueChange >= 0 ? 'positive' : 'negative'}">
                            ${data.revenueChange >= 0 ? '+' : ''}${data.revenueChange || 0}%
                        </div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-icon">📈</div>
                    <div class="metric-content">
                        <h3>Конверсия</h3>
                        <div class="metric-value">${data.conversionRate || 0}%</div>
                        <div class="metric-change ${data.conversionChange >= 0 ? 'positive' : 'negative'}">
                            ${data.conversionChange >= 0 ? '+' : ''}${data.conversionChange || 0}%
                        </div>
                    </div>
                </div>

                <div class="metric-card">
                    <div class="metric-icon">🛒</div>
                    <div class="metric-content">
                        <h3>Заказы</h3>
                        <div class="metric-value">${data.totalOrders || 0}</div>
                        <div class="metric-change ${data.ordersChange >= 0 ? 'positive' : 'negative'}">
                            ${data.ordersChange >= 0 ? '+' : ''}${data.ordersChange || 0}%
                        </div>
                    </div>
                </div>
            </div>

            <div class="charts-section">
                <div class="chart-container">
                    <h3>Динамика пользователей</h3>
                    <canvas id="usersChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Динамика доходов</h3>
                    <canvas id="revenueChart"></canvas>
                </div>
            </div>

            <div class="reports-section">
                <h3>Отчеты</h3>
                <div class="reports-grid">
                    <div class="report-card">
                        <h4>Отчет по пользователям</h4>
                        <p>Детальная аналитика поведения пользователей</p>
                        <button class="btn btn-primary" onclick="analyticsPage.generateReport('users')">
                            Создать отчет
                        </button>
                    </div>
                    <div class="report-card">
                        <h4>Отчет по продажам</h4>
                        <p>Анализ продаж и доходности</p>
                        <button class="btn btn-primary" onclick="analyticsPage.generateReport('sales')">
                            Создать отчет
                        </button>
                    </div>
                    <div class="report-card">
                        <h4>Отчет по конверсии</h4>
                        <p>Анализ воронки конверсии</p>
                        <button class="btn btn-primary" onclick="analyticsPage.generateReport('conversion')">
                            Создать отчет
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.renderCharts(data);
    }

    renderCharts(data) {
        // Render users chart
        const usersCtx = document.getElementById('usersChart');
        if (usersCtx && data.usersChart) {
            this.charts.users = new Chart(usersCtx, {
                type: 'line',
                data: data.usersChart,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Количество пользователей по дням'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Render revenue chart
        const revenueCtx = document.getElementById('revenueChart');
        if (revenueCtx && data.revenueChart) {
            this.charts.revenue = new Chart(revenueCtx, {
                type: 'bar',
                data: data.revenueChart,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Доходы по дням'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }

    setupEventListeners() {
        // Time range filter
        const timeRange = document.getElementById('timeRange');
        if (timeRange) {
            timeRange.addEventListener('change', (e) => {
                this.currentFilters.timeRange = e.target.value;
                this.loadDashboard();
            });
        }

        // Metric type filter
        const metricType = document.getElementById('metricType');
        if (metricType) {
            metricType.addEventListener('change', (e) => {
                this.currentFilters.metricType = e.target.value;
                this.loadDashboard();
            });
        }
    }

    async generateReport(type) {
        try {
            this.showLoading();
            const report = await window.ApiService.getAnalyticsReports({
                type: type,
                ...this.currentFilters
            });

            // Create and download report
            this.downloadReport(report, type);
        } catch (error) {
            console.error('Failed to generate report:', error);
            this.showError('Не удалось создать отчет');
        } finally {
            this.hideLoading();
        }
    }

    downloadReport(report, type) {
        const blob = new Blob([JSON.stringify(report, null, 2)], {
            type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytics-report-${type}-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showLoading() {
        const container = document.getElementById('analytics-container');
        if (container) {
            container.innerHTML = '<div class="loading">Загрузка аналитики...</div>';
        }
    }

    hideLoading() {
        // Loading will be replaced by actual content
    }

    showError(message) {
        const container = document.getElementById('analytics-container');
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <h3>Ошибка</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="analyticsPage.loadDashboard()">
                        Попробовать снова
                    </button>
                </div>
            `;
        }
    }
}

// Initialize analytics page
let analyticsPage;
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('analytics-container')) {
        analyticsPage = new AnalyticsPage();
    }
});

// Export for global access
window.AnalyticsPage = AnalyticsPage;