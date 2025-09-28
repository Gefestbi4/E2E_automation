/**
 * Social Connections Manager - система подписок, поиска и профилей
 */

class SocialConnectionsManager {
    constructor() {
        this.following = new Map(); // Подписки пользователя
        this.followers = new Map(); // Подписчики пользователя
        this.searchResults = []; // Результаты поиска
        this.profiles = new Map(); // Кэш профилей
        this.isInitialized = false;

        console.log('👥 Social Connections Manager initialized');
    }

    /**
     * Инициализация системы социальных связей
     */
    async init() {
        try {
            // Загружаем сохраненные данные
            await this.loadStoredData();

            // Настраиваем обработчики событий
            this.setupEventListeners();

            // Инициализируем поиск
            this.initSearch();

            this.isInitialized = true;
            console.log('👥 Social connections system initialized successfully');
        } catch (error) {
            console.error('👥 Failed to initialize social connections:', error);
        }
    }

    /**
     * Загрузка сохраненных данных из localStorage
     */
    async loadStoredData() {
        try {
            // Загружаем подписки
            const storedFollowing = localStorage.getItem('social_following');
            if (storedFollowing) {
                this.following = new Map(JSON.parse(storedFollowing));
            }

            // Загружаем подписчиков
            const storedFollowers = localStorage.getItem('social_followers');
            if (storedFollowers) {
                this.followers = new Map(JSON.parse(storedFollowers));
            }

            // Загружаем профили
            const storedProfiles = localStorage.getItem('social_profiles');
            if (storedProfiles) {
                this.profiles = new Map(JSON.parse(storedProfiles));
            }

            console.log('👥 Stored data loaded:', {
                following: this.following.size,
                followers: this.followers.size,
                profiles: this.profiles.size
            });
        } catch (error) {
            console.error('👥 Error loading stored data:', error);
        }
    }

    /**
     * Сохранение данных в localStorage
     */
    saveData() {
        try {
            localStorage.setItem('social_following', JSON.stringify([...this.following]));
            localStorage.setItem('social_followers', JSON.stringify([...this.followers]));
            localStorage.setItem('social_profiles', JSON.stringify([...this.profiles]));
        } catch (error) {
            console.error('👥 Error saving data:', error);
        }
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Обработчик для подписок
        document.addEventListener('click', (e) => {
            if (e.target.matches('.follow-btn, .follow-btn *')) {
                e.preventDefault();
                const userId = e.target.closest('[data-user-id]')?.dataset.userId;
                if (userId) {
                    this.toggleFollow(userId);
                }
            }
        });

        // Обработчик для поиска
        document.addEventListener('input', (e) => {
            if (e.target.matches('.user-search-input')) {
                const query = e.target.value.trim();
                if (query.length >= 2) {
                    this.searchUsers(query);
                } else {
                    this.clearSearchResults();
                }
            }
        });

        // Обработчик для просмотра профилей
        document.addEventListener('click', (e) => {
            if (e.target.matches('.view-profile-btn, .view-profile-btn *')) {
                e.preventDefault();
                const userId = e.target.closest('[data-user-id]')?.dataset.userId;
                if (userId) {
                    this.viewProfile(userId);
                }
            }
        });

        console.log('👥 Event listeners setup complete');
    }

    /**
     * Инициализация поиска
     */
    initSearch() {
        // Создаем контейнер для результатов поиска если его нет
        this.createSearchContainer();
    }

    /**
     * Создание контейнера для результатов поиска
     */
    createSearchContainer() {
        let searchContainer = document.getElementById('search-results-container');
        if (!searchContainer) {
            searchContainer = document.createElement('div');
            searchContainer.id = 'search-results-container';
            searchContainer.className = 'search-results-container';
            searchContainer.style.display = 'none';
            document.body.appendChild(searchContainer);
        }
    }

