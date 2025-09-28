/**
 * Social Feed utilities for enhanced social networking features
 * Provides post management, interactions, and real-time updates
 */

class SocialFeedManager {
    constructor() {
        this.posts = [];
        this.currentUser = null;
        this.filters = {
            type: 'all', // all, text, image, video, link
            author: null,
            tags: [],
            dateRange: null
        };
        this.sortBy = 'newest'; // newest, oldest, popular, trending
        this.isLoading = false;
        this.hasMore = true;
        this.page = 1;
        this.pageSize = 20;
        this.observers = new Set();
        this.init();
    }

    /**
     * Initialize social feed manager
     */
    init() {
        this.setupEventListeners();
        this.setupInfiniteScroll();
        this.setupRealTimeUpdates();
        console.log('📱 Social Feed Manager initialized');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Post creation
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="create-post"]')) {
                this.showCreatePostModal();
            }
            if (e.target.matches('[data-action="edit-post"]')) {
                const postId = e.target.dataset.postId;
                this.showEditPostModal(postId);
            }
            if (e.target.matches('[data-action="delete-post"]')) {
                const postId = e.target.dataset.postId;
                this.deletePost(postId);
            }
        });

        // Interactions
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="like-post"]')) {
                const postId = e.target.dataset.postId;
                this.toggleLike(postId);
            }
            if (e.target.matches('[data-action="share-post"]')) {
                const postId = e.target.dataset.postId;
                this.sharePost(postId);
            }
            if (e.target.matches('[data-action="bookmark-post"]')) {
                const postId = e.target.dataset.postId;
                this.toggleBookmark(postId);
            }
        });

        // Comments
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="show-comments"]')) {
                const postId = e.target.dataset.postId;
                this.showComments(postId);
            }
            if (e.target.matches('[data-action="add-comment"]')) {
                const postId = e.target.dataset.postId;
                this.addComment(postId);
            }
        });
    }

    /**
     * Setup infinite scroll
     */
    setupInfiniteScroll() {
        const feedContainer = document.querySelector('.social-feed');
        if (!feedContainer) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && this.hasMore && !this.isLoading) {
                    this.loadMorePosts();
                }
            });
        }, {
            rootMargin: '100px'
        });

        // Observe the last post for infinite scroll trigger
        this.scrollObserver = observer;
    }

    /**
     * Setup real-time updates
     */
    setupRealTimeUpdates() {
        // Simulate real-time updates with polling
        setInterval(() => {
            this.checkForNewPosts();
        }, 30000); // Check every 30 seconds

        // Listen for custom events
        document.addEventListener('postCreated', (e) => {
            this.addPostToFeed(e.detail.post);
        });

        document.addEventListener('postUpdated', (e) => {
            this.updatePostInFeed(e.detail.post);
        });

        document.addEventListener('postDeleted', (e) => {
            this.removePostFromFeed(e.detail.postId);
        });
    }

    /**
     * Load posts with filters and pagination
     */
    async loadPosts(refresh = false) {
        if (this.isLoading) return;

        this.isLoading = true;

        if (refresh) {
            this.page = 1;
            this.hasMore = true;
            this.posts = [];
        }

        try {
            const params = {
                page: this.page,
                limit: this.pageSize,
                sort: this.sortBy,
                type: this.filters.type,
                author: this.filters.author,
                tags: this.filters.tags.join(','),
                date_from: this.filters.dateRange?.from,
                date_to: this.filters.dateRange?.to
            };

            const response = await window.SocialService.getPosts(params);

            if (response && response.items) {
                const newPosts = response.items;

                if (refresh) {
                    this.posts = newPosts;
                } else {
                    this.posts.push(...newPosts);
                }

                this.hasMore = newPosts.length === this.pageSize;
                this.page++;

                this.renderPosts(newPosts, refresh);
                this.notifyObservers('postsLoaded', { posts: newPosts, refresh });
            }
        } catch (error) {
            console.error('Failed to load posts:', error);
            this.notifyObservers('error', { error: error.message });
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Load more posts for infinite scroll
     */
    async loadMorePosts() {
        await this.loadPosts(false);
    }

    /**
     * Render posts in the feed
     */
    renderPosts(posts, refresh = false) {
        const feedContainer = document.querySelector('.social-feed');
        if (!feedContainer) return;

        if (refresh) {
            feedContainer.innerHTML = '';
        }

        posts.forEach(post => {
            const postElement = this.createPostElement(post);
            feedContainer.appendChild(postElement);
        });

        // Setup infinite scroll observer
        if (this.scrollObserver && posts.length > 0) {
            const lastPost = feedContainer.lastElementChild;
            if (lastPost) {
                this.scrollObserver.observe(lastPost);
            }
        }

        // Trigger animations
        if (window.Animations) {
            window.Animations.animateOnScroll();
        }
    }

    /**
     * Create post element
     */
    createPostElement(post) {
        const postDiv = document.createElement('div');
        postDiv.className = 'post-card hover-lift animate-on-scroll card-optimized';
        postDiv.setAttribute('data-post-id', post.id);
        postDiv.setAttribute('data-animation', 'slideInUp');

        postDiv.innerHTML = `
            <div class="post-header">
                <div class="post-author">
                    <img src="${post.author.avatar || 'https://via.placeholder.com/40x40?text=U'}" 
                         alt="${post.author.name}" class="author-avatar optimized">
                    <div class="author-info">
                        <h4 class="author-name">${post.author.name}</h4>
                        <span class="post-time">${this.formatTime(post.created_at)}</span>
                    </div>
                </div>
                <div class="post-actions">
                    <button class="btn btn-sm btn-ghost" data-action="edit-post" data-post-id="${post.id}">
                        <i class="fas fa-edit" aria-hidden="true"></i>
                    </button>
                    <button class="btn btn-sm btn-ghost" data-action="delete-post" data-post-id="${post.id}">
                        <i class="fas fa-trash" aria-hidden="true"></i>
                    </button>
                </div>
            </div>

            <div class="post-content">
                ${this.renderPostContent(post)}
            </div>

            <div class="post-engagement">
                <div class="engagement-stats">
                    <span class="likes-count">${post.likes_count || 0} лайков</span>
                    <span class="comments-count">${post.comments_count || 0} комментариев</span>
                    <span class="shares-count">${post.shares_count || 0} репостов</span>
                </div>
                <div class="engagement-actions">
                    <button class="btn btn-sm btn-ghost ${post.is_liked ? 'liked' : ''}" 
                            data-action="like-post" data-post-id="${post.id}">
                        <i class="fas fa-heart" aria-hidden="true"></i>
                        <span>Лайк</span>
                    </button>
                    <button class="btn btn-sm btn-ghost" data-action="show-comments" data-post-id="${post.id}">
                        <i class="fas fa-comment" aria-hidden="true"></i>
                        <span>Комментарий</span>
                    </button>
                    <button class="btn btn-sm btn-ghost" data-action="share-post" data-post-id="${post.id}">
                        <i class="fas fa-share" aria-hidden="true"></i>
                        <span>Поделиться</span>
                    </button>
                    <button class="btn btn-sm btn-ghost ${post.is_bookmarked ? 'bookmarked' : ''}" 
                            data-action="bookmark-post" data-post-id="${post.id}">
                        <i class="fas fa-bookmark" aria-hidden="true"></i>
                        <span>Сохранить</span>
                    </button>
                </div>
            </div>

            <div class="post-comments" id="comments-${post.id}" style="display: none;">
                <div class="comments-list"></div>
                <div class="add-comment">
                    <input type="text" placeholder="Добавить комментарий..." class="comment-input">
                    <button class="btn btn-primary btn-sm" data-action="add-comment" data-post-id="${post.id}">
                        Отправить
                    </button>
                </div>
            </div>
        `;

        return postDiv;
    }

    /**
     * Render post content based on type
     */
    renderPostContent(post) {
        let content = '';

        // Text content
        if (post.content) {
            content += `<div class="post-text">${this.formatPostText(post.content)}</div>`;
        }

        // Media content
        if (post.media && post.media.length > 0) {
            content += `<div class="post-media">${this.renderMedia(post.media)}</div>`;
        }

        // Link preview
        if (post.link) {
            content += `<div class="post-link-preview">${this.renderLinkPreview(post.link)}</div>`;
        }

        // Tags
        if (post.tags && post.tags.length > 0) {
            content += `<div class="post-tags">${this.renderTags(post.tags)}</div>`;
        }

        return content;
    }

    /**
     * Render media content
     */
    renderMedia(media) {
        return media.map(item => {
            if (item.type === 'image') {
                return `
                    <img src="${item.url}" alt="${item.alt || 'Media'}" 
                         class="post-image optimized responsive" loading="lazy">
                `;
            } else if (item.type === 'video') {
                return `
                    <video controls class="post-video optimized responsive">
                        <source src="${item.url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                `;
            }
            return '';
        }).join('');
    }

    /**
     * Render link preview
     */
    renderLinkPreview(link) {
        return `
            <div class="link-preview">
                <div class="link-preview-content">
                    <h5 class="link-title">${link.title || 'Link'}</h5>
                    <p class="link-description">${link.description || ''}</p>
                    <span class="link-url">${link.url}</span>
                </div>
                ${link.image ? `<img src="${link.image}" alt="Preview" class="link-image optimized">` : ''}
            </div>
        `;
    }

    /**
     * Render tags
     */
    renderTags(tags) {
        return tags.map(tag =>
            `<span class="post-tag" data-tag="${tag}">#${tag}</span>`
        ).join('');
    }

    /**
     * Format post text with mentions and hashtags
     */
    formatPostText(text) {
        // Convert mentions to links
        text = text.replace(/@(\w+)/g, '<a href="#user/$1" class="mention">@$1</a>');

        // Convert hashtags to links
        text = text.replace(/#(\w+)/g, '<a href="#tag/$1" class="hashtag">#$1</a>');

        // Convert URLs to links
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');

        // Convert line breaks to <br>
        text = text.replace(/\n/g, '<br>');

        return text;
    }

    /**
     * Format time for display
     */
    formatTime(timestamp) {
        const now = new Date();
        const postTime = new Date(timestamp);
        const diff = now - postTime;

        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'только что';
        if (minutes < 60) return `${minutes}м назад`;
        if (hours < 24) return `${hours}ч назад`;
        if (days < 7) return `${days}д назад`;

        return postTime.toLocaleDateString();
    }

    /**
     * Show create post modal
     */
    showCreatePostModal() {
        if (window.AdvancedModal) {
            const modal = new window.AdvancedModal({
                title: 'Создать пост',
                content: this.getCreatePostForm(),
                size: 'large',
                onConfirm: (data) => this.createPost(data)
            });
            modal.show();
        }
    }

    /**
     * Get create post form HTML
     */
    getCreatePostForm() {
        return `
            <form class="create-post-form">
                <div class="form-group">
                    <textarea name="content" placeholder="Что у вас нового?" 
                              class="form-control" rows="4" required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Тип поста:</label>
                    <select name="type" class="form-control">
                        <option value="text">Текст</option>
                        <option value="image">Изображение</option>
                        <option value="video">Видео</option>
                        <option value="link">Ссылка</option>
                    </select>
                </div>
                
                <div class="form-group" id="media-upload" style="display: none;">
                    <label>Медиа файлы:</label>
                    <input type="file" name="media" multiple accept="image/*,video/*" class="form-control">
                </div>
                
                <div class="form-group" id="link-input" style="display: none;">
                    <label>Ссылка:</label>
                    <input type="url" name="link_url" placeholder="https://..." class="form-control">
                </div>
                
                <div class="form-group">
                    <label>Теги (через запятую):</label>
                    <input type="text" name="tags" placeholder="тег1, тег2, тег3" class="form-control">
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="is_public" checked>
                        Публичный пост
                    </label>
                </div>
            </form>
        `;
    }

    /**
     * Create new post
     */
    async createPost(data) {
        try {
            const response = await window.SocialService.createPost(data);

            if (response) {
                this.addPostToFeed(response);
                this.notifyObservers('postCreated', { post: response });

                if (window.Toast) {
                    window.Toast.success('Пост успешно создан!');
                }
            }
        } catch (error) {
            console.error('Failed to create post:', error);
            if (window.Toast) {
                window.Toast.error('Ошибка при создании поста');
            }
        }
    }

    /**
     * Add post to feed
     */
    addPostToFeed(post) {
        this.posts.unshift(post);
        const feedContainer = document.querySelector('.social-feed');
        if (feedContainer) {
            const postElement = this.createPostElement(post);
            feedContainer.insertBefore(postElement, feedContainer.firstChild);
        }
    }

    /**
     * Toggle like on post
     */
    async toggleLike(postId) {
        try {
            const post = this.posts.find(p => p.id === postId);
            if (!post) return;

            const response = await window.SocialService.likePost(postId);

            if (response) {
                post.is_liked = !post.is_liked;
                post.likes_count += post.is_liked ? 1 : -1;

                this.updatePostInFeed(post);
                this.notifyObservers('postLiked', { postId, isLiked: post.is_liked });
            }
        } catch (error) {
            console.error('Failed to toggle like:', error);
        }
    }

    /**
     * Update post in feed
     */
    updatePostInFeed(post) {
        const postElement = document.querySelector(`[data-post-id="${post.id}"]`);
        if (postElement) {
            const newPostElement = this.createPostElement(post);
            postElement.replaceWith(newPostElement);
        }
    }

    /**
     * Add observer for events
     */
    addObserver(callback) {
        this.observers.add(callback);
    }

    /**
     * Remove observer
     */
    removeObserver(callback) {
        this.observers.delete(callback);
    }

    /**
     * Notify observers
     */
    notifyObservers(event, data) {
        this.observers.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.error('Observer error:', error);
            }
        });
    }

    /**
     * Set filters
     */
    setFilters(filters) {
        this.filters = { ...this.filters, ...filters };
        this.loadPosts(true);
    }

    /**
     * Set sort order
     */
    setSortBy(sortBy) {
        this.sortBy = sortBy;
        this.loadPosts(true);
    }

    /**
     * Refresh feed
     */
    refresh() {
        this.loadPosts(true);
    }

    /**
     * Check for new posts
     */
    async checkForNewPosts() {
        try {
            const response = await window.SocialService.getPosts({ limit: 5 });
            if (response && response.items) {
                const newPosts = response.items.filter(post =>
                    !this.posts.some(existingPost => existingPost.id === post.id)
                );

                if (newPosts.length > 0) {
                    this.notifyObservers('newPostsAvailable', { count: newPosts.length });
                }
            }
        } catch (error) {
            console.error('Failed to check for new posts:', error);
        }
    }

    /**
     * Обновление ленты с новыми данными
     */
    updateFeed(data) {
        if (data && data.items) {
            this.posts = data.items;
            // Обновляем UI через SocialModule если доступен
            if (window.SocialModule && typeof window.SocialModule.loadPosts === 'function') {
                window.SocialModule.loadPosts();
            }
            console.log('📱 Feed updated with new posts:', data.items.length);
        }
    }
}

// Export for global access
window.SocialFeedManager = SocialFeedManager;
console.log('📱 Social Feed utilities loaded');
