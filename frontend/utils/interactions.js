/**
 * Interactions Manager - система лайков, комментариев и уведомлений
 */

class InteractionsManager {
    constructor() {
        this.likes = new Map(); // Хранилище лайков
        this.comments = new Map(); // Хранилище комментариев
        this.notifications = []; // Уведомления
        this.isInitialized = false;

        console.log('💬 Interactions Manager initialized');
    }

    /**
     * Инициализация системы взаимодействий
     */
    async init() {
        try {
            // Загружаем сохраненные данные
            await this.loadStoredData();

            // Настраиваем обработчики событий
            this.setupEventListeners();

            // Инициализируем уведомления
            this.initNotifications();

            this.isInitialized = true;
            console.log('💬 Interactions system initialized successfully');
        } catch (error) {
            console.error('💬 Failed to initialize interactions:', error);
        }
    }

    /**
     * Загрузка сохраненных данных из localStorage
     */
    async loadStoredData() {
        try {
            // Загружаем лайки
            const storedLikes = localStorage.getItem('interactions_likes');
            if (storedLikes) {
                this.likes = new Map(JSON.parse(storedLikes));
            }

            // Загружаем комментарии
            const storedComments = localStorage.getItem('interactions_comments');
            if (storedComments) {
                this.comments = new Map(JSON.parse(storedComments));
            }

            // Загружаем уведомления
            const storedNotifications = localStorage.getItem('interactions_notifications');
            if (storedNotifications) {
                this.notifications = JSON.parse(storedNotifications);
            }

            console.log('💬 Stored data loaded:', {
                likes: this.likes.size,
                comments: this.comments.size,
                notifications: this.notifications.length
            });
        } catch (error) {
            console.error('💬 Error loading stored data:', error);
        }
    }

    /**
     * Сохранение данных в localStorage
     */
    saveData() {
        try {
            localStorage.setItem('interactions_likes', JSON.stringify([...this.likes]));
            localStorage.setItem('interactions_comments', JSON.stringify([...this.comments]));
            localStorage.setItem('interactions_notifications', JSON.stringify(this.notifications));
        } catch (error) {
            console.error('💬 Error saving data:', error);
        }
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Обработчик для лайков
        document.addEventListener('click', (e) => {
            if (e.target.matches('.like-btn, .like-btn *')) {
                e.preventDefault();
                const postId = e.target.closest('[data-post-id]')?.dataset.postId;
                if (postId) {
                    this.toggleLike(postId);
                }
            }
        });

        // Обработчик для комментариев
        document.addEventListener('click', (e) => {
            if (e.target.matches('.comment-btn, .comment-btn *')) {
                e.preventDefault();
                const postId = e.target.closest('[data-post-id]')?.dataset.postId;
                if (postId) {
                    this.toggleComments(postId);
                }
            }
        });

        // Обработчик для отправки комментариев
        document.addEventListener('submit', (e) => {
            if (e.target.matches('.comment-form')) {
                e.preventDefault();
                const postId = e.target.closest('[data-post-id]')?.dataset.postId;
                const commentText = e.target.querySelector('.comment-input')?.value;
                if (postId && commentText) {
                    this.addComment(postId, commentText);
                    e.target.reset();
                }
            }
        });

        console.log('💬 Event listeners setup complete');
    }

    /**
     * Инициализация уведомлений
     */
    initNotifications() {
        // Проверяем поддержку уведомлений
        if ('Notification' in window) {
            if (Notification.permission === 'granted') {
                console.log('💬 Notifications already granted');
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(permission => {
                    console.log('💬 Notification permission:', permission);
                });
            }
        }
    }

    /**
     * Переключение лайка
     */
    async toggleLike(postId) {
        try {
            const isLiked = this.likes.has(postId);

            if (isLiked) {
                // Убираем лайк
                this.likes.delete(postId);
                await this.unlikePost(postId);
                this.showNotification('Лайк убран', 'info');
            } else {
                // Добавляем лайк
                this.likes.set(postId, {
                    postId,
                    timestamp: Date.now(),
                    userId: this.getCurrentUserId()
                });
                await this.likePost(postId);
                this.showNotification('Лайк добавлен', 'success');
            }

            // Обновляем UI
            this.updateLikeUI(postId);

            // Сохраняем данные
            this.saveData();

            console.log('💬 Like toggled for post:', postId, 'liked:', !isLiked);
        } catch (error) {
            console.error('💬 Error toggling like:', error);
            this.showNotification('Ошибка при изменении лайка', 'error');
        }
    }

    /**
     * Лайк поста через API
     */
    async likePost(postId) {
        try {
            if (window.SocialService && typeof window.SocialService.likePost === 'function') {
                await window.SocialService.likePost(postId);
            }
        } catch (error) {
            console.error('💬 API like error:', error);
        }
    }

    /**
     * Убираем лайк через API
     */
    async unlikePost(postId) {
        try {
            if (window.SocialService && typeof window.SocialService.unlikePost === 'function') {
                await window.SocialService.unlikePost(postId);
            }
        } catch (error) {
            console.error('💬 API unlike error:', error);
        }
    }

