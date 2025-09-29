// API service
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
    }

    async request(endpoint, options = {}) {
        // Убеждаемся, что baseURL установлен
        if (!this.baseURL) {
            this.baseURL = document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000';
        }

        const url = `${this.baseURL}${endpoint}`;
        const token = localStorage.getItem('auth_token');

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

        try {
            const response = await fetch(url, config);

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
                    this.clearAuth();
                    window.location.href = '/login.html';
                    return;
                }
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.detail || errorData.message || `HTTP ${response.status}`;

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
            // Логируем ошибку
            if (window.Logger) {
                window.Logger.error('API_EXCEPTION', `Request exception: ${error.message}`, {
                    endpoint: endpoint,
                    url: url,
                    error: error.message,
                    stack: error.stack
                });
            }

            console.error('API request failed:', error);

            // Используем централизованную обработку ошибок
            if (window.ErrorHandler) {
                const errorInfo = window.ErrorHandler.handle(error, `API request to ${endpoint}`);
                window.ErrorHandler.showError(errorInfo);
            }

            throw error;
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
