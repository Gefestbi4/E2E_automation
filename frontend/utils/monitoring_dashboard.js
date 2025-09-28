/**
 * Дашборд мониторинга и логирования
 */

class MonitoringDashboard {
    constructor() {
        this.isInitialized = false;
        this.refreshInterval = null;
        this.refreshDelay = 30000; // 30 секунд
        this.dashboardData = null;
        this.charts = {};
    }

    /**
     * Инициализация дашборда мониторинга
     */
    async init() {
        console.log('📊 Initializing Monitoring Dashboard...');

        try {
            // Инициализируем UI
            this.initUI();

            // Загружаем данные
            await this.loadDashboardData();

            // Запускаем автообновление
            this.startAutoRefresh();

            this.isInitialized = true;
            console.log('📊 Monitoring Dashboard initialized successfully');

        } catch (error) {
            console.error('📊 Failed to initialize Monitoring Dashboard:', error);
        }
    }

    /**
     * Инициализация UI
     */
    initUI() {
        // Создаем модальное окно для дашборда мониторинга
        const modalHTML = `
            <div id="monitoring-dashboard-modal" class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-chart-line"></i>
                                Дашборд мониторинга
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <!-- Статус системы -->
                            <div class="row mb-4">
                                <div class="col-12">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Статус системы</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="system-status" class="system-status">
                                                <!-- Статус будет загружен здесь -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Метрики системы -->
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Системные метрики</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="system-metrics" class="metrics-grid">
                                                <!-- Метрики будут загружены здесь -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Метрики приложения</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="application-metrics" class="metrics-grid">
                                                <!-- Метрики будут загружены здесь -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Графики -->
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Использование ресурсов</h6>
                                        </div>
                                        <div class="card-body">
                                            <canvas id="resources-chart" width="400" height="200"></canvas>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Статистика запросов</h6>
                                        </div>
                                        <div class="card-body">
                                            <canvas id="requests-chart" width="400" height="200"></canvas>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Алерты -->
                            <div class="row mb-4">
                                <div class="col-12">
                                    <div class="card">
                                        <div class="card-header d-flex justify-content-between align-items-center">
                                            <h6 class="mb-0">Алерты</h6>
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.monitoringDashboard.refreshAlerts()">
                                                <i class="fas fa-sync"></i>
                                                Обновить
                                            </button>
                                        </div>
                                        <div class="card-body">
                                            <div id="alerts-list" class="alerts-list">
                                                <!-- Алерты будут загружены здесь -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Логи -->
                            <div class="row">
                                <div class="col-12">
                                    <div class="card">
                                        <div class="card-header d-flex justify-content-between align-items-center">
                                            <h6 class="mb-0">Последние логи</h6>
                                            <div class="btn-group" role="group">
                                                <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.monitoringDashboard.filterLogs('all')">
                                                    Все
                                                </button>
                                                <button type="button" class="btn btn-sm btn-outline-danger" onclick="window.monitoringDashboard.filterLogs('ERROR')">
                                                    Ошибки
                                                </button>
                                                <button type="button" class="btn btn-sm btn-outline-warning" onclick="window.monitoringDashboard.filterLogs('WARNING')">
                                                    Предупреждения
                                                </button>
                                            </div>
                                        </div>
                                        <div class="card-body">
                                            <div id="logs-list" class="logs-list">
                                                <!-- Логи будут загружены здесь -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-primary" onclick="window.monitoringDashboard.refreshAll()">
                                <i class="fas fa-sync"></i>
                                Обновить все
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Добавляем модальное окно в DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Добавляем CSS стили
        this.addStyles();
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const styles = `
            <style>
                .metrics-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 1rem;
                }
                
                .metric-item {
                    padding: 0.5rem;
                    border: 1px solid #dee2e6;
                    border-radius: 0.25rem;
                    text-align: center;
                }
                
                .metric-value {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #007bff;
                }
                
                .metric-label {
                    font-size: 0.875rem;
                    color: #6c757d;
                }
                
                .status-healthy {
                    color: #28a745;
                }
                
                .status-warning {
                    color: #ffc107;
                }
                
                .status-unhealthy {
                    color: #dc3545;
                }
                
                .alert-item {
                    padding: 0.75rem;
                    margin-bottom: 0.5rem;
                    border-left: 4px solid;
                    border-radius: 0.25rem;
                }
                
                .alert-critical {
                    border-left-color: #dc3545;
                    background-color: #f8d7da;
                }
                
                .alert-error {
                    border-left-color: #fd7e14;
                    background-color: #fff3cd;
                }
                
                .alert-warning {
                    border-left-color: #ffc107;
                    background-color: #fff3cd;
                }
                
                .log-item {
                    padding: 0.5rem;
                    margin-bottom: 0.25rem;
                    border-radius: 0.25rem;
                    font-family: monospace;
                    font-size: 0.875rem;
                }
                
                .log-debug {
                    background-color: #f8f9fa;
                }
                
                .log-info {
                    background-color: #d1ecf1;
                }
                
                .log-warning {
                    background-color: #fff3cd;
                }
                
                .log-error {
                    background-color: #f8d7da;
                }
                
