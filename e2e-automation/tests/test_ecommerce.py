"""
E-commerce tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.ecommerce_page import EcommercePage
from pages.cart_page import CartPage
from utils.logger import TestLogger
from utils.ecommerce_testing import EcommerceTesting


@allure.feature("E-commerce Tests")
@allure.story("E-commerce Testing")
class TestEcommerce(BaseTest):
    """Test class for e-commerce testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestEcommerce")
        self.ecommerce_testing = EcommerceTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.cart_page = CartPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test e-commerce page loads correctly")
    @pytest.mark.ecommerce
    def test_ecommerce_page_loads(self):
        """Test e-commerce page loads correctly"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.ecommerce_page.get_page_title() == "E-commerce"
            ), "Page title should be correct"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test product listing")
    @pytest.mark.ecommerce
    def test_product_listing(self):
        """Test product listing"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test product grid loads"):
            assert (
                self.ecommerce_page.is_product_grid_loaded()
            ), "Product grid should load"
            assert self.ecommerce_page.get_product_count() > 0, "Should have products"

        with allure.step("Test product cards display correctly"):
            products = self.ecommerce_page.get_products()
            for product in products:
                assert self.ecommerce_page.is_product_card_complete(
                    product
                ), "Product card should be complete"
                assert (
                    self.ecommerce_page.get_product_name(product) != ""
                ), "Product name should not be empty"
                assert (
                    self.ecommerce_page.get_product_price(product) > 0
                ), "Product price should be positive"
                assert (
                    self.ecommerce_page.get_product_image(product) != ""
                ), "Product image should be present"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test product search")
    @pytest.mark.ecommerce
    def test_product_search(self):
        """Test product search"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test product search functionality"):
            search_term = "laptop"
            self.ecommerce_page.search_products(search_term)
            assert (
                self.ecommerce_page.wait_for_search_results()
            ), "Search results should load"
            assert (
                self.ecommerce_page.get_search_results_count() > 0
            ), "Should have search results"

        with allure.step("Test search results accuracy"):
            search_results = self.ecommerce_page.get_search_results()
            for product in search_results:
                assert (
                    search_term.lower() in product["name"].lower()
                ), "Search results should match search term"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test product filtering")
    @pytest.mark.ecommerce
    def test_product_filtering(self):
        """Test product filtering"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test category filtering"):
            category = "Electronics"
            self.ecommerce_page.filter_by_category(category)
            assert (
                self.ecommerce_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.ecommerce_page.get_filter_results_count() > 0
            ), "Should have filter results"

        with allure.step("Test price range filtering"):
            min_price = 100
            max_price = 500
            self.ecommerce_page.filter_by_price_range(min_price, max_price)
            assert (
                self.ecommerce_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.ecommerce_page.get_filter_results_count() > 0
            ), "Should have filter results"

        with allure.step("Test in-stock filtering"):
            self.ecommerce_page.filter_by_in_stock()
            assert (
                self.ecommerce_page.wait_for_filter_results()
            ), "Filter results should load"
            assert (
                self.ecommerce_page.get_filter_results_count() > 0
            ), "Should have filter results"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test add to cart functionality")
    @pytest.mark.ecommerce
    def test_add_to_cart(self):
        """Test add to cart functionality"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test add product to cart"):
            product = self.ecommerce_page.get_first_product()
            product_name = self.ecommerce_page.get_product_name(product)
            self.ecommerce_page.add_to_cart(product)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert self.ecommerce_page.get_cart_count() > 0, "Cart should have items"

        with allure.step("Test cart notification"):
            assert (
                self.ecommerce_page.is_cart_notification_displayed()
            ), "Cart notification should be displayed"
            assert (
                self.ecommerce_page.get_cart_notification_message()
                == f"{product_name} added to cart"
            ), "Cart notification message should be correct"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test cart management")
    @pytest.mark.ecommerce
    def test_cart_management(self):
        """Test cart management"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test add multiple products to cart"):
            products = self.ecommerce_page.get_products()[:3]  # Add first 3 products
            for product in products:
                self.ecommerce_page.add_to_cart(product)
                assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert self.ecommerce_page.get_cart_count() == 3, "Cart should have 3 items"

        with allure.step("Test update product quantity"):
            product = self.ecommerce_page.get_first_cart_item()
            self.ecommerce_page.update_cart_item_quantity(product, 2)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert (
                self.ecommerce_page.get_cart_item_quantity(product) == 2
            ), "Cart item quantity should be updated"

        with allure.step("Test remove product from cart"):
            product = self.ecommerce_page.get_first_cart_item()
            self.ecommerce_page.remove_from_cart(product)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert self.ecommerce_page.get_cart_count() == 2, "Cart should have 2 items"

        with allure.step("Test clear cart"):
            self.ecommerce_page.clear_cart()
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert self.ecommerce_page.get_cart_count() == 0, "Cart should be empty"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test checkout process")
    @pytest.mark.ecommerce
    def test_checkout_process(self):
        """Test checkout process"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test add product to cart"):
            product = self.ecommerce_page.get_first_product()
            self.ecommerce_page.add_to_cart(product)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"

        with allure.step("Test proceed to checkout"):
            self.ecommerce_page.proceed_to_checkout()
            assert (
                self.ecommerce_page.wait_for_checkout_page()
            ), "Checkout page should load"
            assert (
                self.ecommerce_page.is_checkout_form_present()
            ), "Checkout form should be present"

        with allure.step("Test fill checkout form"):
            checkout_data = self.settings.get_checkout_data()
            self.ecommerce_page.fill_checkout_form(checkout_data)
            assert (
                self.ecommerce_page.is_checkout_form_valid()
            ), "Checkout form should be valid"

        with allure.step("Test place order"):
            self.ecommerce_page.place_order()
            assert (
                self.ecommerce_page.wait_for_order_confirmation()
            ), "Order confirmation should be displayed"
            assert (
                self.ecommerce_page.get_order_number() != ""
            ), "Order number should be generated"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test product reviews")
    @pytest.mark.ecommerce
    def test_product_reviews(self):
        """Test product reviews"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test view product details"):
            product = self.ecommerce_page.get_first_product()
            self.ecommerce_page.view_product_details(product)
            assert (
                self.ecommerce_page.wait_for_product_details()
            ), "Product details should load"

        with allure.step("Test product reviews display"):
            assert (
                self.ecommerce_page.is_reviews_section_present()
            ), "Reviews section should be present"
            assert self.ecommerce_page.get_reviews_count() > 0, "Should have reviews"

        with allure.step("Test add product review"):
            review_data = self.settings.get_review_data()
            self.ecommerce_page.add_product_review(review_data)
            assert self.ecommerce_page.wait_for_review_added(), "Review should be added"
            assert self.ecommerce_page.is_review_displayed(
                review_data
            ), "Review should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test wishlist functionality")
    @pytest.mark.ecommerce
    def test_wishlist_functionality(self):
        """Test wishlist functionality"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test add product to wishlist"):
            product = self.ecommerce_page.get_first_product()
            self.ecommerce_page.add_to_wishlist(product)
            assert (
                self.ecommerce_page.wait_for_wishlist_update()
            ), "Wishlist should update"
            assert (
                self.ecommerce_page.get_wishlist_count() > 0
            ), "Wishlist should have items"

        with allure.step("Test view wishlist"):
            self.ecommerce_page.view_wishlist()
            assert (
                self.ecommerce_page.wait_for_wishlist_page()
            ), "Wishlist page should load"
            assert (
                self.ecommerce_page.get_wishlist_items_count() > 0
            ), "Wishlist should have items"

        with allure.step("Test remove product from wishlist"):
            product = self.ecommerce_page.get_first_wishlist_item()
            self.ecommerce_page.remove_from_wishlist(product)
            assert (
                self.ecommerce_page.wait_for_wishlist_update()
            ), "Wishlist should update"
            assert (
                self.ecommerce_page.get_wishlist_count() == 0
            ), "Wishlist should be empty"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test e-commerce API")
    @pytest.mark.ecommerce
    def test_ecommerce_api(self):
        """Test e-commerce API"""
        with allure.step("Test products API"):
            response = self.api_client.get("/api/ecommerce/products")
            assert response.status_code == 200, "Products API should return 200"
            assert len(response.json()) > 0, "Should have products"

        with allure.step("Test product details API"):
            response = self.api_client.get("/api/ecommerce/products/1")
            assert response.status_code == 200, "Product details API should return 200"
            assert "name" in response.json(), "Product should have name"

        with allure.step("Test cart API"):
            response = self.api_client.get("/api/ecommerce/cart")
            assert response.status_code == 200, "Cart API should return 200"
            assert "items" in response.json(), "Cart should have items"

        with allure.step("Test add to cart API"):
            response = self.api_client.post(
                "/api/ecommerce/cart/add", {"product_id": 1, "quantity": 1}
            )
            assert response.status_code == 200, "Add to cart API should return 200"
            assert "message" in response.json(), "Should return success message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test e-commerce error handling")
    @pytest.mark.ecommerce
    def test_ecommerce_error_handling(self):
        """Test e-commerce error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test error handling for invalid product"):
            self.ecommerce_page.add_to_cart("invalid_product")
            assert (
                self.ecommerce_page.wait_for_error_message()
            ), "Should show error for invalid product"
            assert (
                self.ecommerce_page.get_error_message() != ""
            ), "Error message should not be empty"

        with allure.step("Test error handling for out of stock product"):
            self.ecommerce_page.add_to_cart("out_of_stock_product")
            assert (
                self.ecommerce_page.wait_for_error_message()
            ), "Should show error for out of stock product"
            assert (
                "out of stock" in self.ecommerce_page.get_error_message().lower()
            ), "Should show out of stock error"

        with allure.step("Test error handling for invalid search"):
            self.ecommerce_page.search_products("invalid_search_term")
            assert (
                self.ecommerce_page.wait_for_no_results_message()
            ), "Should show no results message"
            assert (
                self.ecommerce_page.get_no_results_message() != ""
            ), "No results message should not be empty"

    # Shopping Cart Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing shopping cart")
    @pytest.mark.cart
    def test_view_shopping_cart(self):
        """Test viewing shopping cart"""
        with allure.step("Login and navigate to e-commerce"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

        with allure.step("Add product to cart"):
            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()
            assert self.cart_page.is_cart_loaded(), "Cart page should load correctly"

        with allure.step("Verify cart contents"):
            cart_items = self.cart_page.get_cart_items()
            assert len(cart_items) > 0, "Cart should contain items"
            assert (
                self.cart_page.get_item_name(0) == product_data["name"]
            ), "Product name should match"
            assert (
                self.cart_page.get_item_price(0) != ""
            ), "Product price should be displayed"
            assert (
                self.cart_page.get_item_quantity(0) > 0
            ), "Product quantity should be greater than 0"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test adding product to cart")
    @pytest.mark.cart
    def test_add_product_to_cart(self):
        """Test adding product to cart"""
        with allure.step("Login and navigate to e-commerce"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

        with allure.step("Add product to cart"):
            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Verify product added to cart"):
            notification = self.ecommerce_page.get_cart_notification_message()
            assert (
                "добавлен в корзину" in notification.lower()
            ), "Should show add to cart notification"

            cart_counter = self.ecommerce_page.get_cart_counter_value()
            assert cart_counter > 0, "Cart counter should increase"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test changing item quantity in cart")
    @pytest.mark.cart
    def test_change_item_quantity(self):
        """Test changing item quantity in cart"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Change item quantity"):
            new_quantity = 3
            self.cart_page.change_item_quantity(0, new_quantity)

        with allure.step("Verify quantity updated"):
            assert (
                self.cart_page.get_item_quantity(0) == new_quantity
            ), "Item quantity should be updated"

            # Verify total is recalculated
            total = self.cart_page.get_cart_total()
            assert total != "", "Cart total should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test removing item from cart")
    @pytest.mark.cart
    def test_remove_item_from_cart(self):
        """Test removing item from cart"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Remove item from cart"):
            self.cart_page.remove_item(0)

        with allure.step("Verify item removed"):
            cart_items = self.cart_page.get_cart_items()
            assert len(cart_items) == 0, "Cart should be empty after removing item"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test clearing entire cart")
    @pytest.mark.cart
    def test_clear_cart(self):
        """Test clearing entire cart"""
        with allure.step("Login and add multiple products to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            # Add multiple products
            products = self.settings.get_test_data()["products"]["sample_products"][:2]
            for product in products:
                self.ecommerce_page.add_product_to_cart(product["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Clear entire cart"):
            self.cart_page.click_clear_cart()
            self.cart_page.confirm_clear_cart()

        with allure.step("Verify cart is empty"):
            assert self.cart_page.is_cart_empty(), "Cart should be empty after clearing"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test applying promo code")
    @pytest.mark.cart
    def test_apply_promo_code(self):
        """Test applying promo code"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Apply valid promo code"):
            promo_data = self.settings.get_test_data()["ecommerce_cart"]["promo_codes"]
            self.cart_page.apply_promo_code(promo_data["valid"])

        with allure.step("Verify promo code applied"):
            discount = self.cart_page.get_discount_amount()
            assert discount != "", "Discount amount should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test invalid promo code")
    @pytest.mark.cart
    def test_invalid_promo_code(self):
        """Test applying invalid promo code"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Apply invalid promo code"):
            promo_data = self.settings.get_test_data()["ecommerce_cart"]["promo_codes"]
            self.cart_page.apply_promo_code(promo_data["invalid"])

        with allure.step("Verify error message"):
            error = self.cart_page.get_promo_code_error()
            assert (
                error != ""
            ), "Error message should be displayed for invalid promo code"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test cart persistence")
    @pytest.mark.cart
    def test_cart_persistence(self):
        """Test cart persistence across sessions"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Logout and login again"):
            self.dashboard_page.logout()
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()

        with allure.step("Navigate to cart and verify persistence"):
            self.cart_page.load()
            assert self.cart_page.is_item_in_cart(
                product_data["name"]
            ), "Item should persist in cart after logout/login"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test cart checkout process")
    @pytest.mark.cart
    def test_cart_checkout(self):
        """Test cart checkout process"""
        with allure.step("Login and add product to cart"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.ecommerce_page.load()

            product_data = self.settings.get_test_data()["products"]["sample_products"][
                0
            ]
            self.ecommerce_page.add_product_to_cart(product_data["name"])

        with allure.step("Navigate to cart"):
            self.cart_page.load()

        with allure.step("Click checkout"):
            self.cart_page.click_checkout()

        with allure.step("Verify checkout process started"):
            # Should be redirected to checkout page or show checkout form
            assert (
                "checkout" in self.driver.current_url.lower()
                or self.cart_page.get_success_message() != ""
            ), "Checkout process should start"
