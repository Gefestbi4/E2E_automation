// E-commerce page module
class EcommerceModule {
    constructor() {
        this.ecommerceService = new EcommerceService();
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('Initializing E-commerce module...');

        try {
            await this.loadProducts();
            this.bindEvents();
            this.isInitialized = true;
            console.log('E-commerce module initialized successfully');
        } catch (error) {
            console.error('Failed to initialize E-commerce module:', error);
            throw error;
        }
    }

    async loadProducts() {
        try {
            // Mock data for demo
            const products = [
                {
                    id: 1,
                    name: 'Demo Product 1',
                    price: 99.99,
                    description: 'Описание товара 1',
                    image: typeof AvatarUtils !== 'undefined' ? AvatarUtils.getDefaultAvatar() : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K',
                    category: 'Electronics'
                },
                {
                    id: 2,
                    name: 'Demo Product 2',
                    price: 149.99,
                    description: 'Описание товара 2',
                    image: typeof AvatarUtils !== 'undefined' ? AvatarUtils.getDefaultAvatar() : 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNFNUU3RUIiLz4KPGNpcmNsZSBjeD0iMzIiIGN5PSIyNCIgcj0iMTAiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTE2IDQ4QzE2IDQwIDIyIDM0IDMyIDM0QzQyIDM0IDQ4IDQwIDQ4IDQ4VjUySDE2VjQ4WiIgZmlsbD0iIzlDQTNBRiIvPgo8L3N2Zz4K',
                    category: 'Clothing'
                }
            ];

            this.renderProducts(products);
        } catch (error) {
            console.error('Failed to load products:', error);
            this.renderError('Failed to load products');
        }
    }

    renderProducts(products) {
        const ecommerceElement = document.getElementById('ecommerce-page');
        if (!ecommerceElement) return;

        ecommerceElement.innerHTML = `
            <div class="page-header">
                <h1>E-commerce</h1>
                <p>Интернет-магазин с полным функционалом</p>
            </div>

            <div class="ecommerce-content">
                <div class="products-section">
                    <div class="section-header">
                        <h2>Товары</h2>
                        <button class="btn btn-primary" id="add-product-btn">Добавить товар</button>
                    </div>
                    
                    <div class="products-grid">
                        ${products.map(product => `
                            <div class="product-card" data-product-id="${product.id}">
                                <div class="product-image">
                                    <img src="${product.image}" alt="${product.name}">
                                </div>
                                <div class="product-info">
                                    <h3 class="product-name">${product.name}</h3>
                                    <p class="product-description">${product.description}</p>
                                    <div class="product-meta">
                                        <span class="product-category">${product.category}</span>
                                        <span class="product-price">$${product.price}</span>
                                    </div>
                                    <div class="product-actions">
                                        <button class="btn btn-secondary btn-sm" onclick="this.addToCart(${product.id})">В корзину</button>
                                        <button class="btn btn-primary btn-sm" onclick="this.viewProduct(${product.id})">Подробнее</button>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="cart-section">
                    <h2>Корзина</h2>
                    <div class="cart-items" id="cart-items">
                        <p class="empty-cart">Корзина пуста</p>
                    </div>
                    <div class="cart-summary" id="cart-summary" style="display: none;">
                        <div class="cart-total">
                            <strong>Итого: $<span id="cart-total">0.00</span></strong>
                        </div>
                        <button class="btn btn-primary" id="checkout-btn">Оформить заказ</button>
                    </div>
                </div>
            </div>
        `;
    }

    renderError(message) {
        const ecommerceElement = document.getElementById('ecommerce-page');
        if (!ecommerceElement) return;

        ecommerceElement.innerHTML = `
            <div class="page-header">
                <h1>E-commerce</h1>
                <p>Интернет-магазин с полным функционалом</p>
            </div>
            <div class="error-message">
                <p>${message}</p>
                <button class="btn btn-primary" onclick="window.App.modules.ecommerce.loadProducts()">Попробовать снова</button>
            </div>
        `;
    }

    bindEvents() {
        // Add product button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'add-product-btn') {
                this.showAddProductModal();
            }
        });
    }

    showAddProductModal() {
        // Placeholder for add product modal
        Toast.info('Функция добавления товара будет реализована в следующих версиях');
    }

    onPageShow() {
        console.log('E-commerce page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.EcommerceModule = EcommerceModule;
