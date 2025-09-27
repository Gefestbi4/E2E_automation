// Social network page module
class SocialModule {
    constructor() {
        this.socialService = new SocialService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Social module...');

        try {
            await this.loadPosts();
            this.bindEvents();
            this.isInitialized = true;
            console.log('Social module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Social module:', error);
            throw error;
        }
    }

    async loadPosts() {
        try {
            // Mock data for demo
            const posts = [
                {
                    id: 1,
                    content: 'Добро пожаловать в социальную сеть! Это демо-пост для тестирования функциональности.',
                    author: {
                        name: 'Demo User',
                        avatar: typeof AvatarUtils !== 'undefined' ? AvatarUtils.createInitialsAvatar('Demo User') : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K'
                    },
                    created_at: new Date().toISOString(),
                    likes_count: 5,
                    comments_count: 2
                },
                {
                    id: 2,
                    content: 'Второй демо-пост для демонстрации ленты новостей.',
                    author: {
                        name: 'Test User',
                        avatar: typeof AvatarUtils !== 'undefined' ? AvatarUtils.createInitialsAvatar('Test User') : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K'
                    },
                    created_at: new Date(Date.now() - 3600000).toISOString(),
                    likes_count: 3,
                    comments_count: 1
                }
            ];

            this.renderPosts(posts);
        } catch (error) {
            console.error('Failed to load posts:', error);
            this.renderError('Failed to load posts');
        }
    }

    renderPosts(posts) {
        const socialElement = document.getElementById('social-page');
        if (!socialElement) return;

        socialElement.innerHTML = `
            <div class="page-header">
                <h1>Social Network</h1>
                <p>Социальная сеть с постами и чатами</p>
            </div>

            <div class="social-content">
                <div class="create-post-section">
                    <div class="create-post-form">
                        <textarea id="new-post-content" placeholder="Что у вас нового?" rows="3"></textarea>
                        <div class="post-actions">
                            <button class="btn btn-primary" id="publish-post-btn">Опубликовать</button>
                        </div>
                    </div>
                </div>

                <div class="posts-feed">
                    ${posts.map(post => `
                        <div class="post-card" data-post-id="${post.id}">
                            <div class="post-header">
                                <div class="post-author">
                                    <img src="${post.author.avatar}" alt="${post.author.name}" class="author-avatar">
                                    <div class="author-info">
                                        <h4>${post.author.name}</h4>
                                        <span class="post-time">${this.formatTime(post.created_at)}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="post-content">
                                <p>${post.content}</p>
                            </div>
                            <div class="post-footer">
                                <button class="post-action-btn like-btn" data-post-id="${post.id}">
                                    👍 ${post.likes_count}
                                </button>
                                <button class="post-action-btn comment-btn" data-post-id="${post.id}">
                                    💬 ${post.comments_count}
                                </button>
                                <button class="post-action-btn share-btn" data-post-id="${post.id}">
                                    🔗 Поделиться
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    formatTime(timestamp) {
        const now = new Date();
        const postTime = new Date(timestamp);
        const diffInMinutes = Math.floor((now - postTime) / (1000 * 60));

        if (diffInMinutes < 1) return 'только что';
        if (diffInMinutes < 60) return `${diffInMinutes} мин назад`;

        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours} ч назад`;

        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays} дн назад`;
    }

    renderError(message) {
        const socialElement = document.getElementById('social-page');
        if (!socialElement) return;

        socialElement.innerHTML = `
            <div class="page-header">
                <h1>Social Network</h1>
                <p>Социальная сеть с постами и чатами</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.App.modules.social.loadPosts()">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Publish post
        document.addEventListener('click', (e) => {
            if (e.target.id === 'publish-post-btn') {
                this.publishPost();
            }
        });

        // Like post
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('like-btn')) {
                const postId = e.target.dataset.postId;
                this.likePost(postId);
            }
        });
    }

    async publishPost() {
        const content = document.getElementById('new-post-content').value.trim();
        if (!content) {
            Toast.warning('Введите текст поста');
            return;
        }

        try {
            Toast.info('Пост публикуется...');
            // Simulate API call
            setTimeout(() => {
                Toast.success('Пост опубликован!');
                document.getElementById('new-post-content').value = '';
                this.loadPosts(); // Reload posts
            }, 1000);
        } catch (error) {
            console.error('Failed to publish post:', error);
            Toast.error('Ошибка при публикации поста');
        }
    }

    async likePost(postId) {
        try {
            Toast.info('Лайк добавлен!');
            // Simulate API call
        } catch (error) {
            console.error('Failed to like post:', error);
            Toast.error('Ошибка при добавлении лайка');
        }
    }

    onPageShow() {
        console.log('Social page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.SocialModule = SocialModule;
