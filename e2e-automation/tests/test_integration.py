"""
Integration tests for the application
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
from utils.integration_testing import IntegrationTesting


@allure.feature("Integration Tests")
@allure.story("Integration Testing")
class TestIntegration(BaseTest):
    """Test class for integration testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestIntegration")
        self.integration_testing = IntegrationTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test end-to-end user workflow")
    @pytest.mark.integration
    def test_end_to_end_user_workflow(self):
        """Test end-to-end user workflow"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard loads"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in"

        with allure.step("Test e-commerce workflow"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Add product to cart
            product = self.ecommerce_page.get_first_product()
            self.ecommerce_page.add_to_cart(product)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
            assert self.ecommerce_page.get_cart_count() > 0, "Cart should have items"

        with allure.step("Test social workflow"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Create a post
            post_data = self.settings.get_post_data()
            self.social_page.create_post(post_data)
            assert self.social_page.wait_for_post_created(), "Post should be created"
            assert self.social_page.is_post_displayed(
                post_data
            ), "Post should be displayed"

        with allure.step("Test tasks workflow"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Create a task
            task_data = self.settings.get_task_data()
            self.tasks_page.create_task(task_data)
            assert self.tasks_page.wait_for_task_created(), "Task should be created"
            assert self.tasks_page.is_task_displayed(
                task_data
            ), "Task should be displayed"

        with allure.step("Test content workflow"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Create an article
            article_data = self.settings.get_article_data()
            self.content_page.create_article(article_data)
            assert (
                self.content_page.wait_for_article_created()
            ), "Article should be created"
            assert self.content_page.is_article_displayed(
                article_data
            ), "Article should be displayed"

        with allure.step("Test analytics workflow"):
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # Check analytics dashboard
            assert (
                self.analytics_page.is_dashboard_loaded()
            ), "Analytics dashboard should load"
            assert self.analytics_page.get_metrics_count() > 0, "Should have metrics"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test cross-module data consistency")
    @pytest.mark.integration
    def test_cross_module_data_consistency(self):
        """Test cross-module data consistency"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test user data consistency across modules"):
            # Check user data in dashboard
            dashboard_username = self.dashboard_page.get_logged_in_username()

            # Check user data in e-commerce
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            ecommerce_username = self.ecommerce_page.get_logged_in_username()
            assert (
                ecommerce_username == dashboard_username
            ), "Username should be consistent across modules"

            # Check user data in social
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            social_username = self.social_page.get_logged_in_username()
            assert (
                social_username == dashboard_username
            ), "Username should be consistent across modules"

        with allure.step("Test session consistency across modules"):
            # Check session in dashboard
            assert (
                self.dashboard_page.is_session_created()
            ), "Session should be created in dashboard"

            # Check session in e-commerce
            assert (
                self.ecommerce_page.is_session_created()
            ), "Session should be created in e-commerce"

            # Check session in social
            assert (
                self.social_page.is_session_created()
            ), "Session should be created in social"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test module navigation")
    @pytest.mark.integration
    def test_module_navigation(self):
        """Test module navigation"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test navigation from dashboard to e-commerce"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            self.dashboard_page.click_ecommerce_card()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

        with allure.step("Test navigation from e-commerce to social"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            self.ecommerce_page.navigate_to_social()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

        with allure.step("Test navigation from social to tasks"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            self.social_page.navigate_to_tasks()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

        with allure.step("Test navigation from tasks to content"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            self.tasks_page.navigate_to_content()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

        with allure.step("Test navigation from content to analytics"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            self.content_page.navigate_to_analytics()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test data flow between modules")
    @pytest.mark.integration
    def test_data_flow_between_modules(self):
        """Test data flow between modules"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce to analytics data flow"):
            # Create e-commerce data
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            product = self.ecommerce_page.get_first_product()
            self.ecommerce_page.add_to_cart(product)
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"

            # Check analytics reflects e-commerce data
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            assert self.analytics_page.is_metric_displayed(
                "total_revenue"
            ), "Total revenue metric should be displayed"
            assert (
                self.analytics_page.get_metric_value("total_revenue") > 0
            ), "Total revenue should be positive"

        with allure.step("Test social to analytics data flow"):
            # Create social data
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            post_data = self.settings.get_post_data()
            self.social_page.create_post(post_data)
            assert self.social_page.wait_for_post_created(), "Post should be created"

            # Check analytics reflects social data
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            assert self.analytics_page.is_metric_displayed(
                "total_posts"
            ), "Total posts metric should be displayed"
            assert (
                self.analytics_page.get_metric_value("total_posts") > 0
            ), "Total posts should be positive"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test error propagation between modules")
    @pytest.mark.integration
    def test_error_propagation_between_modules(self):
        """Test error propagation between modules"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test error in e-commerce affects analytics"):
            # Create error in e-commerce
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            self.ecommerce_page.add_to_cart("invalid_product")
            assert (
                self.ecommerce_page.wait_for_error_message()
            ), "Should show error for invalid product"

            # Check analytics handles error gracefully
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            assert (
                self.analytics_page.is_dashboard_loaded()
            ), "Analytics dashboard should still load"

        with allure.step("Test error in social affects analytics"):
            # Create error in social
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            self.social_page.create_post({"content": ""})
            assert (
                self.social_page.wait_for_validation_error()
            ), "Should show validation error for empty post"

            # Check analytics handles error gracefully
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            assert (
                self.analytics_page.is_dashboard_loaded()
            ), "Analytics dashboard should still load"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test performance across modules")
    @pytest.mark.integration
    def test_performance_across_modules(self):
        """Test performance across modules"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test page load times"):
            # Test dashboard load time
            start_time = self.dashboard_page.get_current_time()
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            dashboard_load_time = self.dashboard_page.get_current_time() - start_time
            assert dashboard_load_time < 5, "Dashboard should load within 5 seconds"

            # Test e-commerce load time
            start_time = self.ecommerce_page.get_current_time()
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            ecommerce_load_time = self.ecommerce_page.get_current_time() - start_time
            assert (
                ecommerce_load_time < 5
            ), "E-commerce page should load within 5 seconds"

            # Test social load time
            start_time = self.social_page.get_current_time()
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            social_load_time = self.social_page.get_current_time() - start_time
            assert social_load_time < 5, "Social page should load within 5 seconds"

        with allure.step("Test API response times"):
            # Test API response times
            api_response_times = self.integration_testing.measure_api_response_times()
            for endpoint, response_time in api_response_times.items():
                assert (
                    response_time < 2
                ), f"API {endpoint} should respond within 2 seconds"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test integration API")
    @pytest.mark.integration
    def test_integration_api(self):
        """Test integration API"""
        with allure.step("Test cross-module API calls"):
            # Test e-commerce API
            response = self.api_client.get("/api/ecommerce/products")
            assert response.status_code == 200, "E-commerce API should return 200"

            # Test social API
            response = self.api_client.get("/api/social/posts")
            assert response.status_code == 200, "Social API should return 200"

            # Test tasks API
            response = self.api_client.get("/api/tasks")
            assert response.status_code == 200, "Tasks API should return 200"

            # Test content API
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Content API should return 200"

            # Test analytics API
            response = self.api_client.get("/api/analytics/metrics")
            assert response.status_code == 200, "Analytics API should return 200"

        with allure.step("Test API data consistency"):
            # Test user data consistency across APIs
            user_response = self.api_client.get("/api/auth/me")
            assert user_response.status_code == 200, "User API should return 200"
            user_data = user_response.json()

            # Test e-commerce user data
            ecommerce_response = self.api_client.get("/api/ecommerce/user")
            assert (
                ecommerce_response.status_code == 200
            ), "E-commerce user API should return 200"
            ecommerce_user_data = ecommerce_response.json()
            assert (
                ecommerce_user_data["id"] == user_data["id"]
            ), "User ID should be consistent across APIs"

            # Test social user data
            social_response = self.api_client.get("/api/social/user")
            assert (
                social_response.status_code == 200
            ), "Social user API should return 200"
            social_user_data = social_response.json()
            assert (
                social_user_data["id"] == user_data["id"]
            ), "User ID should be consistent across APIs"
