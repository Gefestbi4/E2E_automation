// Content management service
class ContentService {
    constructor() {
        this.api = window.ApiService;
    }

    async getArticles(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/content/articles?${queryString}`);
    }

    async createArticle(articleData) {
        return this.api.post('/api/content/articles', articleData);
    }

    async getArticle(id) {
        return this.api.get(`/api/content/articles/${id}`);
    }

    async updateArticle(id, articleData) {
        return this.api.put(`/api/content/articles/${id}`, articleData);
    }

    async deleteArticle(id) {
        return this.api.delete(`/api/content/articles/${id}`);
    }

    async publishArticle(id) {
        return this.api.post(`/api/content/articles/${id}/publish`);
    }

    async unpublishArticle(id) {
        return this.api.post(`/api/content/articles/${id}/unpublish`);
    }

    async getCategories() {
        return this.api.get('/api/content/categories');
    }

    async createCategory(categoryData) {
        return this.api.post('/api/content/categories', categoryData);
    }

    async updateCategory(id, categoryData) {
        return this.api.put(`/api/content/categories/${id}`, categoryData);
    }

    async deleteCategory(id) {
        return this.api.delete(`/api/content/categories/${id}`);
    }

    async getTags() {
        return this.api.get('/api/content/tags');
    }

    async createTag(tagData) {
        return this.api.post('/api/content/tags', tagData);
    }

    async getArticleComments(articleId) {
        return this.api.get(`/api/content/articles/${articleId}/comments`);
    }

    async addArticleComment(articleId, commentData) {
        return this.api.post(`/api/content/articles/${articleId}/comments`, commentData);
    }

    async updateArticleComment(commentId, commentData) {
        return this.api.put(`/api/content/comments/${commentId}`, commentData);
    }

    async deleteArticleComment(commentId) {
        return this.api.delete(`/api/content/comments/${commentId}`);
    }

    async likeArticle(articleId) {
        return this.api.post(`/api/content/articles/${articleId}/like`);
    }

    async unlikeArticle(articleId) {
        return this.api.delete(`/api/content/articles/${articleId}/like`);
    }

    async likeComment(commentId) {
        return this.api.post(`/api/content/comments/${commentId}/like`);
    }

    async unlikeComment(commentId) {
        return this.api.delete(`/api/content/comments/${commentId}/like`);
    }

    async uploadMedia(file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.api.upload('/api/content/media', formData);
    }

    async deleteMedia(mediaId) {
        return this.api.delete(`/api/content/media/${mediaId}`);
    }

    async getMediaList(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/content/media?${queryString}`);
    }

    async moderateContent(contentId, action, reason = '') {
        return this.api.post(`/api/content/${contentId}/moderate`, {
            action: action,
            reason: reason
        });
    }

    async getModerationQueue() {
        return this.api.get('/api/content/moderation/queue');
    }

    async trackView(contentId, contentType) {
        return this.api.post('/api/content/views', {
            content_id: contentId,
            content_type: contentType
        });
    }
}

// Создаем экземпляр и экспортируем для глобального доступа
window.ContentService = new ContentService();
