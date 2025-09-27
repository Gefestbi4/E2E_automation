// E-commerce service
class EcommerceService {
    constructor() {
        this.api = new ApiService();
    }

    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.api.get(`/api/ecommerce/products?${queryString}`);
    }

    async getProduct(id) {
        return this.api.get(`/api/ecommerce/products/${id}`);
    }

    async getCategories() {
        return this.api.get('/api/ecommerce/categories');
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

// Export for global access
window.EcommerceService = EcommerceService;
