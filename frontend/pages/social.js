// Social page module
class SocialPage {
    constructor() {
        this.posts = [];
        this.currentUser = null;
        this.init();
    }

    async init() {
        await this.loadUser();
        await this.loadPosts();
        this.setupEventListeners();
    }

    async loadUser() {
        try {
            const user = await window.ApiService.getProfile();
            this.currentUser = user;
        } catch (error) {
            console.error('Failed to load user:', error);
        }
    }

    async loadPosts() {
        try {
            this.showLoading();
            const posts = await window.ApiService.getPosts();
            this.posts = posts;
            this.renderPosts();
        } catch (error) {
            console.error('Failed to load posts:', error);
            this.showError('Не удалось загрузить посты');
        } finally {
            this.hideLoading();
        }
    }

    renderPosts() {
        const container = document.getElementById('social-container');
        if (!container) return;

        container.innerHTML = `
            <div class="social-header">
                <h1>Социальная лента</h1>
                <button class="btn btn-primary" onclick="socialPage.showCreatePostModal()">
                    Создать пост
                </button>
            </div>

            <div class="posts-feed">
                ${this.posts.map(post => this.renderPost(post)).join('')}
            </div>
        `;

        this.setupPostEventListeners();
    }

    renderPost(post) {
        const isLiked = post.likes?.some(like => like.userId === this.currentUser?.id);
        const isFollowing = post.author?.followers?.some(follower => follower.id === this.currentUser?.id);

        return `
            <div class="post-card" data-post-id="${post.id}">
                <div class="post-header">
                    <div class="post-author">
                        <img src="${post.author?.avatar || '/default-avatar.png'}" 
                             alt="${post.author?.name}" class="author-avatar">
                        <div class="author-info">
                            <h4>${post.author?.name || 'Неизвестный пользователь'}</h4>
                            <span class="post-time">${this.formatTime(post.createdAt)}</span>
                        </div>
                    </div>
                    <div class="post-actions">
                        ${!isFollowing ? `
                            <button class="btn btn-sm btn-outline" onclick="socialPage.followUser('${post.author?.id}')">
                                Подписаться
                            </button>
                        ` : ''}
                        <button class="btn btn-sm btn-outline" onclick="socialPage.showPostOptions('${post.id}')">
                            ⋯
                        </button>
                    </div>
                </div>

                <div class="post-content">
                    <p>${post.content}</p>
                    ${post.image ? `<img src="${post.image}" alt="Post image" class="post-image">` : ''}
                </div>

                <div class="post-stats">
                    <div class="post-engagement">
                        <button class="engagement-btn ${isLiked ? 'liked' : ''}" 
                                onclick="socialPage.toggleLike('${post.id}')">
                            <span class="icon">❤️</span>
                            <span class="count">${post.likes?.length || 0}</span>
                        </button>
                        <button class="engagement-btn" onclick="socialPage.showComments('${post.id}')">
                            <span class="icon">💬</span>
                            <span class="count">${post.comments?.length || 0}</span>
                        </button>
                        <button class="engagement-btn" onclick="socialPage.sharePost('${post.id}')">
                            <span class="icon">📤</span>
                            <span class="count">Поделиться</span>
                        </button>
                    </div>
                </div>

                <div class="post-comments" id="comments-${post.id}" style="display: none;">
                    <div class="comments-list">
                        ${post.comments?.map(comment => this.renderComment(comment)).join('') || ''}
                    </div>
                    <div class="add-comment">
                        <input type="text" placeholder="Добавить комментарий..." 
                               class="comment-input" data-post-id="${post.id}">
                        <button class="btn btn-sm btn-primary" 
                                onclick="socialPage.addComment('${post.id}')">
                            Отправить
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    renderComment(comment) {
        return `
            <div class="comment">
                <img src="${comment.author?.avatar || '/default-avatar.png'}" 
                     alt="${comment.author?.name}" class="comment-avatar">
                <div class="comment-content">
                    <div class="comment-header">
                        <span class="comment-author">${comment.author?.name}</span>
                        <span class="comment-time">${this.formatTime(comment.createdAt)}</span>
                    </div>
                    <p>${comment.content}</p>
                </div>
            </div>
        `;
    }

    setupPostEventListeners() {
        // Comment input handlers
        document.querySelectorAll('.comment-input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const postId = e.target.dataset.postId;
                    this.addComment(postId);
                }
            });
        });
    }

    setupEventListeners() {
        // Global event listeners
        document.addEventListener('click', (e) => {
            if (e.target.closest('.post-card')) {
                // Handle post interactions
            } else {
                // Close any open modals
                this.hideCreatePostModal();
            }
        });
    }

    async toggleLike(postId) {
        try {
            await window.ApiService.likePost(postId);
            await this.loadPosts(); // Refresh posts
        } catch (error) {
            console.error('Failed to toggle like:', error);
            this.showError('Не удалось поставить лайк');
        }
    }

    async followUser(userId) {
        try {
            await window.ApiService.followUser(userId);
            await this.loadPosts(); // Refresh posts
        } catch (error) {
            console.error('Failed to follow user:', error);
            this.showError('Не удалось подписаться на пользователя');
        }
    }

    async addComment(postId) {
        const input = document.querySelector(`input[data-post-id="${postId}"]`);
        const content = input.value.trim();

        if (!content) return;

        try {
            await window.ApiService.commentOnPost(postId, content);
            input.value = '';
            await this.loadPosts(); // Refresh posts
        } catch (error) {
            console.error('Failed to add comment:', error);
            this.showError('Не удалось добавить комментарий');
        }
    }

    showComments(postId) {
        const commentsDiv = document.getElementById(`comments-${postId}`);
        if (commentsDiv) {
            commentsDiv.style.display = commentsDiv.style.display === 'none' ? 'block' : 'none';
        }
    }

    showCreatePostModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Создать пост</h3>
                    <button class="modal-close" onclick="socialPage.hideCreatePostModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="createPostForm">
                        <div class="form-group">
                            <textarea id="postContent" placeholder="Что у вас нового?" 
                                      class="form-control" rows="4" required></textarea>
                        </div>
                        <div class="form-group">
                            <input type="file" id="postImage" accept="image/*" class="form-control">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="socialPage.hideCreatePostModal()">
                        Отмена
                    </button>
                    <button class="btn btn-primary" onclick="socialPage.createPost()">
                        Опубликовать
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    hideCreatePostModal() {
        const modal = document.querySelector('.modal');
        if (modal) {
            modal.remove();
        }
    }

    async createPost() {
        const content = document.getElementById('postContent').value.trim();
        const imageInput = document.getElementById('postImage');

        if (!content) return;

        try {
            const postData = { content };

            if (imageInput.files[0]) {
                const imageUrl = await window.ApiService.uploadMedia(imageInput.files[0]);
                postData.image = imageUrl;
            }

            await window.ApiService.createPost(postData);
            this.hideCreatePostModal();
            await this.loadPosts(); // Refresh posts
        } catch (error) {
            console.error('Failed to create post:', error);
            this.showError('Не удалось создать пост');
        }
    }

    sharePost(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
            const shareUrl = `${window.location.origin}/post/${postId}`;
            navigator.clipboard.writeText(shareUrl).then(() => {
                this.showSuccess('Ссылка скопирована в буфер обмена');
            }).catch(() => {
                this.showError('Не удалось скопировать ссылку');
            });
        }
    }

    showPostOptions(postId) {
        // Show post options modal
        console.log('Show post options for:', postId);
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) return 'только что';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`;
        return date.toLocaleDateString();
    }

    showLoading() {
        const container = document.getElementById('social-container');
        if (container) {
            container.innerHTML = '<div class="loading">Загрузка постов...</div>';
        }
    }

    hideLoading() {
        // Loading will be replaced by actual content
    }

    showError(message) {
        // Show error message
        console.error(message);
        // You can implement a toast notification system here
    }

    showSuccess(message) {
        // Show success message
        console.log(message);
        // You can implement a toast notification system here
    }
}

// Initialize social page
let socialPage;
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('social-container')) {
        socialPage = new SocialPage();
    }
});

// Export for global access
window.SocialPage = SocialPage;