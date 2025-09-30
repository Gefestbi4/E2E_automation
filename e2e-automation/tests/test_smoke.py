"""
Smoke tests for the application
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
from utils.smoke_testing import SmokeTesting


@allure.feature("Smoke Tests")
@allure.story("Smoke Testing")
class TestSmoke(BaseTest):
    """Test class for smoke testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestSmoke")
        self.smoke_testing = SmokeTesting(self)
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

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test application basic functionality")
    @pytest.mark.smoke
    def test_application_basic_functionality(self):
        """Test application basic functionality"""
        with allure.step("Test application loads"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Check critical elements are present
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

        with allure.step("Test user authentication"):
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in"

        with allure.step("Test navigation works"):
            # Test navigation to different modules
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

            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test E-commerce basic functionality")
    @pytest.mark.smoke
    def test_ecommerce_basic_functionality(self):
        """Test E-commerce basic functionality"""
        with allure.step("Test E-commerce page loads"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Check critical elements are present
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.SEARCH_BAR
            ), "Search bar should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRODUCTS_GRID
            ), "Products grid should be present"

        with allure.step("Test products load"):
            self.ecommerce_page.wait_for_products_load()
            assert (
                self.ecommerce_page.get_product_count() > 0
            ), "Products should be loaded"

        with allure.step("Test search functionality"):
            self.ecommerce_page.search_products("laptop")
            assert self.ecommerce_page.wait_for_search_results(), "Search should work"

        with allure.step("Test filter functionality"):
            self.ecommerce_page.select_category("Electronics")
            assert self.ecommerce_page.wait_for_filtered_results(), "Filter should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Social basic functionality")
    @pytest.mark.smoke
    def test_social_basic_functionality(self):
        """Test Social basic functionality"""
        with allure.step("Test Social page loads"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Check critical elements are present
            assert self.social_page.is_element_present(
                *self.social_page.CREATE_POST_BUTTON
            ), "Create post button should be present"
            assert self.social_page.is_element_present(
                *self.social_page.FEED_CONTAINER
            ), "Feed container should be present"

        with allure.step("Test feed loads"):
            self.social_page.wait_for_feed_load()
            assert self.social_page.get_post_count() > 0, "Posts should be loaded"

        with allure.step("Test post creation"):
            self.social_page.click_create_post_button()
            assert (
                self.social_page.is_create_post_modal_visible()
            ), "Create post modal should be visible"

        with allure.step("Test like functionality"):
            self.social_page.like_post(0)
            assert self.social_page.wait_for_like_animation(), "Like should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Tasks basic functionality")
    @pytest.mark.smoke
    def test_tasks_basic_functionality(self):
        """Test Tasks basic functionality"""
        with allure.step("Test Tasks page loads"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Check critical elements are present
            assert self.tasks_page.is_element_present(
                *self.tasks_page.CREATE_TASK_BUTTON
            ), "Create task button should be present"
            assert self.tasks_page.is_element_present(
                *self.tasks_page.TASK_BOARD
            ), "Task board should be present"

        with allure.step("Test tasks load"):
            self.tasks_page.wait_for_task_board_load()
            assert self.tasks_page.get_task_count() > 0, "Tasks should be loaded"

        with allure.step("Test task creation"):
            self.tasks_page.click_create_task_button()
            assert (
                self.tasks_page.is_create_task_modal_visible()
            ), "Create task modal should be visible"

        with allure.step("Test task movement"):
            self.tasks_page.move_task_to_column(0, "In Progress")
            assert self.tasks_page.wait_for_task_moved(), "Task movement should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Content basic functionality")
    @pytest.mark.smoke
    def test_content_basic_functionality(self):
        """Test Content basic functionality"""
        with allure.step("Test Content page loads"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Check critical elements are present
            assert self.content_page.is_element_present(
                *self.content_page.CREATE_CONTENT_BUTTON
            ), "Create content button should be present"
            assert self.content_page.is_element_present(
                *self.content_page.CONTENT_LIST
            ), "Content list should be present"

        with allure.step("Test content loads"):
            self.content_page.wait_for_content_load()
            assert self.content_page.get_content_count() > 0, "Content should be loaded"

        with allure.step("Test content creation"):
            self.content_page.click_create_content_button()
            assert (
                self.content_page.is_create_content_modal_visible()
            ), "Create content modal should be visible"

        with allure.step("Test content preview"):
            self.content_page.click_preview_content_button(0)
            assert (
                self.content_page.is_preview_modal_visible()
            ), "Content preview should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Analytics basic functionality")
    @pytest.mark.smoke
    def test_analytics_basic_functionality(self):
        """Test Analytics basic functionality"""
        with allure.step("Test Analytics page loads"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # Check critical elements are present
            assert self.analytics_page.is_element_present(
                *self.analytics_page.DASHBOARD_CONTAINER
            ), "Dashboard container should be present"
            assert self.analytics_page.is_element_present(
                *self.analytics_page.CHARTS_CONTAINER
            ), "Charts container should be present"

        with allure.step("Test analytics loads"):
            self.analytics_page.wait_for_dashboard_load()
            assert (
                self.analytics_page.get_metric_count() > 0
            ), "Analytics should be loaded"

        with allure.step("Test date range filter"):
            self.analytics_page.select_date_range("Last 7 days")
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Date range filter should work"

        with allure.step("Test metric type filter"):
            self.analytics_page.select_metric_type("Revenue")
            assert (
                self.analytics_page.wait_for_filtered_analytics()
            ), "Metric type filter should work"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test API basic functionality")
    @pytest.mark.smoke
    def test_api_basic_functionality(self):
        """Test API basic functionality"""
        with allure.step("Test health check API"):
            response = self.api_client.get("/api/health")
            assert response.status_code == 200, "Health check API should return 200"
            assert response.json()["status"] == "ok", "API should be healthy"

        with allure.step("Test authentication API"):
            user_data = self.settings.get_user_credentials("regular_user")
            response = self.api_client.post(
                "/api/auth/login",
                {"email": user_data["email"], "password": user_data["password"]},
            )
            assert response.status_code == 200, "Authentication API should return 200"
            assert "access_token" in response.json(), "Login should return access token"

        with allure.step("Test get current user API"):
            response = self.api_client.get("/api/auth/me")
            assert response.status_code == 200, "Get current user API should return 200"
            assert (
                response.json()["email"] == user_data["email"]
            ), "Should return correct user email"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test data loading basic functionality")
    @pytest.mark.smoke
    def test_data_loading_basic_functionality(self):
        """Test data loading basic functionality"""
        with allure.step("Test E-commerce data loading"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            self.ecommerce_page.wait_for_products_load()
            assert (
                self.ecommerce_page.get_product_count() > 0
            ), "Products should be loaded"

        with allure.step("Test Social data loading"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            self.social_page.wait_for_feed_load()
            assert self.social_page.get_post_count() > 0, "Posts should be loaded"

        with allure.step("Test Tasks data loading"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"
            self.tasks_page.wait_for_task_board_load()
            assert self.tasks_page.get_task_count() > 0, "Tasks should be loaded"

        with allure.step("Test Content data loading"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"
            self.content_page.wait_for_content_load()
            assert self.content_page.get_content_count() > 0, "Content should be loaded"

        with allure.step("Test Analytics data loading"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            self.analytics_page.wait_for_dashboard_load()
            assert (
                self.analytics_page.get_metric_count() > 0
            ), "Analytics should be loaded"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test user interface basic functionality")
    @pytest.mark.smoke
    def test_user_interface_basic_functionality(self):
        """Test user interface basic functionality"""
        with allure.step("Test navigation elements"):
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

        with allure.step("Test form elements"):
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

        with allure.step("Test button elements"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test button elements
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.ECOMMERCE_CARD
            ), "E-commerce card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.SOCIAL_CARD
            ), "Social card should be present"
            assert self.dashboard_page.is_element_present(
                *self.dashboard_page.TASKS_CARD
            ), "Tasks card should be present"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test error handling basic functionality")
    @pytest.mark.smoke
    def test_error_handling_basic_functionality(self):
        """Test error handling basic functionality"""
        with allure.step("Test login error handling"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test invalid credentials
            self.login_page.login("invalid@example.com", "wrongpassword")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid credentials"

        with allure.step("Test form validation error handling"):
            # Test form validation
            self.login_page.login("", "")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for empty fields"

        with allure.step("Test API error handling"):
            # Test API error handling
            response = self.api_client.get("/api/nonexistent")
            assert (
                response.status_code == 404
            ), "Should return 404 for nonexistent endpoint"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test performance basic functionality")
    @pytest.mark.smoke
    def test_performance_basic_functionality(self):
        """Test performance basic functionality"""
        with allure.step("Test page load performance"):
            start_time = self.get_current_time()
            self.dashboard_page.navigate_to()
            self.dashboard_page.verify_page_loaded()
            end_time = self.get_current_time()

            load_time = end_time - start_time
            assert (
                load_time < 5.0
            ), f"Dashboard should load within 5 seconds, took {load_time:.2f}s"

        with allure.step("Test data loading performance"):
            start_time = self.get_current_time()
            self.ecommerce_page.navigate_to()
            self.ecommerce_page.wait_for_products_load()
            end_time = self.get_current_time()

            data_load_time = end_time - start_time
            assert (
                data_load_time < 5.0
            ), f"E-commerce data should load within 5 seconds, took {data_load_time:.2f}s"

        with allure.step("Test API response performance"):
            start_time = self.get_current_time()
            response = self.api_client.get("/api/health")
            end_time = self.get_current_time()

            api_time = end_time - start_time
            assert (
                api_time < 2.0
            ), f"Health check API should respond within 2 seconds, took {api_time:.2f}s"

    def get_current_time(self):
        """Get current timestamp in seconds"""
        import time

        return time.time()
