/**
 * Расширенный менеджер уведомлений с умными функциями
 */

class AdvancedNotificationsManager {
    constructor() {
        this.notifications = [];
        this.preferences = {};
        this.analytics = {};
        this.isInitialized = false;
        this.pollingInterval = null;
        this.pollingDelay = 30000; // 30 секунд
    }

    /**
     * Инициализация расширенного менеджера уведомлений
     */
    async init() {
        console.log('🔔 Initializing Advanced Notifications Manager...');

        try {
            // Загружаем настройки
            await this.loadPreferences();

            // Загружаем уведомления
            await this.loadNotifications();

            // Загружаем аналитику
            await this.loadAnalytics();

            // Инициализируем UI
            this.initUI();

            // Запускаем опрос
            this.startPolling();

            this.isInitialized = true;
            console.log('🔔 Advanced Notifications Manager initialized successfully');

            // Показываем уведомление об инициализации
            this.showNotification('Система уведомлений', 'Расширенная система уведомлений активирована', 'info');

        } catch (error) {
            console.error('🔔 Failed to initialize Advanced Notifications Manager:', error);
        }
    }

    /**
     * Загрузка настроек уведомлений
     */
    async loadPreferences() {
        try {
            const response = await window.ApiService.get('/api/advanced-notifications/preferences');
            this.preferences = response;
            console.log('🔔 Preferences loaded:', this.preferences);
        } catch (error) {
            console.error('🔔 Failed to load preferences:', error);
            // Используем настройки по умолчанию
            this.preferences = {
                enabled: true,
                email_notifications: true,
                push_notifications: true,
                in_app_notifications: true,
                quiet_hours: { enabled: true, start: "22:00", end: "08:00" },
                categories: { system: true, social: true, work: true, product: true, security: true },
                priorities: { critical: true, high: true, medium: true, low: false },
                batch_similar: true,
                max_daily: 50,
                digest_frequency: "daily"
            };
        }
    }

    /**
     * Загрузка уведомлений
     */
    async loadNotifications(limit = 20, offset = 0, filters = {}) {
        try {
            const params = new URLSearchParams({
                limit: limit.toString(),
                offset: offset.toString(),
                ...filters
            });

            const response = await window.ApiService.get(`/api/advanced-notifications/?${params}`);
            this.notifications = response.notifications || [];

            console.log('🔔 Notifications loaded:', this.notifications.length);
            return response;
        } catch (error) {
            console.error('🔔 Failed to load notifications:', error);
            return { notifications: [], total: 0, unread_count: 0 };
        }
    }

    /**
     * Загрузка аналитики уведомлений
     */
    async loadAnalytics(periodDays = 30) {
        try {
            const response = await window.ApiService.get(`/api/advanced-notifications/analytics?period_days=${periodDays}`);
            this.analytics = response;
            console.log('🔔 Analytics loaded:', this.analytics);
            return response;
        } catch (error) {
            console.error('🔔 Failed to load analytics:', error);
            return {};
        }
    }

    /**
     * Создание умного уведомления
     */
    async createSmartNotification(type, title, message, data = {}, smartFeatures = true) {
        try {
            const response = await window.ApiService.post('/api/advanced-notifications/create', {
                notification_type: type,
                title: title,
                message: message,
                data: data,
                smart_features: smartFeatures
            });

            console.log('🔔 Smart notification created:', response);

            // Обновляем список уведомлений
            await this.loadNotifications();

            return response;
        } catch (error) {
            console.error('🔔 Failed to create smart notification:', error);
            throw error;
        }
    }

    /**
     * Отметить уведомление как прочитанное
     */
    async markAsRead(notificationId) {
        try {
            await window.ApiService.put(`/api/advanced-notifications/${notificationId}/read`);

            // Обновляем локальное состояние
            const notification = this.notifications.find(n => n.id === notificationId);
            if (notification) {
                notification.is_read = true;
                notification.read_at = new Date().toISOString();
            }

            console.log('🔔 Notification marked as read:', notificationId);
            this.updateUI();
        } catch (error) {
            console.error('🔔 Failed to mark notification as read:', error);
        }
    }

