# Frontend Quick Start Plan - Immediate Actions

## 🚨 Критические проблемы (исправить СЕЙЧАС)

### 1. Исправить проблему с index.html
**Время: 5 минут**

```bash
# В директории frontend
mv index_new.html index.html
```

**Проверка:**
- Перезапустить frontend контейнер
- Проверить http://localhost:3000

### 2. Обновить API endpoints в сервисах
**Время: 30 минут**

**⚠️ ВАЖНО:** После перезапуска контейнеров база данных очищается, поэтому нужно будет создать тестового пользователя заново.

Нужно обновить все API endpoints в `frontend/services/` под новые бекенд endpoints:

#### services/ecommerce.js - добавить недостающие endpoints:
```javascript
// Добавить методы для работы с новыми API
async getProducts(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/ecommerce/products?${params}`);
}

async createProduct(productData) {
    return this.api.post('/api/ecommerce/products', productData);
}

async updateProduct(productId, productData) {
    return this.api.put(`/api/ecommerce/products/${productId}`, productData);
}

async deleteProduct(productId) {
    return this.api.delete(`/api/ecommerce/products/${productId}`);
}

async getCart() {
    return this.api.get('/api/ecommerce/cart');
}

async addToCart(productId, quantity) {
    return this.api.post('/api/ecommerce/cart/items', { product_id: productId, quantity });
}

async updateCartItem(itemId, quantity) {
    return this.api.put(`/api/ecommerce/cart/items/${itemId}`, { quantity });
}

async removeFromCart(itemId) {
    return this.api.delete(`/api/ecommerce/cart/items/${itemId}`);
}

async clearCart() {
    return this.api.delete('/api/ecommerce/cart');
}

async createOrder(orderData) {
    return this.api.post('/api/ecommerce/orders', orderData);
}

async getOrders(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/ecommerce/orders?${params}`);
}
```

#### services/social.js - добавить недостающие endpoints:
```javascript
async getPosts(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/social/posts?${params}`);
}

async createPost(postData) {
    return this.api.post('/api/social/posts', postData);
}

async updatePost(postId, postData) {
    return this.api.put(`/api/social/posts/${postId}`, postData);
}

async deletePost(postId) {
    return this.api.delete(`/api/social/posts/${postId}`);
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

async createComment(postId, commentData) {
    return this.api.post(`/api/social/posts/${postId}/comments`, commentData);
}

async followUser(userId) {
    return this.api.post(`/api/social/users/${userId}/follow`);
}

async unfollowUser(userId) {
    return this.api.delete(`/api/social/users/${userId}/follow`);
}
```

#### services/tasks.js - добавить недостающие endpoints:
```javascript
async getBoards(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/tasks/boards?${params}`);
}

async createBoard(boardData) {
    return this.api.post('/api/tasks/boards', boardData);
}

async updateBoard(boardId, boardData) {
    return this.api.put(`/api/tasks/boards/${boardId}`, boardData);
}

async deleteBoard(boardId) {
    return this.api.delete(`/api/tasks/boards/${boardId}`);
}

async getCards(boardId, filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/tasks/boards/${boardId}/cards?${params}`);
}

async createCard(boardId, cardData) {
    return this.api.post(`/api/tasks/boards/${boardId}/cards`, cardData);
}

async updateCard(cardId, cardData) {
    return this.api.put(`/api/tasks/cards/${cardId}`, cardData);
}

async deleteCard(cardId) {
    return this.api.delete(`/api/tasks/cards/${cardId}`);
}

async moveCard(cardId, newBoardId, newPosition) {
    return this.api.put(`/api/tasks/cards/${cardId}/move`, { 
        board_id: newBoardId, 
        position: newPosition 
    });
}
```

#### services/content.js - добавить недостающие endpoints:
```javascript
async getArticles(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/content/articles?${params}`);
}

async createArticle(articleData) {
    return this.api.post('/api/content/articles', articleData);
}

async updateArticle(articleId, articleData) {
    return this.api.put(`/api/content/articles/${articleId}`, articleData);
}

async deleteArticle(articleId) {
    return this.api.delete(`/api/content/articles/${articleId}`);
}

async getCategories() {
    return this.api.get('/api/content/categories');
}

async createCategory(categoryData) {
    return this.api.post('/api/content/categories', categoryData);
}

async uploadMedia(formData) {
    return this.api.upload('/api/content/media', formData);
}

async getMediaFiles(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/content/media?${params}`);
}
```

#### services/analytics.js - добавить недостающие endpoints:
```javascript
async getDashboard() {
    return this.api.get('/api/analytics/dashboard');
}

