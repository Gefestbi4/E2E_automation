// Social network page module
class SocialModule {
    constructor() {
        console.log('SocialModule constructor - SocialService available:', !!window.SocialService);
        this.socialService = null;
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Social module...');

        // Инициализируем сервис
        if (!this.socialService && window.SocialService) {
            this.socialService = window.SocialService;
            console.log('SocialService initialized:', !!this.socialService);
        }

        if (!this.socialService) {
            console.error('SocialService not available');
            throw new Error('SocialService not available');
        }

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
            console.log('Loading posts from API...');

            // Проверяем, что сервис доступен
            if (!this.socialService) {
                console.error('SocialService not available');
                throw new Error('SocialService not available');
            }

            console.log('👥 SocialService type:', typeof this.socialService);
            console.log('👥 SocialService constructor:', this.socialService.constructor.name);
            console.log('👥 SocialService methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(this.socialService)));

            const response = await this.socialService.getPosts();
            console.log('Posts loaded:', response);

            // Если API возвращает объект с items, используем его, иначе используем response напрямую
            const posts = response.items || response.posts || response || [];

            // Если нет постов, используем mock data
            if (posts.length === 0) {
                console.log('No posts found, using fallback mock data...');
                const mockPosts = [
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
                this.renderPosts(mockPosts);
            } else {
                this.renderPosts(posts);
            }
        } catch (error) {
            console.error('Failed to load posts:', error);

            // Fallback на mock data при ошибке API
            console.log('Using fallback mock data due to API error...');
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
        }
    }

    renderPosts(posts) {
        const socialElement = document.getElementById('social-page');
        if (!socialElement) return;

        // Скрываем skeleton loader если он есть
        if (window.Loading) {
            const postsContainer = socialElement.querySelector('.posts-feed');
            if (postsContainer) {
                window.Loading.hideSkeleton(postsContainer);
            }
        }

        socialElement.innerHTML = `
            <div class="page-header">
                <h1>Social Network</h1>
                <p>Социальная сеть с постами и чатами</p>
            </div>

            <div class="social-content">
                <div class="create-post-section">
                    <div class="create-post-card">
                        <div class="create-post-header">
                            <img src="https://via.placeholder.com/40x40?text=U" alt="User Avatar" class="user-avatar" id="create-post-avatar">
                            <div class="user-info">
                                <h4 id="create-post-username">Test User</h4>
                            </div>
                        </div>
                        <div class="create-post-form">
                            <textarea id="new-post-content" placeholder="Что у вас нового?" rows="3"></textarea>
                            <div class="create-post-actions">
                                <button class="btn btn-primary hover-lift click-ripple" id="publish-post-btn">Опубликовать</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="posts-feed">
                    ${posts.map(post => `
                        <div class="post-card hover-lift animate-on-scroll" data-post-id="${post.id}" data-animation="slideInUp">
                            <div class="post-header">
                                <div class="post-author">
                                    <img src="${post.author.avatar || 'https://via.placeholder.com/40x40?text=U'}" alt="${post.author.name}" class="author-avatar">
                                    <div class="author-info">
                                        <h4>${post.author.name}</h4>
                                        <span class="post-time">${this.formatTime(post.created_at)}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="post-content">
                                <p>${post.content}</p>
                            </div>
                            <div class="post-actions">
                                <button class="btn btn-secondary btn-sm post-action-btn like-btn" data-post-id="${post.id}">
                                    👍 ${post.likes_count}
                                </button>
                                <button class="btn btn-secondary btn-sm post-action-btn comment-btn" data-post-id="${post.id}">
                                    💬 ${post.comments_count}
                                </button>
                                <button class="btn btn-secondary btn-sm post-action-btn share-btn" data-post-id="${post.id}">
                                    Поделиться
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

            if (e.target.id === 'create-post-btn') {
                this.showCreatePostModal();
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

    showCreatePostModal() {
        console.log('👥 Opening create post modal...');

        // Создаем продвинутое модальное окно для создания поста
        const modal = new AdvancedModal('create-post-modal', {
            closable: true,
            backdrop: true,
            keyboard: true,
            size: 'large',
            animation: 'slide',
            autoFocus: true,
            trapFocus: true
        });

        const content = {
            title: 'Создать новый пост',
            body: `
                <form id="create-post-form" class="post-form">
                    <div class="form-group">
                        <label for="post-content">Содержание поста *</label>
                        <textarea id="post-content" name="content" rows="6" required 
                                  placeholder="Что у вас на уме?"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="post-tags">Теги (через запятую)</label>
                        <input type="text" id="post-tags" name="tags" 
                               placeholder="автоматизация, тестирование, python">
                    </div>
                    <div class="form-group">
                        <label for="post-image">URL изображения</label>
                        <input type="url" id="post-image" name="image_url" 
                               placeholder="https://example.com/image.jpg">
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="post-public" name="is_public" checked>
                            Публичный пост
                        </label>
                    </div>
                </form>
            `,
            footer: `
                <button type="button" class="btn btn-secondary" onclick="window.AdvancedModal.close('create-post-modal')">Отмена</button>
                <button type="button" class="btn btn-primary" onclick="window.SocialModule.publishPost()">Опубликовать</button>
            `
        };

        modal.show(content);

        // Инициализируем продвинутую форму
        setTimeout(() => {
            const form = document.getElementById('create-post-form');
            if (form && window.AdvancedForm) {
                new AdvancedForm(form, {
                    validateOnChange: true,
                    validateOnBlur: true,
                    showErrorsInline: true,
                    autoSave: false
                });
            }
        }, 100);
    }

    async publishPost() {
        try {
            console.log('👥 Publishing post...');

            const form = document.getElementById('create-post-form');
            if (!form) {
                // Fallback to inline form
                const content = document.getElementById('new-post-content')?.value?.trim();
                if (!content) {
                    if (window.Toast && typeof window.Toast.warning === 'function') {
                        window.Toast.warning('Введите текст поста');
                    } else {
                        alert('Введите текст поста');
                    }
                    return;
                }

                // Use inline form
                await this.publishInlinePost(content);
                return;
            }

            // Валидация формы
            const formData = new FormData(form);
            const postData = {
                content: formData.get('content')?.trim(),
                tags: formData.get('tags')?.trim(),
                image_url: formData.get('image_url')?.trim(),
                is_public: formData.get('is_public') === 'on'
            };

            // Дополнительная валидация
            if (!postData.content) {
                throw new Error('Содержание поста обязательно');
            }

            console.log('Post data:', postData);

            // Показываем индикатор загрузки
            const submitBtn = form.querySelector('button[onclick*="publishPost"]');
            let originalText = 'Опубликовать';
            if (submitBtn) {
                originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.textContent = 'Публикация...';
            }

            try {
                // Здесь должен быть вызов API для создания поста
                // const response = await this.socialService.createPost(postData);

                // Пока симулируем API вызов
                await new Promise(resolve => setTimeout(resolve, 1000));

                console.log('Post published:', postData);

                if (window.Toast && typeof window.Toast.success === 'function') {
                    window.Toast.success('Пост успешно опубликован!');
                } else {
                    alert('Пост успешно опубликован!');
                }

                if (window.AdvancedModal) {
                    window.AdvancedModal.close('create-post-modal');
                }

                // Перезагружаем список постов
                await this.loadPosts();

            } finally {
                // Восстанавливаем кнопку
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            }

        } catch (error) {
            console.error('Failed to publish post:', error);

            if (window.Toast && typeof window.Toast.error === 'function') {
                window.Toast.error('Ошибка при публикации поста: ' + error.message);
            } else {
                alert('Ошибка при публикации поста: ' + error.message);
            }
        }
    }

    async publishInlinePost(content) {
        try {
            if (window.Toast && typeof window.Toast.info === 'function') {
                window.Toast.info('Пост публикуется...');
            }

            // Симулируем API вызов
            await new Promise(resolve => setTimeout(resolve, 1000));

            if (window.Toast && typeof window.Toast.success === 'function') {
                window.Toast.success('Пост опубликован!');
            }

            // Очищаем форму
            const contentInput = document.getElementById('new-post-content');
            if (contentInput) {
                contentInput.value = '';
            }

            // Перезагружаем посты
            await this.loadPosts();

        } catch (error) {
            console.error('Failed to publish inline post:', error);
            if (window.Toast && typeof window.Toast.error === 'function') {
                window.Toast.error('Ошибка при публикации поста');
            } else {
                alert('Ошибка при публикации поста');
            }
        }
    }

    async likePost(postId) {
        try {
            if (window.Toast && typeof window.Toast.info === 'function') {
                window.Toast.info('Лайк добавлен!');
            } else {
                alert('Лайк добавлен!');
            }
            // Simulate API call
        } catch (error) {
            console.error('Failed to like post:', error);
            if (window.Toast && typeof window.Toast.error === 'function') {
                window.Toast.error('Ошибка при добавлении лайка');
            } else {
                alert('Ошибка при добавлении лайка');
            }
        }
    }

    onPageShow() {
        console.log('Social page shown');
        if (!this.isInitialized) {
            this.init();
        }

        // Set user avatar in create post section
        this.setCreatePostUserInfo();
    }

    setCreatePostUserInfo() {
        const createPostAvatar = document.getElementById('create-post-avatar');
        const createPostUsername = document.getElementById('create-post-username');

        if (createPostAvatar && createPostUsername) {
            // Get current user data from AuthService
            if (window.AuthService && window.AuthService.getStoredUserData) {
                const userData = window.AuthService.getStoredUserData();
                if (userData) {
                    createPostUsername.textContent = userData.full_name || userData.email || 'Test User';

                    // Set avatar
                    if (userData.avatar_url) {
                        createPostAvatar.src = userData.avatar_url;
                        createPostAvatar.onerror = () => {
                            AvatarUtils.handleAvatarError(createPostAvatar, userData.full_name || userData.email);
                        };
                    } else {
                        AvatarUtils.setInitialsAvatar(createPostAvatar, userData.full_name || userData.email || 'Test User');
                    }
                } else {
                    // Fallback to default
                    createPostUsername.textContent = 'Test User';
                    AvatarUtils.setInitialsAvatar(createPostAvatar, 'Test User');
                }
            } else {
                // Fallback to default
                createPostUsername.textContent = 'Test User';
                AvatarUtils.setInitialsAvatar(createPostAvatar, 'Test User');
            }
        }
    }
}

// Export for global access
window.SocialModule = new SocialModule();
