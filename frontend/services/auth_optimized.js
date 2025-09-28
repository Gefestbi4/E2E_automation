/**
 * Оптимизированный сервис авторизации для Automation Learning Platform
 * Управляет аутентификацией пользователей, токенами и защищенными запросами
 */

class AuthService {
    constructor() {
        this.apiBase = (document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000').replace(/\/?$/, '');
        this.refreshTimer = null;
        this.isRefreshing = false;
        this.pendingRequests = [];
        this.user = null;
        this.init();
    }

    /**
     * Инициализация сервиса
     */
    init() {
        this.setupTokenRefresh();
        this.checkAuthStatus();
        this.setupRequestInterceptors();
    }

    /**
     * Настройка перехватчиков запросов для автоматического обновления токена
     */
    setupRequestInterceptors() {
        // Сохраняем оригинальный fetch
        this.originalFetch = window.fetch;

        // Перехватываем все fetch запросы
        window.fetch = async (url, options = {}) => {
            return this.interceptRequest(url, options);
        };
    }

    /**
     * Перехват запроса с автоматическим обновлением токена
     */
    async interceptRequest(url, options = {}) {
        // Добавляем токен к запросу
        const token = localStorage.getItem('auth_token');
        if (token && !options.headers?.['Authorization']) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            };
        }