    /**
     * Обновление UI лайка
     */
    updateLikeUI(postId) {
        const likeBtn = document.querySelector(`[data-post-id="${postId}"] .like-btn`);
        if (!likeBtn) return;

        const isLiked = this.likes.has(postId);
        const icon = likeBtn.querySelector('i');
        const count = likeBtn.querySelector('.like-count');

        if (icon) {
            icon.className = isLiked ? 'fas fa-heart' : 'far fa-heart';
        }

        if (count) {
            const currentCount = parseInt(count.textContent) || 0;
            const newCount = isLiked ? currentCount + 1 : Math.max(0, currentCount - 1);
            count.textContent = newCount;
        }

        // Анимация
        likeBtn.classList.toggle('liked', isLiked);
        if (isLiked) {
            this.animateLike(likeBtn);
        }
    }

    /**
     * Анимация лайка
     */
    animateLike(element) {
        element.style.transform = 'scale(1.2)';
        element.style.color = '#e74c3c';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    }

    /**
     * Переключение комментариев
     */
    toggleComments(postId) {
        const commentsContainer = document.querySelector(`[data-post-id="${postId}"] .comments-container`);
        if (!commentsContainer) return;

        const isVisible = commentsContainer.style.display !== 'none';
        commentsContainer.style.display = isVisible ? 'none' : 'block';

        if (!isVisible) {
            this.loadComments(postId);
        }
    }

    /**
     * Загрузка комментариев
     */
    async loadComments(postId) {
        try {
            // Загружаем комментарии из API
            if (window.SocialService && typeof window.SocialService.getComments === 'function') {
                const comments = await window.SocialService.getComments(postId);
                this.renderComments(postId, comments);
            } else {
                // Используем локальные комментарии
                const comments = this.comments.get(postId) || [];
                this.renderComments(postId, comments);
            }
        } catch (error) {
            console.error('💬 Error loading comments:', error);
        }
    }

    /**
     * Добавление комментария
     */
    async addComment(postId, text) {
        try {
            const comment = {
                id: Date.now().toString(),
                postId,
                text,
                author: this.getCurrentUser(),
                timestamp: Date.now()
            };

            // Добавляем в локальное хранилище
            if (!this.comments.has(postId)) {
                this.comments.set(postId, []);
            }
            this.comments.get(postId).push(comment);

            // Отправляем через API
            if (window.SocialService && typeof window.SocialService.addComment === 'function') {
                await window.SocialService.addComment(postId, text);
            }

            // Обновляем UI
            this.renderComments(postId, this.comments.get(postId));

            // Показываем уведомление
            this.showNotification('Комментарий добавлен', 'success');

            // Сохраняем данные
            this.saveData();

            console.log('💬 Comment added:', comment);
        } catch (error) {
            console.error('💬 Error adding comment:', error);
            this.showNotification('Ошибка при добавлении комментария', 'error');
        }
    }

    /**
     * Рендеринг комментариев
     */
    renderComments(postId, comments) {
        const commentsContainer = document.querySelector(`[data-post-id="${postId}"] .comments-container`);
        if (!commentsContainer) return;

        // Убеждаемся, что comments - это массив
        const commentsArray = Array.isArray(comments) ? comments : [];
        const commentsHTML = commentsArray.map(comment => `
            <div class="comment-item">
                <div class="comment-author">
                    <img src="${comment.author?.avatar || 'https://via.placeholder.com/30x30?text=U'}" 
                         alt="${comment.author?.name || 'User'}" class="comment-avatar">
                    <span class="comment-author-name">${comment.author?.name || 'User'}</span>
                </div>
                <div class="comment-text">${this.escapeHtml(comment.text)}</div>
                <div class="comment-time">${this.formatTime(comment.timestamp)}</div>
            </div>
        `).join('');

        commentsContainer.innerHTML = `
            <div class="comments-list">
                ${commentsHTML}
            </div>
            <form class="comment-form">
                <div class="comment-input-group">
                    <input type="text" class="comment-input" placeholder="Написать комментарий..." required>
                    <button type="submit" class="comment-submit-btn">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </form>
        `;
    }

    /**
     * Показ уведомления
     */
    showNotification(message, type = 'info') {
        // Используем глобальную систему уведомлений
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
     * Получение текущего пользователя
     */
    getCurrentUser() {
        // Пытаемся получить из AuthService
        if (window.AuthService && window.AuthService.user) {
            return window.AuthService.user;
        }

        // Fallback данные
        return {
            id: 1,
            name: 'User',
            avatar: 'https://via.placeholder.com/40x40?text=U'
        };
    }

    /**
     * Получение ID текущего пользователя
     */
    getCurrentUserId() {
        const user = this.getCurrentUser();
        return user?.id || 1;
    }

    /**
     * Экранирование HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Форматирование времени
     */
    formatTime(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'только что';
        if (minutes < 60) return `${minutes}м назад`;
        if (hours < 24) return `${hours}ч назад`;
        return `${days}д назад`;
    }

    /**
     * Получение статистики
     */
    getStats() {
        return {
            totalLikes: this.likes.size,
            totalComments: Array.from(this.comments.values()).reduce((sum, comments) => sum + comments.length, 0),
            totalNotifications: this.notifications.length
        };
    }

    /**
     * Очистка данных
     */
    clearData() {
        this.likes.clear();
        this.comments.clear();
        this.notifications = [];
        this.saveData();
        console.log('💬 All interactions data cleared');
    }
}

// Экспорт для глобального доступа
window.InteractionsManager = InteractionsManager;