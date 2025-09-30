"""
Sanity tests for the application
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


@allure.feature("Sanity Tests")
@allure.story("Sanity Testing")
class TestSanity(BaseTest):
    """Test class for sanity testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestSanity")
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
    @allure.description("Application sanity check")
    @pytest.mark.sanity
    def test_application_sanity(self):
        """Test application sanity"""
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("E-commerce sanity check")
    @pytest.mark.sanity
    def test_ecommerce_sanity(self):
        """Test E-commerce sanity"""
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Social sanity check")
    @pytest.mark.sanity
    def test_social_sanity(self):
        """Test Social sanity"""
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Tasks sanity check")
    @pytest.mark.sanity
    def test_tasks_sanity(self):
        """Test Tasks sanity"""
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Content sanity check")
    @pytest.mark.sanity
    def test_content_sanity(self):
        """Test Content sanity"""
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Analytics sanity check")
    @pytest.mark.sanity
    def test_analytics_sanity(self):
        """Test Analytics sanity"""
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

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Data consistency sanity check")
    @pytest.mark.sanity
    def test_data_consistency_sanity(self):
        """Test data consistency sanity"""
        with allure.step("Test data loads consistently"):
            # Test data loading across modules
            self.ecommerce_page.navigate_to()
            self.ecommerce_page.wait_for_products_load()
            ecommerce_products = self.ecommerce_page.get_product_count()

            self.social_page.navigate_to()
            self.social_page.wait_for_feed_load()
            social_posts = self.social_page.get_post_count()

            self.tasks_page.navigate_to()
            self.tasks_page.wait_for_task_board_load()
            tasks_count = self.tasks_page.get_task_count()

            self.content_page.navigate_to()
            self.content_page.wait_for_content_load()
            content_count = self.content_page.get_content_count()

            self.analytics_page.navigate_to()
            self.analytics_page.wait_for_dashboard_load()
            analytics_metrics = self.analytics_page.get_metric_count()

            # Data should be consistent
            assert ecommerce_products > 0, "E-commerce should have products"
            assert social_posts > 0, "Social should have posts"
            assert tasks_count > 0, "Tasks should have tasks"
            assert content_count > 0, "Content should have content"
            assert analytics_metrics > 0, "Analytics should have metrics"

        with allure.step("Test user session consistency"):
            # Test user session across modules
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in"

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

            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # User should remain logged in
            assert (
                self.analytics_page.get_logged_in_username() != "Guest"
            ), "User should remain logged in"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Performance sanity check")
    @pytest.mark.sanity
    def test_performance_sanity(self):
        """Test performance sanity"""
        with allure.step("Test page load performance"):
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

            start_time = self.get_current_time()
            self.tasks_page.navigate_to()
            self.tasks_page.verify_page_loaded()
            tasks_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.content_page.navigate_to()
            self.content_page.verify_page_loaded()
            content_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.analytics_page.navigate_to()
            self.analytics_page.verify_page_loaded()
            analytics_time = self.get_current_time() - start_time

            # Check performance thresholds
            assert (
                dashboard_time < 5.0
            ), f"Dashboard should load within 5 seconds, took {dashboard_time:.2f}s"
            assert (
                ecommerce_time < 8.0
            ), f"E-commerce should load within 8 seconds, took {ecommerce_time:.2f}s"
            assert (
                social_time < 8.0
            ), f"Social should load within 8 seconds, took {social_time:.2f}s"
            assert (
                tasks_time < 8.0
            ), f"Tasks should load within 8 seconds, took {tasks_time:.2f}s"
            assert (
                content_time < 8.0
            ), f"Content should load within 8 seconds, took {content_time:.2f}s"
            assert (
                analytics_time < 10.0
            ), f"Analytics should load within 10 seconds, took {analytics_time:.2f}s"

        with allure.step("Test data loading performance"):
            # Test data loading performance
            start_time = self.get_current_time()
            self.ecommerce_page.navigate_to()
            self.ecommerce_page.wait_for_products_load()
            ecommerce_data_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.social_page.navigate_to()
            self.social_page.wait_for_feed_load()
            social_data_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.tasks_page.navigate_to()
            self.tasks_page.wait_for_task_board_load()
            tasks_data_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.content_page.navigate_to()
            self.content_page.wait_for_content_load()
            content_data_time = self.get_current_time() - start_time

            start_time = self.get_current_time()
            self.analytics_page.navigate_to()
            self.analytics_page.wait_for_dashboard_load()
            analytics_data_time = self.get_current_time() - start_time

            # Check data loading performance thresholds
            assert (
                ecommerce_data_time < 5.0
            ), f"E-commerce data should load within 5 seconds, took {ecommerce_data_time:.2f}s"
            assert (
                social_data_time < 5.0
            ), f"Social data should load within 5 seconds, took {social_data_time:.2f}s"
            assert (
                tasks_data_time < 5.0
            ), f"Tasks data should load within 5 seconds, took {tasks_data_time:.2f}s"
            assert (
                content_data_time < 5.0
            ), f"Content data should load within 5 seconds, took {content_data_time:.2f}s"
            assert (
                analytics_data_time < 8.0
            ), f"Analytics data should load within 8 seconds, took {analytics_data_time:.2f}s"

    def get_current_time(self):
        """Get current timestamp in seconds"""
        import time

        return time.time()

    @allure.severity(allure.severity_level.LOW)
    @allure.description("UI sanity check")
    @pytest.mark.sanity
    def test_ui_sanity(self):
        """Test UI sanity"""
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
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test form elements
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.SEARCH_BAR
            ), "Search bar should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.CATEGORY_FILTER
            ), "Category filter should be present"
            assert self.ecommerce_page.is_element_present(
                *self.ecommerce_page.PRICE_RANGE_FILTER
            ), "Price range filter should be present"

        with allure.step("Test button elements"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test button elements
            assert self.social_page.is_element_present(
                *self.social_page.CREATE_POST_BUTTON
            ), "Create post button should be present"
            assert self.social_page.is_element_present(
                *self.social_page.LIKE_BUTTON
            ), "Like button should be present"
            assert self.social_page.is_element_present(
                *self.social_page.COMMENT_BUTTON
            ), "Comment button should be present"

        with allure.step("Test modal elements"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Test modal elements
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

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Error handling sanity check")
    @pytest.mark.sanity
    def test_error_handling_sanity(self):
        """Test error handling sanity"""
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
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test empty search
            self.ecommerce_page.search_products("")
            assert (
                self.ecommerce_page.wait_for_validation_error()
            ), "Should show validation error for empty search"

        with allure.step("Test network error handling"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test network error handling
            self.social_page.click_create_post_button()
            self.social_page.fill_post_content("!@#$%^&*()")
            self.social_page.submit_post()
            # Should handle network error gracefully
