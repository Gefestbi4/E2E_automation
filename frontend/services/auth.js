/**
 * Сервис авторизации для Automation Learning Platform
 * Управляет аутентификацией пользователей, токенами и защищенными запросами
 */

class AuthService {
    constructor() {
        this.apiBase = (document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000').replace(/\/?$/, '');
        this.refreshTimer = null;
        this.init();
    }

    /**
     * Инициализация сервиса
     */
    init() {
        this.setupTokenRefresh();
        this.checkAuthStatus();
    }

    /**
     * Проверка статуса авторизации при загрузке
     */
    checkAuthStatus() {
        const token = localStorage.getItem('auth_token');
        if (token && this.isTokenValid(token)) {
            this.startTokenRefresh();
        }
    }

    /**
     * Проверка валидности токена
     */
    isTokenValid(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.exp * 1000 > Date.now();
        } catch {
            return false;
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
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok && data.access_token) {
                // Сохраняем токены
                localStorage.setItem('auth_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                localStorage.setItem('token_expires', Date.now() + (data.expires_in * 1000));

                // Запускаем автоматическое обновление токенов
                this.startTokenRefresh();

                return { success: true, user: data };
            } else {
                return { success: false, error: data.detail || 'Ошибка авторизации' };
            }
        } catch (error) {
            console.error('Ошибка авторизации:', error);
            return { success: false, error: 'Сетевая ошибка' };
        }
    }

