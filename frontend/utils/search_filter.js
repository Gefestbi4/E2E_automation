/**
 * Система поиска и фильтрации
 * Поддерживает поиск постов, пользователей, тегов
 */

class SearchFilterManager {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.searchHistory = [];
        this.currentFilters = {};
        this.searchTimeout = null;
        this.isSearching = false;
    }

    /**
     * Инициализация системы поиска
     */
    init() {
        this.createSearchUI();
        this.setupEventListeners();
        this.loadSearchHistory();
        console.log('🔍 Search Filter Manager initialized');
    }

    /**
     * Создание UI для поиска
     */
    createSearchUI() {
        // Создаем контейнер для поиска
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <div class="search-header">
                <h2><i class="fas fa-search"></i> Поиск и фильтрация</h2>
            </div>
            
            <div class="search-input-container">
                <div class="search-input-wrapper">
                    <input type="text" id="search-input" class="search-input" placeholder="Поиск постов, пользователей, тегов...">
                    <button id="search-btn" class="btn btn-primary search-btn">
                        <i class="fas fa-search"></i>
                    </button>
                    <button id="clear-search-btn" class="btn btn-secondary clear-btn" style="display: none;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="search-suggestions" id="search-suggestions" style="display: none;"></div>
            </div>

            <div class="search-filters">
                <div class="filter-section">
                    <h3>Фильтры</h3>
                    <div class="filter-grid">
                        <div class="filter-group">
                            <label>Тип контента</label>
                            <select id="content-type-filter">
                                <option value="">Все типы</option>
                                <option value="posts">Посты</option>
                                <option value="users">Пользователи</option>
                                <option value="tags">Теги</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label>Категория</label>
                            <select id="category-filter">
                                <option value="">Все категории</option>
                                <option value="programming">Программирование</option>
                                <option value="design">Дизайн</option>
                                <option value="business">Бизнес</option>
                                <option value="lifestyle">Образ жизни</option>
                            </select>
                        </div>
                        
                        <div class="filter-group">
                            <label>Теги</label>
                            <input type="text" id="tags-filter" placeholder="python, react, vue...">
                        </div>
                        
                        <div class="filter-group">
                            <label>Дата от</label>
                            <input type="date" id="date-from-filter">
                        </div>
                        
                        <div class="filter-group">
                            <label>Дата до</label>
                            <input type="date" id="date-to-filter">
                        </div>
                        
                        <div class="filter-group">
                            <label>Автор</label>
                            <input type="text" id="author-filter" placeholder="Имя автора...">
                        </div>
                    </div>
                    
                    <div class="filter-actions">
                        <button id="apply-filters-btn" class="btn btn-primary">
                            <i class="fas fa-filter"></i> Применить фильтры
                        </button>
                        <button id="clear-filters-btn" class="btn btn-secondary">
                            <i class="fas fa-times"></i> Очистить
                        </button>
                    </div>
                </div>
            </div>

            <div class="search-results" id="search-results">
                <div class="results-header">
                    <h3>Результаты поиска</h3>
                    <div class="results-info">
                        <span id="results-count">0 результатов</span>
                        <div class="sort-options">
                            <label>Сортировка:</label>
                            <select id="sort-select">
                                <option value="relevance">По релевантности</option>
                                <option value="date">По дате</option>
                                <option value="popularity">По популярности</option>
                                <option value="alphabetical">По алфавиту</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="results-content" id="results-content">
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <p>Введите поисковый запрос для начала поиска</p>
                    </div>
                </div>
                
                <div class="pagination" id="pagination" style="display: none;">
                    <button id="prev-page-btn" class="btn btn-secondary" disabled>
                        <i class="fas fa-chevron-left"></i> Назад
                    </button>
                    <span id="page-info">Страница 1 из 1</span>
                    <button id="next-page-btn" class="btn btn-secondary" disabled>
                        Вперед <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>

            <div class="search-sidebar">
                <div class="search-history">
                    <h3>История поиска</h3>
                    <div id="search-history-list" class="history-list"></div>
                    <button id="clear-history-btn" class="btn btn-sm btn-secondary">
                        <i class="fas fa-trash"></i> Очистить историю
                    </button>
                </div>
                
                <div class="popular-searches">
                    <h3>Популярные запросы</h3>
                    <div id="popular-searches-list" class="popular-list"></div>
                </div>
            </div>
        `;

        // Добавляем стили
        this.addStyles();

        // Добавляем в DOM
        document.body.appendChild(searchContainer);
    }

    /**
     * Добавление CSS стилей
     */
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .search-container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                display: grid;
                grid-template-columns: 1fr 300px;
                gap: 20px;
            }

            .search-header {
                grid-column: 1 / -1;
                margin-bottom: 20px;
            }

            .search-header h2 {
                color: #333;
                margin: 0;
            }

            .search-input-container {
                grid-column: 1 / -1;
                position: relative;
                margin-bottom: 20px;
            }

            .search-input-wrapper {
                display: flex;
                gap: 10px;
            }

            .search-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }

            .search-input:focus {
                outline: none;
                border-color: #007bff;
            }

            .search-btn, .clear-btn {
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 500;
            }

            .search-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border: 1px solid #ddd;
                border-top: none;
                border-radius: 0 0 8px 8px;
                max-height: 200px;
                overflow-y: auto;
                z-index: 1000;
            }

            .suggestion-item {
                padding: 10px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                transition: background-color 0.2s ease;
            }

            .suggestion-item:hover {
                background-color: #f8f9fa;
            }

            .search-filters {
                grid-column: 1 / -1;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }

            .filter-section h3 {
                margin: 0 0 15px 0;
                color: #333;
            }

            .filter-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }

            .filter-group {
                display: flex;
                flex-direction: column;
            }

            .filter-group label {
                font-weight: 500;
                margin-bottom: 5px;
                color: #555;
            }

            .filter-group input,
            .filter-group select {
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }

            .filter-actions {
                display: flex;
                gap: 10px;
            }

            .search-results {
                grid-column: 1;
            }

            .results-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #eee;
            }

            .results-header h3 {
                margin: 0;
                color: #333;
            }

            .results-info {
                display: flex;
                align-items: center;
                gap: 20px;
            }

            .sort-options {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .sort-options select {
                padding: 5px 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }

            .results-content {
                min-height: 200px;
            }

            .no-results {
                text-align: center;
                padding: 40px;
                color: #666;
            }

            .no-results i {
                font-size: 48px;
                margin-bottom: 20px;
                color: #ddd;
            }

            .result-item {
                background: white;
                border: 1px solid #eee;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 15px;
                transition: box-shadow 0.2s ease;
            }

            .result-item:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 10px;
            }

            .result-title {
                font-size: 18px;
                font-weight: 600;
                color: #333;
                margin: 0;
            }

            .result-meta {
                font-size: 12px;
                color: #666;
            }

            .result-content {
                color: #555;
                line-height: 1.5;
                margin-bottom: 15px;
            }

            .result-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-bottom: 10px;
            }

            .result-tag {
                background: #e3f2fd;
                color: #1976d2;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 12px;
            }

            .result-actions {
                display: flex;
                gap: 10px;
            }

            .pagination {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin-top: 30px;
            }

            .search-sidebar {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }

            .search-history,
            .popular-searches {
                background: white;
                border: 1px solid #eee;
                border-radius: 8px;
                padding: 20px;
            }

            .search-history h3,
            .popular-searches h3 {
                margin: 0 0 15px 0;
                color: #333;
                font-size: 16px;
            }

            .history-list,
            .popular-list {
                margin-bottom: 15px;
            }

            .history-item,
            .popular-item {
                padding: 8px 12px;
                margin-bottom: 5px;
                background: #f8f9fa;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.2s ease;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .history-item:hover,
            .popular-item:hover {
                background: #e9ecef;
            }

            .history-item .remove-btn,
            .popular-item .trend {
                font-size: 12px;
                color: #666;
            }

            .trend.up {
                color: #28a745;
            }

            .trend.down {
                color: #dc3545;
            }

            .trend.stable {
                color: #6c757d;
            }

            @media (max-width: 768px) {
                .search-container {
                    grid-template-columns: 1fr;
                }
                
                .filter-grid {
                    grid-template-columns: 1fr;
                }
                
                .results-header {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 10px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        const searchInput = document.getElementById('search-input');
        const searchBtn = document.getElementById('search-btn');
        const clearSearchBtn = document.getElementById('clear-search-btn');
        const applyFiltersBtn = document.getElementById('apply-filters-btn');
        const clearFiltersBtn = document.getElementById('clear-filters-btn');
        const clearHistoryBtn = document.getElementById('clear-history-btn');

        // Поиск по вводу
        searchInput.addEventListener('input', (e) => {
            this.handleSearchInput(e.target.value);
        });

        // Поиск по кнопке
        searchBtn.addEventListener('click', () => {
            this.performSearch();
        });

        // Очистка поиска
        clearSearchBtn.addEventListener('click', () => {
            this.clearSearch();
        });

        // Применение фильтров
        applyFiltersBtn.addEventListener('click', () => {
            this.applyFilters();
        });

        // Очистка фильтров
        clearFiltersBtn.addEventListener('click', () => {
            this.clearFilters();
        });

        // Очистка истории
        clearHistoryBtn.addEventListener('click', () => {
            this.clearSearchHistory();
        });

        // Поиск по Enter
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
    }

    /**
     * Обработка ввода поискового запроса
     */
    handleSearchInput(query) {
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }

        // Очищаем предыдущий таймаут
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }

        // Устанавливаем новый таймаут для автодополнения
        this.searchTimeout = setTimeout(() => {
            this.getSuggestions(query);
        }, 300);
    }

    /**
     * Получение предложений для автодополнения
     */
    async getSuggestions(query) {
        try {
            const response = await fetch(`${this.apiBase}/api/search/suggestions?q=${encodeURIComponent(query)}&limit=5`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.showSuggestions(data.suggestions);

        } catch (error) {
            console.error('Error getting suggestions:', error);
        }
    }

    /**
     * Показ предложений
     */
    showSuggestions(suggestions) {
        const container = document.getElementById('search-suggestions');

        if (suggestions.length === 0) {
            container.style.display = 'none';
            return;
        }

        container.innerHTML = suggestions.map(suggestion => `
            <div class="suggestion-item" onclick="window.searchFilterManager.selectSuggestion('${suggestion}')">
                ${suggestion}
            </div>
        `).join('');

        container.style.display = 'block';
    }

    /**
     * Скрытие предложений
     */
    hideSuggestions() {
        const container = document.getElementById('search-suggestions');
        container.style.display = 'none';
    }

    /**
     * Выбор предложения
     */
    selectSuggestion(suggestion) {
        document.getElementById('search-input').value = suggestion;
        this.hideSuggestions();
        this.performSearch();
    }

    /**
     * Выполнение поиска
     */
    async performSearch() {
        const query = document.getElementById('search-input').value.trim();

        if (!query) {
            this.showError('Введите поисковый запрос');
            return;
        }

        this.isSearching = true;
        this.showLoading(true);

        try {
            // Определяем тип поиска
            const contentType = document.getElementById('content-type-filter').value;

            let results;
            if (contentType === 'users') {
                results = await this.searchUsers(query);
            } else if (contentType === 'tags') {
                results = await this.searchTags(query);
            } else {
                results = await this.searchPosts(query);
            }

            this.displayResults(results, contentType);
            this.saveToHistory(query);

        } catch (error) {
            this.showError(`Ошибка поиска: ${error.message}`);
        } finally {
            this.isSearching = false;
            this.showLoading(false);
        }
    }

    /**
     * Поиск постов
     */
    async searchPosts(query) {
        const filters = this.getCurrentFilters();

        const response = await fetch(`${this.apiBase}/api/search/posts?q=${encodeURIComponent(query)}&${this.buildQueryString(filters)}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Поиск пользователей
     */
    async searchUsers(query) {
        const filters = this.getCurrentFilters();

        const response = await fetch(`${this.apiBase}/api/search/users?q=${encodeURIComponent(query)}&${this.buildQueryString(filters)}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Поиск тегов
     */
    async searchTags(query) {
        const response = await fetch(`${this.apiBase}/api/search/tags?q=${encodeURIComponent(query)}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Получение текущих фильтров
     */
    getCurrentFilters() {
        return {
            category: document.getElementById('category-filter').value,
            tags: document.getElementById('tags-filter').value.split(',').map(tag => tag.trim()).filter(tag => tag),
            date_from: document.getElementById('date-from-filter').value,
            date_to: document.getElementById('date-to-filter').value,
            author: document.getElementById('author-filter').value,
        };
    }

    /**
     * Построение query string
     */
    buildQueryString(filters) {
        const params = new URLSearchParams();

        Object.entries(filters).forEach(([key, value]) => {
            if (value !== '' && value !== null && value !== undefined) {
                if (Array.isArray(value)) {
                    params.append(key, value.join(','));
                } else {
                    params.append(key, value);
                }
            }
        });

        return params.toString();
    }

    /**
     * Отображение результатов
     */
    displayResults(results, contentType) {
        const container = document.getElementById('results-content');
        const countElement = document.getElementById('results-count');

        countElement.textContent = `${results.total} результатов`;

        if (results.results.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <p>По вашему запросу ничего не найдено</p>
                </div>
            `;
            return;
        }

        let html = '';

        if (contentType === 'users') {
            html = results.results.map(user => this.renderUserResult(user)).join('');
        } else if (contentType === 'tags') {
            html = results.results.map(tag => this.renderTagResult(tag)).join('');
        } else {
            html = results.results.map(post => this.renderPostResult(post)).join('');
        }

        container.innerHTML = html;
    }

    /**
     * Рендер результата поста
     */
    renderPostResult(post) {
        return `
            <div class="result-item">
                <div class="result-header">
                    <h4 class="result-title">${post.title}</h4>
                    <div class="result-meta">
                        ${post.created_at} • ${post.views_count} просмотров
                    </div>
                </div>
                <div class="result-content">${post.content.substring(0, 200)}...</div>
                <div class="result-tags">
                    ${post.tags.map(tag => `<span class="result-tag">${tag}</span>`).join('')}
                </div>
                <div class="result-actions">
                    <button class="btn btn-sm btn-primary">Читать</button>
                    <button class="btn btn-sm btn-secondary">Поделиться</button>
                </div>
            </div>
        `;
    }

    /**
     * Рендер результата пользователя
     */
    renderUserResult(user) {
        return `
            <div class="result-item">
                <div class="result-header">
                    <h4 class="result-title">${user.full_name}</h4>
                    <div class="result-meta">
                        @${user.username} • ${user.followers_count} подписчиков
                    </div>
                </div>
                <div class="result-content">${user.bio}</div>
                <div class="result-meta">${user.location}</div>
                <div class="result-actions">
                    <button class="btn btn-sm btn-primary">Подписаться</button>
                    <button class="btn btn-sm btn-secondary">Профиль</button>
                </div>
            </div>
        `;
    }

    /**
     * Рендер результата тега
     */
    renderTagResult(tag) {
        return `
            <div class="result-item">
                <div class="result-header">
                    <h4 class="result-title">#${tag.name}</h4>
                    <div class="result-meta">
                        ${tag.count} постов
                    </div>
                </div>
                <div class="result-actions">
                    <button class="btn btn-sm btn-primary">Подписаться на тег</button>
                </div>
            </div>
        `;
    }

    /**
     * Применение фильтров
     */
    applyFilters() {
        this.currentFilters = this.getCurrentFilters();
        this.performSearch();
    }

    /**
     * Очистка фильтров
     */
    clearFilters() {
        document.getElementById('category-filter').value = '';
        document.getElementById('tags-filter').value = '';
        document.getElementById('date-from-filter').value = '';
        document.getElementById('date-to-filter').value = '';
        document.getElementById('author-filter').value = '';

        this.currentFilters = {};
    }

    /**
     * Очистка поиска
     */
    clearSearch() {
        document.getElementById('search-input').value = '';
        document.getElementById('results-content').innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>Введите поисковый запрос для начала поиска</p>
            </div>
        `;
        document.getElementById('results-count').textContent = '0 результатов';
        document.getElementById('clear-search-btn').style.display = 'none';
    }

    /**
     * Показ загрузки
     */
    showLoading(show) {
        const container = document.getElementById('results-content');
        if (show) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-spinner fa-spin"></i>
                    <p>Поиск...</p>
                </div>
            `;
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
     * Сохранение в историю
     */
    saveToHistory(query) {
        if (!this.searchHistory.includes(query)) {
            this.searchHistory.unshift(query);
            if (this.searchHistory.length > 20) {
                this.searchHistory = this.searchHistory.slice(0, 20);
            }
            this.saveSearchHistory();
        }
    }

    /**
     * Загрузка истории поиска
     */
    loadSearchHistory() {
        const saved = localStorage.getItem('searchHistory');
        if (saved) {
            this.searchHistory = JSON.parse(saved);
            this.renderSearchHistory();
        }
        this.loadPopularSearches();
    }

    /**
     * Сохранение истории поиска
     */
    saveSearchHistory() {
        localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
        this.renderSearchHistory();
    }

    /**
     * Рендер истории поиска
     */
    renderSearchHistory() {
        const container = document.getElementById('search-history-list');
        container.innerHTML = this.searchHistory.map(query => `
            <div class="history-item" onclick="window.searchFilterManager.selectSuggestion('${query}')">
                <span>${query}</span>
                <button class="remove-btn" onclick="event.stopPropagation(); window.searchFilterManager.removeFromHistory('${query}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
    }

    /**
     * Удаление из истории
     */
    removeFromHistory(query) {
        this.searchHistory = this.searchHistory.filter(q => q !== query);
        this.saveSearchHistory();
    }

    /**
     * Очистка истории поиска
     */
    clearSearchHistory() {
        this.searchHistory = [];
        this.saveSearchHistory();
    }

    /**
     * Загрузка популярных поисков
     */
    async loadPopularSearches() {
        try {
            const response = await fetch(`${this.apiBase}/api/search/popular?limit=10`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            this.renderPopularSearches(data.popular_searches);

        } catch (error) {
            console.error('Error loading popular searches:', error);
        }
    }

    /**
     * Рендер популярных поисков
     */
    renderPopularSearches(popular) {
        const container = document.getElementById('popular-searches-list');
        container.innerHTML = popular.map(item => `
            <div class="popular-item" onclick="window.searchFilterManager.selectSuggestion('${item.query}')">
                <span>${item.query}</span>
                <span class="trend ${item.trend}">${item.count}</span>
            </div>
        `).join('');
    }
}

// Экспорт для глобального доступа
console.log('🔍 SearchFilterManager class defined:', typeof SearchFilterManager);
window.SearchFilterManager = SearchFilterManager;
window.searchFilterManager = new SearchFilterManager();
console.log('🔍 SearchFilterManager exported to window:', typeof window.SearchFilterManager);
