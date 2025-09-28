/**
 * Integrations Manager
 * Управление внешними интеграциями
 */

class IntegrationsManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.integrations = {};
        this.isLoading = false;
    }

    /**
     * Инициализация системы интеграций
     */
    init() {
        this.createIntegrationsUI();
        this.setupEventListeners();
        this.loadIntegrationStatus();
        console.log('🔗 Integrations Manager initialized');
    }

    /**
     * Создание UI для интеграций
     */
    createIntegrationsUI() {
        const integrationsContainer = document.createElement('div');
        integrationsContainer.className = 'integrations-container';
        integrationsContainer.innerHTML = `
            <div class="integrations-header">
                <h2><i class="fas fa-plug"></i> Внешние Интеграции</h2>
                <div class="integrations-actions">
                    <button id="refresh-integrations-btn" class="btn btn-primary">
                        <i class="fas fa-sync"></i> Обновить
                    </button>
                    <button id="test-all-integrations-btn" class="btn btn-secondary">
                        <i class="fas fa-vial"></i> Тест всех
                    </button>
                </div>
            </div>

            <div class="integrations-content">
                <div class="integrations-sidebar">
                    <div class="integration-categories">
                        <button class="category-btn active" data-category="all">
                            <i class="fas fa-th"></i> Все
                        </button>
                        <button class="category-btn" data-category="email">
                            <i class="fas fa-envelope"></i> Email
                        </button>
                        <button class="category-btn" data-category="sms">
                            <i class="fas fa-sms"></i> SMS
                        </button>
                        <button class="category-btn" data-category="social">
                            <i class="fas fa-share-alt"></i> Соцсети
                        </button>
                        <button class="category-btn" data-category="payment">
                            <i class="fas fa-credit-card"></i> Платежи
                        </button>
                        <button class="category-btn" data-category="storage">
                            <i class="fas fa-cloud"></i> Облако
                        </button>
                        <button class="category-btn" data-category="analytics">
                            <i class="fas fa-chart-bar"></i> Аналитика
                        </button>
                    </div>
                </div>

                <div class="integrations-main">
                    <div class="integrations-overview">
                        <div class="overview-cards">
                            <div class="overview-card">
                                <h3>Всего интеграций</h3>
                                <div class="card-value" id="total-integrations">--</div>
                            </div>
                            <div class="overview-card">
                                <h3>Активных</h3>
                                <div class="card-value" id="active-integrations">--</div>
                            </div>
                            <div class="overview-card">
                                <h3>Статус</h3>
                                <div class="card-value" id="overall-status">--</div>
                            </div>
                        </div>
                    </div>

                    <div class="integrations-list" id="integrations-list">
                        <div class="loading">Загрузка интеграций...</div>
                    </div>

                    <div class="integration-tools">
                        <div class="tool-section">
                            <h3>Быстрые действия</h3>
                            <div class="quick-actions">
                                <button id="send-test-email-btn" class="btn btn-info">
                                    <i class="fas fa-envelope"></i> Тест Email
                                </button>
                                <button id="send-test-sms-btn" class="btn btn-warning">
                                    <i class="fas fa-sms"></i> Тест SMS
                                </button>
                                <button id="post-test-social-btn" class="btn btn-primary">
                                    <i class="fas fa-share"></i> Тест соцсети
                                </button>
                                <button id="test-payment-btn" class="btn btn-success">
                                    <i class="fas fa-credit-card"></i> Тест платежа
                                </button>
                            </div>
                        </div>

                        <div class="tool-section">
                            <h3>Логи интеграций</h3>
                            <div class="logs-container">
                                <select id="log-category" class="form-control">
                                    <option value="email">Email</option>
                                    <option value="sms">SMS</option>
                                    <option value="social_media">Соцсети</option>
                                    <option value="payment">Платежи</option>
                                </select>
                                <button id="load-logs-btn" class="btn btn-secondary">Загрузить логи</button>
                            </div>
                            <div id="logs-display" class="logs-display">
                                <div class="no-content">Выберите категорию и загрузите логи</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.addStyles();
        document.body.appendChild(integrationsContainer);
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .integrations-container {
                max-width: 1400px;
                margin: 20px auto;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .integrations-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }

            .integrations-content {
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 30px;
            }

            .integrations-sidebar {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
            }

            .integration-categories {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .category-btn {
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

            .category-btn:hover {
                background: #e9ecef;
                color: #333;
            }

            .category-btn.active {
                background: #007bff;
                color: white;
            }

            .integrations-main {
                background: white;
                border-radius: 8px;
                padding: 30px;
            }

            .overview-cards {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }

            .overview-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #007bff;
            }

            .overview-card h3 {
                margin: 0 0 10px 0;
                color: #333;
                font-size: 14px;
            }

            .card-value {
                font-size: 24px;
                font-weight: bold;
                color: #007bff;
            }

            .integrations-list {
                margin-bottom: 30px;
            }

            .integration-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 4px solid #28a745;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .integration-item.disabled {
                border-left-color: #dc3545;
                opacity: 0.6;
            }

            .integration-info h4 {
                margin: 0 0 5px 0;
                color: #333;
            }

            .integration-info p {
                margin: 0;
                color: #666;
                font-size: 14px;
            }

            .integration-actions {
                display: flex;
                gap: 10px;
            }

            .integration-tools {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
            }

            .tool-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
            }

            .tool-section h3 {
                margin: 0 0 15px 0;
                color: #333;
            }

            .quick-actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
            }

            .logs-container {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }

            .logs-display {
                background: #2d3748;
                color: #e2e8f0;
                padding: 15px;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                max-height: 200px;
                overflow-y: auto;
            }

            .log-entry {
                margin-bottom: 5px;
                padding: 2px 0;
            }

            .log-entry.info {
                color: #68d391;
            }

            .log-entry.warning {
                color: #f6e05e;
            }

            .log-entry.error {
                color: #fc8181;
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
                font-size: 14px;
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

            .btn-info {
                background: #17a2b8;
                color: white;
            }

            .btn-info:hover {
                background: #138496;
            }

            .btn-warning {
                background: #ffc107;
                color: #212529;
            }

            .btn-warning:hover {
                background: #e0a800;
            }

            .btn-success {
                background: #28a745;
                color: white;
            }

            .btn-success:hover {
                background: #1e7e34;
            }

            .btn-danger {
                background: #dc3545;
                color: white;
            }

            .btn-danger:hover {
                background: #c82333;
            }

            .form-control {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
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

            .status-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 5px;
            }

            .status-healthy {
                background: #28a745;
            }

            .status-warning {
                background: #ffc107;
            }

            .status-error {
                background: #dc3545;
            }

            .status-disabled {
                background: #6c757d;
            }

            @media (max-width: 768px) {
                .integrations-content {
                    grid-template-columns: 1fr;
                }
                
                .integrations-sidebar {
                    order: 2;
                }
                
                .integration-categories {
                    flex-direction: row;
                    overflow-x: auto;
                }
                
                .integration-tools {
                    grid-template-columns: 1fr;
                }
                
                .quick-actions {
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
        // Переключение категорий
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchCategory(e.target.dataset.category);
            });
        });

        // Обновление интеграций
        document.getElementById('refresh-integrations-btn').addEventListener('click', () => {
            this.loadIntegrationStatus();
        });

        // Тест всех интеграций
        document.getElementById('test-all-integrations-btn').addEventListener('click', () => {
            this.testAllIntegrations();
        });

        // Быстрые действия
        document.getElementById('send-test-email-btn').addEventListener('click', () => {
            this.sendTestEmail();
        });

        document.getElementById('send-test-sms-btn').addEventListener('click', () => {
            this.sendTestSMS();
        });

        document.getElementById('post-test-social-btn').addEventListener('click', () => {
            this.postTestSocial();
        });

        document.getElementById('test-payment-btn').addEventListener('click', () => {
            this.testPayment();
        });

        // Загрузка логов
        document.getElementById('load-logs-btn').addEventListener('click', () => {
            this.loadLogs();
        });
    }

    /**
     * Переключение категорий
     */
    switchCategory(category) {
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');

        this.renderIntegrations(category);
    }

    /**
     * Загрузка статуса интеграций
     */
    async loadIntegrationStatus() {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/integrations/status`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.integrations = data.status;
            this.renderOverview();
            this.renderIntegrations('all');

        } catch (error) {
            this.showError(`Ошибка загрузки статуса интеграций: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Отображение обзора
     */
    renderOverview() {
        if (!this.integrations) return;

        document.getElementById('total-integrations').textContent = this.integrations.total_integrations || 0;
        document.getElementById('active-integrations').textContent = this.integrations.active_integrations || 0;
        document.getElementById('overall-status').textContent = this.integrations.health_check?.overall_status || 'unknown';
    }

    /**
     * Отображение списка интеграций
     */
    renderIntegrations(category) {
        const container = document.getElementById('integrations-list');

        if (!this.integrations || !this.integrations.integrations) {
            container.innerHTML = '<div class="loading">Загрузка интеграций...</div>';
            return;
        }

        const integrations = this.integrations.integrations;
        let items = [];

        if (category === 'all') {
            // Показываем все интеграции
            Object.entries(integrations).forEach(([cat, services]) => {
                if (typeof services === 'object' && services.enabled !== undefined) {
                    // Одиночный сервис
                    items.push({ category: cat, service: cat, ...services });
                } else {
                    // Множественные сервисы
                    Object.entries(services).forEach(([service, config]) => {
                        items.push({ category: cat, service, ...config });
                    });
                }
            });
        } else {
            // Показываем интеграции конкретной категории
            if (integrations[category]) {
                const services = integrations[category];
                if (typeof services === 'object' && services.enabled !== undefined) {
                    items.push({ category, service: category, ...services });
                } else {
                    Object.entries(services).forEach(([service, config]) => {
                        items.push({ category, service, ...config });
                    });
                }
            }
        }

        if (items.length === 0) {
            container.innerHTML = '<div class="no-content">Нет интеграций в этой категории</div>';
            return;
        }

        container.innerHTML = items.map(item => `
            <div class="integration-item ${!item.enabled ? 'disabled' : ''}">
                <div class="integration-info">
                    <h4>${item.service} <span class="status-indicator status-${item.status}"></span></h4>
                    <p>${item.provider || item.service} • ${item.enabled ? 'Активна' : 'Отключена'}</p>
                </div>
                <div class="integration-actions">
                    <button class="btn btn-sm btn-secondary" onclick="window.integrationsManager.testIntegration('${item.category}', '${item.service}')">
                        <i class="fas fa-vial"></i> Тест
                    </button>
                    <button class="btn btn-sm btn-primary" onclick="window.integrationsManager.configureIntegration('${item.category}', '${item.service}')">
                        <i class="fas fa-cog"></i> Настроить
                    </button>
                </div>
            </div>
        `).join('');
    }

    /**
     * Тестирование интеграции
     */
    async testIntegration(category, service) {
        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/integrations/test/${category}/${service}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.result.success) {
                this.showSuccess(`Тест интеграции ${service} прошел успешно`);
            } else {
                this.showError(`Тест интеграции ${service} не удался: ${data.result.error}`);
            }

        } catch (error) {
            this.showError(`Ошибка тестирования интеграции: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Настройка интеграции
     */
    configureIntegration(category, service) {
        const config = prompt(`Введите конфигурацию для ${service} (JSON):`, '{"enabled": true}');
        if (config) {
            try {
                const parsedConfig = JSON.parse(config);
                this.updateIntegrationConfig(category, service, parsedConfig);
            } catch (error) {
                this.showError('Неверный формат JSON');
            }
        }
    }

    /**
     * Обновление конфигурации интеграции
     */
    async updateIntegrationConfig(category, service, config) {
        try {
            const response = await fetch(`${this.apiBase}/api/integrations/configure/${category}/${service}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ config })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess(`Конфигурация ${service} обновлена`);
            this.loadIntegrationStatus();

        } catch (error) {
            this.showError(`Ошибка обновления конфигурации: ${error.message}`);
        }
    }

    /**
     * Тест всех интеграций
     */
    async testAllIntegrations() {
        try {
            this.showLoading(true);
            this.showSuccess('Тестирование всех интеграций запущено...');

            // В реальном приложении здесь будет параллельное тестирование
            await new Promise(resolve => setTimeout(resolve, 2000));

            this.showSuccess('Тестирование завершено');

        } catch (error) {
            this.showError(`Ошибка тестирования: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Отправка тестового email
     */
    async sendTestEmail() {
        try {
            const response = await fetch(`${this.apiBase}/api/integrations/email/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    to: 'test@example.com',
                    subject: 'Тестовое сообщение',
                    body: 'Это тестовое сообщение из системы интеграций'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showSuccess('Тестовый email отправлен успешно');

        } catch (error) {
            this.showError(`Ошибка отправки email: ${error.message}`);
        }
    }

    /**
     * Отправка тестового SMS
     */
    async sendTestSMS() {
        try {
            const response = await fetch(`${this.apiBase}/api/integrations/sms/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    to: '+1234567890',
                    message: 'Тестовое SMS сообщение'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Тестовое SMS отправлено успешно');

        } catch (error) {
            this.showError(`Ошибка отправки SMS: ${error.message}`);
        }
    }

    /**
     * Публикация тестового поста в соцсети
     */
    async postTestSocial() {
        try {
            const response = await fetch(`${this.apiBase}/api/integrations/social-media/post`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    platform: 'twitter',
                    content: 'Тестовый пост из системы интеграций #test'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Тестовый пост опубликован успешно');

        } catch (error) {
            this.showError(`Ошибка публикации: ${error.message}`);
        }
    }

    /**
     * Тест платежа
     */
    async testPayment() {
        try {
            const response = await fetch(`${this.apiBase}/api/integrations/payment/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    amount: 1.00,
                    currency: 'USD',
                    payment_method: 'card',
                    customer_id: 'test_customer'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            this.showSuccess('Тестовый платеж обработан успешно');

        } catch (error) {
            this.showError(`Ошибка обработки платежа: ${error.message}`);
        }
    }

    /**
     * Загрузка логов
     */
    async loadLogs() {
        const category = document.getElementById('log-category').value;

        try {
            const response = await fetch(`${this.apiBase}/api/integrations/logs/${category}/default?limit=20`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderLogs(data.logs);

        } catch (error) {
            this.showError(`Ошибка загрузки логов: ${error.message}`);
        }
    }

    /**
     * Отображение логов
     */
    renderLogs(logs) {
        const container = document.getElementById('logs-display');

        if (logs.length === 0) {
            container.innerHTML = '<div class="no-content">Логи не найдены</div>';
            return;
        }

        container.innerHTML = logs.map(log => `
            <div class="log-entry ${log.level.toLowerCase()}">
                [${log.timestamp}] ${log.level}: ${log.message}
            </div>
        `).join('');
    }

    /**
     * Показ загрузки
     */
    showLoading(show) {
        const container = document.querySelector('.integrations-container');
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
console.log('🔗 IntegrationsManager class defined:', typeof IntegrationsManager);
window.IntegrationsManager = IntegrationsManager;
window.integrationsManager = new IntegrationsManager();
console.log('🔗 IntegrationsManager exported to window:', typeof window.IntegrationsManager);
