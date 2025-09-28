/**
 * Notifications system for real-time updates
 * Provides in-app, push, and email notifications
 */

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.unreadCount = 0;
        this.permission = 'default';
        this.isSupported = 'Notification' in window;
        this.observers = new Set();
        this.apiBase = 'http://localhost:5000';
        this.init();
    }

    /**
     * Initialize notification manager
     */
    init() {
        this.setupPermission();
        this.setupEventListeners();
        this.setupServiceWorker();
        this.loadStoredNotifications();
        console.log('🔔 Notification Manager initialized');
    }

    /**
     * Setup notification permission
     */
    async setupPermission() {
        if (!this.isSupported) {
            console.warn('Notifications not supported');
            return;
        }

        try {
            this.permission = await Notification.requestPermission();
            console.log('Notification permission:', this.permission);
        } catch (error) {
            console.error('Failed to request notification permission:', error);
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for visibility change to update unread count
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.markAllAsRead();
            }
        });

        // Listen for custom notification events
        document.addEventListener('showNotification', (e) => {
            this.showNotification(e.detail);
        });

        // Listen for notification clicks
        document.addEventListener('click', (e) => {
            if (e.target.matches('.notification-item')) {
                this.handleNotificationClick(e.target.dataset.notificationId);
            }
        });
    }

    /**
     * Setup service worker for push notifications
     */
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                    this.serviceWorkerRegistration = registration;
                })
                .catch(error => {
                    console.error('Service Worker registration failed:', error);
                });
        }
    }

    /**
     * Load stored notifications from localStorage
     */
    loadStoredNotifications() {
        try {
            const stored = localStorage.getItem('notifications');
            if (stored) {
                this.notifications = JSON.parse(stored);
                this.updateUnreadCount();
            }
        } catch (error) {
            console.error('Failed to load stored notifications:', error);
        }
    }

    /**
     * Save notifications to localStorage
     */
    saveNotifications() {
        try {
            localStorage.setItem('notifications', JSON.stringify(this.notifications));
        } catch (error) {
            console.error('Failed to save notifications:', error);
        }
    }

    /**
     * Show notification
     */
    showNotification(notification) {
        const notificationObj = {
            id: this.generateId(),
            title: notification.title,
            message: notification.message,
            type: notification.type || 'info',
            icon: notification.icon || this.getDefaultIcon(notification.type),
            url: notification.url,
            timestamp: new Date().toISOString(),
            read: false,
            persistent: notification.persistent || false
        };

        this.notifications.unshift(notificationObj);
        this.updateUnreadCount();
        this.saveNotifications();

        // Show browser notification if permission granted
        if (this.permission === 'granted') {
            this.showBrowserNotification(notificationObj);
        }

        // Show in-app notification
        this.showInAppNotification(notificationObj);

        // Notify observers
        this.notifyObservers('notificationAdded', notificationObj);
    }

    /**
     * Show browser notification
     */
    showBrowserNotification(notification) {
        if (!this.isSupported || this.permission !== 'granted') return;

        const browserNotification = new Notification(notification.title, {
            body: notification.message,
            icon: notification.icon,
            badge: '/favicon.ico',
            tag: notification.id,
            requireInteraction: notification.persistent
        });

        browserNotification.onclick = () => {
            this.handleNotificationClick(notification.id);
            browserNotification.close();
        };

        // Auto close after 5 seconds unless persistent
        if (!notification.persistent) {
            setTimeout(() => {
                browserNotification.close();
            }, 5000);
        }
    }

    /**
     * Show in-app notification
     */
    showInAppNotification(notification) {
        const container = this.getNotificationContainer();
        const notificationElement = this.createNotificationElement(notification);

        container.appendChild(notificationElement);

        // Animate in
        setTimeout(() => {
            notificationElement.classList.add('show');
        }, 100);

        // Auto remove after 5 seconds unless persistent
        if (!notification.persistent) {
            setTimeout(() => {
                this.removeInAppNotification(notificationElement);
            }, 5000);
        }
    }

    /**
     * Get or create notification container
     */
    getNotificationContainer() {
        let container = document.querySelector('.notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notifications-container';
            document.body.appendChild(container);
        }
        return container;
    }

    /**
     * Create notification element
     */
    createNotificationElement(notification) {
        const element = document.createElement('div');
        element.className = `notification-item notification-${notification.type}`;
        element.setAttribute('data-notification-id', notification.id);

        element.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="${notification.icon}" aria-hidden="true"></i>
                </div>
                <div class="notification-text">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-message">${notification.message}</div>
                </div>
                <button class="notification-close" data-action="close-notification">
                    <i class="fas fa-times" aria-hidden="true"></i>
                </button>
            </div>
        `;

        // Add close handler
        element.querySelector('.notification-close').addEventListener('click', (e) => {
            e.stopPropagation();
            this.removeInAppNotification(element);
        });

        return element;
    }

    /**
     * Remove in-app notification
     */
    removeInAppNotification(element) {
        element.classList.add('hide');
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 300);
    }

    /**
     * Handle notification click
     */
    handleNotificationClick(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (!notification) return;

        // Mark as read
        notification.read = true;
        this.updateUnreadCount();
        this.saveNotifications();

        // Navigate to URL if provided
        if (notification.url) {
            window.location.href = notification.url;
        }

        // Notify observers
        this.notifyObservers('notificationClicked', notification);
    }

    /**
     * Mark all notifications as read
     */
    markAllAsRead() {
        this.notifications.forEach(notification => {
            notification.read = true;
        });
        this.updateUnreadCount();
        this.saveNotifications();
        this.notifyObservers('allNotificationsRead');
    }

    /**
     * Update unread count
     */
    updateUnreadCount() {
        this.unreadCount = this.notifications.filter(n => !n.read).length;
        this.updateUnreadBadge();
    }

    /**
     * Update unread badge in UI
     */
    updateUnreadBadge() {
        const badges = document.querySelectorAll('.notification-badge');
        badges.forEach(badge => {
            if (this.unreadCount > 0) {
                badge.textContent = this.unreadCount > 99 ? '99+' : this.unreadCount;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        });
    }

    /**
     * Get default icon for notification type
     */
    getDefaultIcon(type) {
        const icons = {
            info: 'fas fa-info-circle',
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle',
            like: 'fas fa-heart',
            comment: 'fas fa-comment',
            follow: 'fas fa-user-plus',
            message: 'fas fa-envelope'
        };
        return icons[type] || icons.info;
    }

    /**
     * Generate unique ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Add observer
     */
    addObserver(callback) {
        this.observers.add(callback);
    }

    /**
     * Remove observer
     */
    removeObserver(callback) {
        this.observers.delete(callback);
    }

    /**
     * Notify observers
     */
    notifyObservers(event, data) {
        this.observers.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.error('Observer error:', error);
            }
        });
    }

    /**
     * Get notifications
     */
    getNotifications(limit = 50) {
        return this.notifications.slice(0, limit);
    }

    /**
     * Get unread count
     */
    getUnreadCount() {
        return this.unreadCount;
    }

    /**
     * Clear all notifications
     */
    clearAll() {
        this.notifications = [];
        this.unreadCount = 0;
        this.updateUnreadBadge();
        this.saveNotifications();
        this.notifyObservers('notificationsCleared');
    }

    /**
     * Clear old notifications
     */
    clearOld(days = 7) {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - days);

        this.notifications = this.notifications.filter(notification =>
            new Date(notification.timestamp) > cutoff
        );

        this.updateUnreadCount();
        this.saveNotifications();
    }

    /**
     * Test notification
     */
    test() {
        this.showNotification({
            title: 'Test Notification',
            message: 'This is a test notification',
            type: 'info'
        });
    }

    /**
     * Получение уведомлений с сервера
     */
    async fetchNotifications(limit = 20, offset = 0) {
        try {
            const response = await fetch(`${this.apiBase}/api/notifications/?limit=${limit}&offset=${offset}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (response.ok) {
                const notifications = await response.json();
                this.notifications = notifications;
                this.renderNotifications();
                return notifications;
            }
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        }
        return [];
    }

    /**
     * Получение статистики уведомлений
     */
    async fetchNotificationStats() {
        try {
            const response = await fetch(`${this.apiBase}/api/notifications/stats`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (response.ok) {
                const stats = await response.json();
                this.updateNotificationBadge(stats.unread);
                return stats;
            }
        } catch (error) {
            console.error('Failed to fetch notification stats:', error);
        }
        return { total: 0, unread: 0, by_type: {} };
    }

    /**
     * Отметить уведомление как прочитанное
     */
    async markAsRead(notificationId) {
        try {
            const response = await fetch(`${this.apiBase}/api/notifications/mark-read/${notificationId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (response.ok) {
                // Обновляем локальное состояние
                const notification = this.notifications.find(n => n.id === notificationId);
                if (notification) {
                    notification.is_read = true;
                    this.updateUnreadCount();
                    this.updateNotificationBadge();
                }
                return true;
            }
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
        return false;
    }

    /**
     * Отметить все уведомления как прочитанные
     */
    async markAllAsRead() {
        try {
            const response = await fetch(`${this.apiBase}/api/notifications/mark-all-read`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (response.ok) {
                // Обновляем локальное состояние
                this.notifications.forEach(n => n.is_read = true);
                this.updateUnreadCount();
                this.updateNotificationBadge(0);
                return true;
            }
        } catch (error) {
            console.error('Failed to mark all notifications as read:', error);
        }
        return false;
    }

    /**
     * Отправка тестового уведомления
     */
    async sendTestNotification() {
        try {
            const response = await fetch(`${this.apiBase}/api/notifications/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    type: 'test',
                    title: 'Test Notification',
                    message: 'This is a test notification from the server',
                    channels: ['in_app'],
                    data: { test: true }
                })
            });

            if (response.ok) {
                this.showNotification({
                    title: 'Test Sent',
                    message: 'Test notification sent successfully',
                    type: 'success'
                });
                // Обновляем список уведомлений
                await this.fetchNotifications();
            }
        } catch (error) {
            console.error('Failed to send test notification:', error);
        }
    }
}

// Export for global access
window.NotificationManager = NotificationManager;
console.log('🔔 Notification utilities loaded');
