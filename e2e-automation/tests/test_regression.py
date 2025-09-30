"""
Regression tests for the application
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
from utils.regression_testing import RegressionTesting


@allure.feature("Regression Tests")
@allure.story("Regression Testing")
class TestRegression(BaseTest):
    """Test class for regression testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestRegression")
        self.regression_testing = RegressionTesting(self)
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
    @allure.description("Test critical user workflows regression")
    @pytest.mark.regression
    def test_critical_user_workflows_regression(self):
        """Test critical user workflows regression"""
        with allure.step("Test login workflow regression"):
            # Test login workflow
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Should login successfully"

            # Test dashboard navigation
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in"

        with allure.step("Test E-commerce workflow regression"):
            # Test E-commerce workflow
            self.dashboard_page.click_ecommerce_card()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            self.ecommerce_page.wait_for_products_load()
            assert self.ecommerce_page.get_product_count() > 0, "Should have products"

            # Test product search
            self.ecommerce_page.search_products("laptop")
            assert self.ecommerce_page.wait_for_search_results(), "Search should work"

            # Test product filtering
            self.ecommerce_page.select_category("Electronics")
            assert self.ecommerce_page.wait_for_filtered_results(), "Filter should work"

        with allure.step("Test Social workflow regression"):
            # Test Social workflow
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_social_card()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            self.social_page.wait_for_feed_load()
            assert self.social_page.get_post_count() > 0, "Should have posts"

            # Test post creation
            self.social_page.click_create_post_button()
            assert (
                self.social_page.is_create_post_modal_visible()
            ), "Create post modal should be visible"
            self.social_page.fill_post_content("Test post")
            self.social_page.submit_post()
            assert self.social_page.wait_for_post_created(), "Post should be created"

        with allure.step("Test Tasks workflow regression"):
            # Test Tasks workflow
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_tasks_card()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"
            self.tasks_page.wait_for_task_board_load()
            assert self.tasks_page.get_task_count() > 0, "Should have tasks"

            # Test task creation
            self.tasks_page.click_create_task_button()
            assert (
                self.tasks_page.is_create_task_modal_visible()
            ), "Create task modal should be visible"
            self.tasks_page.fill_task_title("Test task")
            self.tasks_page.fill_task_description("Test description")
            self.tasks_page.submit_task()
            assert self.tasks_page.wait_for_task_created(), "Task should be created"

        with allure.step("Test Content workflow regression"):
            # Test Content workflow
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_content_card()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"
            self.content_page.wait_for_content_load()
            assert self.content_page.get_content_count() > 0, "Should have content"

            # Test content creation
            self.content_page.click_create_content_button()
            assert (
                self.content_page.is_create_content_modal_visible()
            ), "Create content modal should be visible"
            self.content_page.fill_content_title("Test content")
            self.content_page.fill_content_content("Test content body")
            self.content_page.submit_content()
            assert (
                self.content_page.wait_for_content_created()
            ), "Content should be created"

        with allure.step("Test Analytics workflow regression"):
            # Test Analytics workflow
            self.dashboard_page.navigate_to()
            self.dashboard_page.click_analytics_card()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            self.analytics_page.wait_for_dashboard_load()
            assert (
                self.analytics_page.get_metric_count() > 0
            ), "Should have analytics data"

            # Test analytics filtering
            self.analytics_page.select_date_range("Last 7 days")
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Date range filter should work"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test data consistency regression")
    @pytest.mark.regression
    def test_data_consistency_regression(self):
        """Test data consistency regression"""
        with allure.step("Test user data consistency"):
            # Test user data consistency across modules
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            dashboard_username = self.dashboard_page.get_logged_in_username()

            # Check user data in E-commerce
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            ecommerce_username = self.ecommerce_page.get_logged_in_username()
            assert (
                ecommerce_username == dashboard_username
            ), "Username should be consistent across modules"

            # Check user data in Social
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            social_username = self.social_page.get_logged_in_username()
            assert (
                social_username == dashboard_username
            ), "Username should be consistent across modules"

        with allure.step("Test session consistency"):
            # Test session persistence across modules
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Navigate through modules
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # User should remain logged in
            assert (
                self.tasks_page.get_logged_in_username() == dashboard_username
            ), "User should remain logged in across modules"

        with allure.step("Test data synchronization"):
            # Test data synchronization between modules
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Add product to cart
            self.ecommerce_page.add_product_to_cart("Test Product")
            assert self.ecommerce_page.wait_for_cart_updated(), "Cart should be updated"

            # Check if cart data is synchronized
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.dashboard_page.get_cart_count() > 0
            ), "Cart count should be synchronized"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test performance regression")
    @pytest.mark.regression
    def test_performance_regression(self):
        """Test performance regression"""
        with allure.step("Test page load performance regression"):
            # Test page load performance
            start_time = self.get_current_time()
            self.dashboard_page.navigate_to()
            self.dashboard_page.verify_page_loaded()
            dashboard_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.ecommerce_page.navigate_to()
            self.ecommerce_page.verify_page_loaded()
            ecommerce_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.social_page.navigate_to()
            self.social_page.verify_page_loaded()
            social_time = self.get_current_time() - start_time

            # Check performance thresholds
            assert (
                dashboard_time < 3.0
            ), f"Dashboard should load within 3 seconds, took {dashboard_time:.2f}s"
            assert (
                ecommerce_time < 5.0
            ), f"E-commerce should load within 5 seconds, took {ecommerce_time:.2f}s"
            assert (
                social_time < 5.0
            ), f"Social should load within 5 seconds, took {social_time:.2f}s"

        with allure.step("Test data loading performance regression"):
            # Test data loading performance
            start_time = self.get_current_time()
            self.ecommerce_page.navigate_to()
            self.ecommerce_page.wait_for_products_load()
            ecommerce_data_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.social_page.navigate_to()
            self.social_page.wait_for_feed_load()
            social_data_time = self.get_current_time() - start_time

            # Check data loading performance thresholds
            assert (
                ecommerce_data_time < 3.0
            ), f"E-commerce data should load within 3 seconds, took {ecommerce_data_time:.2f}s"
            assert (
                social_data_time < 3.0
            ), f"Social data should load within 3 seconds, took {social_data_time:.2f}s"

        with allure.step("Test API response performance regression"):
            # Test API response performance
            start_time = self.get_current_time()
            response = self.api_client.get("/api/health")
            api_time = self.get_current_time() - start_time

            assert response.status_code == 200, "Health check API should return 200"
            assert (
                api_time < 1.0
            ), f"Health check API should respond within 1 second, took {api_time:.2f}s"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test UI regression")
    @pytest.mark.regression
    def test_ui_regression(self):
        """Test UI regression"""
        with allure.step("Test navigation UI regression"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test navigation elements
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_USER_NAME
            ), "User name should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_LOGOUT_BUTTON
            ), "Logout button should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.NAVBAR_DROPDOWN
            ), "User dropdown should be present"

        with allure.step("Test form UI regression"):
            # Test form elements
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            assert self.login_page.is_element_present(
                *self.login_page.EMAIL_INPUT
            ), "Email input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.PASSWORD_INPUT
            ), "Password input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.LOGIN_BUTTON
            ), "Login button should be present"

        with allure.step("Test modal UI regression"):
            # Test modal elements
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

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

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test error handling regression")
    @pytest.mark.regression
    def test_error_handling_regression(self):
        """Test error handling regression"""
        with allure.step("Test login error handling regression"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test invalid credentials
            self.login_page.login("invalid@example.com", "wrongpassword")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid credentials"
            assert (
                "Invalid email or password" in self.login_page.get_error_message()
            ), "Should show correct error message"

        with allure.step("Test form validation error handling regression"):
            # Test form validation
            self.login_page.login("", "")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for empty fields"
            assert (
                "Email is required" in self.login_page.get_email_error_message()
            ), "Should show email required error"
            assert (
                "Password is required" in self.login_page.get_password_error_message()
            ), "Should show password required error"

        with allure.step("Test API error handling regression"):
            # Test API error handling
            response = self.api_client.get("/api/nonexistent")
            assert (
                response.status_code == 404
            ), "Should return 404 for nonexistent endpoint"
            assert (
                "Not Found" in response.json()["message"]
            ), "Should return Not Found message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test accessibility regression")
    @pytest.mark.regression
    def test_accessibility_regression(self):
        """Test accessibility regression"""
        with allure.step("Test keyboard navigation regression"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test keyboard navigation
            self.dashboard_page.press_tab_key()
            assert self.dashboard_page.is_element_focused(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be focused"

            self.dashboard_page.press_tab_key()
            assert self.dashboard_page.is_element_focused(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be focused"

        with allure.step("Test screen reader support regression"):
            # Test screen reader support
            assert (
                self.dashboard_page.is_screen_reader_supported()
            ), "Screen reader should be supported"
            assert (
                self.dashboard_page.are_landmarks_defined()
            ), "Landmarks should be defined"
            assert (
                self.dashboard_page.are_headings_properly_structured()
            ), "Headings should be properly structured"

        with allure.step("Test color contrast regression"):
            # Test color contrast
            assert self.dashboard_page.has_good_color_contrast(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should have good color contrast"
            assert self.dashboard_page.has_good_color_contrast(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should have good color contrast"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test security regression")
    @pytest.mark.regression
    def test_security_regression(self):
        """Test security regression"""
        with allure.step("Test authentication security regression"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test password security
            assert self.login_page.is_password_required(), "Password should be required"
            assert (
                self.login_page.is_password_minimum_length_enforced()
            ), "Password minimum length should be enforced"
            assert (
                self.login_page.is_password_complexity_enforced()
            ), "Password complexity should be enforced"

        with allure.step("Test input validation security regression"):
            # Test input validation
            self.login_page.login("invalid-email", "password")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for invalid email"
            assert (
                "Invalid email format" in self.login_page.get_email_error_message()
            ), "Should show email format error"

        with allure.step("Test session security regression"):
            # Test session security
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert self.dashboard_page.is_session_created(), "Session should be created"
            assert (
                self.dashboard_page.is_session_id_present()
            ), "Session ID should be present"
            assert (
                self.dashboard_page.is_session_id_secure()
            ), "Session ID should be secure"

    def get_current_time(self):
        """Get current timestamp in seconds"""
        import time

        return time.time()