    /**
     * Регистрация нового пользователя
     */
    async register(userData) {
        try {
            const response = await fetch(`${this.apiBase}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, user: data };
            } else {
                return { success: false, error: data.detail || 'Ошибка регистрации' };
            }
        } catch (error) {
            console.error('Ошибка регистрации:', error);
            return { success: false, error: 'Сетевая ошибка' };
        }
    }

    /**
     * Обновление токена доступа
     */
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            this.logout();
            return false;
        }

        try {
            const response = await fetch(`${this.apiBase}/api/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            const data = await response.json();

            if (response.ok && data.access_token) {
                localStorage.setItem('auth_token', data.access_token);
                localStorage.setItem('token_expires', Date.now() + (data.expires_in * 1000));
                return true;
            } else {
                this.logout();
                return false;
            }
        } catch (error) {
            console.error('Ошибка обновления токена:', error);
            this.logout();
            return false;
        }
    }

    /**
     * Выход из системы
     */
    async logout() {
        try {
            const token = localStorage.getItem('auth_token');
            if (token) {
                await fetch(`${this.apiBase}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
            }
        } catch (error) {
            console.error('Ошибка выхода:', error);
        } finally {
            // Очищаем локальное хранилище
            localStorage.removeItem('auth_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('token_expires');
            localStorage.removeItem('user_data');

            // Останавливаем обновление токенов
            this.stopTokenRefresh();

            // Перенаправляем на страницу входа
            if (window.location.pathname !== '/login_new.html') {
                window.location.href = '/login_new.html';
            }
        }
    }

    /**
     * Получение информации о текущем пользователе
     */
    async getCurrentUser() {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            console.log('No auth token found');
            return null;
        }

        try {
            console.log('Fetching user data from API...');
            const response = await fetch(`${this.apiBase}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('API response status:', response.status);

            if (response.ok) {
                const user = await response.json();
                console.log('User data received:', user);
                localStorage.setItem('user_data', JSON.stringify(user));
                return user;
            } else {
                console.log('API returned error, logging out');
                this.logout();
                return null;
            }
        } catch (error) {
            console.error('Ошибка получения данных пользователя:', error);
            this.logout();
            return null;
        }
    }

    /**
     * Проверка авторизации
     */
    isAuthenticated() {
        const token = localStorage.getItem('auth_token');
        const expires = localStorage.getItem('token_expires');

        console.log('Checking authentication...');
        console.log('Token exists:', !!token);
        console.log('Expires:', expires);
        console.log('Current time:', Date.now());

        if (!token || !expires) {
            console.log('No token or expires found');
            return false;
        }

        // Проверяем, не истек ли токен
        const isTokenValid = Date.now() < parseInt(expires);
        console.log('Token is valid:', isTokenValid);

        if (!isTokenValid) {
            console.log('Token expired, clearing auth');
            this.logout();
        }

        return isTokenValid;
    }

    /**
     * Получение токена авторизации
     */
    getAuthToken() {
        return localStorage.getItem('auth_token');
    }

    /**
     * Создание заголовков для авторизованных запросов
     */
    getAuthHeaders() {
        const token = this.getAuthToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    /**
     * Настройка автоматического обновления токенов
     */
    setupTokenRefresh() {
        // Проверяем токен каждые 5 минут
        this.refreshTimer = setInterval(async () => {
            const expires = localStorage.getItem('token_expires');
            if (expires && Date.now() > (parseInt(expires) - 300000)) { // За 5 минут до истечения
                await this.refreshToken();
            }
        }, 300000); // 5 минут
    }

    /**
     * Запуск автоматического обновления токенов
     */
    startTokenRefresh() {
        this.stopTokenRefresh();
        this.setupTokenRefresh();
    }

    /**
     * Остановка автоматического обновления токенов
     */
    stopTokenRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    /**
     * Обновление профиля пользователя
     */
    async updateProfile(userData) {
        const token = this.getAuthToken();
        if (!token) {
            return { success: false, error: 'Не авторизован' };
        }

        try {
            const response = await fetch(`${this.apiBase}/api/auth/me`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('user_data', JSON.stringify(data));
                return { success: true, user: data };
            } else {
                return { success: false, error: data.detail || 'Ошибка обновления профиля' };
            }
        } catch (error) {
            console.error('Ошибка обновления профиля:', error);
            return { success: false, error: 'Сетевая ошибка' };
        }
    }

    /**
     * Смена пароля
     */
    async changePassword(currentPassword, newPassword, confirmPassword) {
        const token = this.getAuthToken();
        if (!token) {
            return { success: false, error: 'Не авторизован' };
        }

        try {
            const response = await fetch(`${this.apiBase}/api/auth/change-password`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                })
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, message: data.message };
            } else {
                return { success: false, error: data.detail || 'Ошибка смены пароля' };
            }
        } catch (error) {
            console.error('Ошибка смены пароля:', error);
            return { success: false, error: 'Сетевая ошибка' };
        }
    }

    /**
     * Получение данных пользователя из localStorage
     */
    getStoredUserData() {
        try {
            const userData = localStorage.getItem('user_data');
            return userData ? JSON.parse(userData) : null;
        } catch {
            return null;
        }
    }
}

// Экспортируем класс и создаем экземпляр
window.AuthServiceClass = AuthService;

// Создаем экземпляр AuthService
const authInstance = new AuthService();

// Привязываем все методы экземпляра к глобальному объекту window.AuthService
// Это гарантирует, что 'this' внутри методов будет указывать на authInstance
window.AuthService = {};
for (const key of Object.getOwnPropertyNames(AuthService.prototype)) {
    if (key !== 'constructor' && typeof authInstance[key] === 'function') {
        window.AuthService[key] = authInstance[key].bind(authInstance);
    }
}

// Fallback для ошибок во время создания AuthService (можно убрать после отладки)
if (typeof window.AuthService.isAuthenticated !== 'function') {
    console.error('Error creating AuthService: isAuthenticated is not a function. Creating a fallback.');
    window.AuthService = {
        isAuthenticated: () => { console.error('AuthService fallback: isAuthenticated called'); return false; },
        logout: () => console.error('AuthService fallback: logout called'),
        getCurrentUser: async () => { console.error('AuthService fallback: getCurrentUser called'); return null; },
        login: async () => { console.error('AuthService fallback: login called'); return null; },
        register: async () => { console.error('AuthService fallback: register called'); return null; },
        getAuthToken: () => { console.error('AuthService fallback: getAuthToken called'); return null; },
        getAuthHeaders: () => { console.error('AuthService fallback: getAuthHeaders called'); return {}; },
        updateProfile: async () => { console.error('AuthService fallback: updateProfile called'); return null; },
        changePassword: async () => { console.error('AuthService fallback: changePassword called'); return null; },
        getStoredUserData: () => { console.error('AuthService fallback: getStoredUserData called'); return null; }
    };
}
