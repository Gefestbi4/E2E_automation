// API service
// Исправляем все API endpoints согласно документации
const API_ENDPOINTS = {
    // Auth endpoints
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    REFRESH: '/api/auth/refresh',
    LOGOUT: '/api/auth/logout',
    VERIFY_EMAIL: '/api/auth/verify-email',
    RESET_PASSWORD: '/api/auth/reset-password',
    CHANGE_PASSWORD: '/api/auth/change-password',

    // User endpoints
    PROFILE: '/api/users/profile',
    UPDATE_PROFILE: '/api/users/profile',
    DELETE_ACCOUNT: '/api/users/account',

    // Analytics endpoints
    ANALYTICS_DASHBOARD: '/api/analytics/dashboard',
    ANALYTICS_REPORTS: '/api/analytics/reports',
    ANALYTICS_METRICS: '/api/analytics/metrics',

    // E-commerce endpoints
    PRODUCTS: '/api/ecommerce/products',
    ORDERS: '/api/ecommerce/orders',
    CART: '/api/ecommerce/cart',
    CHECKOUT: '/api/ecommerce/checkout',

    // Social endpoints
    POSTS: '/api/social/posts',
    COMMENTS: '/api/social/comments',
    LIKES: '/api/social/likes',
    FOLLOW: '/api/social/follow',

    // Tasks endpoints
    TASKS: '/api/tasks',
    TASK_CREATE: '/api/tasks',
    TASK_UPDATE: '/api/tasks',
    TASK_DELETE: '/api/tasks',

    // Content endpoints
    CONTENT: '/api/content',
    MEDIA: '/api/media',

    // Monitoring endpoints
    HEALTH: '/api/monitoring/health',
    METRICS: '/api/monitoring/metrics',
    LOGS: '/api/monitoring/logs'
};