                .log-critical {
                    background-color: #f5c6cb;
                    font-weight: bold;
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    /**
     * Загрузка данных дашборда
     */
    async loadDashboardData() {
        try {
            const response = await window.ApiService.get('/api/monitoring/dashboard');
            this.dashboardData = response;
            this.updateUI();
        } catch (error) {
            console.error('📊 Failed to load dashboard data:', error);
        }
    }

    /**
     * Обновление UI
     */
    updateUI() {
        this.updateSystemStatus();
        this.updateSystemMetrics();
        this.updateApplicationMetrics();
        this.updateCharts();
        this.updateAlerts();
        this.updateLogs();
    }

    /**
     * Обновление статуса системы
     */
    updateSystemStatus() {
        const container = document.getElementById('system-status');
        if (!container || !this.dashboardData) return;

        const systemMetrics = this.dashboardData.system_metrics;
        const appMetrics = this.dashboardData.application_metrics;

        let status = 'healthy';
        let statusClass = 'status-healthy';
        let issues = [];

        if (systemMetrics) {
            if (systemMetrics.cpu_percent > 80) {
                status = 'warning';
                statusClass = 'status-warning';
                issues.push(`CPU: ${systemMetrics.cpu_percent}%`);
            }

            if (systemMetrics.memory_percent > 85) {
                status = 'warning';
                statusClass = 'status-warning';
                issues.push(`Memory: ${systemMetrics.memory_percent}%`);
            }

            if (systemMetrics.disk_usage_percent > 90) {
                status = 'unhealthy';
                statusClass = 'status-unhealthy';
                issues.push(`Disk: ${systemMetrics.disk_usage_percent}%`);
            }
        }

        if (appMetrics && appMetrics.error_rate > 5) {
            status = 'warning';
            statusClass = 'status-warning';
            issues.push(`Error rate: ${appMetrics.error_rate}%`);
        }

        const statusHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="mb-1 ${statusClass}">${status.toUpperCase()}</h5>
                    <p class="mb-0 text-muted">${issues.length > 0 ? issues.join(', ') : 'All systems operational'}</p>
                </div>
                <div class="text-end">
                    <small class="text-muted">Last updated: ${new Date().toLocaleTimeString()}</small>
                </div>
            </div>
        `;

        container.innerHTML = statusHTML;
    }

    /**
     * Обновление системных метрик
     */
    updateSystemMetrics() {
        const container = document.getElementById('system-metrics');
        if (!container || !this.dashboardData?.system_metrics) return;

        const metrics = this.dashboardData.system_metrics;

        const metricsHTML = `
            <div class="metric-item">
                <div class="metric-value">${metrics.cpu_percent.toFixed(1)}%</div>
                <div class="metric-label">CPU</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.memory_percent.toFixed(1)}%</div>
                <div class="metric-label">Memory</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.disk_usage_percent.toFixed(1)}%</div>
                <div class="metric-label">Disk</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.active_connections}</div>
                <div class="metric-label">Connections</div>
            </div>
        `;

        container.innerHTML = metricsHTML;
    }

    /**
     * Обновление метрик приложения
     */
    updateApplicationMetrics() {
        const container = document.getElementById('application-metrics');
        if (!container || !this.dashboardData?.application_metrics) return;

        const metrics = this.dashboardData.application_metrics;

        const metricsHTML = `
            <div class="metric-item">
                <div class="metric-value">${metrics.total_requests}</div>
                <div class="metric-label">Total Requests</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.successful_requests}</div>
                <div class="metric-label">Successful</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.failed_requests}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">${metrics.error_rate.toFixed(1)}%</div>
                <div class="metric-label">Error Rate</div>
            </div>
        `;

        container.innerHTML = metricsHTML;
    }

    /**
     * Обновление графиков
     */
    updateCharts() {
        // Простые графики без внешних библиотек
        this.updateResourcesChart();
        this.updateRequestsChart();
    }

    /**
     * Обновление графика ресурсов
     */
    updateResourcesChart() {
        const canvas = document.getElementById('resources-chart');
        if (!canvas || !this.dashboardData?.system_metrics) return;

        const ctx = canvas.getContext('2d');
        const metrics = this.dashboardData.system_metrics;

        // Очищаем canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Рисуем простой график
        const data = [metrics.cpu_percent, metrics.memory_percent, metrics.disk_usage_percent];
        const labels = ['CPU', 'Memory', 'Disk'];
        const colors = ['#007bff', '#28a745', '#ffc107'];

        const barWidth = canvas.width / data.length;
        const maxValue = 100;

        data.forEach((value, index) => {
            const barHeight = (value / maxValue) * canvas.height;
            const x = index * barWidth;
            const y = canvas.height - barHeight;

            ctx.fillStyle = colors[index];
            ctx.fillRect(x + 10, y, barWidth - 20, barHeight);

            // Подписи
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(labels[index], x + barWidth / 2, canvas.height - 5);
            ctx.fillText(`${value.toFixed(1)}%`, x + barWidth / 2, y - 5);
        });
    }

    /**
     * Обновление графика запросов
     */
    updateRequestsChart() {
        const canvas = document.getElementById('requests-chart');
        if (!canvas || !this.dashboardData?.application_metrics) return;

        const ctx = canvas.getContext('2d');
        const metrics = this.dashboardData.application_metrics;

        // Очищаем canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Рисуем круговую диаграмму
        const total = metrics.total_requests;
        const successful = metrics.successful_requests;
        const failed = metrics.failed_requests;

        if (total === 0) return;

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;

        // Успешные запросы
        const successfulAngle = (successful / total) * 2 * Math.PI;
        ctx.fillStyle = '#28a745';
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, 0, successfulAngle);
        ctx.closePath();
        ctx.fill();

        // Неудачные запросы
        const failedAngle = (failed / total) * 2 * Math.PI;
        ctx.fillStyle = '#dc3545';
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, successfulAngle, successfulAngle + failedAngle);
        ctx.closePath();
        ctx.fill();

        // Подписи
        ctx.fillStyle = '#333';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`Total: ${total}`, centerX, centerY - 10);
        ctx.fillText(`Success: ${successful}`, centerX, centerY + 5);
        ctx.fillText(`Failed: ${failed}`, centerX, centerY + 20);
    }

    /**
     * Обновление алертов
     */
    async updateAlerts() {
        const container = document.getElementById('alerts-list');
        if (!container) return;

        try {
            const response = await window.ApiService.get('/api/monitoring/alerts?resolved=false');
            const alerts = response;

            if (alerts.length === 0) {
                container.innerHTML = '<div class="text-center text-muted">Нет активных алертов</div>';
                return;
            }

            const alertsHTML = alerts.map(alert => `
                <div class="alert-item alert-${alert.severity}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="mb-1">${alert.message}</h6>
                            <p class="mb-1 text-muted">${alert.type}</p>
                            <small class="text-muted">${new Date(alert.timestamp).toLocaleString()}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-primary" onclick="window.monitoringDashboard.resolveAlert(${alert.id})">
                            Разрешить
                        </button>
                    </div>
                </div>
            `).join('');

            container.innerHTML = alertsHTML;
        } catch (error) {
            console.error('📊 Failed to load alerts:', error);
            container.innerHTML = '<div class="text-center text-danger">Ошибка загрузки алертов</div>';
        }
    }

    /**
     * Обновление логов
     */
    async updateLogs(level = 'all') {
        const container = document.getElementById('logs-list');
        if (!container) return;

        try {
            const params = level !== 'all' ? `?level=${level}` : '';
            const response = await window.ApiService.get(`/api/monitoring/logs${params}&limit=20`);
            const logs = response;

            if (logs.length === 0) {
                container.innerHTML = '<div class="text-center text-muted">Нет логов</div>';
                return;
            }

            const logsHTML = logs.map(log => `
                <div class="log-item log-${log.level.toLowerCase()}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <span class="badge bg-${this.getLogLevelColor(log.level)} me-2">${log.level}</span>
                            <span class="text-muted">${log.module}:${log.function}</span>
                            <div class="mt-1">${log.message}</div>
                        </div>
                        <small class="text-muted">${new Date(log.timestamp).toLocaleString()}</small>
                    </div>
                </div>
            `).join('');

            container.innerHTML = logsHTML;
        } catch (error) {
            console.error('📊 Failed to load logs:', error);
            container.innerHTML = '<div class="text-center text-danger">Ошибка загрузки логов</div>';
        }
    }

    /**
     * Получение цвета для уровня лога
     */
    getLogLevelColor(level) {
        const colors = {
            'DEBUG': 'secondary',
            'INFO': 'info',
            'WARNING': 'warning',
            'ERROR': 'danger',
            'CRITICAL': 'dark'
        };
        return colors[level] || 'secondary';
    }

    /**
     * Фильтрация логов
     */
    filterLogs(level) {
        this.updateLogs(level);
    }

    /**
     * Разрешение алерта
     */
    async resolveAlert(alertId) {
        try {
            await window.ApiService.put(`/api/monitoring/alerts/${alertId}/resolve`);
            await this.updateAlerts();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Алерт разрешен');
            }
        } catch (error) {
            console.error('📊 Failed to resolve alert:', error);
        }
    }

    /**
     * Обновление алертов
     */
    async refreshAlerts() {
        await this.updateAlerts();
    }

    /**
     * Обновление всех данных
     */
    async refreshAll() {
        await this.loadDashboardData();
    }

    /**
     * Запуск автообновления
     */
    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        this.refreshInterval = setInterval(async () => {
            await this.loadDashboardData();
        }, this.refreshDelay);
    }

    /**
     * Остановка автообновления
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    /**
     * Открытие дашборда
     */
    async openDashboard() {
        try {
            await this.loadDashboardData();

            const modal = new bootstrap.Modal(document.getElementById('monitoring-dashboard-modal'));
            modal.show();
        } catch (error) {
            console.error('📊 Failed to open dashboard:', error);
        }
    }

    /**
     * Очистка ресурсов
     */
    destroy() {
        this.stopAutoRefresh();
        this.isInitialized = false;
    }
}

// Создаем глобальный экземпляр
window.monitoringDashboard = new MonitoringDashboard();
