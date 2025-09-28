// Content management page module
class ContentModule {
    constructor() {
        this.contentService = new ContentService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing Content module...');

        try {
            await this.loadArticles();
            this.bindEvents();
            this.isInitialized = true;
            console.log('Content module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Content module:', error);
            throw error;
        }
    }

    async loadArticles() {
        try {
            // Mock data for demo
            const articles = [
                {
                    id: 1,
                    title: 'Демо-статья 1',
                    content: 'Содержимое демо-статьи для тестирования системы управления контентом.',
                    author: { name: 'Demo Author', avatar: typeof AvatarUtils !== 'undefined' ? AvatarUtils.createInitialsAvatar('Demo Author') : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K' },
                    status: 'published',
                    created_at: new Date().toISOString(),
                    views_count: 125,
                    likes_count: 8
                },
                {
                    id: 2,
                    title: 'Демо-статья 2',
                    content: 'Вторая демо-статья с различными элементами контента.',
                    author: { name: 'Test Author', avatar: typeof AvatarUtils !== 'undefined' ? AvatarUtils.createInitialsAvatar('Test Author') : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K' },
                    status: 'draft',
                    created_at: new Date(Date.now() - 86400000).toISOString(),
                    views_count: 45,
                    likes_count: 3
                }
            ];

            this.renderArticles(articles);
        } catch (error) {
            console.error('Failed to load articles:', error);
            this.renderError('Failed to load articles');
        }
    }

    renderArticles(articles) {
        const contentElement = document.getElementById('content-page');
        if (!contentElement) return;

        contentElement.innerHTML = `
            <div class="page-header">
                <h1>Content Management</h1>
                <p>Система управления контентом</p>
            </div>

            <div class="content-dashboard">
                <div class="content-stats">
                    <div class="stat-card">
                        <div class="stat-icon">📝</div>
                        <div class="stat-content">
                            <h3>${articles.length}</h3>
                            <p>Статей</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">👁️</div>
                        <div class="stat-content">
                            <h3>${articles.reduce((sum, article) => sum + article.views_count, 0)}</h3>
                            <p>Просмотров</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">👍</div>
                        <div class="stat-content">
                            <h3>${articles.reduce((sum, article) => sum + article.likes_count, 0)}</h3>
                            <p>Лайков</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📊</div>
                        <div class="stat-content">
                            <h3>${articles.filter(article => article.status === 'published').length}</h3>
                            <p>Опубликовано</p>
                        </div>
                    </div>
                </div>

                <div class="content-actions">
                    <button class="btn btn-primary" id="create-article-btn">Создать статью</button>
                    <button class="btn btn-secondary" id="manage-categories-btn">Управление категориями</button>
                    <button class="btn btn-secondary" id="media-library-btn">Медиа-библиотека</button>
                </div>

                <div class="articles-section">
                    <div class="section-header">
                        <h2>Статьи</h2>
                        <div class="filters">
                            <select id="status-filter">
                                <option value="">Все статусы</option>
                                <option value="published">Опубликованные</option>
                                <option value="draft">Черновики</option>
                                <option value="archived">Архивные</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="articles-list">
                        ${articles.map(article => `
                            <div class="article-card" data-article-id="${article.id}">
                                <div class="article-header">
                                    <h3 class="article-title">${article.title}</h3>
                                    <span class="article-status status-${article.status}">${article.status}</span>
                                </div>
                                <div class="article-meta">
                                    <div class="article-author">
                                        <img src="${article.author.avatar || 'https://via.placeholder.com/40x40?text=U'}" alt="${article.author.name}" class="author-avatar">
                                        <span>${article.author.name}</span>
                                    </div>
                                    <span class="article-date">${this.formatDate(article.created_at)}</span>
                                </div>
                                <div class="article-content">
                                    <p>${article.content.substring(0, 150)}${article.content.length > 150 ? '...' : ''}</p>
                                </div>
                                <div class="article-stats">
                                    <span class="stat">👁️ ${article.views_count}</span>
                                    <span class="stat">👍 ${article.likes_count}</span>
                                </div>
                                <div class="article-actions">
                                    <button class="btn btn-secondary btn-sm" data-action="edit-article" data-article-id="${article.id}">Редактировать</button>
                                    <button class="btn btn-primary btn-sm" data-action="view-article" data-article-id="${article.id}">Просмотр</button>
                                    ${article.status === 'draft' ?
                `<button class="btn btn-success btn-sm" data-action="publish-article" data-article-id="${article.id}">Опубликовать</button>` :
                `<button class="btn btn-warning btn-sm" data-action="unpublish-article" data-article-id="${article.id}">Снять с публикации</button>`
            }
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    formatDate(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    renderError(message) {
        const contentElement = document.getElementById('content-page');
        if (!contentElement) return;

        contentElement.innerHTML = `
            <div class="page-header">
                <h1>Content Management</h1>
                <p>Система управления контентом</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.App.modules.content.loadArticles()">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Create article button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'create-article-btn') {
                this.showCreateArticleModal();
            }
        });

        // Article actions
        document.addEventListener('click', (e) => {
            if (e.target.dataset.action === 'edit-article') {
                const articleId = parseInt(e.target.dataset.articleId);
                this.editArticle(articleId);
            } else if (e.target.dataset.action === 'view-article') {
                const articleId = parseInt(e.target.dataset.articleId);
                this.viewArticle(articleId);
            } else if (e.target.dataset.action === 'publish-article') {
                const articleId = parseInt(e.target.dataset.articleId);
                this.publishArticle(articleId);
            } else if (e.target.dataset.action === 'unpublish-article') {
                const articleId = parseInt(e.target.dataset.articleId);
                this.unpublishArticle(articleId);
            }
        });

        // Other action buttons
        document.addEventListener('click', (e) => {
            if (e.target.id === 'manage-categories-btn') {
                Toast.info('Функция управления категориями будет реализована');
            } else if (e.target.id === 'media-library-btn') {
                Toast.info('Функция медиа-библиотеки будет реализована');
            }
        });

        // Status filter
        document.addEventListener('change', (e) => {
            if (e.target.id === 'status-filter') {
                this.filterArticles(e.target.value);
            }
        });
    }

    showCreateArticleModal() {
        Toast.info('Функция создания статьи будет реализована в следующих версиях');
    }

    filterArticles(status) {
        // Placeholder for filtering logic
        Toast.info(`Фильтрация по статусу: ${status || 'все'}`);
    }

    editArticle(articleId) {
        console.log('Editing article:', articleId);
        Toast.info(`Редактирование статьи ${articleId} будет реализовано в следующих версиях`);
    }

    viewArticle(articleId) {
        console.log('Viewing article:', articleId);
        Toast.info(`Просмотр статьи ${articleId} будет реализован в следующих версиях`);
    }

    publishArticle(articleId) {
        console.log('Publishing article:', articleId);
        Toast.info(`Публикация статьи ${articleId} будет реализована в следующих версиях`);
    }

    unpublishArticle(articleId) {
        console.log('Unpublishing article:', articleId);
        Toast.info(`Снятие с публикации статьи ${articleId} будет реализовано в следующих версиях`);
    }

    onPageShow() {
        console.log('Content page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.ContentModule = ContentModule;
