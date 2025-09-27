// Social network service
class SocialService {
    constructor() {
        this.api = new ApiService();
    }

    async getPosts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/social/posts?${queryString}`);
    }

    async createPost(postData) {
        return this.api.post('/api/social/posts', postData);
    }

    async getPost(id) {
        return this.api.get(`/api/social/posts/${id}`);
    }

    async updatePost(id, postData) {
        return this.api.put(`/api/social/posts/${id}`, postData);
    }

    async deletePost(id) {
        return this.api.delete(`/api/social/posts/${id}`);
    }

    async likePost(postId) {
        return this.api.post(`/api/social/posts/${postId}/like`);
    }

    async unlikePost(postId) {
        return this.api.delete(`/api/social/posts/${postId}/like`);
    }

    async getComments(postId) {
        return this.api.get(`/api/social/posts/${postId}/comments`);
    }

    async addComment(postId, commentData) {
        return this.api.post(`/api/social/posts/${postId}/comments`, commentData);
    }

    async updateComment(commentId, commentData) {
        return this.api.put(`/api/social/comments/${commentId}`, commentData);
    }

    async deleteComment(commentId) {
        return this.api.delete(`/api/social/comments/${commentId}`);
    }

    async likeComment(commentId) {
        return this.api.post(`/api/social/comments/${commentId}/like`);
    }

    async unlikeComment(commentId) {
        return this.api.delete(`/api/social/comments/${commentId}/like`);
    }

    async followUser(userId) {
        return this.api.post(`/api/social/users/${userId}/follow`);
    }

    async unfollowUser(userId) {
        return this.api.delete(`/api/social/users/${userId}/follow`);
    }

    async getFollowers(userId) {
        return this.api.get(`/api/social/users/${userId}/followers`);
    }

    async getFollowing(userId) {
        return this.api.get(`/api/social/users/${userId}/following`);
    }

    async getMessages(chatId) {
        return this.api.get(`/api/social/chats/${chatId}/messages`);
    }

    async sendMessage(chatId, messageData) {
        return this.api.post(`/api/social/chats/${chatId}/messages`, messageData);
    }

    async getChats() {
        return this.api.get('/api/social/chats');
    }

    async createChat(userId) {
        return this.api.post('/api/social/chats', { user_id: userId });
    }
}

// Export for global access
window.SocialService = SocialService;