    /**
     * Отметить все уведомления как прочитанные
     */
    async markAllAsRead() {
        try {
            const response = await window.ApiService.put('/api/advanced-notifications/mark-all-read');

            // Обновляем локальное состояние
            this.notifications.forEach(notification => {
                notification.is_read = true;
                notification.read_at = new Date().toISOString();
            });

            console.log('🔔 All notifications marked as read');
            this.updateUI();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success(response.message);
            } else {
                alert(response.message);
            }
        } catch (error) {
            console.error('🔔 Failed to mark all notifications as read:', error);
        }
    }

    /**
     * Удалить уведомление
     */
    async deleteNotification(notificationId) {
        try {
            await window.ApiService.delete(`/api/advanced-notifications/${notificationId}`);

            // Удаляем из локального состояния
            this.notifications = this.notifications.filter(n => n.id !== notificationId);

            console.log('🔔 Notification deleted:', notificationId);
            this.updateUI();
        } catch (error) {
            console.error('🔔 Failed to delete notification:', error);
        }
    }

    /**
     * Обновить настройки уведомлений
     */
    async updatePreferences(newPreferences) {
        try {
            const response = await window.ApiService.put('/api/advanced-notifications/preferences', newPreferences);
            this.preferences = response;

            console.log('🔔 Preferences updated:', this.preferences);

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Настройки уведомлений обновлены');
            } else {
                alert('Настройки уведомлений обновлены');
            }

            return response;
        } catch (error) {
            console.error('🔔 Failed to update preferences:', error);
            throw error;
        }
    }

    /**
     * Отправить тестовое уведомление
     */
    async sendTestNotification(type = 'system_alert') {
        try {
            const response = await window.ApiService.post(`/api/advanced-notifications/test?notification_type=${type}`);

            console.log('🔔 Test notification sent:', response);

            // Обновляем список уведомлений
            await this.loadNotifications();

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Тестовое уведомление отправлено');
            } else {
                alert('Тестовое уведомление отправлено');
            }

            return response;
        } catch (error) {
            console.error('🔔 Failed to send test notification:', error);
            throw error;
        }
    }

    /**
     * Инициализация UI
     */
    initUI() {
        // Создаем контейнер для расширенных уведомлений
        this.createAdvancedNotificationUI();

        // Добавляем обработчики событий
        this.attachEventListeners();
    }

    /**
     * Создание расширенного UI для уведомлений
     */
    createAdvancedNotificationUI() {
        // Создаем модальное окно для расширенных уведомлений
        const modalHTML = `
            <div id="advanced-notifications-modal" class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-bell"></i>
                                Расширенные уведомления
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <!-- Левая панель: Список уведомлений -->
                                <div class="col-md-8">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <h6>Уведомления</h6>
                                        <div class="btn-group" role="group">
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.advancedNotificationsManager.filterNotifications('all')">
                                                Все
                                            </button>
                                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.advancedNotificationsManager.filterNotifications('unread')">
                                                Непрочитанные
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div id="notifications-list" class="notifications-list">
                                        <!-- Уведомления будут загружены здесь -->
                                    </div>
                                    
                                    <div class="d-flex justify-content-center mt-3">
                                        <button type="button" class="btn btn-outline-primary" onclick="window.advancedNotificationsManager.loadMoreNotifications()">
                                            Загрузить еще
                                        </button>
                                    </div>
                                </div>
                                
                                <!-- Правая панель: Настройки и аналитика -->
                                <div class="col-md-4">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Настройки</h6>
                                        </div>
                                        <div class="card-body">
                                            <div class="form-check mb-2">
                                                <input class="form-check-input" type="checkbox" id="notifications-enabled" checked>
                                                <label class="form-check-label" for="notifications-enabled">
                                                    Уведомления включены
                                                </label>
                                            </div>
                                            
                                            <div class="form-check mb-2">
                                                <input class="form-check-input" type="checkbox" id="email-notifications" checked>
                                                <label class="form-check-label" for="email-notifications">
                                                    Email уведомления
                                                </label>
                                            </div>
                                            
                                            <div class="form-check mb-2">
                                                <input class="form-check-input" type="checkbox" id="push-notifications" checked>
                                                <label class="form-check-label" for="push-notifications">
                                                    Push уведомления
                                                </label>
                                            </div>
                                            
                                            <div class="form-check mb-2">
                                                <input class="form-check-input" type="checkbox" id="batch-similar" checked>
                                                <label class="form-check-label" for="batch-similar">
                                                    Группировать похожие
                                                </label>
                                            </div>
                                            
                                            <div class="mt-3">
                                                <label for="max-daily" class="form-label">Максимум в день</label>
                                                <input type="number" class="form-control form-control-sm" id="max-daily" value="50" min="1" max="100">
                                            </div>
                                            
                                            <div class="mt-3">
                                                <button type="button" class="btn btn-primary btn-sm w-100" onclick="window.advancedNotificationsManager.savePreferences()">
                                                    Сохранить настройки
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="card mt-3">
                                        <div class="card-header">
                                            <h6 class="mb-0">Аналитика</h6>
                                        </div>
                                        <div class="card-body">
                                            <div id="notification-analytics">
                                                <!-- Аналитика будет загружена здесь -->
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="card mt-3">
                                        <div class="card-header">
                                            <h6 class="mb-0">Тестирование</h6>
                                        </div>
                                        <div class="card-body">
                                            <div class="d-grid gap-2">
                                                <button type="button" class="btn btn-sm btn-outline-success" onclick="window.advancedNotificationsManager.sendTestNotification('system_alert')">
                                                    Тест системного уведомления
                                                </button>
                                                <button type="button" class="btn btn-sm btn-outline-info" onclick="window.advancedNotificationsManager.sendTestNotification('new_follower')">
                                                    Тест социального уведомления
                                                </button>
                                                <button type="button" class="btn btn-sm btn-outline-warning" onclick="window.advancedNotificationsManager.sendTestNotification('security_alert')">
                                                    Тест критического уведомления
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-primary" onclick="window.advancedNotificationsManager.markAllAsRead()">
                                Отметить все как прочитанные
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
        `;

        // Добавляем модальное окно в DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    /**
     * Прикрепление обработчиков событий
     */
    attachEventListeners() {
        // Обработчик для кнопки открытия модального окна
        document.addEventListener('click', (e) => {
            if (e.target && e.target.id === 'test-advanced-notifications-btn') {
                this.openAdvancedNotificationsModal();
            }
        });
    }

    /**
     * Открытие модального окна расширенных уведомлений
     */
    async openAdvancedNotificationsModal() {
        try {
            // Загружаем актуальные данные
            await this.loadNotifications();
            await this.loadAnalytics();

            // Обновляем UI
            this.updateUI();
            this.updateAnalyticsUI();
            this.updatePreferencesUI();

            // Показываем модальное окно
            const modal = new bootstrap.Modal(document.getElementById('advanced-notifications-modal'));
            modal.show();

        } catch (error) {
            console.error('🔔 Failed to open advanced notifications modal:', error);
        }
    }

    /**
     * Обновление UI уведомлений
     */
    updateUI() {
        const container = document.getElementById('notifications-list');
        if (!container) return;

        if (this.notifications.length === 0) {
            container.innerHTML = '<div class="text-center text-muted">Нет уведомлений</div>';
            return;
        }

        const notificationsHTML = this.notifications.map(notification => {
            const priorityClass = this.getPriorityClass(notification.priority);
            const readClass = notification.is_read ? '' : 'fw-bold';
            const timeAgo = this.getTimeAgo(notification.created_at);

            return `
                <div class="notification-item border-bottom py-2 ${readClass}" data-id="${notification.id}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                <span class="badge ${priorityClass} me-2">${notification.priority}</span>
                                <span class="badge bg-secondary me-2">${notification.category}</span>
                                <small class="text-muted">${timeAgo}</small>
                            </div>
                            <h6 class="mb-1">${notification.title}</h6>
                            <p class="mb-1 text-muted">${notification.message}</p>
                            ${notification.smart_features && notification.smart_features.escalated ?
                    '<span class="badge bg-warning">Повышенный приоритет</span>' : ''}
                        </div>
                        <div class="btn-group-vertical btn-group-sm">
                            ${!notification.is_read ?
                    `<button class="btn btn-outline-primary btn-sm" onclick="window.advancedNotificationsManager.markAsRead(${notification.id})">
                                    <i class="fas fa-check"></i>
                                </button>` : ''}
                            <button class="btn btn-outline-danger btn-sm" onclick="window.advancedNotificationsManager.deleteNotification(${notification.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = notificationsHTML;
    }

    /**
     * Обновление UI аналитики
     */
    updateAnalyticsUI() {
        const container = document.getElementById('notification-analytics');
        if (!container || !this.analytics) return;

        const analyticsHTML = `
            <div class="mb-2">
                <small class="text-muted">Всего уведомлений</small>
                <div class="h5 mb-0">${this.analytics.total_notifications || 0}</div>
            </div>
            <div class="mb-2">
                <small class="text-muted">Прочитано</small>
                <div class="h6 mb-0">${this.analytics.read_notifications || 0}</div>
            </div>
            <div class="mb-2">
                <small class="text-muted">Непрочитано</small>
                <div class="h6 mb-0">${this.analytics.unread_notifications || 0}</div>
            </div>
            <div class="mb-2">
                <small class="text-muted">Процент прочтения</small>
                <div class="h6 mb-0">${Math.round((this.analytics.read_rate || 0) * 100)}%</div>
            </div>
            <div class="mb-2">
                <small class="text-muted">Средне в день</small>
                <div class="h6 mb-0">${Math.round(this.analytics.average_daily || 0)}</div>
            </div>
        `;

        container.innerHTML = analyticsHTML;
    }

    /**
     * Обновление UI настроек
     */
    updatePreferencesUI() {
        if (!this.preferences) return;

        // Обновляем чекбоксы
        const enabledCheckbox = document.getElementById('notifications-enabled');
        const emailCheckbox = document.getElementById('email-notifications');
        const pushCheckbox = document.getElementById('push-notifications');
        const batchCheckbox = document.getElementById('batch-similar');
        const maxDailyInput = document.getElementById('max-daily');

        if (enabledCheckbox) enabledCheckbox.checked = this.preferences.enabled;
        if (emailCheckbox) emailCheckbox.checked = this.preferences.email_notifications;
        if (pushCheckbox) pushCheckbox.checked = this.preferences.push_notifications;
        if (batchCheckbox) batchCheckbox.checked = this.preferences.batch_similar;
        if (maxDailyInput) maxDailyInput.value = this.preferences.max_daily;
    }

    /**
     * Сохранение настроек
     */
    async savePreferences() {
        try {
            const newPreferences = {
                enabled: document.getElementById('notifications-enabled').checked,
                email_notifications: document.getElementById('email-notifications').checked,
                push_notifications: document.getElementById('push-notifications').checked,
                batch_similar: document.getElementById('batch-similar').checked,
                max_daily: parseInt(document.getElementById('max-daily').value)
            };

            await this.updatePreferences(newPreferences);
        } catch (error) {
            console.error('🔔 Failed to save preferences:', error);
        }
    }

    /**
     * Фильтрация уведомлений
     */
    async filterNotifications(filter) {
        const filters = {};
        if (filter === 'unread') {
            filters.unread_only = true;
        }

        await this.loadNotifications(20, 0, filters);
        this.updateUI();
    }

    /**
     * Загрузка дополнительных уведомлений
     */
    async loadMoreNotifications() {
        const currentCount = this.notifications.length;
        await this.loadNotifications(20, currentCount);
        this.updateUI();
    }

    /**
     * Запуск опроса уведомлений
     */
    startPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }

        this.pollingInterval = setInterval(async () => {
            try {
                await this.loadNotifications();
                this.updateUI();
            } catch (error) {
                console.error('🔔 Polling error:', error);
            }
        }, this.pollingDelay);
    }

    /**
     * Остановка опроса уведомлений
     */
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    /**
     * Показать уведомление
     */
    showNotification(title, message, type = 'info') {
        if (window.Toast && typeof window.Toast[type] === 'function') {
            window.Toast[type](message, title);
        } else {
            console.log(`🔔 ${type.toUpperCase()}: ${title} - ${message}`);
        }
    }

    /**
     * Получить CSS класс для приоритета
     */
    getPriorityClass(priority) {
        const classes = {
            'critical': 'bg-danger',
            'high': 'bg-warning',
            'medium': 'bg-info',
            'low': 'bg-secondary'
        };
        return classes[priority] || 'bg-secondary';
    }

    /**
     * Получить время назад
     */
    getTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) return 'только что';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} мин назад`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} ч назад`;
        return `${Math.floor(diffInSeconds / 86400)} дн назад`;
    }

    /**
     * Очистка ресурсов
     */
    destroy() {
        this.stopPolling();
        this.isInitialized = false;
    }
}

// Создаем глобальный экземпляр
window.advancedNotificationsManager = new AdvancedNotificationsManager();
