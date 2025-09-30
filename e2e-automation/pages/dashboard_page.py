"""
Dashboard page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import TestLogger


class DashboardPage(BasePage):
    """Page object for dashboard page"""

    # Page URL
    url = "/index.html"
    url_fragment = "dashboard"

    # Locators
    DASHBOARD_PAGE = (By.CSS_SELECTOR, "#dashboard-page")
    PAGE_HEADER = (By.CSS_SELECTOR, ".page-header h1")
    DASHBOARD_GRID = (By.CSS_SELECTOR, ".dashboard-grid")

    # Module cards
    ECOMMERCE_CARD = (By.CSS_SELECTOR, "[data-module='ecommerce']")
    SOCIAL_CARD = (By.CSS_SELECTOR, "[data-module='social']")
    TASKS_CARD = (By.CSS_SELECTOR, "[data-module='tasks']")
    CONTENT_CARD = (By.CSS_SELECTOR, "[data-module='content']")
    ANALYTICS_CARD = (By.CSS_SELECTOR, "[data-module='analytics']")

    # Navigation
    NAVBAR = (By.CSS_SELECTOR, ".navbar")
    NAVBAR_ITEMS = (By.CSS_SELECTOR, ".navbar-item")
    DASHBOARD_NAV = (By.CSS_SELECTOR, "[data-page='dashboard']")
    ECOMMERCE_NAV = (By.CSS_SELECTOR, "[data-page='ecommerce']")
    SOCIAL_NAV = (By.CSS_SELECTOR, "[data-page='social']")
    TASKS_NAV = (By.CSS_SELECTOR, "[data-page='tasks']")
    CONTENT_NAV = (By.CSS_SELECTOR, "[data-page='content']")
    ANALYTICS_NAV = (By.CSS_SELECTOR, "[data-page='analytics']")

    # User menu
    USER_MENU = (By.CSS_SELECTOR, "#user-menu")
    USER_DROPDOWN = (By.CSS_SELECTOR, "#user-dropdown")
    USER_NAME = (By.CSS_SELECTOR, "#user-name")
    USER_AVATAR = (By.CSS_SELECTOR, "#user-avatar")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "#logout-btn")

    # Theme toggle
    THEME_TOGGLE = (By.CSS_SELECTOR, "#theme-toggle")
    THEME_ICON = (By.CSS_SELECTOR, ".theme-icon")

    # Statistics
    ECOMMERCE_PRODUCTS_COUNT = (By.CSS_SELECTOR, "#ecommerce-products")
    ECOMMERCE_ORDERS_COUNT = (By.CSS_SELECTOR, "#ecommerce-orders")
    SOCIAL_USERS_COUNT = (By.CSS_SELECTOR, "#social-users")
    SOCIAL_POSTS_COUNT = (By.CSS_SELECTOR, "#social-posts")
    TASKS_PROJECTS_COUNT = (By.CSS_SELECTOR, "#tasks-projects")
    TASKS_COMPLETED_COUNT = (By.CSS_SELECTOR, "#tasks-completed")
    CONTENT_ARTICLES_COUNT = (By.CSS_SELECTOR, "#content-articles")
    CONTENT_VIEWS_COUNT = (By.CSS_SELECTOR, "#content-views")

    # Loading and status indicators
    LOADING_OVERLAY = (By.CSS_SELECTOR, "#loading-overlay")
    CONNECTION_STATUS = (By.CSS_SELECTOR, "#connection-status")
    LIVE_UPDATE_INDICATOR = (By.CSS_SELECTOR, "#live-update-indicator")

    # Key elements for page verification
    key_elements = [
        {"by": DASHBOARD_PAGE[0], "value": DASHBOARD_PAGE[1]},
        {"by": PAGE_HEADER[0], "value": PAGE_HEADER[1]},
        {"by": DASHBOARD_GRID[0], "value": DASHBOARD_GRID[1]},
    ]

    def __init__(self, driver, base_test):
        super().__init__(driver, base_test)
        self.logger = TestLogger("DashboardPage")

    def wait_for_dashboard_load(self):
        """Wait for dashboard to load completely"""
        self.wait_for_page_load()
        self.wait_for_element_visible(*self.DASHBOARD_PAGE)
        self.wait_for_element_visible(*self.DASHBOARD_GRID)

    def get_page_title(self) -> str:
        """Get dashboard page title"""
        return self.get_element_text(*self.PAGE_HEADER)

    def is_dashboard_visible(self) -> bool:
        """Check if dashboard is visible"""
        return self.is_element_visible(*self.DASHBOARD_PAGE)

    def get_module_cards(self) -> list:
        """Get all module cards"""
        return self.find_elements(*self.DASHBOARD_GRID)

    def click_ecommerce_card(self):
        """Click ecommerce module card"""
        self.log_page_action("Click ecommerce card")
        self.click_element(*self.ECOMMERCE_CARD)

    def click_social_card(self):
        """Click social module card"""
        self.log_page_action("Click social card")
        self.click_element(*self.SOCIAL_CARD)

    def click_tasks_card(self):
        """Click tasks module card"""
        self.log_page_action("Click tasks card")
        self.click_element(*self.TASKS_CARD)

    def click_content_card(self):
        """Click content module card"""
        self.log_page_action("Click content card")
        self.click_element(*self.CONTENT_CARD)

    def click_analytics_card(self):
        """Click analytics module card"""
        self.log_page_action("Click analytics card")
        self.click_element(*self.ANALYTICS_CARD)

    def navigate_to_ecommerce(self):
        """Navigate to ecommerce page"""
        self.log_page_action("Navigate to ecommerce")
        self.click_element(*self.ECOMMERCE_NAV)

    def navigate_to_social(self):
        """Navigate to social page"""
        self.log_page_action("Navigate to social")
        self.click_element(*self.SOCIAL_NAV)

    def navigate_to_tasks(self):
        """Navigate to tasks page"""
        self.log_page_action("Navigate to tasks")
        self.click_element(*self.TASKS_NAV)

    def navigate_to_content(self):
        """Navigate to content page"""
        self.log_page_action("Navigate to content")
        self.click_element(*self.CONTENT_NAV)

    def navigate_to_analytics(self):
        """Navigate to analytics page"""
        self.log_page_action("Navigate to analytics")
        self.click_element(*self.ANALYTICS_NAV)

    def get_user_name(self) -> str:
        """Get current user name"""
        return self.get_element_text(*self.USER_NAME)

    def get_user_avatar_src(self) -> str:
        """Get user avatar source"""
        return self.get_element_attribute(*self.USER_AVATAR, "src")

    def click_user_menu(self):
        """Click user menu dropdown"""
        self.log_page_action("Click user menu")
        self.click_element(*self.USER_MENU)

    def is_user_dropdown_visible(self) -> bool:
        """Check if user dropdown is visible"""
        return self.is_element_visible(*self.USER_DROPDOWN)

    def click_logout(self):
        """Click logout button"""
        self.log_page_action("Click logout")
        self.click_element(*self.LOGOUT_BUTTON)

    def logout(self):
        """Complete logout process"""
        self.click_user_menu()
        self.wait_for_element_visible(*self.USER_DROPDOWN)
        self.click_logout()

    def toggle_theme(self):
        """Toggle theme between light and dark"""
        self.log_page_action("Toggle theme")
        self.click_element(*self.THEME_TOGGLE)

    def get_theme_icon(self) -> str:
        """Get current theme icon"""
        return self.get_element_text(*self.THEME_ICON)

    def is_dark_theme(self) -> bool:
        """Check if dark theme is active"""
        return "☀️" in self.get_theme_icon()

    def is_light_theme(self) -> bool:
        """Check if light theme is active"""
        return "🌙" in self.get_theme_icon()

    def get_ecommerce_products_count(self) -> str:
        """Get ecommerce products count"""
        return self.get_element_text(*self.ECOMMERCE_PRODUCTS_COUNT)

    def get_ecommerce_orders_count(self) -> str:
        """Get ecommerce orders count"""
        return self.get_element_text(*self.ECOMMERCE_ORDERS_COUNT)

    def get_social_users_count(self) -> str:
        """Get social users count"""
        return self.get_element_text(*self.SOCIAL_USERS_COUNT)

    def get_social_posts_count(self) -> str:
        """Get social posts count"""
        return self.get_element_text(*self.SOCIAL_POSTS_COUNT)

    def get_tasks_projects_count(self) -> str:
        """Get tasks projects count"""
        return self.get_element_text(*self.TASKS_PROJECTS_COUNT)

    def get_tasks_completed_count(self) -> str:
        """Get tasks completed count"""
        return self.get_element_text(*self.TASKS_COMPLETED_COUNT)

    def get_content_articles_count(self) -> str:
        """Get content articles count"""
        return self.get_element_text(*self.CONTENT_ARTICLES_COUNT)

    def get_content_views_count(self) -> str:
        """Get content views count"""
        return self.get_element_text(*self.CONTENT_VIEWS_COUNT)

    def get_all_statistics(self) -> dict:
        """Get all dashboard statistics"""
        return {
            "ecommerce_products": self.get_ecommerce_products_count(),
            "ecommerce_orders": self.get_ecommerce_orders_count(),
            "social_users": self.get_social_users_count(),
            "social_posts": self.get_social_posts_count(),
            "tasks_projects": self.get_tasks_projects_count(),
            "tasks_completed": self.get_tasks_completed_count(),
            "content_articles": self.get_content_articles_count(),
            "content_views": self.get_content_views_count(),
        }

    def is_loading_visible(self) -> bool:
        """Check if loading overlay is visible"""
        return self.is_element_visible(*self.LOADING_OVERLAY)

    def wait_for_loading_complete(self, timeout: int = 30):
        """Wait for loading to complete"""
        try:
            # Wait for loading overlay to disappear
            from selenium.webdriver.support import expected_conditions as EC

            wait = self.base_test.wait
            wait.until(EC.invisibility_of_element_located(self.LOADING_OVERLAY))
            self.logger.info("Loading completed")
        except Exception as e:
            self.logger.warning(f"Loading wait timeout: {str(e)}")

    def get_connection_status(self) -> str:
        """Get connection status text"""
        if self.is_element_visible(*self.CONNECTION_STATUS):
            return self.get_element_text(*self.CONNECTION_STATUS)
        return ""

    def is_connected(self) -> bool:
        """Check if connected to backend"""
        status = self.get_connection_status()
        return "connected" in status.lower() or "подключено" in status.lower()

    def is_live_update_active(self) -> bool:
        """Check if live update indicator is visible"""
        return self.is_element_visible(*self.LIVE_UPDATE_INDICATOR)

    def get_navbar_items(self) -> list:
        """Get all navbar items"""
        return self.find_elements(*self.NAVBAR_ITEMS)

    def get_active_nav_item(self) -> str:
        """Get active navigation item"""
        try:
            active_item = self.find_element(By.CSS_SELECTOR, ".navbar-item.active")
            return active_item.get_attribute("data-page")
        except Exception:
            return ""

    def is_navbar_visible(self) -> bool:
        """Check if navbar is visible"""
        return self.is_element_visible(*self.NAVBAR)

    def get_module_card_by_name(self, module_name: str) -> dict:
        """Get module card information by name"""
        try:
            card = self.find_element(By.CSS_SELECTOR, f"[data-module='{module_name}']")
            return {
                "title": card.find_element(By.CSS_SELECTOR, "h3").text,
                "description": card.find_element(By.CSS_SELECTOR, "p").text,
                "is_visible": card.is_displayed(),
                "is_enabled": card.is_enabled(),
            }
        except Exception as e:
            self.logger.error(f"Failed to get module card {module_name}: {str(e)}")
            return {}

    def verify_all_modules_loaded(self) -> bool:
        """Verify all modules are loaded and visible"""
        modules = ["ecommerce", "social", "tasks", "content", "analytics"]

        for module in modules:
            if not self.is_element_present(
                By.CSS_SELECTOR, f"[data-module='{module}']"
            ):
                self.logger.error(f"Module {module} not found")
                return False

        return True

    def wait_for_statistics_load(self, timeout: int = 10):
        """Wait for statistics to load"""
        try:
            # Wait for at least one statistic to be visible
            self.wait_for_element_visible(*self.ECOMMERCE_PRODUCTS_COUNT, timeout)
            self.logger.info("Statistics loaded")
        except Exception as e:
            self.logger.warning(f"Statistics load timeout: {str(e)}")

    def refresh_dashboard(self):
        """Refresh dashboard data"""
        self.log_page_action("Refresh dashboard")
        self.refresh_page()
        self.wait_for_dashboard_load()

    def get_dashboard_info(self) -> dict:
        """Get comprehensive dashboard information"""
        return {
            "title": self.get_page_title(),
            "user_name": self.get_user_name(),
            "theme": "dark" if self.is_dark_theme() else "light",
            "statistics": self.get_all_statistics(),
            "connection_status": self.get_connection_status(),
            "is_connected": self.is_connected(),
            "active_nav": self.get_active_nav_item(),
            "modules_loaded": self.verify_all_modules_loaded(),
        }

    def verify_dashboard_functionality(self) -> bool:
        """Verify dashboard basic functionality"""
        try:
            # Check if dashboard is visible
            if not self.is_dashboard_visible():
                return False

            # Check if user menu is accessible
            self.click_user_menu()
            if not self.is_user_dropdown_visible():
                return False

            # Check if theme toggle works
            initial_theme = self.is_dark_theme()
            self.toggle_theme()
            if self.is_dark_theme() == initial_theme:
                return False

            # Check if navigation works
            if not self.is_navbar_visible():
                return False

            return True
        except Exception as e:
            self.logger.error(f"Dashboard functionality verification failed: {str(e)}")
            return False
