/**
 * AI и Machine Learning Manager
 * Рекомендации, анализ контента, персонализация
 */

class AIManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.recommendations = [];
        this.trendingTopics = [];
        this.userInsights = null;
        this.isLoading = false;
    }

    /**
     * Инициализация AI системы
     */
    init() {
        this.createAIUI();
        this.setupEventListeners();
        this.loadTrendingTopics();
        this.loadUserInsights();
        console.log('🤖 AI Manager initialized');
    }

    /**
     * Создание AI UI
     */
    createAIUI() {
        // Создаем контейнер для AI функций
        const aiContainer = document.createElement('div');
        aiContainer.className = 'ai-container';
        aiContainer.innerHTML = `
            <div class="ai-header">
                <h2><i class="fas fa-brain"></i> AI & Machine Learning</h2>
                <div class="ai-actions">
                    <button id="refresh-recommendations-btn" class="btn btn-primary">
                        <i class="fas fa-sync"></i> Обновить рекомендации
                    </button>
                    <button id="analyze-content-btn" class="btn btn-secondary">
                        <i class="fas fa-search"></i> Анализ контента
                    </button>
                </div>
            </div>

            <div class="ai-content">
                <div class="ai-sidebar">
                    <div class="ai-section">
                        <h3><i class="fas fa-fire"></i> Тренды</h3>
                        <div id="trending-topics" class="trending-list">
                            <div class="loading">Загрузка трендов...</div>
                        </div>
                    </div>

                    <div class="ai-section">
                        <h3><i class="fas fa-chart-line"></i> Инсайты</h3>
                        <div id="user-insights" class="insights-list">
                            <div class="loading">Загрузка инсайтов...</div>
                        </div>
                    </div>
                </div>

                <div class="ai-main">
                    <div class="ai-tabs">
                        <button class="tab-btn active" data-tab="recommendations">
                            <i class="fas fa-lightbulb"></i> Рекомендации
                        </button>
                        <button class="tab-btn" data-tab="analysis">
                            <i class="fas fa-microscope"></i> Анализ
                        </button>
                        <button class="tab-btn" data-tab="personalization">
                            <i class="fas fa-user-cog"></i> Персонализация
                        </button>
                    </div>

                    <!-- Рекомендации -->
                    <div id="recommendations-tab" class="ai-tab-content active">
                        <div class="recommendations-header">
                            <h3>Рекомендации контента</h3>
                            <div class="recommendation-filters">
                                <select id="content-type-filter" class="form-control">
                                    <option value="posts">Посты</option>
                                    <option value="users">Пользователи</option>
                                    <option value="topics">Темы</option>
                                </select>
                                <button id="load-recommendations-btn" class="btn btn-primary">
                                    <i class="fas fa-refresh"></i> Загрузить
                                </button>
                            </div>
                        </div>
                        <div id="recommendations-list" class="recommendations-list">
                            <div class="loading">Загрузка рекомендаций...</div>
                        </div>
                    </div>

                    <!-- Анализ -->
                    <div id="analysis-tab" class="ai-tab-content">
                        <div class="analysis-tools">
                            <h3>Анализ контента</h3>
                            <div class="analysis-form">
                                <div class="form-group">
                                    <label>Введите текст для анализа:</label>
                                    <textarea id="content-to-analyze" class="form-control" rows="4" 
                                        placeholder="Введите текст для анализа тональности, тегов и спама..."></textarea>
                                </div>
                                <div class="analysis-buttons">
                                    <button id="analyze-sentiment-btn" class="btn btn-info">
                                        <i class="fas fa-smile"></i> Анализ тональности
                                    </button>
                                    <button id="extract-tags-btn" class="btn btn-warning">
                                        <i class="fas fa-tags"></i> Извлечь теги
                                    </button>
                                    <button id="generate-summary-btn" class="btn btn-success">
                                        <i class="fas fa-compress"></i> Краткое содержание
                                    </button>
                                    <button id="detect-spam-btn" class="btn btn-danger">
                                        <i class="fas fa-shield-alt"></i> Детекция спама
                                    </button>
                                </div>
                            </div>
                            <div id="analysis-results" class="analysis-results">
                                <div class="no-content">Выберите тип анализа и введите текст</div>
                            </div>
                        </div>
                    </div>

                    <!-- Персонализация -->
                    <div id="personalization-tab" class="ai-tab-content">
                        <div class="personalization-tools">
                            <h3>Персонализация ленты</h3>
                            <div class="personalization-info">
                                <p>AI анализирует ваши предпочтения и поведение для персонализации контента</p>
                                <div class="personalization-stats">
                                    <div class="stat-item">
                                        <span class="stat-label">Релевантность:</span>
                                        <span class="stat-value" id="relevance-score">--</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Персонализация:</span>
                                        <span class="stat-value" id="personalization-level">--</span>
                                    </div>
                                    <div class="stat-item">
                                        <span class="stat-label">Обновлено:</span>
                                        <span class="stat-value" id="last-update">--</span>
                                    </div>
                                </div>
                            </div>
                            <div class="personalization-actions">
                                <button id="optimize-feed-btn" class="btn btn-primary">
                                    <i class="fas fa-magic"></i> Оптимизировать ленту
                                </button>
                                <button id="reset-preferences-btn" class="btn btn-secondary">
                                    <i class="fas fa-undo"></i> Сбросить предпочтения
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Добавляем стили
        this.addStyles();

        // Добавляем в DOM
        document.body.appendChild(aiContainer);
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .ai-container {
                max-width: 1400px;
                margin: 20px auto;
                padding: 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .ai-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #eee;
            }

            .ai-header h2 {
                margin: 0;
                color: #333;
            }

            .ai-actions {
                display: flex;
                gap: 10px;
            }

            .ai-content {
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 30px;
            }

            .ai-sidebar {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
            }

            .ai-section {
                margin-bottom: 30px;
            }

            .ai-section h3 {
                margin: 0 0 15px 0;
                color: #333;
                font-size: 16px;
            }

            .trending-list, .insights-list {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .trending-item, .insight-item {
                background: white;
                padding: 12px;
                border-radius: 6px;
                border-left: 3px solid #007bff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .trending-item h4, .insight-item h4 {
                margin: 0 0 5px 0;
                font-size: 14px;
                color: #333;
            }

            .trending-item p, .insight-item p {
                margin: 0;
                font-size: 12px;
                color: #666;
            }

            .trending-stats {
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
                font-size: 11px;
                color: #888;
            }

            .ai-main {
                background: white;
                border-radius: 8px;
                padding: 30px;
            }

            .ai-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #eee;
            }

            .tab-btn {
                padding: 12px 20px;
                border: none;
                background: transparent;
                color: #666;
                cursor: pointer;
                border-bottom: 2px solid transparent;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .tab-btn:hover {
                color: #007bff;
                background: #f8f9fa;
            }

            .tab-btn.active {
                color: #007bff;
                border-bottom-color: #007bff;
            }

            .ai-tab-content {
                display: none;
            }

            .ai-tab-content.active {
                display: block;
            }

            .recommendations-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .recommendation-filters {
                display: flex;
                gap: 10px;
                align-items: center;
            }

            .recommendations-list {
                display: grid;
                gap: 15px;
            }

            .recommendation-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #007bff;
            }

            .recommendation-item h4 {
                margin: 0 0 10px 0;
                color: #333;
            }

            .recommendation-item p {
                margin: 0 0 10px 0;
                color: #666;
                line-height: 1.5;
            }

            .recommendation-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #888;
            }

            .recommendation-score {
                background: #007bff;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-weight: bold;
            }

            .analysis-form {
                margin-bottom: 30px;
            }

            .analysis-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 15px;
            }

            .analysis-results {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                min-height: 200px;
            }

            .analysis-result {
                background: white;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 15px;
                border-left: 4px solid #28a745;
            }

            .analysis-result h4 {
                margin: 0 0 10px 0;
                color: #333;
            }

            .analysis-result p {
                margin: 0;
                color: #666;
            }

            .personalization-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }

            .stat-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                text-align: center;
            }

            .stat-label {
                display: block;
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
            }

            .stat-value {
                display: block;
                font-size: 18px;
                font-weight: bold;
                color: #007bff;
            }

            .personalization-actions {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }

            .loading {
                text-align: center;
                color: #666;
                padding: 20px;
            }

            .no-content {
                text-align: center;
                color: #999;
                padding: 40px;
                font-style: italic;
            }

            .btn {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                font-size: 14px;
            }

            .btn-primary {
                background: #007bff;
                color: white;
            }

            .btn-primary:hover {
                background: #0056b3;
            }

            .btn-secondary {
                background: #6c757d;
                color: white;
            }

            .btn-secondary:hover {
                background: #545b62;
            }

            .btn-info {
                background: #17a2b8;
                color: white;
            }

            .btn-info:hover {
                background: #138496;
            }

            .btn-warning {
                background: #ffc107;
                color: #212529;
            }

            .btn-warning:hover {
                background: #e0a800;
            }

            .btn-success {
                background: #28a745;
                color: white;
            }

            .btn-success:hover {
                background: #1e7e34;
            }

            .btn-danger {
                background: #dc3545;
                color: white;
            }

            .btn-danger:hover {
                background: #c82333;
            }

            .form-control {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }

            .form-control:focus {
                outline: none;
                border-color: #007bff;
                box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
            }

            .form-group {
                margin-bottom: 15px;
            }

            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #555;
            }

            @media (max-width: 768px) {
                .ai-content {
                    grid-template-columns: 1fr;
                }
                
                .ai-sidebar {
                    order: 2;
                }
                
                .analysis-buttons {
                    flex-direction: column;
                }
                
                .personalization-stats {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Переключение табов
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Загрузка рекомендаций
        document.getElementById('load-recommendations-btn').addEventListener('click', () => {
            this.loadRecommendations();
        });

        // Обновление рекомендаций
        document.getElementById('refresh-recommendations-btn').addEventListener('click', () => {
            this.loadRecommendations();
        });

        // Анализ контента
        document.getElementById('analyze-sentiment-btn').addEventListener('click', () => {
            this.analyzeSentiment();
        });

        document.getElementById('extract-tags-btn').addEventListener('click', () => {
            this.extractTags();
        });

        document.getElementById('generate-summary-btn').addEventListener('click', () => {
            this.generateSummary();
        });

        document.getElementById('detect-spam-btn').addEventListener('click', () => {
            this.detectSpam();
        });

        // Персонализация
        document.getElementById('optimize-feed-btn').addEventListener('click', () => {
            this.optimizeFeed();
        });

        document.getElementById('reset-preferences-btn').addEventListener('click', () => {
            this.resetPreferences();
        });
    }

    /**
     * Переключение табов
     */
    switchTab(tabName) {
        // Убираем активный класс
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.ai-tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Активируем выбранный таб
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    /**
     * Загрузка трендовых тем
     */
    async loadTrendingTopics() {
        try {
            const response = await fetch(`${this.apiBase}/api/ai/trending/topics`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.trendingTopics = data.trending_topics;
            this.renderTrendingTopics();

        } catch (error) {
            console.error('Error loading trending topics:', error);
            document.getElementById('trending-topics').innerHTML =
                '<div class="error">Ошибка загрузки трендов</div>';
        }
    }

    /**
     * Отображение трендовых тем
     */
    renderTrendingTopics() {
        const container = document.getElementById('trending-topics');

        if (this.trendingTopics.length === 0) {
            container.innerHTML = '<div class="no-content">Нет трендовых тем</div>';
            return;
        }

        container.innerHTML = this.trendingTopics.map(topic => `
            <div class="trending-item">
                <h4>${topic.topic}</h4>
                <p>${topic.mentions} упоминаний</p>
                <div class="trending-stats">
                    <span>Рост: ${topic.growth}%</span>
                    <span class="sentiment-${topic.sentiment}">${topic.sentiment}</span>
                </div>
            </div>
        `).join('');
    }

    /**
     * Загрузка инсайтов пользователя
     */
    async loadUserInsights() {
        try {
            const response = await fetch(`${this.apiBase}/api/ai/insights/user`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.userInsights = data.insights;
            this.renderUserInsights();

        } catch (error) {
            console.error('Error loading user insights:', error);
            document.getElementById('user-insights').innerHTML =
                '<div class="error">Ошибка загрузки инсайтов</div>';
        }
    }

    /**
     * Отображение инсайтов пользователя
     */
    renderUserInsights() {
        const container = document.getElementById('user-insights');

        if (!this.userInsights) {
            container.innerHTML = '<div class="no-content">Нет данных</div>';
            return;
        }

        const insights = [
            {
                title: 'Активность',
                value: `${this.userInsights.activity_patterns.engagement_trends.likes_per_day} лайков/день`
            },
            {
                title: 'Интересы',
                value: this.userInsights.content_preferences.favorite_topics.slice(0, 2).join(', ')
            },
            {
                title: 'Рост сети',
                value: `${this.userInsights.social_behavior.network_growth_rate}%`
            }
        ];

        container.innerHTML = insights.map(insight => `
            <div class="insight-item">
                <h4>${insight.title}</h4>
                <p>${insight.value}</p>
            </div>
        `).join('');
    }

    /**
     * Загрузка рекомендаций
     */
    async loadRecommendations() {
        try {
            this.showLoading(true);

            const contentType = document.getElementById('content-type-filter').value;
            const response = await fetch(`${this.apiBase}/api/ai/recommendations/${contentType}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.recommendations = data.recommendations;
            this.renderRecommendations();

        } catch (error) {
            this.showError(`Ошибка загрузки рекомендаций: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Отображение рекомендаций
     */
    renderRecommendations() {
        const container = document.getElementById('recommendations-list');

        if (this.recommendations.length === 0) {
            container.innerHTML = '<div class="no-content">Нет рекомендаций</div>';
            return;
        }

        container.innerHTML = this.recommendations.map(rec => `
            <div class="recommendation-item">
                <h4>${rec.title || rec.username || rec.topic}</h4>
                <p>${rec.content || rec.bio || rec.description || ''}</p>
                <div class="recommendation-meta">
                    <span>${rec.recommendation_reason || rec.reason || ''}</span>
                    <span class="recommendation-score">${Math.round((rec.relevance_score || rec.similarity_score || 0) * 100)}%</span>
                </div>
            </div>
        `).join('');
    }

    /**
     * Анализ тональности
     */
    async analyzeSentiment() {
        const content = document.getElementById('content-to-analyze').value;
        if (!content.trim()) {
            this.showError('Введите текст для анализа');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/ai/analyze/sentiment`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showAnalysisResult('Анализ тональности', data.analysis);

        } catch (error) {
            this.showError(`Ошибка анализа тональности: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Извлечение тегов
     */
    async extractTags() {
        const content = document.getElementById('content-to-analyze').value;
        if (!content.trim()) {
            this.showError('Введите текст для анализа');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/ai/analyze/tags`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showAnalysisResult('Извлеченные теги', { tags: data.tags.join(', ') });

        } catch (error) {
            this.showError(`Ошибка извлечения тегов: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Генерация краткого содержания
     */
    async generateSummary() {
        const content = document.getElementById('content-to-analyze').value;
        if (!content.trim()) {
            this.showError('Введите текст для анализа');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/ai/analyze/summary`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showAnalysisResult('Краткое содержание', { summary: data.summary });

        } catch (error) {
            this.showError(`Ошибка генерации содержания: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Детекция спама
     */
    async detectSpam() {
        const content = document.getElementById('content-to-analyze').value;
        if (!content.trim()) {
            this.showError('Введите текст для анализа');
            return;
        }

        try {
            this.showLoading(true);

            const response = await fetch(`${this.apiBase}/api/ai/analyze/spam`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({ content })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showAnalysisResult('Детекция спама', data.analysis);

        } catch (error) {
            this.showError(`Ошибка детекции спама: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Показ результата анализа
     */
    showAnalysisResult(title, data) {
        const container = document.getElementById('analysis-results');

        let resultHtml = `<div class="analysis-result">
            <h4>${title}</h4>
            <p>${JSON.stringify(data, null, 2)}</p>
        </div>`;

        container.innerHTML = resultHtml;
    }

    /**
     * Оптимизация ленты
     */
    async optimizeFeed() {
        try {
            this.showLoading(true);

            // В реальном приложении здесь будет запрос к API
            this.showSuccess('Лента оптимизирована!');

            // Обновляем статистику
            document.getElementById('relevance-score').textContent = '95%';
            document.getElementById('personalization-level').textContent = 'Высокая';
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();

        } catch (error) {
            this.showError(`Ошибка оптимизации: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Сброс предпочтений
     */
    async resetPreferences() {
        if (!confirm('Вы уверены, что хотите сбросить все предпочтения?')) {
            return;
        }

        try {
            this.showLoading(true);

            // В реальном приложении здесь будет запрос к API
            this.showSuccess('Предпочтения сброшены!');

            // Обновляем статистику
            document.getElementById('relevance-score').textContent = '--';
            document.getElementById('personalization-level').textContent = '--';
            document.getElementById('last-update').textContent = '--';

        } catch (error) {
            this.showError(`Ошибка сброса: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Показ загрузки
     */
    showLoading(show) {
        const container = document.querySelector('.ai-container');
        if (show) {
            container.style.opacity = '0.6';
            container.style.pointerEvents = 'none';
        } else {
            container.style.opacity = '1';
            container.style.pointerEvents = 'auto';
        }
    }

    /**
     * Показ ошибки
     */
    showError(message) {
        if (window.Toast && typeof window.Toast.error === 'function') {
            window.Toast.error(message);
        } else {
            alert(`Ошибка: ${message}`);
        }
    }

    /**
     * Показ успеха
     */
    showSuccess(message) {
        if (window.Toast && typeof window.Toast.success === 'function') {
            window.Toast.success(message);
        } else {
            alert(`Успех: ${message}`);
        }
    }
}

// Экспорт для глобального доступа
console.log('🤖 AIManager class defined:', typeof AIManager);
window.AIManager = AIManager;
window.aiManager = new AIManager();
console.log('🤖 AIManager exported to window:', typeof window.AIManager);