    /**
     * Переключение подписки
     */
    async toggleFollow(userId) {
        try {
            const isFollowing = this.following.has(userId);

            if (isFollowing) {
                // Отписываемся
                this.following.delete(userId);
                await this.unfollowUser(userId);
                this.showNotification('Вы отписались от пользователя', 'info');
            } else {
                // Подписываемся
                this.following.set(userId, {
                    userId,
                    timestamp: Date.now(),
                    followedBy: this.getCurrentUserId()
                });
                await this.followUser(userId);
                this.showNotification('Вы подписались на пользователя', 'success');
            }

            // Обновляем UI
            this.updateFollowUI(userId);

            // Сохраняем данные
            this.saveData();

            console.log('👥 Follow toggled for user:', userId, 'following:', !isFollowing);
        } catch (error) {
            console.error('👥 Error toggling follow:', error);
            this.showNotification('Ошибка при изменении подписки', 'error');
        }
    }

    /**
     * Подписка на пользователя через API
     */
    async followUser(userId) {
        try {
            if (window.SocialService && typeof window.SocialService.followUser === 'function') {
                await window.SocialService.followUser(userId);
            }
        } catch (error) {
            console.error('👥 API follow error:', error);
        }
    }

    /**
     * Отписка от пользователя через API
     */
    async unfollowUser(userId) {
        try {
            if (window.SocialService && typeof window.SocialService.unfollowUser === 'function') {
                await window.SocialService.unfollowUser(userId);
            }
        } catch (error) {
            console.error('👥 API unfollow error:', error);
        }
    }

    /**
     * Обновление UI подписки
     */
    updateFollowUI(userId) {
        const followBtn = document.querySelector(`[data-user-id="${userId}"] .follow-btn`);
        if (!followBtn) return;

        const isFollowing = this.following.has(userId);
        const icon = followBtn.querySelector('i');
        const text = followBtn.querySelector('.follow-text');

        if (icon) {
            icon.className = isFollowing ? 'fas fa-user-minus' : 'fas fa-user-plus';
        }

        if (text) {
            text.textContent = isFollowing ? 'Отписаться' : 'Подписаться';
        }

        // Анимация
        followBtn.classList.toggle('following', isFollowing);
        if (isFollowing) {
            this.animateFollow(followBtn);
        }
    }

    /**
     * Анимация подписки
     */
    animateFollow(element) {
        element.style.transform = 'scale(1.1)';
        element.style.backgroundColor = '#27ae60';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    }

    /**
     * Поиск пользователей
     */
    async searchUsers(query) {
        try {
            console.log('👥 Searching users:', query);

            // Показываем индикатор загрузки
            this.showSearchLoading();

            // Ищем в API
            let users = [];
            if (window.SocialService && typeof window.SocialService.searchUsers === 'function') {
                users = await window.SocialService.searchUsers(query);
            } else {
                // Fallback - поиск в локальных данных
                users = this.searchUsersLocal(query);
            }

            this.searchResults = users;
            this.renderSearchResults(users);

            console.log('👥 Search results:', users.length);
        } catch (error) {
            console.error('👥 Error searching users:', error);
            this.showNotification('Ошибка при поиске пользователей', 'error');
        }
    }

    /**
     * Локальный поиск пользователей
     */
    searchUsersLocal(query) {
        // Mock данные для демонстрации
        const mockUsers = [
            {
                id: '1',
                username: 'john_doe',
                full_name: 'John Doe',
                avatar: 'https://via.placeholder.com/50x50?text=JD',
                bio: 'Software Developer',
                followers_count: 150,
                following_count: 75,
                posts_count: 42
            },
            {
                id: '2',
                username: 'jane_smith',
                full_name: 'Jane Smith',
                avatar: 'https://via.placeholder.com/50x50?text=JS',
                bio: 'UI/UX Designer',
                followers_count: 89,
                following_count: 120,
                posts_count: 28
            },
            {
                id: '3',
                username: 'mike_wilson',
                full_name: 'Mike Wilson',
                avatar: 'https://via.placeholder.com/50x50?text=MW',
                bio: 'Product Manager',
                followers_count: 203,
                following_count: 95,
                posts_count: 67
            }
        ];

        return mockUsers.filter(user =>
            user.username.toLowerCase().includes(query.toLowerCase()) ||
            user.full_name.toLowerCase().includes(query.toLowerCase()) ||
            user.bio.toLowerCase().includes(query.toLowerCase())
        );
    }