        try {
            const response = await this.originalFetch(url, options);

            // Если токен истек, пытаемся обновить его
            if (response.status === 401 && token) {
                return this.handleTokenExpiry(url, options);
            }

            return response;
        } catch (error) {
            console.error('Request failed:', error);
            throw error;
        }
    }

    /**
     * Обработка истечения токена
     */
    async handleTokenExpiry(originalUrl, originalOptions) {
        if (this.isRefreshing) {
            // Если уже обновляем токен, ждем в очереди
            return new Promise((resolve, reject) => {
                this.pendingRequests.push({ resolve, reject, url: originalUrl, options: originalOptions });
            });
        }

        try {
            this.isRefreshing = true;
            await this.refreshAccessToken();

            // Повторяем оригинальный запрос с новым токеном
            const newToken = localStorage.getItem('auth_token');
            const newOptions = {
                ...originalOptions,
                headers: {
                    ...originalOptions.headers,
                    'Authorization': `Bearer ${newToken}`
                }
            };

            const response = await this.originalFetch(originalUrl, newOptions);

            // Обрабатываем ожидающие запросы
            this.pendingRequests.forEach(({ resolve, url, options }) => {
                const newOptions = {
                    ...options,
                    headers: {
                        ...options.headers,
                        'Authorization': `Bearer ${newToken}`
                    }
                };
                this.originalFetch(url, newOptions).then(resolve).catch(reject);
            });

            this.pendingRequests = [];
            return response;

        } catch (error) {
            // Если обновление токена не удалось, перенаправляем на логин
            this.pendingRequests.forEach(({ reject }) => reject(error));
            this.pendingRequests = [];
            this.logout();
            throw error;
        } finally {
            this.isRefreshing = false;
        }
    }

    /**
     * Проверка статуса авторизации при загрузке
     */
    async checkAuthStatus() {
        const token = localStorage.getItem('auth_token');
        if (token && this.isTokenValid(token)) {
            try {
                await this.fetchUserData();
                this.startTokenRefresh();
            } catch (error) {
                console.error('Failed to fetch user data:', error);
                this.logout();
            }
        }
    }

    /**
     * Улучшенная проверка валидности токена
     */
    isTokenValid(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const now = Date.now();
            const exp = payload.exp * 1000;

            // Токен валиден, если до истечения больше 1 минуты
            return exp > (now + 60000);
        } catch (error) {
            console.error('Token validation error:', error);
            return false;
        }
    }

    /**
     * Получение данных пользователя
     */
    async fetchUserData() {
        const response = await fetch(`${this.apiBase}/api/auth/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }

        this.user = await response.json();
        this.updateUserInterface();
        return this.user;
    }

    /**
     * Обновление интерфейса пользователя
     */
    updateUserInterface() {
        if (!this.user) return;

        // Обновляем навбар
        const userNameElement = document.getElementById('user-name');
        const userAvatarElement = document.getElementById('user-avatar');

        if (userNameElement) {
            userNameElement.textContent = this.user.full_name || this.user.username;
        }

        if (userAvatarElement) {
            userAvatarElement.src = AvatarUtils?.getDefaultAvatar() || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K';
        }

        // Показываем навбар пользователя
        const navbarUser = document.getElementById('navbar-user');
        if (navbarUser) {
            navbarUser.style.display = 'block';
        }
    }

    /**
     * Авторизация пользователя
     */
    async login(email, password) {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }

            const data = await response.json();

            // Сохраняем токен
            localStorage.setItem('auth_token', data.access_token);
            localStorage.setItem('token_expires', (Date.now() + 30 * 60 * 1000).toString());

            // Получаем данные пользователя
            await this.fetchUserData();

            // Запускаем обновление токена
            this.startTokenRefresh();

            return data;

        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    /**
     * Регистрация пользователя
     */
    async register(userData) {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Registration failed');
            }

            return await response.json();

        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    /**
     * Выход из системы
     */
    async logout() {
        try {
            // Останавливаем обновление токенов
            this.stopTokenRefresh();

            // Отправляем запрос на выход (если есть токен)
            const token = localStorage.getItem('auth_token');
            if (token) {
                await fetch(`${this.apiBase}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            }

        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Очищаем данные
            localStorage.removeItem('auth_token');
            localStorage.removeItem('token_expires');
            this.user = null;

            // Скрываем навбар пользователя
            const navbarUser = document.getElementById('navbar-user');
            if (navbarUser) {
                navbarUser.style.display = 'none';
            }

            // Перенаправляем на страницу входа
            if (window.location.pathname !== '/login.html') {
                window.location.href = '/login.html';
            }
        }
    }

    /**
     * Обновление access токена
     */
    async refreshAccessToken() {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error('Token refresh failed');
            }

            const data = await response.json();

            // Обновляем токен
            localStorage.setItem('auth_token', data.access_token);
            localStorage.setItem('token_expires', (Date.now() + 30 * 60 * 1000).toString());

            console.log('Token refreshed successfully');
            return data.access_token;

        } catch (error) {
            console.error('Token refresh failed:', error);
            throw error;
        }
    }

    /**
     * Настройка автоматического обновления токена
     */
    setupTokenRefresh() {
        // Проверяем токен каждые 5 минут
        setInterval(() => {
            const token = localStorage.getItem('auth_token');
            if (token && this.isTokenValid(token)) {
                this.refreshAccessToken().catch(error => {
                    console.error('Scheduled token refresh failed:', error);
                    this.logout();
                });
            }
        }, 5 * 60 * 1000);
    }

    /**
     * Запуск обновления токена
     */
    startTokenRefresh() {
        this.stopTokenRefresh();

        const token = localStorage.getItem('auth_token');
        if (!token) return;

        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const exp = payload.exp * 1000;
            const now = Date.now();
            const timeUntilExpiry = exp - now - 60000; // Обновляем за 1 минуту до истечения

            if (timeUntilExpiry > 0) {
                this.refreshTimer = setTimeout(() => {
                    this.refreshAccessToken().catch(error => {
                        console.error('Token refresh failed:', error);
                        this.logout();
                    });
                }, timeUntilExpiry);
            }
        } catch (error) {
            console.error('Token parsing error:', error);
            this.logout();
        }
    }

    /**
     * Остановка обновления токена
     */
    stopTokenRefresh() {
        if (this.refreshTimer) {
            clearTimeout(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    /**
     * Проверка авторизации пользователя
     */
    isAuthenticated() {
        const token = localStorage.getItem('auth_token');
        return token && this.isTokenValid(token);
    }

    /**
     * Получение текущего пользователя
     */
    getCurrentUser() {
        return this.user;
    }

    /**
     * Изменение пароля
     */
    async changePassword(currentPassword, newPassword) {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/change-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Password change failed');
            }

            return await response.json();

        } catch (error) {
            console.error('Password change error:', error);
            throw error;
        }
    }

    /**
     * Верификация email
     */
    async verifyEmail(token) {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/verify-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Email verification failed');
            }

            return await response.json();

        } catch (error) {
            console.error('Email verification error:', error);
            throw error;
        }
    }
}

// Экспорт для глобального доступа
window.AuthService = AuthService;
