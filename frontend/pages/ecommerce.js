// E-commerce page module
class EcommerceModule {
    constructor() {
        this.products = [];
        this.cart = [];
        this.categories = [];
        this.currentFilters = {};
        this.isInitialized = false;
        this.init();
    }

    async init() {
        if (this.isInitialized) return;

        try {
            await this.loadProducts();
            await this.loadCart();
            await this.loadCategories();
            this.renderPage();
            this.setupEventListeners();
            this.isInitialized = true;
        } catch (error) {
            console.error('Failed to initialize E-commerce module:', error);
            this.showError('Не удалось инициализировать модуль E-commerce');
        }
    }

    async loadProducts() {
        try {
            const products = await window.ApiService.getProducts(this.currentFilters);
            this.products = products;
        } catch (error) {
            console.error('Failed to load products:', error);
            this.products = this.getMockProducts();
        }
    }

    async loadCart() {
        try {
            const cart = await window.ApiService.getCart();
            this.cart = cart;
        } catch (error) {
            console.error('Failed to load cart:', error);
            this.cart = [];
        }
    }

    async loadCategories() {
        try {
            this.categories = [
                { id: 'electronics', name: 'Электроника' },
                { id: 'clothing', name: 'Одежда' },
                { id: 'books', name: 'Книги' },
                { id: 'home', name: 'Дом и сад' },
                { id: 'sports', name: 'Спорт' }
            ];
        } catch (error) {
            console.error('Failed to load categories:', error);
            this.categories = [];
        }
    }

    getMockProducts() {
        return [
            {
                id: 1,
                name: 'Смартфон iPhone 15',
                description: 'Новейший смартфон с продвинутой камерой',
                price: 999.99,
                category: 'electronics',
                image: '/default-avatar.png',
                stock: 10,
                rating: 4.8,
                reviews: 256
            },
            {
                id: 2,
                name: 'Ноутбук MacBook Pro',
                description: 'Мощный ноутбук для профессионалов',
                price: 2499.99,
                category: 'electronics',
                image: '/default-avatar.png',
                stock: 5,
                rating: 4.9,
                reviews: 128
            },
            {
                id: 3,
                name: 'Футболка Nike',
                description: 'Удобная спортивная футболка',
                price: 29.99,
                category: 'clothing',
                image: '/default-avatar.png',
                stock: 50,
                rating: 4.5,
                reviews: 89
            },
            {
                id: 4,
                name: 'Книга "JavaScript для начинающих"',
                description: 'Полное руководство по изучению JavaScript',
                price: 39.99,
                category: 'books',
                image: '/default-avatar.png',
                stock: 25,
                rating: 4.7,
                reviews: 156
            }
        ];
    }

