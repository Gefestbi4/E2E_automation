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

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }

            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
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
