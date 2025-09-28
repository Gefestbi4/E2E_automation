// Analytics service
class AnalyticsService {
    constructor() {
        this.api = window.ApiService;
    }

    async getDashboardData() {
        return this.api.get('/api/analytics/dashboard');
    }

    async getMetrics(metricType, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/analytics/metrics/${metricType}?${queryString}`);
    }

    async getMetricData(metricId, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/analytics/metrics/${metricId}/data?${queryString}`);
    }

    async createMetric(metricData) {
        return this.api.post('/api/analytics/metrics', metricData);
    }

    async updateMetric(id, metricData) {
        return this.api.put(`/api/analytics/metrics/${id}`, metricData);
    }

    async deleteMetric(id) {
        return this.api.delete(`/api/analytics/metrics/${id}`);
    }

    async getReports(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/analytics/reports?${queryString}`);
    }

    async createReport(reportData) {
        return this.api.post('/api/analytics/reports', reportData);
    }

    async getReport(id) {
        return this.api.get(`/api/analytics/reports/${id}`);
    }

    async updateReport(id, reportData) {
        return this.api.put(`/api/analytics/reports/${id}`, reportData);
    }

    async deleteReport(id) {
        return this.api.delete(`/api/analytics/reports/${id}`);
    }

    async exportReport(id, format = 'pdf') {
        return this.api.get(`/api/analytics/reports/${id}/export?format=${format}`);
    }

    async getDashboards() {
        return this.api.get('/api/analytics/dashboards');
    }

    async createDashboard(dashboardData) {
        return this.api.post('/api/analytics/dashboards', dashboardData);
    }

    async getDashboard(id) {
        return this.api.get(`/api/analytics/dashboards/${id}`);
    }

    async updateDashboard(id, dashboardData) {
        return this.api.put(`/api/analytics/dashboards/${id}`, dashboardData);
    }

    async deleteDashboard(id) {
        return this.api.delete(`/api/analytics/dashboards/${id}`);
    }

    async getDashboardWidgets(dashboardId) {
        return this.api.get(`/api/analytics/dashboards/${dashboardId}/widgets`);
    }

    async addDashboardWidget(dashboardId, widgetData) {
        return this.api.post(`/api/analytics/dashboards/${dashboardId}/widgets`, widgetData);
    }

    async updateDashboardWidget(widgetId, widgetData) {
        return this.api.put(`/api/analytics/widgets/${widgetId}`, widgetData);
    }

    async deleteDashboardWidget(widgetId) {
        return this.api.delete(`/api/analytics/widgets/${widgetId}`);
    }

    async getUserActivity(userId, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/analytics/users/${userId}/activity?${queryString}`);
    }

    async getSystemEvents(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/analytics/system/events?${queryString}`);
    }

    async getAlerts() {
        return this.api.get('/api/analytics/alerts');
    }

    async createAlert(alertData) {
        return this.api.post('/api/analytics/alerts', alertData);
    }

    async updateAlert(id, alertData) {
        return this.api.put(`/api/analytics/alerts/${id}`, alertData);
    }

    async deleteAlert(id) {
        return this.api.delete(`/api/analytics/alerts/${id}`);
    }

    async trackEvent(eventType, eventData) {
        return this.api.post('/api/analytics/events', {
            type: eventType,
            data: eventData,
            timestamp: new Date().toISOString()
        });
    }
}

// Создаем экземпляр и экспортируем для глобального доступа
window.AnalyticsService = new AnalyticsService();