    renderPage() {
        const container = document.getElementById('ecommerce-container');
        if (!container) return;

        container.innerHTML = `
            <div class="ecommerce-header">
                <h1>Интернет-магазин</h1>
                <div class="ecommerce-actions">
                    <button class="btn btn-primary" onclick="ecommerceModule.showAddProductModal()">
                        Добавить товар
                    </button>
                    <div class="cart-icon" onclick="ecommerceModule.showCart()">
                        🛒 <span class="cart-count">${this.cart.length}</span>
                    </div>
                </div>
            </div>

            <div class="ecommerce-content">
                <div class="filters-sidebar">
                    <h3>Фильтры</h3>
                    
                    <div class="filter-group">
                        <label>Категория</label>
                        <select id="categoryFilter" class="form-control">
                            <option value="">Все категории</option>
                            ${this.categories.map(cat =>
            `<option value="${cat.id}">${cat.name}</option>`
        ).join('')}
                        </select>
                    </div>

                    <div class="filter-group">
                        <label>Цена</label>
                        <div class="price-range">
                            <input type="range" id="priceMin" min="0" max="1000" value="0" class="form-control">
                            <input type="range" id="priceMax" min="0" max="1000" value="1000" class="form-control">
                            <div class="price-display">
                                $<span id="priceMinValue">0</span> - $<span id="priceMaxValue">1000</span>
                            </div>
                        </div>
                    </div>

                    <div class="filter-group">
                        <label>Рейтинг</label>
                        <select id="ratingFilter" class="form-control">
                            <option value="">Любой рейтинг</option>
                            <option value="4">4+ звезды</option>
                            <option value="3">3+ звезды</option>
                            <option value="2">2+ звезды</option>
                        </select>
                    </div>

                    <div class="filter-group">
                        <label>Наличие</label>
                        <label class="checkbox-label">
                            <input type="checkbox" id="inStockOnly">
                            Только в наличии
                        </label>
                    </div>

                    <button class="btn btn-secondary" onclick="ecommerceModule.clearFilters()">
                        Очистить фильтры
                    </button>
                </div>

                <div class="products-section">
                    <div class="products-header">
                        <h2>Товары (${this.products.length})</h2>
                        <div class="sort-controls">
                            <label>Сортировка:</label>
                            <select id="sortBy" class="form-control">
                                <option value="name">По названию</option>
                                <option value="price-asc">Цена: по возрастанию</option>
                                <option value="price-desc">Цена: по убыванию</option>
                                <option value="rating">По рейтингу</option>
                                <option value="reviews">По количеству отзывов</option>
                            </select>
                        </div>
                    </div>

                    <div class="products-grid">
                        ${this.products.map(product => this.renderProduct(product)).join('')}
                    </div>
                </div>
            </div>

            <div class="cart-section" id="cartSection" style="display: none;">
                <h2>Корзина</h2>
                <div class="cart-items" id="cartItems">
                    ${this.renderCartItems()}
                </div>
                <div class="cart-summary">
                    <div class="cart-total">
                        <strong>Итого: $<span id="cartTotal">${this.calculateCartTotal()}</span></strong>
                    </div>
                    <div class="cart-actions">
                        <button class="btn btn-secondary" onclick="ecommerceModule.clearCart()">
                            Очистить корзину
                        </button>
                        <button class="btn btn-primary" onclick="ecommerceModule.checkout()">
                            Оформить заказ
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.setupFilterListeners();
    }

    renderProduct(product) {
        const isInCart = this.cart.some(item => item.productId === product.id);

        return `
            <div class="product-card" data-product-id="${product.id}">
                <div class="product-image">
                    <img src="${product.image}" alt="${product.name}" loading="lazy">
                    ${product.stock === 0 ? '<div class="out-of-stock">Нет в наличии</div>' : ''}
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-description">${product.description}</p>
                    
                    <div class="product-rating">
                        ${this.renderStars(product.rating)}
                        <span class="rating-text">${product.rating} (${product.reviews} отзывов)</span>
                    </div>

                    <div class="product-meta">
                        <span class="product-category">${this.getCategoryName(product.category)}</span>
                        <span class="product-stock">В наличии: ${product.stock}</span>
                    </div>

                    <div class="product-price">
                        <span class="price">$${product.price}</span>
                    </div>

                    <div class="product-actions">
                        ${product.stock > 0 ? `
                            <button class="btn btn-primary ${isInCart ? 'btn-secondary' : ''}" 
                                    onclick="ecommerceModule.toggleCart(${product.id})"
                                    ${isInCart ? 'disabled' : ''}>
                                ${isInCart ? 'В корзине' : 'В корзину'}
                            </button>
                        ` : `
                            <button class="btn btn-secondary" disabled>
                                Нет в наличии
                            </button>
                        `}
                        <button class="btn btn-outline" onclick="ecommerceModule.viewProduct(${product.id})">
                            Подробнее
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    renderStars(rating) {
        const stars = Math.floor(rating);
        const hasHalf = rating % 1 !== 0;
        let starsHTML = '';

        for (let i = 1; i <= 5; i++) {
            if (i <= stars) {
                starsHTML += '<span class="star filled">★</span>';
            } else if (i === stars + 1 && hasHalf) {
                starsHTML += '<span class="star half">★</span>';
            } else {
                starsHTML += '<span class="star">☆</span>';
            }
        }

        return `<div class="stars">${starsHTML}</div>`;
    }

    renderCartItems() {
        if (this.cart.length === 0) {
            return '<p class="empty-cart">Корзина пуста</p>';
        }

        return this.cart.map(item => {
            const product = this.products.find(p => p.id === item.productId);
            if (!product) return '';

            return `
                <div class="cart-item" data-item-id="${item.id}">
                    <div class="cart-item-image">
                        <img src="${product.image}" alt="${product.name}">
                    </div>
                    <div class="cart-item-info">
                        <h4>${product.name}</h4>
                        <p>$${product.price} за штуку</p>
                    </div>
                    <div class="cart-item-quantity">
                        <button class="btn btn-sm" onclick="ecommerceModule.updateCartQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="btn btn-sm" onclick="ecommerceModule.updateCartQuantity(${item.id}, ${item.quantity + 1})">+</button>
                    </div>
                    <div class="cart-item-total">
                        $${(product.price * item.quantity).toFixed(2)}
                    </div>
                    <div class="cart-item-actions">
                        <button class="btn btn-sm btn-danger" onclick="ecommerceModule.removeFromCart(${item.id})">
                            Удалить
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    getCategoryName(categoryId) {
        const category = this.categories.find(cat => cat.id === categoryId);
        return category ? category.name : categoryId;
    }

    calculateCartTotal() {
        return this.cart.reduce((total, item) => {
            const product = this.products.find(p => p.id === item.productId);
            return total + (product ? product.price * item.quantity : 0);
        }, 0).toFixed(2);
    }

    setupEventListeners() {
        // Global event listeners are set up in setupFilterListeners
    }

    setupFilterListeners() {
        // Category filter
        const categoryFilter = document.getElementById('categoryFilter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.currentFilters.category = e.target.value;
                this.applyFilters();
            });
        }

        // Price range filters
        const priceMin = document.getElementById('priceMin');
        const priceMax = document.getElementById('priceMax');
        const priceMinValue = document.getElementById('priceMinValue');
        const priceMaxValue = document.getElementById('priceMaxValue');

        if (priceMin && priceMax && priceMinValue && priceMaxValue) {
            const updatePriceFilter = () => {
                this.currentFilters.priceMin = parseFloat(priceMin.value);
                this.currentFilters.priceMax = parseFloat(priceMax.value);
                priceMinValue.textContent = priceMin.value;
                priceMaxValue.textContent = priceMax.value;
                this.applyFilters();
            };

            priceMin.addEventListener('input', updatePriceFilter);
            priceMax.addEventListener('input', updatePriceFilter);
        }

        // Rating filter
        const ratingFilter = document.getElementById('ratingFilter');
        if (ratingFilter) {
            ratingFilter.addEventListener('change', (e) => {
                this.currentFilters.minRating = e.target.value;
                this.applyFilters();
            });
        }

        // Stock filter
        const inStockOnly = document.getElementById('inStockOnly');
        if (inStockOnly) {
            inStockOnly.addEventListener('change', (e) => {
                this.currentFilters.inStock = e.target.checked;
                this.applyFilters();
            });
        }

        // Sort filter
        const sortBy = document.getElementById('sortBy');
        if (sortBy) {
            sortBy.addEventListener('change', (e) => {
                this.currentFilters.sortBy = e.target.value;
                this.applyFilters();
            });
        }
    }

    applyFilters() {
        let filteredProducts = [...this.products];

        // Category filter
        if (this.currentFilters.category) {
            filteredProducts = filteredProducts.filter(p => p.category === this.currentFilters.category);
        }

        // Price filter
        if (this.currentFilters.priceMin !== undefined) {
            filteredProducts = filteredProducts.filter(p => p.price >= this.currentFilters.priceMin);
        }
        if (this.currentFilters.priceMax !== undefined) {
            filteredProducts = filteredProducts.filter(p => p.price <= this.currentFilters.priceMax);
        }

        // Rating filter
        if (this.currentFilters.minRating) {
            filteredProducts = filteredProducts.filter(p => p.rating >= parseFloat(this.currentFilters.minRating));
        }

        // Stock filter
        if (this.currentFilters.inStock) {
            filteredProducts = filteredProducts.filter(p => p.stock > 0);
        }

        // Sort
        if (this.currentFilters.sortBy) {
            filteredProducts = this.sortProducts(filteredProducts, this.currentFilters.sortBy);
        }

        // Re-render products
        const productsGrid = document.querySelector('.products-grid');
        if (productsGrid) {
            productsGrid.innerHTML = filteredProducts.map(product => this.renderProduct(product)).join('');
        }

        // Update products count
        const productsHeader = document.querySelector('.products-header h2');
        if (productsHeader) {
            productsHeader.textContent = `Товары (${filteredProducts.length})`;
        }
    }

    sortProducts(products, sortBy) {
        return products.sort((a, b) => {
            switch (sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'price-asc':
                    return a.price - b.price;
                case 'price-desc':
                    return b.price - a.price;
                case 'rating':
                    return b.rating - a.rating;
                case 'reviews':
                    return b.reviews - a.reviews;
                default:
                    return 0;
            }
        });
    }

    clearFilters() {
        this.currentFilters = {};

        // Reset form elements
        const categoryFilter = document.getElementById('categoryFilter');
        if (categoryFilter) categoryFilter.value = '';

        const priceMin = document.getElementById('priceMin');
        const priceMax = document.getElementById('priceMax');
        if (priceMin && priceMax) {
            priceMin.value = 0;
            priceMax.value = 1000;
            document.getElementById('priceMinValue').textContent = '0';
            document.getElementById('priceMaxValue').textContent = '1000';
        }

        const ratingFilter = document.getElementById('ratingFilter');
        if (ratingFilter) ratingFilter.value = '';

        const inStockOnly = document.getElementById('inStockOnly');
        if (inStockOnly) inStockOnly.checked = false;

        const sortBy = document.getElementById('sortBy');
        if (sortBy) sortBy.value = 'name';

        this.applyFilters();
    }

    async toggleCart(productId) {
        try {
            const isInCart = this.cart.some(item => item.productId === productId);

            if (isInCart) {
                await this.removeFromCart(this.cart.find(item => item.productId === productId).id);
            } else {
                await this.addToCart(productId);
            }
        } catch (error) {
            console.error('Failed to toggle cart:', error);
            this.showError('Не удалось обновить корзину');
        }
    }

    async addToCart(productId) {
        try {
            await window.ApiService.addToCart(productId, 1);
            await this.loadCart();
            this.updateCartDisplay();
            this.showSuccess('Товар добавлен в корзину');
        } catch (error) {
            console.error('Failed to add to cart:', error);
            this.showError('Не удалось добавить товар в корзину');
        }
    }

    async removeFromCart(itemId) {
        try {
            await window.ApiService.removeFromCart(itemId);
            await this.loadCart();
            this.updateCartDisplay();
            this.showSuccess('Товар удален из корзины');
        } catch (error) {
            console.error('Failed to remove from cart:', error);
            this.showError('Не удалось удалить товар из корзины');
        }
    }

    async updateCartQuantity(itemId, newQuantity) {
        if (newQuantity <= 0) {
            await this.removeFromCart(itemId);
            return;
        }

        try {
            await window.ApiService.updateCartItem(itemId, newQuantity);
            await this.loadCart();
            this.updateCartDisplay();
        } catch (error) {
            console.error('Failed to update cart quantity:', error);
            this.showError('Не удалось обновить количество товара');
        }
    }

    async clearCart() {
        if (!confirm('Очистить корзину?')) return;

        try {
            // Remove all items from cart
            for (const item of this.cart) {
                await window.ApiService.removeFromCart(item.id);
            }
            await this.loadCart();
            this.updateCartDisplay();
            this.showSuccess('Корзина очищена');
        } catch (error) {
            console.error('Failed to clear cart:', error);
            this.showError('Не удалось очистить корзину');
        }
    }

    async checkout() {
        try {
            const orderData = {
                items: this.cart,
                total: this.calculateCartTotal(),
                shippingAddress: {
                    // Get from user profile or form
                }
            };

            await window.ApiService.checkout(orderData);
            this.showSuccess('Заказ успешно оформлен!');
            await this.clearCart();
        } catch (error) {
            console.error('Failed to checkout:', error);
            this.showError('Не удалось оформить заказ');
        }
    }

    updateCartDisplay() {
        // Update cart icon count
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = this.cart.length;
        }

        // Update cart section if visible
        const cartItems = document.getElementById('cartItems');
        if (cartItems) {
            cartItems.innerHTML = this.renderCartItems();
        }

        // Update cart total
        const cartTotal = document.getElementById('cartTotal');
        if (cartTotal) {
            cartTotal.textContent = this.calculateCartTotal();
        }

        // Re-render products to update cart button states
        this.renderPage();
    }

    showCart() {
        const cartSection = document.getElementById('cartSection');
        if (cartSection) {
            cartSection.style.display = cartSection.style.display === 'none' ? 'block' : 'none';
        }
    }

    viewProduct(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;

        // Show product details modal
        this.showProductModal(product);
    }

    showProductModal(product) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${product.name}</h3>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="product-details">
                        <div class="product-details-image">
                            <img src="${product.image}" alt="${product.name}">
                        </div>
                        <div class="product-details-info">
                            <p class="product-description">${product.description}</p>
                            <div class="product-rating">
                                ${this.renderStars(product.rating)}
                                <span>${product.rating} (${product.reviews} отзывов)</span>
                            </div>
                            <div class="product-meta">
                                <p><strong>Категория:</strong> ${this.getCategoryName(product.category)}</p>
                                <p><strong>В наличии:</strong> ${product.stock} шт.</p>
                                <p><strong>Цена:</strong> $${product.price}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="this.closest('.modal').remove()">
                        Закрыть
                    </button>
                    ${product.stock > 0 ? `
                        <button class="btn btn-primary" onclick="ecommerceModule.addToCart(${product.id}); this.closest('.modal').remove();">
                            В корзину
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showAddProductModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Добавить товар</h3>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="addProductForm">
                        <div class="form-group">
                            <label for="productName">Название товара</label>
                            <input type="text" id="productName" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label for="productDescription">Описание</label>
                            <textarea id="productDescription" class="form-control" rows="3"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="productPrice">Цена</label>
                            <input type="number" id="productPrice" class="form-control" step="0.01" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="productCategory">Категория</label>
                            <select id="productCategory" class="form-control">
                                ${this.categories.map(cat =>
            `<option value="${cat.id}">${cat.name}</option>`
        ).join('')}
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="productStock">Количество на складе</label>
                            <input type="number" id="productStock" class="form-control" min="0" value="1">
                        </div>
                        <div class="form-group">
                            <label for="productImage">URL изображения</label>
                            <input type="url" id="productImage" class="form-control">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="this.closest('.modal').remove()">
                        Отмена
                    </button>
                    <button class="btn btn-primary" onclick="ecommerceModule.createProduct(); this.closest('.modal').remove();">
                        Создать товар
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    async createProduct() {
        try {
            const productData = {
                name: document.getElementById('productName').value,
                description: document.getElementById('productDescription').value,
                price: parseFloat(document.getElementById('productPrice').value),
                category: document.getElementById('productCategory').value,
                stock: parseInt(document.getElementById('productStock').value),
                image: document.getElementById('productImage').value || '/default-avatar.png'
            };

            // Validate required fields
            if (!productData.name || !productData.price) {
                this.showError('Заполните обязательные поля');
                return;
            }

            await window.ApiService.createProduct(productData);
            await this.loadProducts();
            this.renderPage();
            this.showSuccess('Товар успешно создан');
        } catch (error) {
            console.error('Failed to create product:', error);
            this.showError('Не удалось создать товар');
        }
    }

    showSuccess(message) {
        // Simple success notification
        const notification = document.createElement('div');
        notification.className = 'notification success';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    showError(message) {
        // Simple error notification
        const notification = document.createElement('div');
        notification.className = 'notification error';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    onPageShow() {
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.EcommerceModule = EcommerceModule;
