/**
 * Real-time Manager - система WebSocket и live updates
 */

class RealtimeManager {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.isConnected = false;
        this.eventListeners = new Map();
        this.messageQueue = [];
        this.heartbeatInterval = null;
        this.isInitialized = false;

        console.log('⚡ Realtime Manager initialized');
    }

    /**
     * Инициализация системы реального времени
     */
    async init() {
        try {
            // Проверяем поддержку WebSocket
            if (!window.WebSocket) {
                console.warn('⚡ WebSocket not supported, using polling fallback');
                this.initPollingFallback();
                return;
            }

            // Подключаемся к WebSocket
            await this.connect();

            // Настраиваем обработчики событий
            this.setupEventListeners();

            // Настраиваем heartbeat
            this.setupHeartbeat();

            this.isInitialized = true;
            console.log('⚡ Realtime system initialized successfully');
        } catch (error) {
            console.error('⚡ Failed to initialize realtime:', error);
            // Fallback на polling
            this.initPollingFallback();
        }
    }

    /**
     * Подключение к WebSocket
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                const wsUrl = this.getWebSocketUrl();
                console.log('⚡ Connecting to WebSocket:', wsUrl);

                this.ws = new WebSocket(wsUrl);

                this.ws.onopen = (event) => {
                    console.log('⚡ WebSocket connected');
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this.processMessageQueue();
                    this.setupHeartbeat();

                    // Подписываемся на все типы событий
                    this.subscribeToEvents();

                    resolve();
                };

                this.ws.onmessage = (event) => {
                    this.handleMessage(event);
                };

                this.ws.onclose = (event) => {
                    console.log('⚡ WebSocket disconnected:', event.code, event.reason);
                    this.isConnected = false;
                    this.clearHeartbeat();
                    this.handleReconnect();
                };

                this.ws.onerror = (error) => {
                    console.error('⚡ WebSocket error:', error);
                    reject(error);
                };

                // Таймаут подключения
                setTimeout(() => {
                    if (!this.isConnected) {
                        reject(new Error('WebSocket connection timeout'));
                    }
                }, 5000);

            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Получение URL WebSocket
     */
    getWebSocketUrl() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Всегда используем localhost:5000 для браузера
        const host = 'localhost:5000';
        return `${protocol}//${host}/ws`;
    }

    /**
     * Подписка на события
     */
    subscribeToEvents() {
        const events = ['social', 'ecommerce', 'tasks', 'analytics', 'content', 'system'];
        events.forEach(eventType => {
            this.send({
                type: 'subscribe',
                event_type: eventType
            });
        });
        console.log('⚡ Subscribed to events:', events);
    }

    /**
     * Отправка сообщения через WebSocket
     */
    send(message) {
        if (this.isConnected && this.ws) {
            try {
                this.ws.send(JSON.stringify(message));
                console.log('⚡ Sent message:', message);
            } catch (error) {
                console.error('⚡ Error sending message:', error);
                this.messageQueue.push(message);
            }
        } else {
            console.log('⚡ WebSocket not connected, queuing message:', message);
            this.messageQueue.push(message);
        }
    }

    /**
     * Обработка сообщений WebSocket
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            console.log('⚡ Received message:', data);

            // Обрабатываем разные типы сообщений
            switch (data.type) {
                case 'social_update':
                    this.handleSocialUpdate(data);
                    break;
                case 'ecommerce_update':
                    this.handleEcommerceUpdate(data);
                    break;
                case 'tasks_update':
                    this.handleTasksUpdate(data);
                    break;
                case 'analytics_update':
                    this.handleAnalyticsUpdate(data);
                    break;
                case 'content_update':
                    this.handleContentUpdate(data);
                    break;
                case 'system_notification':
                    this.handleSystemNotification(data);
                    break;
                case 'user_notification':
                    this.handleUserNotification(data);
                    break;
                case 'subscription_confirmed':
                    console.log('⚡ Subscription confirmed:', data.event_type);
                    break;
                case 'unsubscription_confirmed':
                    console.log('⚡ Unsubscription confirmed:', data.event_type);
                    break;
                case 'pong':
                    console.log('⚡ Pong received');
                    break;
                case 'connection':
                    console.log('⚡ Connection message:', data.message);
                    break;
                case 'error':
                    console.error('⚡ WebSocket error:', data.message);
                    break;
                // Legacy support
                case 'post_created':
                    this.handlePostCreated(data);
                    break;
                case 'post_updated':
                    this.handlePostUpdated(data);
                    break;
                case 'post_deleted':
                    this.handlePostDeleted(data);
                    break;
                case 'like_added':
                    this.handleLikeAdded(data);
                    break;
                case 'like_removed':
                    this.handleLikeRemoved(data);
                    break;
                case 'comment_added':
                    this.handleCommentAdded(data);
                    break;
                case 'comment_updated':
                    this.handleCommentUpdated(data);
                    break;
                case 'comment_deleted':
                    this.handleCommentDeleted(data);
                    break;
                case 'user_followed':
                    this.handleUserFollowed(data);
                    break;
                case 'user_unfollowed':
                    this.handleUserUnfollowed(data);
                    break;
                case 'notification':
                    this.handleNotification(data);
                    break;
                case 'pong':
                    // Heartbeat response
                    break;
                default:
                    console.log('⚡ Unknown message type:', data.type);
            }

            // Вызываем пользовательские обработчики
            this.triggerEventListeners(data.type, data);

        } catch (error) {
            console.error('⚡ Error parsing WebSocket message:', error);
        }
    }

    /**
     * Обработка создания поста
     */
    handlePostCreated(data) {
        console.log('⚡ Post created:', data.post);

        // Обновляем социальную ленту
        if (window.socialFeedManager) {
            window.socialFeedManager.addPost(data.post);
        }

        // Показываем уведомление
        this.showNotification('Новый пост от ' + data.post.author.name, 'info');
    }

    /**
     * Обработка обновления поста
     */
    handlePostUpdated(data) {
        console.log('⚡ Post updated:', data.post);

        // Обновляем пост в ленте
        if (window.socialFeedManager) {
            window.socialFeedManager.updatePost(data.post);
        }
    }

    /**
     * Обработка удаления поста
     */
    handlePostDeleted(data) {
        console.log('⚡ Post deleted:', data.postId);

        // Удаляем пост из ленты
        if (window.socialFeedManager) {
            window.socialFeedManager.removePost(data.postId);
        }
    }

    /**
     * Обработка добавления лайка
     */
    handleLikeAdded(data) {
        console.log('⚡ Like added:', data);

        // Обновляем счетчик лайков
        this.updateLikeCount(data.postId, 1);
    }

    /**
     * Обработка удаления лайка
     */
    handleLikeRemoved(data) {
        console.log('⚡ Like removed:', data);

        // Обновляем счетчик лайков
        this.updateLikeCount(data.postId, -1);
    }

    /**
     * Обработка добавления комментария
     */
    handleCommentAdded(data) {
        console.log('⚡ Comment added:', data);

        // Обновляем счетчик комментариев
        this.updateCommentCount(data.postId, 1);

        // Показываем уведомление
        this.showNotification('Новый комментарий к посту', 'info');
    }

    /**
     * Обработка обновления комментария
     */
    handleCommentUpdated(data) {
        console.log('⚡ Comment updated:', data);

        // Обновляем комментарий в UI
        this.updateComment(data.comment);
    }

    /**
     * Обработка удаления комментария
     */
    handleCommentDeleted(data) {
        console.log('⚡ Comment deleted:', data);

        // Обновляем счетчик комментариев
        this.updateCommentCount(data.postId, -1);
    }

    /**
     * Обработка подписки на пользователя
     */
    handleUserFollowed(data) {
        console.log('⚡ User followed:', data);

        // Обновляем счетчик подписчиков
        this.updateFollowerCount(data.userId, 1);

        // Показываем уведомление
        this.showNotification('Новый подписчик!', 'success');
    }

    /**
     * Обработка отписки от пользователя
     */
    handleUserUnfollowed(data) {
        console.log('⚡ User unfollowed:', data);

        // Обновляем счетчик подписчиков
        this.updateFollowerCount(data.userId, -1);
    }

    /**
     * Обработка уведомления
     */
    handleNotification(data) {
        console.log('⚡ Notification received:', data);

        // Показываем уведомление
        if (window.notificationManager) {
            window.notificationManager.show(data.message, data.type || 'info');
        }
    }

    /**
     * Обновление счетчика лайков
     */
    updateLikeCount(postId, delta) {
        const likeBtn = document.querySelector(`[data-post-id="${postId}"] .like-count`);
        if (likeBtn) {
            const currentCount = parseInt(likeBtn.textContent) || 0;
            likeBtn.textContent = Math.max(0, currentCount + delta);
        }
    }

    /**
     * Обновление счетчика комментариев
     */
    updateCommentCount(postId, delta) {
        const commentBtn = document.querySelector(`[data-post-id="${postId}"] .comment-count`);
        if (commentBtn) {
            const currentCount = parseInt(commentBtn.textContent) || 0;
            commentBtn.textContent = Math.max(0, currentCount + delta);
        }
    }

    /**
     * Обновление счетчика подписчиков
     */
    updateFollowerCount(userId, delta) {
        const followerCount = document.querySelector(`[data-user-id="${userId}"] .follower-count`);
        if (followerCount) {
            const currentCount = parseInt(followerCount.textContent) || 0;
            followerCount.textContent = Math.max(0, currentCount + delta);
        }
    }

    /**
     * Обновление комментария
     */
    updateComment(comment) {
        const commentElement = document.querySelector(`[data-comment-id="${comment.id}"]`);
        if (commentElement) {
            const textElement = commentElement.querySelector('.comment-text');
            if (textElement) {
                textElement.textContent = comment.text;
            }
        }
    }

    /**
     * Отправка сообщения
     */
    sendMessage(type, data) {
        const message = {
            type,
            data,
            timestamp: Date.now()
        };

        if (this.isConnected && this.ws) {
            try {
                this.ws.send(JSON.stringify(message));
                console.log('⚡ Message sent:', message);
            } catch (error) {
                console.error('⚡ Error sending message:', error);
                this.messageQueue.push(message);
            }
        } else {
            console.log('⚡ WebSocket not connected, queuing message:', message);
            this.messageQueue.push(message);
        }
    }

    /**
     * Обработка очереди сообщений
     */
    processMessageQueue() {
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.sendMessage(message.type, message.data);
        }
    }

    /**
     * Обработка переподключения
     */
    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

            console.log(`⚡ Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

            setTimeout(() => {
                this.connect().catch(error => {
                    console.error('⚡ Reconnection failed:', error);
                });
            }, delay);
        } else {
            console.error('⚡ Max reconnection attempts reached, switching to polling');
            this.initPollingFallback();
        }
    }

    /**
     * Fallback на polling
     */
    initPollingFallback() {
        console.log('⚡ Initializing polling fallback');

        // Polling каждые 30 секунд (уменьшаем нагрузку)
        setInterval(() => {
            this.pollForUpdates();
        }, 30000);

        this.isInitialized = true;
    }

    /**
     * Polling для обновлений
     */
    async pollForUpdates() {
        try {
            // Получаем последние посты
            if (window.SocialService) {
                const posts = await window.SocialService.getPosts({ limit: 10 });
                this.handlePollingUpdate('posts', posts);
            }

            // Получаем уведомления
            if (window.notificationManager) {
                // Здесь можно добавить API для получения уведомлений
            }

        } catch (error) {
            console.error('⚡ Polling error:', error);
        }
    }

    /**
     * Обработка обновлений от polling
     */
    handlePollingUpdate(type, data) {
        console.log('⚡ Polling update:', type, data);

        switch (type) {
            case 'posts':
                if (window.socialFeedManager && typeof window.socialFeedManager.updateFeed === 'function') {
                    window.socialFeedManager.updateFeed(data);
                } else if (window.SocialModule && typeof window.SocialModule.loadPosts === 'function') {
                    // Fallback to SocialModule
                    window.SocialModule.loadPosts();
                }
                break;
        }
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Обработчик для отправки сообщений
        document.addEventListener('realtime:send', (event) => {
            this.sendMessage(event.detail.type, event.detail.data);
        });

        console.log('⚡ Event listeners setup complete');
    }

    /**
     * Настройка heartbeat
     */
    setupHeartbeat() {
        this.clearHeartbeat();

        this.heartbeatInterval = setInterval(() => {
            if (this.isConnected && this.ws) {
                this.sendMessage('ping', {});
            }
        }, 30000); // Каждые 30 секунд
    }

    /**
     * Очистка heartbeat
     */
    clearHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }

    /**
     * Добавление обработчика событий
     */
    addEventListener(eventType, callback) {
        if (!this.eventListeners.has(eventType)) {
            this.eventListeners.set(eventType, []);
        }
        this.eventListeners.get(eventType).push(callback);
    }

    /**
     * Удаление обработчика событий
     */
    removeEventListener(eventType, callback) {
        if (this.eventListeners.has(eventType)) {
            const listeners = this.eventListeners.get(eventType);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Вызов обработчиков событий
     */
    triggerEventListeners(eventType, data) {
        if (this.eventListeners.has(eventType)) {
            this.eventListeners.get(eventType).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('⚡ Event listener error:', error);
                }
            });
        }
    }

    /**
     * Показ уведомления
     */
    showNotification(message, type = 'info') {
        if (window.notificationManager && typeof window.notificationManager.show === 'function') {
            window.notificationManager.show(message, type);
        } else if (window.Toast) {
            if (type === 'success' && typeof window.Toast.success === 'function') {
                window.Toast.success(message);
            } else if (type === 'error' && typeof window.Toast.error === 'function') {
                window.Toast.error(message);
            } else if (typeof window.Toast.info === 'function') {
                window.Toast.info(message);
            } else {
                alert(message);
            }
        } else {
            alert(message);
        }
    }

    /**
     * Получение статуса подключения
     */
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            reconnectAttempts: this.reconnectAttempts,
            messageQueueLength: this.messageQueue.length
        };
    }

    /**
     * Отключение
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.clearHeartbeat();
        this.isConnected = false;
        console.log('⚡ Realtime disconnected');
    }

    /**
     * Очистка данных
     */
    clearData() {
        this.disconnect();
        this.eventListeners.clear();
        this.messageQueue = [];
        console.log('⚡ All realtime data cleared');
    }
    /**
     * Обработчики новых типов событий
     */
    handleSocialUpdate(data) {
        console.log('⚡ Social update received:', data);
        const event = data.event;
        const eventData = data.data;

        switch (event) {
            case 'post_created':
                this.handlePostCreated(eventData);
                break;
            case 'post_updated':
                this.handlePostUpdated(eventData);
                break;
            case 'post_deleted':
                this.handlePostDeleted(eventData);
                break;
            case 'like_added':
                this.handleLikeAdded(eventData);
                break;
            case 'like_removed':
                this.handleLikeRemoved(eventData);
                break;
            case 'comment_added':
                this.handleCommentAdded(eventData);
                break;
            case 'comment_updated':
                this.handleCommentUpdated(eventData);
                break;
            case 'comment_deleted':
                this.handleCommentDeleted(eventData);
                break;
            case 'user_followed':
                this.handleUserFollowed(eventData);
                break;
            case 'user_unfollowed':
                this.handleUserUnfollowed(eventData);
                break;
            default:
                console.log('⚡ Unknown social event:', event);
        }
    }

    handleEcommerceUpdate(data) {
        console.log('⚡ E-commerce update received:', data);
        // Здесь можно добавить обработку e-commerce событий
        this.showNotification('E-commerce update received', 'info');
    }

    handleTasksUpdate(data) {
        console.log('⚡ Tasks update received:', data);
        // Здесь можно добавить обработку задач
        this.showNotification('Tasks update received', 'info');
    }

    handleAnalyticsUpdate(data) {
        console.log('⚡ Analytics update received:', data);
        // Здесь можно добавить обработку аналитики
        this.showNotification('Analytics update received', 'info');
    }

    handleContentUpdate(data) {
        console.log('⚡ Content update received:', data);
        // Здесь можно добавить обработку контента
        this.showNotification('Content update received', 'info');
    }

    handleSystemNotification(data) {
        console.log('⚡ System notification received:', data);
        this.showNotification(data.message, data.notification_type || 'info');
    }

    handleUserNotification(data) {
        console.log('⚡ User notification received:', data);
        this.showNotification(data.message, data.notification_type || 'info');
    }
}

// Экспорт для глобального доступа
console.log('⚡ RealtimeManager class defined:', typeof RealtimeManager);
window.RealtimeManager = RealtimeManager;
console.log('⚡ RealtimeManager exported to window:', typeof window.RealtimeManager);
