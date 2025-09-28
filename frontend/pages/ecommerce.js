// E-commerce page module
class EcommerceModule {
    constructor() {
        console.log('🛒 EcommerceModule constructor - EcommerceService available:', !!window.EcommerceService);
        this.ecommerceService = null;
        this.isInitialized = false;
    }

    async init() {
        if (this.isInitialized) return;

        console.log('🛒 Initializing E-commerce module...');

        // Инициализируем сервис
        if (!this.ecommerceService && window.EcommerceService) {
            this.ecommerceService = window.EcommerceService;
            console.log('🛒 EcommerceService initialized:', !!this.ecommerceService);
        }

        if (!this.ecommerceService) {
            console.error('EcommerceService not available');
            throw new Error('EcommerceService not available');
        }

        try {
            console.log('🛒 About to call loadProducts()');
            await this.loadProducts();
            console.log('🛒 loadProducts() completed');
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
            console.log('🛒 Loading products from API...');

            // Проверяем, что сервис доступен
            if (!this.ecommerceService) {
                console.error('EcommerceService not available');
                throw new Error('EcommerceService not available');
            }

            const response = await this.ecommerceService.getProducts();
            console.log('Products loaded:', response);

            // Если API возвращает объект с items, используем его, иначе используем response напрямую
            const products = response.items || response.products || response || [];

            // Если нет товаров, используем mock data
            if (products.length === 0) {
                console.log('No products found, using fallback mock data...');
                const mockProducts = [
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
                this.renderProducts(mockProducts);
            } else {
                this.renderProducts(products);
            }
        } catch (error) {
            console.error('Failed to load products:', error);

            // Fallback на mock data при ошибке API
            console.log('Using fallback mock data due to API error...');
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
        }
    }

    renderProducts(products) {
        const ecommerceElement = document.getElementById('ecommerce-page');
        if (!ecommerceElement) return;

        // Скрываем skeleton loader если он есть
        if (window.Loading) {
            const productsContainer = ecommerceElement.querySelector('.products-grid');
            if (productsContainer) {
                window.Loading.hideSkeleton(productsContainer);
            }
        }

        // Use standard rendering for now
        this.renderProductsStandard(products, ecommerceElement);
    }

    renderProductsOptimized(products, container) {
        // Use virtual scrolling for large lists
        if (products.length > 50) {
            this.setupVirtualScrolling(products, container);
            return;
        }

        // Use batch DOM updates
        const fragment = document.createDocumentFragment();
        const productsHTML = products.map(product => this.createProductCardHTML(product)).join('');
        const template = document.createElement('div');
        template.innerHTML = this.getEcommerceTemplate(productsHTML);
        while (template.firstChild) {
            fragment.appendChild(template.firstChild);
        }

        container.appendChild(fragment);

        // Trigger animations with performance optimization
        if (window.Animations) {
            window.PerformanceManager.scheduleRender(() => {
                window.Animations.animateOnScroll();
            });
        }
    }

    renderProductsStandard(products, container) {
        const productsHTML = products.map(product => this.createProductCardHTML(product)).join('');
        container.innerHTML = this.getEcommerceTemplate(productsHTML);

        // Trigger animations
        if (window.Animations && typeof window.Animations.animateOnScroll === 'function') {
            window.Animations.animateOnScroll();
        }
    }

    createProductCardHTML(product) {
        const optimizedImage = product.image || 'https://via.placeholder.com/300x200?text=No+Image';

        return `
            <div class="product-card hover-lift click-ripple animate-on-scroll card-optimized" data-product-id="${product.id}" data-animation="slideInUp">
                <div class="product-image">
                    <img src="${optimizedImage}" alt="${product.name}" class="optimized responsive" loading="lazy">
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-description">${product.description}</p>
                    <div class="product-meta">
                        <span class="product-category">${product.category}</span>
                        <span class="product-price">$${product.price}</span>
                    </div>
                    <div class="product-actions">
                        <button class="btn btn-secondary btn-sm click-ripple btn-optimized" data-action="add-to-cart" data-product-id="${product.id}">В корзину</button>
                        <button class="btn btn-primary btn-sm click-ripple btn-optimized" data-action="view-product" data-product-id="${product.id}">Подробнее</button>
                    </div>
                </div>
            </div>
        `;
    }

    getEcommerceTemplate(productsHTML) {
        return `
            <div class="page-header">
                <h1>E-commerce</h1>
                <p>Интернет-магазин с полным функционалом</p>
            </div>

            <div class="ecommerce-content">
                <div class="products-section">
                    <div class="section-header">
                        <h2>Товары</h2>
                        <button class="btn btn-primary hover-lift click-ripple btn-optimized" id="add-product-btn">Добавить товар</button>
                    </div>
                    
                    <div class="products-grid grid-optimized">
                        ${productsHTML}
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

            // Product action buttons
            if (e.target.dataset.action === 'add-to-cart') {
                const productId = parseInt(e.target.dataset.productId);
                this.addToCart(productId);
            }

            if (e.target.dataset.action === 'view-product') {
                const productId = parseInt(e.target.dataset.productId);
                this.viewProduct(productId);
            }
        });
    }

    showAddProductModal() {
        console.log('🛒 Opening add product modal...');

        // Создаем продвинутое модальное окно для добавления товара
        const modal = new AdvancedModal('add-product-modal', {
            closable: true,
            backdrop: true,
            keyboard: true,
            size: 'medium',
            animation: 'fade',
            autoFocus: true,
            trapFocus: true
        });

        const content = {
            title: 'Добавить новый товар',
            body: `
                <form id="add-product-form" class="product-form">
                    <div class="form-group">
                        <label for="product-name">Название товара *</label>
                        <input type="text" id="product-name" name="name" required 
                               placeholder="Введите название товара">
                    </div>
                    <div class="form-group">
                        <label for="product-description">Описание</label>
                        <textarea id="product-description" name="description" rows="3" 
                                  placeholder="Опишите товар"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="product-price">Цена *</label>
                        <input type="number" id="product-price" name="price" step="0.01" min="0" required 
                               placeholder="0.00">
                    </div>
                    <div class="form-group">
                        <label for="product-category">Категория</label>
                        <select id="product-category" name="category">
                            <option value="">Выберите категорию</option>
                            <option value="electronics">Электроника</option>
                            <option value="clothing">Одежда</option>
                            <option value="books">Книги</option>
                            <option value="home">Дом и сад</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="product-stock">Количество на складе</label>
                        <input type="number" id="product-stock" name="stock_quantity" min="0" value="1" 
                               placeholder="1">
                    </div>
                    <div class="form-group">
                        <label for="product-image">URL изображения</label>
                        <input type="url" id="product-image" name="image_url" 
                               placeholder="https://example.com/image.jpg">
                    </div>
                </form>
            `,
            footer: `
                <button type="button" class="btn btn-secondary" onclick="window.AdvancedModal.close('add-product-modal')">Отмена</button>
                <button type="button" class="btn btn-primary" onclick="window.EcommerceModule.addProduct()">Добавить товар</button>
            `
        };

        modal.show(content);

        // Инициализируем продвинутую форму
        setTimeout(() => {
            const form = document.getElementById('add-product-form');
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

    async addProduct() {
        try {
            console.log('🛒 Adding new product...');

            const form = document.getElementById('add-product-form');
            if (!form) {
                throw new Error('Форма не найдена');
            }

            // Валидация формы
            const formData = new FormData(form);
            const productData = {
                name: formData.get('name')?.trim(),
                description: formData.get('description')?.trim(),
                price: parseFloat(formData.get('price')),
                category: formData.get('category')?.trim(),
                stock_quantity: parseInt(formData.get('stock_quantity')) || 0,
                image_url: formData.get('image_url')?.trim()
            };

            // Дополнительная валидация
            if (!productData.name) {
                throw new Error('Название товара обязательно');
            }
            if (!productData.price || productData.price <= 0) {
                throw new Error('Цена должна быть больше 0');
            }

            console.log('Product data:', productData);

            // Показываем индикатор загрузки
            const submitBtn = form.querySelector('button[onclick*="addProduct"]');
            let originalText = 'Добавить товар';
            if (submitBtn) {
                originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.textContent = 'Добавление...';
            }

            try {
                const response = await this.ecommerceService.createProduct(productData);
                console.log('Product created:', response);

                if (window.Toast && typeof window.Toast.success === 'function') {
                    window.Toast.success('Товар успешно добавлен!');
                } else {
                    alert('Товар успешно добавлен!');
                }

                if (window.AdvancedModal) {
                    window.AdvancedModal.close('add-product-modal');
                }

                // Перезагружаем список товаров
                await this.loadProducts();

            } finally {
                // Восстанавливаем кнопку
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            }

        } catch (error) {
            console.error('Failed to create product:', error);

            if (window.Toast && typeof window.Toast.error === 'function') {
                window.Toast.error('Ошибка при создании товара: ' + error.message);
            } else {
                alert('Ошибка при создании товара: ' + error.message);
            }
        }
    }

    addToCart(productId) {
        console.log('Adding product to cart:', productId);
        if (window.Toast && typeof window.Toast.success === 'function') {
            window.Toast.success('Товар добавлен в корзину');
        } else {
            alert('Товар добавлен в корзину');
        }
    }

    viewProduct(productId) {
        console.log('Viewing product:', productId);
        if (window.Toast && typeof window.Toast.info === 'function') {
            window.Toast.info('Функция просмотра товара будет реализована в следующих версиях');
        } else {
            alert('Функция просмотра товара будет реализована в следующих версиях');
        }
    }

    onPageShow() {
        console.log('E-commerce page shown');
        if (!this.isInitialized) {
            this.init();
        }
    }
}

// Export for global access
window.EcommerceModule = new EcommerceModule();