class ApiService {
    constructor() {
        // Ждем готовности DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.baseURL = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
            });
        } else {
            this.baseURL = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
        }

        // Retry configuration
        this.retryAttempts = 3;
        this.retryDelay = 1000; // Base delay in ms
    }

    async request(endpoint, options = {}) {
        // Убеждаемся, что baseURL установлен
        if (!this.baseURL) {
            this.baseURL = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
        }

        const url = `${this.baseURL}${endpoint}`;
        const token = localStorage.getItem('auth_token');

        console.log('API Request:', {
            url,
            endpoint,
            token: token ? `${token.substring(0, 20)}...` : 'null',
            method: options?.method || 'GET'
        });

        // Если нет токена и это не публичный эндпоинт, не отправляем запрос
        if (!token && !this.isPublicEndpoint(endpoint)) {
            console.warn('No auth token available for protected endpoint:', endpoint);
            throw new Error('Authentication required');
        }

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        };

        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        // Логируем запрос
        if (window.Logger) {
            window.Logger.debug('API_REQUEST', `Making request to ${endpoint}`, {
                endpoint: endpoint,
                method: options.method || 'GET',
                url: url,
                hasAuth: !!token
            });
        }

        // Retry logic with exponential backoff
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                console.log('Sending request to:', url);
                const response = await fetch(url, config);
                console.log('Response received:', {
                    status: response.status,
                    ok: response.ok,
                    url: response.url
                });

                // Автоматическое обновление токена при 401 ошибке
                if (response.status === 401 && this.isAuthenticated()) {
                    try {
                        if (window.Logger) {
                            window.Logger.info('API_AUTH', 'Token expired, attempting refresh');
                        }
                        console.log('🔄 Attempting token refresh...');
                        await this.refreshAccessToken();

                        // Обновляем токен в заголовках и повторяем запрос
                        const newToken = localStorage.getItem('auth_token');
                        config.headers['Authorization'] = `Bearer ${newToken}`;

                        if (window.Logger) {
                            window.Logger.info('API_AUTH', 'Token refreshed, retrying request');
                        }
                        console.log('🔄 Retrying request with new token...');
                        const retryResponse = await fetch(url, config);

                        if (!retryResponse.ok) {
                            const errorData = await retryResponse.json().catch(() => ({}));
                            const errorMessage = errorData.detail || errorData.message || `HTTP ${retryResponse.status}`;

                            // Enhanced error handling
                            if (window.ErrorHandler) {
                                window.ErrorHandler.logError(new Error(errorMessage), {
                                    endpoint: endpoint,
                                    status: retryResponse.status,
                                    url: url,
                                    type: 'API_REQUEST_FAILED'
                                });
                            }

                            throw new Error(errorMessage);
                        }

                        const contentType = retryResponse.headers.get('content-type');
                        if (contentType && contentType.includes('application/json')) {
                            return await retryResponse.json();
                        }
                        return await retryResponse.text();
                    } catch (refreshError) {
                        if (window.Logger) {
                            window.Logger.error('API_AUTH', 'Token refresh failed', { error: refreshError.message });
                        }
                        console.error('🔄 Token refresh failed:', refreshError);

                        // Enhanced error handling
                        if (window.ErrorHandler) {
                            window.ErrorHandler.logError(refreshError, {
                                endpoint: endpoint,
                                url: url,
                                type: 'TOKEN_REFRESH_FAILED'
                            });
                        }

                        this.clearAuth();
                        window.location.href = '/login.html';
                        return;
                    }
                }

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    const errorMessage = errorData.detail || errorData.message || `HTTP ${response.status}`;

                    // Enhanced error handling
                    if (window.ErrorHandler) {
                        window.ErrorHandler.logError(new Error(errorMessage), {
                            endpoint: endpoint,
                            status: response.status,
                            statusText: response.statusText,
                            url: url,
                            errorData: errorData,
                            type: 'API_REQUEST_FAILED'
                        });
                    }

                    // Логируем ошибку
                    if (window.Logger) {
                        window.Logger.error('API_ERROR', `Request failed: ${errorMessage}`, {
                            status: response.status,
                            statusText: response.statusText,
                            url: url,
                            endpoint: endpoint,
                            errorData: errorData
                        });
                    }

                    // Логируем детали ошибки для отладки
                    console.error('API Error:', {
                        status: response.status,
                        statusText: response.statusText,
                        url: url,
                        errorData: errorData
                    });

                    throw new Error(errorMessage);
                }

                // Логируем успешный ответ
                if (window.Logger) {
                    window.Logger.debug('API_SUCCESS', `Request successful to ${endpoint}`, {
                        status: response.status,
                        url: url,
                        endpoint: endpoint
                    });
                }

                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return await response.json();
                }

                return await response.text();
            } catch (error) {
                // Enhanced error handling for network errors
                if (window.ErrorHandler) {
                    window.ErrorHandler.logError(error, {
                        endpoint: endpoint,
                        url: url,
                        attempt: attempt,
                        type: 'NETWORK_ERROR'
                    });
                }

                // If this is the last attempt, throw the error
                if (attempt === this.retryAttempts) {
                    throw error;
                }

                // Wait before retrying with exponential backoff
                const delay = this.retryDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    async upload(endpoint, formData) {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                ...(token && { 'Authorization': `Bearer ${token}` })
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    }

    // Методы аутентификации
    isAuthenticated() {
        return !!localStorage.getItem('auth_token');
    }

    // Проверка публичных эндпоинтов
    isPublicEndpoint(endpoint) {
        const publicEndpoints = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/auth/verify-email',
            '/api/auth/reset-password',
            '/api/health',
            '/api/metrics'
        ];
        return publicEndpoints.some(publicEndpoint => endpoint.startsWith(publicEndpoint));
    }

    async refreshAccessToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        try {
            const response = await fetch(`${this.baseURL}/api/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: refreshToken }),
            });

            if (!response.ok) {
                throw new Error('Token refresh failed');
            }

            const data = await response.json();
            localStorage.setItem('auth_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            return data.access_token;
        } catch (error) {
            this.clearAuth();
            throw error;
        }
    }

    clearAuth() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
    }

    // Методы для работы с endpoints
    getEndpoint(name) {
        return API_ENDPOINTS[name];
    }

    // Auth methods
    async login(credentials) {
        return this.post(API_ENDPOINTS.LOGIN, credentials);
    }

    async register(userData) {
        return this.post(API_ENDPOINTS.REGISTER, userData);
    }

    async logout() {
        return this.post(API_ENDPOINTS.LOGOUT);
    }

    async verifyEmail(token) {
        return this.post(API_ENDPOINTS.VERIFY_EMAIL, { token });
    }

    async resetPassword(email) {
        return this.post(API_ENDPOINTS.RESET_PASSWORD, { email });
    }

    async changePassword(oldPassword, newPassword) {
        return this.post(API_ENDPOINTS.CHANGE_PASSWORD, { oldPassword, newPassword });
    }

    // User methods
    async getProfile() {
        return this.get(API_ENDPOINTS.PROFILE);
    }

    async updateProfile(userData) {
        return this.put(API_ENDPOINTS.UPDATE_PROFILE, userData);
    }

    async deleteAccount() {
        return this.delete(API_ENDPOINTS.DELETE_ACCOUNT);
    }

    // Analytics methods
    async getAnalyticsDashboard() {
        return this.get(API_ENDPOINTS.ANALYTICS_DASHBOARD);
    }

    async getAnalyticsReports(filters = {}) {
        return this.get(API_ENDPOINTS.ANALYTICS_REPORTS + '?' + new URLSearchParams(filters));
    }

    async getAnalyticsMetrics() {
        return this.get(API_ENDPOINTS.ANALYTICS_METRICS);
    }

    // E-commerce methods
    async getProducts(filters = {}) {
        return this.get(API_ENDPOINTS.PRODUCTS + '?' + new URLSearchParams(filters));
    }

    async getOrders() {
        return this.get(API_ENDPOINTS.ORDERS);
    }

    async getCart() {
        return this.get(API_ENDPOINTS.CART);
    }

    async addToCart(productId, quantity = 1) {
        return this.post(API_ENDPOINTS.CART, { productId, quantity });
    }

    async updateCartItem(itemId, quantity) {
        return this.put(`${API_ENDPOINTS.CART}/${itemId}`, { quantity });
    }

    async removeFromCart(itemId) {
        return this.delete(`${API_ENDPOINTS.CART}/${itemId}`);
    }

    async checkout(orderData) {
        return this.post(API_ENDPOINTS.CHECKOUT, orderData);
    }

    // Social methods
    async getPosts(filters = {}) {
        return this.get(API_ENDPOINTS.POSTS + '?' + new URLSearchParams(filters));
    }

    async createPost(postData) {
        return this.post(API_ENDPOINTS.POSTS, postData);
    }

    async likePost(postId) {
        return this.post(`${API_ENDPOINTS.LIKES}`, { postId });
    }

    async commentOnPost(postId, comment) {
        return this.post(API_ENDPOINTS.COMMENTS, { postId, comment });
    }

    async followUser(userId) {
        return this.post(API_ENDPOINTS.FOLLOW, { userId });
    }

    // Tasks methods
    async getTasks() {
        return this.get(API_ENDPOINTS.TASKS);
    }

    async createTask(taskData) {
        return this.post(API_ENDPOINTS.TASK_CREATE, taskData);
    }

    async updateTask(taskId, taskData) {
        return this.put(`${API_ENDPOINTS.TASK_UPDATE}/${taskId}`, taskData);
    }

    async deleteTask(taskId) {
        return this.delete(`${API_ENDPOINTS.TASK_DELETE}/${taskId}`);
    }

    // Content methods
    async getContent() {
        return this.get(API_ENDPOINTS.CONTENT);
    }

    async uploadMedia(file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.upload(API_ENDPOINTS.MEDIA, formData);
    }

    // Monitoring methods
    async getHealth() {
        return this.get(API_ENDPOINTS.HEALTH);
    }

    async getMetrics() {
        return this.get(API_ENDPOINTS.METRICS);
    }

    async getLogs(filters = {}) {
        return this.get(API_ENDPOINTS.LOGS + '?' + new URLSearchParams(filters));
    }
}

// Export for global access
console.log('🔧 Creating ApiService instance...');
try {
    window.ApiService = new ApiService();
    console.log('🔧 ApiService initialized:', !!window.ApiService);
    console.log('🔧 ApiService type:', typeof window.ApiService);
    console.log('🔧 ApiService methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(window.ApiService)));
} catch (error) {
    console.error('🔧 Error creating ApiService:', error);
}
