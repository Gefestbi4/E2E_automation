"""
UI tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.ecommerce_page import EcommercePage
from pages.social_page import SocialPage
from pages.tasks_page import TasksPage
from pages.content_page import ContentPage
from pages.analytics_page import AnalyticsPage
from utils.logger import TestLogger


@allure.feature("UI Tests")
@allure.story("UI Testing")
class TestUI(BaseTest):
    """Test class for UI testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestUI")
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @pytest.fixture(autouse=True)
    def login_user(self):
        """Login user before each test"""
        self.login_page.navigate_to()
        user_data = self.settings.get_user_credentials("regular_user")
        self.login_page.login(user_data["email"], user_data["password"])
        assert self.login_page.wait_for_login_success(), "Should login successfully"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test navigation UI elements")
    @pytest.mark.ui
    def test_navigation_ui(self):
        """Test navigation UI elements"""
        with allure.step("Test navigation bar elements"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test navigation bar elements
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_USER_NAME
            ), "User name should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_LOGOUT_BUTTON
            ), "Logout button should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_DROPDOWN
            ), "User dropdown should be present"

        with allure.step("Test navigation bar functionality"):
            # Test user dropdown
            self.dashboard_page.click_user_dropdown()
            assert (
                self.dashboard_page.is_user_dropdown_visible()
            ), "User dropdown should be visible"

            # Test logout functionality
            self.dashboard_page.click_logout_button()
            assert (
                self.login_page.verify_page_loaded()
            ), "Should redirect to login page after logout"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test form UI elements")
    @pytest.mark.ui
    def test_form_ui(self):
        """Test form UI elements"""
        with allure.step("Test login form UI"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test form elements
            assert self.login_page.is_element_present(
                *self.login_page.EMAIL_INPUT
            ), "Email input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.PASSWORD_INPUT
            ), "Password input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.LOGIN_BUTTON
            ), "Login button should be present"
            assert self.login_page.is_element_present(
                *self.login_page.REGISTER_LINK
            ), "Register link should be present"

        with allure.step("Test form validation UI"):
            # Test empty field validation
            self.login_page.login("", "")
            assert self.login_page.is_element_present(
                *self.login_page.EMAIL_ERROR_MESSAGE
            ), "Email error message should be present"
            assert self.login_page.is_element_present(
                *self.login_page.PASSWORD_ERROR_MESSAGE
            ), "Password error message should be present"

            # Test invalid email format validation
            self.login_page.login("invalid-email", "password")
            assert self.login_page.is_element_present(
                *self.login_page.EMAIL_ERROR_MESSAGE
            ), "Email format error message should be present"

        with allure.step("Test form input UI"):
            # Test input field behavior
            self.login_page.enter_email("test@example.com")
            assert (
                self.login_page.get_email_value() == "test@example.com"
            ), "Email input should work correctly"

            self.login_page.enter_password("password123")
            assert (
                self.login_page.get_password_value() == "password123"
            ), "Password input should work correctly"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test button UI elements")
    @pytest.mark.ui
    def test_button_ui(self):
        """Test button UI elements"""
        with allure.step("Test dashboard buttons"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test module buttons
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.TASKS_CARD
            ), "Tasks card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.CONTENT_CARD
            ), "Content card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ANALYTICS_CARD
            ), "Analytics card should be present"

        with allure.step("Test button click functionality"):
            # Test E-commerce button
            self.dashboard_page.click_ecommerce_card()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test Social button
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_social_card()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test Tasks button
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_tasks_card()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Test Content button
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_content_card()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Test Analytics button
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_analytics_card()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test modal UI elements")
    @pytest.mark.ui
    def test_modal_ui(self):
        """Test modal UI elements"""
        with allure.step("Test create post modal UI"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test create post modal
            self.social_page.click_create_post_button()
            assert (
                self.social_page.is_create_post_modal_visible()
            ), "Create post modal should be visible"
            assert self.social_page.is_element_present(
                *self.social_page.POST_TITLE_INPUT
            ), "Post title input should be present"
            assert self.social_page.is_element_present(
                *self.social_page.POST_CONTENT_INPUT
            ), "Post content input should be present"
            assert self.social_page.is_element_present(
                *self.social_page.POST_SUBMIT_BUTTON
            ), "Post submit button should be present"
            assert self.social_page.is_element_present(
                *self.social_page.POST_CANCEL_BUTTON
            ), "Post cancel button should be present"

        with allure.step("Test create task modal UI"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Test create task modal
            self.tasks_page.click_create_task_button()
            assert (
                self.tasks_page.is_create_task_modal_visible()
            ), "Create task modal should be visible"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_TITLE_INPUT
            ), "Task title input should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_DESCRIPTION_INPUT
            ), "Task description input should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_PRIORITY_SELECT
            ), "Task priority select should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_SUBMIT_BUTTON
            ), "Task submit button should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_CANCEL_BUTTON
            ), "Task cancel button should be present"

        with allure.step("Test create content modal UI"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Test create content modal
            self.content_page.click_create_content_button()
            assert (
                self.content_page.is_create_content_modal_visible()
            ), "Create content modal should be visible"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_TITLE_INPUT
            ), "Content title input should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_CONTENT_INPUT
            ), "Content content input should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_CATEGORY_SELECT
            ), "Content category select should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_SUBMIT_BUTTON
            ), "Content submit button should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_CANCEL_BUTTON
            ), "Content cancel button should be present"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test table UI elements")
    @pytest.mark.ui
    def test_table_ui(self):
        """Test table UI elements"""
        with allure.step("Test products table UI"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test products table
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCTS_GRID
            ), "Products grid should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCT_CARD
            ), "Product cards should be present"

            # Test table headers
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCT_NAME_HEADER
            ), "Product name header should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCT_PRICE_HEADER
            ), "Product price header should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCT_CATEGORY_HEADER
            ), "Product category header should be present"

        with allure.step("Test tasks table UI"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Test tasks table
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_BOARD
            ), "Task board should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_COLUMN
            ), "Task columns should be present"

            # Test column headers
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TODO_COLUMN_HEADER
            ), "Todo column header should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.IN_PROGRESS_COLUMN_HEADER
            ), "In Progress column header should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.DONE_COLUMN_HEADER
            ), "Done column header should be present"

        with allure.step("Test content table UI"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Test content table
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_LIST
            ), "Content list should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_ITEM
            ), "Content items should be present"

            # Test list headers
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_TITLE_HEADER
            ), "Content title header should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_CATEGORY_HEADER
            ), "Content category header should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_STATUS_HEADER
            ), "Content status header should be present"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test filter UI elements")
    @pytest.mark.ui
    def test_filter_ui(self):
        """Test filter UI elements"""
        with allure.step("Test E-commerce filters UI"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test filter elements
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.CATEGORY_FILTER
            ), "Category filter should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRICE_RANGE_FILTER
            ), "Price range filter should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.IN_STOCK_FILTER
            ), "In stock filter should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.SEARCH_BAR
            ), "Search bar should be present"

        with allure.step("Test filter functionality UI"):
            # Test category filter
            self.ecommerce_page.select_category("Electronics")
            assert (
                self.ecommerce_page.wait_for_filtered_results()
            ), "Category filter should work"

            # Test price range filter
            self.ecommerce_page.set_price_range(500)
            assert (
                self.ecommerce_page.wait_for_filtered_results()
            ), "Price range filter should work"

            # Test in stock filter
            self.ecommerce_page.toggle_in_stock_filter()
            assert (
                self.ecommerce_page.wait_for_filtered_results()
            ), "In stock filter should work"

            # Test search filter
            self.ecommerce_page.search_products("laptop")
            assert (
                self.ecommerce_page.wait_for_search_results()
            ), "Search filter should work"

        with allure.step("Test Analytics filters UI"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # Test filter elements
            assert self.analytics_page.is_element_present(
                *self.analytics_page.DATE_RANGE_FILTER
            ), "Date range filter should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.METRIC_TYPE_FILTER
            ), "Metric type filter should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.APPLY_FILTER_BUTTON
            ), "Apply filter button should be present"

        with allure.step("Test filter functionality UI"):
            # Test date range filter
            self.analytics_page.select_date_range("Last 7 days")
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Date range filter should work"

            # Test metric type filter
            self.analytics_page.select_metric_type("Revenue")
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Metric type filter should work"

            # Test apply filter button
            self.analytics_page.click_apply_filter_button()
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Apply filter button should work"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test chart UI elements")
    @pytest.mark.ui
    def test_chart_ui(self):
        """Test chart UI elements"""
        with allure.step("Test Analytics charts UI"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # Test chart elements
            assert self.analytics_page.is_element_present(
                *self.analytics_page.DASHBOARD_CONTAINER
            ), "Dashboard container should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.CHARTS_CONTAINER
            ), "Charts container should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.REVENUE_CHART
            ), "Revenue chart should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.ORDERS_CHART
            ), "Orders chart should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.USERS_CHART
            ), "Users chart should be present"

        with allure.step("Test chart functionality UI"):
            # Test chart interactions
            self.analytics_page.hover_over_chart(self.analytics_page.REVENUE_CHART)
            assert (
                self.analytics_page.is_chart_tooltip_visible()
            ), "Chart tooltip should be visible"

            # Test chart zoom
            self.analytics_page.zoom_chart(self.analytics_page.REVENUE_CHART)
            assert self.analytics_page.is_chart_zoomed(), "Chart should be zoomed"

            # Test chart reset
            self.analytics_page.reset_chart(self.analytics_page.REVENUE_CHART)
            assert self.analytics_page.is_chart_reset(), "Chart should be reset"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test responsive UI elements")
    @pytest.mark.ui
    def test_responsive_ui(self):
        """Test responsive UI elements"""
        with allure.step("Test mobile viewport"):
            # Set mobile viewport
            self.driver.set_window_size(375, 667)

            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly in mobile view"

            # Test mobile navigation
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.MOBILE_MENU_BUTTON
            ), "Mobile menu button should be present"
            self.dashboard_page.click_mobile_menu_button()
            assert (
                self.dashboard_page.is_mobile_menu_visible()
            ), "Mobile menu should be visible"

        with allure.step("Test tablet viewport"):
            # Set tablet viewport
            self.driver.set_window_size(768, 1024)

            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly in tablet view"

            # Test tablet layout
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be present in tablet view"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be present in tablet view"

        with allure.step("Test desktop viewport"):
            # Set desktop viewport
            self.driver.set_window_size(1920, 1080)

            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly in desktop view"

            # Test desktop layout
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be present in desktop view"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be present in desktop view"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.TASKS_CARD
            ), "Tasks card should be present in desktop view"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.CONTENT_CARD
            ), "Content card should be present in desktop view"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ANALYTICS_CARD
            ), "Analytics card should be present in desktop view"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test accessibility UI elements")
    @pytest.mark.ui
    def test_accessibility_ui(self):
        """Test accessibility UI elements"""
        with allure.step("Test keyboard navigation"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test tab navigation
            self.dashboard_page.press_tab_key()
            assert self.dashboard_page.is_element_focused(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be focused"

            self.dashboard_page.press_tab_key()
            assert self.dashboard_page.is_element_focused(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be focused"

            self.dashboard_page.press_tab_key()
            assert self.dashboard_page.is_element_focused(
                *self.dashboard_page.TASKS_CARD
            ), "Tasks card should be focused"

        with allure.step("Test ARIA labels"):
            # Test ARIA labels on form elements
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            assert self.login_page.has_aria_label(
                *self.login_page.EMAIL_INPUT
            ), "Email input should have ARIA label"
            assert self.login_page.has_aria_label(
                *self.login_page.PASSWORD_INPUT
            ), "Password input should have ARIA label"
            assert self.login_page.has_aria_label(
                *self.login_page.LOGIN_BUTTON
            ), "Login button should have ARIA label"

        with allure.step("Test color contrast"):
            # Test color contrast on important elements
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test button color contrast
            assert self.dashboard_page.has_good_color_contrast(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should have good color contrast"
            assert self.dashboard_page.has_good_color_contrast(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should have good color contrast"
            assert self.dashboard_page.has_good_color_contrast(
                *self.dashboard_page.TASKS_CARD
            ), "Tasks card should have good color contrast"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test loading UI elements")
    @pytest.mark.ui
    def test_loading_ui(self):
        """Test loading UI elements"""
        with allure.step("Test page loading indicators"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test loading indicators
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.LOADING_INDICATOR
            ), "Loading indicator should be present"
            assert (
                self.dashboard_page.wait_for_loading_complete()
            ), "Loading should complete"

        with allure.step("Test data loading indicators"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test data loading indicators
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.DATA_LOADING_INDICATOR
            ), "Data loading indicator should be present"
            assert (
                self.ecommerce_page.wait_for_data_loading_complete()
            ), "Data loading should complete"

        with allure.step("Test button loading states"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test button loading states
            self.social_page.click_create_post_button()
            self.social_page.fill_post_content("Test post")
            self.social_page.submit_post()
            assert self.social_page.is_button_loading(
                *self.social_page.POST_SUBMIT_BUTTON
            ), "Submit button should show loading state"
            assert self.social_page.wait_for_button_loading_complete(
                *self.social_page.POST_SUBMIT_BUTTON
            ), "Button loading should complete"