    /**
     * Показ индикатора загрузки поиска
     */
    showSearchLoading() {
        const container = document.getElementById('search-results-container');
        if (container) {
            container.innerHTML = `
                <div class="search-loading">
                    <div class="loading-spinner"></div>
                    <p>Поиск пользователей...</p>
                </div>
            `;
            container.style.display = 'block';
        }
    }

    /**
     * Рендеринг результатов поиска
     */
    renderSearchResults(users) {
        const container = document.getElementById('search-results-container');
        if (!container) return;

        if (users.length === 0) {
            container.innerHTML = `
                <div class="search-no-results">
                    <i class="fas fa-search"></i>
                    <p>Пользователи не найдены</p>
                </div>
            `;
        } else {
            const usersHTML = users.map(user => this.createUserCardHTML(user)).join('');
            container.innerHTML = `
                <div class="search-results">
                    <h3>Найденные пользователи (${users.length})</h3>
                    <div class="users-list">
                        ${usersHTML}
                    </div>
                </div>
            `;
        }

        container.style.display = 'block';
    }

    /**
     * Создание HTML карточки пользователя
     */
    createUserCardHTML(user) {
        const isFollowing = this.following.has(user.id);

        return `
            <div class="user-card" data-user-id="${user.id}">
                <div class="user-avatar">
                    <img src="${user.avatar || 'https://via.placeholder.com/50x50?text=U'}" 
                         alt="${user.full_name || user.username}" 
                         class="avatar-img">
                </div>
                <div class="user-info">
                    <h4 class="user-name">${user.full_name || user.username}</h4>
                    <p class="user-username">@${user.username}</p>
                    <p class="user-bio">${user.bio || 'Нет описания'}</p>
                    <div class="user-stats">
                        <span class="stat">
                            <i class="fas fa-users"></i>
                            ${user.followers_count || 0} подписчиков
                        </span>
                        <span class="stat">
                            <i class="fas fa-user-plus"></i>
                            ${user.following_count || 0} подписок
                        </span>
                        <span class="stat">
                            <i class="fas fa-image"></i>
                            ${user.posts_count || 0} постов
                        </span>
                    </div>
                </div>
                <div class="user-actions">
                    <button class="btn btn-primary follow-btn ${isFollowing ? 'following' : ''}" 
                            data-user-id="${user.id}">
                        <i class="fas fa-user-${isFollowing ? 'minus' : 'plus'}"></i>
                        <span class="follow-text">${isFollowing ? 'Отписаться' : 'Подписаться'}</span>
                    </button>
                    <button class="btn btn-secondary view-profile-btn" 
                            data-user-id="${user.id}">
                        <i class="fas fa-eye"></i>
                        Профиль
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Очистка результатов поиска
     */
    clearSearchResults() {
        const container = document.getElementById('search-results-container');
        if (container) {
            container.style.display = 'none';
            container.innerHTML = '';
        }
        this.searchResults = [];
    }

    /**
     * Просмотр профиля пользователя
     */
    async viewProfile(userId) {
        try {
            console.log('👥 Viewing profile:', userId);

            // Загружаем профиль
            let profile = this.profiles.get(userId);
            if (!profile) {
                profile = await this.loadUserProfile(userId);
                if (profile) {
                    this.profiles.set(userId, profile);
                    this.saveData();
                }
            }

            if (profile) {
                this.showProfileModal(profile);
            } else {
                this.showNotification('Профиль не найден', 'error');
            }
        } catch (error) {
            console.error('👥 Error viewing profile:', error);
            this.showNotification('Ошибка при загрузке профиля', 'error');
        }
    }

    /**
     * Загрузка профиля пользователя
     */
    async loadUserProfile(userId) {
        try {
            if (window.SocialService && typeof window.SocialService.getUserProfile === 'function') {
                return await window.SocialService.getUserProfile(userId);
            } else {
                // Fallback - возвращаем mock данные
                return {
                    id: userId,
                    username: 'user_' + userId,
                    full_name: 'User ' + userId,
                    avatar: 'https://via.placeholder.com/100x100?text=U',
                    bio: 'Пользователь платформы',
                    followers_count: Math.floor(Math.random() * 1000),
                    following_count: Math.floor(Math.random() * 500),
                    posts_count: Math.floor(Math.random() * 100),
                    joined_date: new Date().toISOString(),
                    is_following: this.following.has(userId)
                };
            }
        } catch (error) {
            console.error('👥 Error loading profile:', error);
            return null;
        }
    }

    /**
     * Показ модального окна профиля
     */
    showProfileModal(profile) {
        const modal = document.createElement('div');
        modal.className = 'profile-modal-overlay';
        modal.innerHTML = `
            <div class="profile-modal">
                <div class="profile-modal-header">
                    <h2>Профиль пользователя</h2>
                    <button class="profile-modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="profile-modal-content">
                    <div class="profile-header">
                        <div class="profile-avatar">
                            <img src="${profile.avatar || 'https://via.placeholder.com/100x100?text=U'}" 
                                 alt="${profile.full_name || profile.username}">
                        </div>
                        <div class="profile-info">
                            <h3>${profile.full_name || profile.username}</h3>
                            <p class="profile-username">@${profile.username}</p>
                            <p class="profile-bio">${profile.bio || 'Нет описания'}</p>
                        </div>
                    </div>
                    <div class="profile-stats">
                        <div class="stat-item">
                            <span class="stat-number">${profile.followers_count || 0}</span>
                            <span class="stat-label">Подписчиков</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">${profile.following_count || 0}</span>
                            <span class="stat-label">Подписок</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">${profile.posts_count || 0}</span>
                            <span class="stat-label">Постов</span>
                        </div>
                    </div>
                    <div class="profile-actions">
                        <button class="btn btn-primary follow-btn ${profile.is_following ? 'following' : ''}" 
                                data-user-id="${profile.id}">
                            <i class="fas fa-user-${profile.is_following ? 'minus' : 'plus'}"></i>
                            <span class="follow-text">${profile.is_following ? 'Отписаться' : 'Подписаться'}</span>
                        </button>
                        <button class="btn btn-secondary" onclick="this.closest('.profile-modal-overlay').remove()">
                            <i class="fas fa-times"></i>
                            Закрыть
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Обработчик закрытия
        modal.querySelector('.profile-modal-close').addEventListener('click', () => {
            modal.remove();
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    /**
     * Получение списка подписок
     */
    getFollowing() {
        return Array.from(this.following.values());
    }

    /**
     * Получение списка подписчиков
     */
    getFollowers() {
        return Array.from(this.followers.values());
    }

    /**
     * Проверка подписки
     */
    isFollowing(userId) {
        return this.following.has(userId);
    }

    /**
     * Получение статистики
     */
    getStats() {
        return {
            following: this.following.size,
            followers: this.followers.size,
            profiles: this.profiles.size,
            searchResults: this.searchResults.length
        };
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
     * Получение текущего пользователя
     */
    getCurrentUser() {
        if (window.AuthService && window.AuthService.user) {
            return window.AuthService.user;
        }

        return {
            id: 1,
            username: 'current_user',
            full_name: 'Current User',
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
     * Очистка данных
     */
    clearData() {
        this.following.clear();
        this.followers.clear();
        this.profiles.clear();
        this.searchResults = [];
        this.saveData();
        console.log('👥 All social connections data cleared');
    }
}

// Экспорт для глобального доступа
console.log('👥 SocialConnectionsManager class defined:', typeof SocialConnectionsManager);
window.SocialConnectionsManager = SocialConnectionsManager;
console.log('👥 SocialConnectionsManager exported to window:', typeof window.SocialConnectionsManager);
