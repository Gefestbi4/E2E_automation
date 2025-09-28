// E-commerce service
class EcommerceService {
    constructor() {
        console.log('🛒 EcommerceService constructor - window.ApiService before assignment:', typeof window.ApiService);
        this.api = window.ApiService;
        console.log('🛒 EcommerceService constructor - API available:', !!this.api);
        console.log('🛒 EcommerceService constructor - API type:', typeof this.api);
        console.log('🛒 EcommerceService constructor - API methods:', this.api ? Object.getOwnPropertyNames(Object.getPrototypeOf(this.api)) : 'null');
    }

    async initApi() {
        // Ждем инициализации ApiService
        while (!window.ApiService) {
            await new Promise(resolve => setTimeout(resolve, 10));
        }
        this.api = window.ApiService;
        console.log('🛒 EcommerceService: ApiService initialized');
    }

    async getProducts(params = {}) {
        console.log('🛒 EcommerceService.getProducts called with params:', params);
        console.log('🛒 API available:', !!this.api);
        console.log('🛒 API type:', typeof this.api);
        console.log('🛒 API methods:', this.api ? Object.getOwnPropertyNames(Object.getPrototypeOf(this.api)) : 'null');

        const queryString = new URLSearchParams(params).toString();
        console.log('🛒 Query string:', queryString);
        const url = `/api/ecommerce/products?${queryString}`;
        console.log('🛒 Full URL:', url);
        return this.api.get(url);
    }

    async getProduct(id) {
        return this.api.get(`/api/ecommerce/products/${id}`);
    }

    async getCategories() {
        return this.api.get('/api/ecommerce/categories');
    }

    async createProduct(productData) {
        // Ждем инициализации API
        if (!this.api) {
            await this.initApi();
        }
        return this.api.post('/api/ecommerce/products', productData);
    }

    async addToCart(productId, quantity = 1) {
        return this.api.post('/api/ecommerce/cart/items', {
            product_id: productId,
            quantity: quantity
        });
    }

    async getCart() {
        return this.api.get('/api/ecommerce/cart');
    }

    async updateCartItem(itemId, quantity) {
        return this.api.put(`/api/ecommerce/cart/items/${itemId}`, {
            quantity: quantity
        });
    }

    async removeFromCart(itemId) {
        return this.api.delete(`/api/ecommerce/cart/items/${itemId}`);
    }

    async createOrder(orderData) {
        return this.api.post('/api/ecommerce/orders', orderData);
    }

    async getOrders() {
        return this.api.get('/api/ecommerce/orders');
    }

    async getOrder(id) {
        return this.api.get(`/api/ecommerce/orders/${id}`);
    }

    async addReview(productId, reviewData) {
        return this.api.post(`/api/ecommerce/products/${productId}/reviews`, reviewData);
    }

    async getReviews(productId) {
        return this.api.get(`/api/ecommerce/products/${productId}/reviews`);
    }
}

// Создаем экземпляр и экспортируем для глобального доступа
window.EcommerceService = new EcommerceService();
