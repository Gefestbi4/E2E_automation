"""
E-commerce page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import TestLogger


class EcommercePage(BasePage):
    """Page object for e-commerce page"""

    # Page URL
    url = "/index.html#ecommerce"
    url_fragment = "ecommerce"

    # Locators
    ECOMMERCE_PAGE = (By.CSS_SELECTOR, "#ecommerce-page")
    PAGE_HEADER = (By.CSS_SELECTOR, ".page-header h1")

    # Action buttons
    ADD_PRODUCT_BTN = (By.CSS_SELECTOR, "#add-product-btn")
    TEST_MEDIA_UPLOAD_BTN = (By.CSS_SELECTOR, "#test-media-upload-btn")
    TEST_SEARCH_BTN = (By.CSS_SELECTOR, "#test-search-btn")
    TEST_SETTINGS_BTN = (By.CSS_SELECTOR, "#test-settings-btn")
    TEST_AI_BTN = (By.CSS_SELECTOR, "#test-ai-btn")
    TEST_ANALYTICS_BTN = (By.CSS_SELECTOR, "#test-analytics-btn")

    # Sidebar filters
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar")
    CATEGORY_FILTER = (By.CSS_SELECTOR, "#category-filter")
    PRICE_RANGE = (By.CSS_SELECTOR, "#price-range")
    PRICE_VALUE = (By.CSS_SELECTOR, "#price-value")
    IN_STOCK_FILTER = (By.CSS_SELECTOR, "#in-stock-filter")

    # Search and products
    SEARCH_BAR = (By.CSS_SELECTOR, ".search-bar")
    PRODUCT_SEARCH_INPUT = (By.CSS_SELECTOR, "#product-search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-bar button")
    PRODUCTS_GRID = (By.CSS_SELECTOR, "#products-grid")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    PAGINATION = (By.CSS_SELECTOR, "#products-pagination")

    # Product card elements
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".product-description")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".add-to-cart-btn")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".product-image")

    # Cart elements
    CART_NAV = (By.CSS_SELECTOR, "[test-id='cart-nav']")
    CART_COUNTER = (By.CSS_SELECTOR, "[test-id='cart-counter']")
    CART_NOTIFICATION = (By.CSS_SELECTOR, "[test-id='cart-notification']")

    # Key elements for page verification
    key_elements = [
        {"by": ECOMMERCE_PAGE[0], "value": ECOMMERCE_PAGE[1]},
        {"by": PAGE_HEADER[0], "value": PAGE_HEADER[1]},
        {"by": PRODUCTS_GRID[0], "value": PRODUCTS_GRID[1]},
    ]

    def __init__(self, driver, base_test):
        super().__init__(driver, base_test)
        self.logger = TestLogger("EcommercePage")

    def wait_for_ecommerce_load(self):
        """Wait for e-commerce page to load completely"""
        self.wait_for_page_load()
        self.wait_for_element_visible(*self.ECOMMERCE_PAGE)
        self.wait_for_element_visible(*self.PRODUCTS_GRID)

    def get_page_title(self) -> str:
        """Get e-commerce page title"""
        return self.get_element_text(*self.PAGE_HEADER)

    def is_ecommerce_visible(self) -> bool:
        """Check if e-commerce page is visible"""
        return self.is_element_visible(*self.ECOMMERCE_PAGE)

    def click_add_product(self):
        """Click add product button"""
        self.log_page_action("Click add product button")
        self.click_element(*self.ADD_PRODUCT_BTN)

    def click_test_media_upload(self):
        """Click test media upload button"""
        self.log_page_action("Click test media upload button")
        self.click_element(*self.TEST_MEDIA_UPLOAD_BTN)

    def click_test_search(self):
        """Click test search button"""
        self.log_page_action("Click test search button")
        self.click_element(*self.TEST_SEARCH_BTN)

    def click_test_settings(self):
        """Click test settings button"""
        self.log_page_action("Click test settings button")
        self.click_element(*self.TEST_SETTINGS_BTN)

    def click_test_ai(self):
        """Click test AI button"""
        self.log_page_action("Click test AI button")
        self.click_element(*self.TEST_AI_BTN)

    def click_test_analytics(self):
        """Click test analytics button"""
        self.log_page_action("Click test analytics button")
        self.click_element(*self.TEST_ANALYTICS_BTN)

    def search_products(self, search_term: str):
        """Search for products"""
        self.log_page_action("Search products", "search input", search_term)
        self.send_keys(*self.PRODUCT_SEARCH_INPUT, search_term)
        self.click_element(*self.SEARCH_BUTTON)

    def clear_search(self):
        """Clear search input"""
        self.log_page_action("Clear search")
        self.find_element(*self.PRODUCT_SEARCH_INPUT).clear()

    def get_search_term(self) -> str:
        """Get current search term"""
        return self.get_element_attribute(*self.PRODUCT_SEARCH_INPUT, "value")

    def select_category(self, category: str):
        """Select product category filter"""
        self.log_page_action("Select category", "category filter", category)
        from selenium.webdriver.support.ui import Select

        category_select = Select(self.find_element(*self.CATEGORY_FILTER))
        category_select.select_by_visible_text(category)

    def get_selected_category(self) -> str:
        """Get selected category"""
        from selenium.webdriver.support.ui import Select

        category_select = Select(self.find_element(*self.CATEGORY_FILTER))
        return category_select.first_selected_option.text

    def set_price_range(self, min_price: int, max_price: int):
        """Set price range filter"""
        self.log_page_action(
            "Set price range", "price range", f"{min_price}-{max_price}"
        )
        price_slider = self.find_element(*self.PRICE_RANGE)
        # Set min and max attributes
        self.execute_javascript(
            f"""
            arguments[0].min = {min_price};
            arguments[0].max = {max_price};
            arguments[0].value = {max_price};
        """,
            price_slider,
        )

    def get_price_range(self) -> str:
        """Get current price range"""
        return self.get_element_text(*self.PRICE_VALUE)

    def toggle_in_stock_filter(self):
        """Toggle in stock filter"""
        self.log_page_action("Toggle in stock filter")
        self.click_element(*self.IN_STOCK_FILTER)

    def is_in_stock_filter_checked(self) -> bool:
        """Check if in stock filter is checked"""
        return self.find_element(*self.IN_STOCK_FILTER).is_selected()

    def get_products(self) -> list:
        """Get all product cards"""
        return self.find_elements(*self.PRODUCT_CARDS)

    def get_product_count(self) -> int:
        """Get number of products displayed"""
        return len(self.get_products())

    def get_product_by_name(self, product_name: str) -> dict:
        """Get product information by name"""
        try:
            products = self.get_products()
            for product in products:
                name_element = product.find_element(*self.PRODUCT_NAME)
                if name_element.text == product_name:
                    return {
                        "name": name_element.text,
                        "price": product.find_element(*self.PRODUCT_PRICE).text,
                        "description": product.find_element(
                            *self.PRODUCT_DESCRIPTION
                        ).text,
                        "is_available": product.find_element(
                            *self.ADD_TO_CART_BTN
                        ).is_enabled(),
                    }
            return {}
        except Exception as e:
            self.logger.error(f"Failed to get product {product_name}: {str(e)}")
            return {}

    def add_product_to_cart(self, product_name: str):
        """Add product to cart by name"""
        self.log_page_action("Add product to cart", "product", product_name)
        products = self.get_products()
        for product in products:
            name_element = product.find_element(*self.PRODUCT_NAME)
            if name_element.text == product_name:
                add_btn = product.find_element(*self.ADD_TO_CART_BTN)
                add_btn.click()
                break

    def click_add_to_cart_by_index(self, index: int):
        """Add product to cart by index"""
        self.log_page_action("Add product to cart by index", "index", str(index))
        products = self.get_products()
        if 0 <= index < len(products):
            add_btn = products[index].find_element(*self.ADD_TO_CART_BTN)
            add_btn.click()

    def get_cart_counter(self) -> str:
        """Get cart counter value"""
        if self.is_element_visible(*self.CART_COUNTER):
            return self.get_element_text(*self.CART_COUNTER)
        return "0"

    def click_cart_nav(self):
        """Click cart navigation"""
        self.log_page_action("Click cart navigation")
        self.click_element(*self.CART_NAV)

    def get_cart_notification(self) -> str:
        """Get cart notification message"""
        if self.is_element_visible(*self.CART_NOTIFICATION):
            return self.get_element_text(*self.CART_NOTIFICATION)
        return ""

    def wait_for_cart_notification(self, timeout: int = 5) -> bool:
        """Wait for cart notification to appear"""
        try:
            self.wait_for_element_visible(*self.CART_NOTIFICATION, timeout)
            return True
        except Exception:
            return False

    def is_product_available(self, product_name: str) -> bool:
        """Check if product is available (in stock)"""
        product = self.get_product_by_name(product_name)
        return product.get("is_available", False)

    def get_product_price(self, product_name: str) -> str:
        """Get product price by name"""
        product = self.get_product_by_name(product_name)
        return product.get("price", "")

    def get_product_description(self, product_name: str) -> str:
        """Get product description by name"""
        product = self.get_product_by_name(product_name)
        return product.get("description", "")

    def is_pagination_visible(self) -> bool:
        """Check if pagination is visible"""
        return self.is_element_visible(*self.PAGINATION)

    def get_pagination_pages(self) -> list:
        """Get pagination page numbers"""
        try:
            pagination = self.find_element(*self.PAGINATION)
            page_links = pagination.find_elements(By.CSS_SELECTOR, "a, button")
            return [link.text for link in page_links if link.text.isdigit()]
        except Exception:
            return []

    def click_pagination_page(self, page_number: int):
        """Click pagination page number"""
        self.log_page_action("Click pagination page", "page", str(page_number))
        try:
            pagination = self.find_element(*self.PAGINATION)
            page_link = pagination.find_element(
                By.CSS_SELECTOR,
                f"a:contains('{page_number}'), button:contains('{page_number}')",
            )
            page_link.click()
        except Exception as e:
            self.logger.error(
                f"Failed to click pagination page {page_number}: {str(e)}"
            )

    def get_sidebar_filters(self) -> dict:
        """Get all sidebar filter values"""
        return {
            "category": self.get_selected_category(),
            "price_range": self.get_price_range(),
            "in_stock": self.is_in_stock_filter_checked(),
        }

    def clear_all_filters(self):
        """Clear all filters"""
        self.log_page_action("Clear all filters")
        # Reset category to "All"
        self.select_category("Все категории")
        # Reset price range
        self.set_price_range(0, 10000)
        # Uncheck in stock filter
        if self.is_in_stock_filter_checked():
            self.toggle_in_stock_filter()

    def wait_for_products_load(self, timeout: int = 10):
        """Wait for products to load"""
        try:
            self.wait_for_element_visible(*self.PRODUCTS_GRID, timeout)
            # Wait for at least one product to be visible
            self.wait_for_element_visible(*self.PRODUCT_CARDS, timeout)
            self.logger.info("Products loaded")
        except Exception as e:
            self.logger.warning(f"Products load timeout: {str(e)}")

    def get_products_info(self) -> list:
        """Get information about all visible products"""
        products_info = []
        products = self.get_products()

        for product in products:
            try:
                info = {
                    "name": product.find_element(*self.PRODUCT_NAME).text,
                    "price": product.find_element(*self.PRODUCT_PRICE).text,
                    "description": product.find_element(*self.PRODUCT_DESCRIPTION).text,
                    "is_available": product.find_element(
                        *self.ADD_TO_CART_BTN
                    ).is_enabled(),
                }
                products_info.append(info)
            except Exception as e:
                self.logger.warning(f"Failed to get product info: {str(e)}")

        return products_info

    def verify_ecommerce_functionality(self) -> bool:
        """Verify e-commerce basic functionality"""
        try:
            # Check if page is visible
            if not self.is_ecommerce_visible():
                return False

            # Check if products are loaded
            if self.get_product_count() == 0:
                return False

            # Check if search works
            self.search_products("test")
            if not self.get_search_term():
                return False

            # Check if filters are present
            if not self.is_element_present(*self.CATEGORY_FILTER):
                return False

            return True
        except Exception as e:
            self.logger.error(f"E-commerce functionality verification failed: {str(e)}")
            return False

    def get_ecommerce_info(self) -> dict:
        """Get comprehensive e-commerce page information"""
        return {
            "title": self.get_page_title(),
            "product_count": self.get_product_count(),
            "cart_counter": self.get_cart_counter(),
            "filters": self.get_sidebar_filters(),
            "search_term": self.get_search_term(),
            "pagination_visible": self.is_pagination_visible(),
            "products_info": self.get_products_info(),
        }
