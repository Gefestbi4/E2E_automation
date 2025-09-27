// Authentication utilities
class AuthUtils {
    static TOKEN_KEY = 'auth_token';
    static REFRESH_TOKEN_KEY = 'refresh_token';
    static USER_KEY = 'user_data';

    static setTokens(accessToken, refreshToken) {
        localStorage.setItem(this.TOKEN_KEY, accessToken);
        localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
    }

    static getAccessToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    static getRefreshToken() {
        return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    }

    static setUser(userData) {
        localStorage.setItem(this.USER_KEY, JSON.stringify(userData));
    }

    static getUser() {
        const userData = localStorage.getItem(this.USER_KEY);
        return userData ? JSON.parse(userData) : null;
    }

    static clearAuth() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.REFRESH_TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    }

    static isAuthenticated() {
        return !!this.getAccessToken();
    }

    static async refreshAccessToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        try {
            const response = await fetch('/api/auth/refresh', {
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
            this.setTokens(data.access_token, data.refresh_token);
            return data.access_token;
        } catch (error) {
            this.clearAuth();
            throw error;
        }
    }
}

// Auto token refresh
setInterval(async () => {
    if (AuthUtils.isAuthenticated()) {
        try {
            await AuthUtils.refreshAccessToken();
            console.log('Token refreshed successfully');
        } catch (error) {
            console.error('Token refresh failed:', error);
            // Redirect to login if refresh fails
            window.location.href = '/login_new.html';
        }
    }
}, 15 * 60 * 1000); // Refresh every 15 minutes