async getReports(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/analytics/reports?${params}`);
}

async createReport(reportData) {
    return this.api.post('/api/analytics/reports', reportData);
}

async getMetrics(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.api.get(`/api/analytics/metrics?${params}`);
}
```

### 3. Обновить модальные окна под новые схемы
**Время: 1 час**

Нужно обновить формы в модальных окнах под новые Pydantic схемы:

#### components/forms.js - обновить формы:
```javascript
// Форма создания товара
createProductForm(productData = {}) {
    return `
        <form id="product-form" class="form">
            <div class="form-group">
                <label for="product-name">Название *</label>
                <input type="text" id="product-name" name="name" value="${productData.name || ''}" required>
            </div>
            
            <div class="form-group">
                <label for="product-description">Описание</label>
                <textarea id="product-description" name="description">${productData.description || ''}</textarea>
            </div>
            
            <div class="form-group">
                <label for="product-price">Цена *</label>
                <input type="number" id="product-price" name="price" step="0.01" min="0" value="${productData.price || ''}" required>
            </div>
            
            <div class="form-group">
                <label for="product-category">Категория</label>
                <input type="text" id="product-category" name="category" value="${productData.category || ''}">
            </div>
            
            <div class="form-group">
                <label for="product-stock">Количество на складе *</label>
                <input type="number" id="product-stock" name="stock_quantity" min="0" value="${productData.stock_quantity || 0}" required>
            </div>
            
            <div class="form-group">
                <label for="product-image">URL изображения</label>
                <input type="url" id="product-image" name="image_url" value="${productData.image_url || ''}">
            </div>
            
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="ModalService.close()">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
            </div>
        </form>
    `;
}

// Форма создания поста
createPostForm(postData = {}) {
    return `
        <form id="post-form" class="form">
            <div class="form-group">
                <label for="post-content">Содержимое поста *</label>
                <textarea id="post-content" name="content" rows="4" required>${postData.content || ''}</textarea>
            </div>
            
            <div class="form-group">
                <label for="post-image">URL изображения</label>
                <input type="url" id="post-image" name="image_url" value="${postData.image_url || ''}">
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_public" ${postData.is_public ? 'checked' : ''}>
                    Публичный пост
                </label>
            </div>
            
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="ModalService.close()">Отмена</button>
                <button type="submit" class="btn btn-primary">Опубликовать</button>
            </div>
        </form>
    `;
}

// Форма создания доски
createBoardForm(boardData = {}) {
    return `
        <form id="board-form" class="form">
            <div class="form-group">
                <label for="board-name">Название доски *</label>
                <input type="text" id="board-name" name="name" value="${boardData.name || ''}" required>
            </div>
            
            <div class="form-group">
                <label for="board-description">Описание</label>
                <textarea id="board-description" name="description">${boardData.description || ''}</textarea>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_public" ${boardData.is_public ? 'checked' : ''}>
                    Публичная доска
                </label>
            </div>
            
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="ModalService.close()">Отмена</button>
                <button type="submit" class="btn btn-primary">Создать</button>
            </div>
        </form>
    `;
}
```

### 4. Обновить обработчики событий
**Время: 30 минут**

Нужно обновить обработчики форм в `pages/` модулях:

#### pages/ecommerce.js - обновить обработчики:
```javascript
// В EcommerceModule
async handleCreateProduct(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const productData = Object.fromEntries(formData.entries());
    
    // Конвертируем типы данных
    productData.price = parseFloat(productData.price);
    productData.stock_quantity = parseInt(productData.stock_quantity);
    
    try {
        this.showLoading();
        const product = await EcommerceService.createProduct(productData);
        this.showSuccess('Товар успешно создан');
        this.loadProducts();
        ModalService.close();
    } catch (error) {
        this.showError('Ошибка создания товара: ' + error.message);
    } finally {
        this.hideLoading();
    }
}

async handleAddToCart(productId, quantity = 1) {
    try {
        this.showLoading();
        await EcommerceService.addToCart(productId, quantity);
        this.showSuccess('Товар добавлен в корзину');
        this.loadCart();
    } catch (error) {
        this.showError('Ошибка добавления в корзину: ' + error.message);
    } finally {
        this.hideLoading();
    }
}
```

## 🎯 Приоритеты на следующие 2 часа

1. **Исправить index.html** (5 мин) ✅
2. **Обновить API endpoints** (30 мин) ✅
3. **Обновить модальные формы** (30 мин) ✅
4. **Обновить обработчики событий** (30 мин) ✅
5. **Протестировать основные функции** (25 мин)

## 🧪 Быстрое тестирование

После внесения изменений протестировать:

- [ ] Загрузка главной страницы (http://localhost:3000)
- [ ] **Создать тестового пользователя** (после перезапуска контейнеров база очищается!)
- [ ] Регистрация пользователя
- [ ] Вход в систему
- [ ] Переход между модулями
- [ ] Создание товара в E-commerce
- [ ] Создание поста в Social
- [ ] Создание доски в Tasks

### ⚠️ Важные моменты для тестирования:

1. **База данных очищается** при перезапуске контейнеров
2. **Проверить все редиректы** после переименования файлов
3. **Проверить все импорты** в JS файлах
4. **Убедиться в корректности ссылок** в HTML

## 📝 Следующие шаги

После быстрого старта перейти к:
1. **Phase 1: Core Infrastructure** (детальный план)
2. **Phase 2: E-commerce Module** 
3. **Phase 3: Social Network Module**

**Общее время быстрого старта: 2 часа 10 минут**
**Результат: Работающий фронтенд с базовой функциональностью**
