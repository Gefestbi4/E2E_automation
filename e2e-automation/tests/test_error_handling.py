"""
Error handling tests for the application
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
from utils.error_handling_testing import ErrorHandlingTesting


@allure.feature("Error Handling Tests")
@allure.story("Error Handling Testing")
class TestErrorHandling(BaseTest):
    """Test class for error handling testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestErrorHandling")
        self.error_handling_testing = ErrorHandlingTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test authentication error handling")
    @pytest.mark.error_handling
    def test_authentication_error_handling(self):
        """Test authentication error handling"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test invalid credentials error"):
            self.login_page.login("invalid@example.com", "wrongpassword")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid credentials"
            assert (
                "Invalid email or password" in self.login_page.get_error_message()
            ), "Should show correct error message"

        with allure.step("Test empty fields error"):
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

        with allure.step("Test invalid email format error"):
            self.login_page.login("invalid-email", "password")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for invalid email format"
            assert (
                "Invalid email format" in self.login_page.get_email_error_message()
            ), "Should show email format error"

        with allure.step("Test account locked error"):
            # Simulate multiple failed login attempts
            for i in range(5):
                self.login_page.login("test@example.com", "wrongpassword")
                if i < 4:
                    assert (
                        self.login_page.wait_for_error_message()
                    ), "Should show error for wrong password"
                else:
                    assert (
                        self.login_page.wait_for_account_locked_message()
                    ), "Account should be locked after multiple attempts"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test API error handling")
    @pytest.mark.error_handling
    def test_api_error_handling(self):
        """Test API error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test 400 Bad Request error"):
            response = self.api_client.post("/api/auth/login", {"invalid": "data"})
            assert response.status_code == 400, "Should return 400 for bad request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 401 Unauthorized error"):
            response = self.api_client.get("/api/auth/me")
            assert (
                response.status_code == 401
            ), "Should return 401 for unauthorized request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 403 Forbidden error"):
            response = self.api_client.get("/api/admin/users")
            assert (
                response.status_code == 403
            ), "Should return 403 for forbidden request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 404 Not Found error"):
            response = self.api_client.get("/api/nonexistent")
            assert (
                response.status_code == 404
            ), "Should return 404 for not found request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 500 Internal Server Error"):
            response = self.api_client.get("/api/error")
            assert (
                response.status_code == 500
            ), "Should return 500 for internal server error"
            assert "error" in response.json(), "Should return error message"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test form validation error handling")
    @pytest.mark.error_handling
    def test_form_validation_error_handling(self):
        """Test form validation error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce form validation"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test empty product search
            self.ecommerce_page.search_products("")
            assert (
                self.ecommerce_page.wait_for_validation_error()
            ), "Should show validation error for empty search"
            assert (
                "Search term is required" in self.ecommerce_page.get_validation_error()
            ), "Should show search required error"

        with allure.step("Test social form validation"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test empty post creation
            self.social_page.create_post({"content": ""})
            assert (
                self.social_page.wait_for_validation_error()
            ), "Should show validation error for empty post"
            assert (
                "Content is required" in self.social_page.get_validation_error()
            ), "Should show content required error"

        with allure.step("Test tasks form validation"):
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Test empty task creation
            self.tasks_page.create_task(
                {"title": "", "description": "Test description"}
            )
            assert (
                self.tasks_page.wait_for_validation_error()
            ), "Should show validation error for empty title"
            assert (
                "Title is required" in self.tasks_page.get_validation_error()
            ), "Should show title required error"

        with allure.step("Test content form validation"):
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Test empty article creation
            self.content_page.create_article({"title": "Test Title", "content": ""})
            assert (
                self.content_page.wait_for_validation_error()
            ), "Should show validation error for empty content"
            assert (
                "Content is required" in self.content_page.get_validation_error()
            ), "Should show content required error"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test network error handling")
    @pytest.mark.error_handling
    def test_network_error_handling(self):
        """Test network error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test connection timeout error"):
            # Simulate connection timeout
            self.error_handling_testing.simulate_connection_timeout()
            assert (
                self.error_handling_testing.wait_for_timeout_error()
            ), "Should show timeout error"
            assert (
                "Connection timeout" in self.error_handling_testing.get_error_message()
            ), "Should show timeout error message"

        with allure.step("Test network unreachable error"):
            # Simulate network unreachable
            self.error_handling_testing.simulate_network_unreachable()
            assert (
                self.error_handling_testing.wait_for_network_error()
            ), "Should show network error"
            assert (
                "Network unreachable" in self.error_handling_testing.get_error_message()
            ), "Should show network error message"

        with allure.step("Test DNS resolution error"):
            # Simulate DNS resolution error
            self.error_handling_testing.simulate_dns_error()
            assert (
                self.error_handling_testing.wait_for_dns_error()
            ), "Should show DNS error"
            assert (
                "DNS resolution failed"
                in self.error_handling_testing.get_error_message()
            ), "Should show DNS error message"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test database error handling")
    @pytest.mark.error_handling
    def test_database_error_handling(self):
        """Test database error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test database connection error"):
            # Simulate database connection error
            self.error_handling_testing.simulate_database_connection_error()
            assert (
                self.error_handling_testing.wait_for_database_error()
            ), "Should show database error"
            assert (
                "Database connection failed"
                in self.error_handling_testing.get_error_message()
            ), "Should show database error message"

        with allure.step("Test database query timeout error"):
            # Simulate database query timeout
            self.error_handling_testing.simulate_database_query_timeout()
            assert (
                self.error_handling_testing.wait_for_query_timeout_error()
            ), "Should show query timeout error"
            assert (
                "Query timeout" in self.error_handling_testing.get_error_message()
            ), "Should show query timeout error message"

        with allure.step("Test database constraint violation error"):
            # Simulate database constraint violation
            self.error_handling_testing.simulate_database_constraint_violation()
            assert (
                self.error_handling_testing.wait_for_constraint_violation_error()
            ), "Should show constraint violation error"
            assert (
                "Constraint violation"
                in self.error_handling_testing.get_error_message()
            ), "Should show constraint violation error message"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test user interface error handling")
    @pytest.mark.error_handling
    def test_user_interface_error_handling(self):
        """Test user interface error handling"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test page load error"):
            # Simulate page load error
            self.error_handling_testing.simulate_page_load_error()
            assert (
                self.error_handling_testing.wait_for_page_load_error()
            ), "Should show page load error"
            assert (
                "Page failed to load" in self.error_handling_testing.get_error_message()
            ), "Should show page load error message"

        with allure.step("Test JavaScript error"):
            # Simulate JavaScript error
            self.error_handling_testing.simulate_javascript_error()
            assert (
                self.error_handling_testing.wait_for_javascript_error()
            ), "Should show JavaScript error"
            assert (
                "JavaScript error" in self.error_handling_testing.get_error_message()
            ), "Should show JavaScript error message"

        with allure.step("Test CSS loading error"):
            # Simulate CSS loading error
            self.error_handling_testing.simulate_css_loading_error()
            assert (
                self.error_handling_testing.wait_for_css_loading_error()
            ), "Should show CSS loading error"
            assert (
                "CSS failed to load" in self.error_handling_testing.get_error_message()
            ), "Should show CSS loading error message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test error recovery")
    @pytest.mark.error_handling
    def test_error_recovery(self):
        """Test error recovery"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test automatic retry"):
            # Test automatic retry mechanism
            assert (
                self.error_handling_testing.test_automatic_retry()
            ), "Automatic retry should work"

            # Test retry limit
            assert (
                self.error_handling_testing.test_retry_limit()
            ), "Retry limit should be enforced"

        with allure.step("Test fallback mechanisms"):
            # Test fallback mechanisms
            assert (
                self.error_handling_testing.test_fallback_mechanisms()
            ), "Fallback mechanisms should work"

            # Test graceful degradation
            assert (
                self.error_handling_testing.test_graceful_degradation()
            ), "Graceful degradation should work"

        with allure.step("Test error notification"):
            # Test error notification
            assert (
                self.error_handling_testing.test_error_notification()
            ), "Error notification should work"

            # Test error reporting
            assert (
                self.error_handling_testing.test_error_reporting()
            ), "Error reporting should work"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test error logging")
    @pytest.mark.error_handling
    def test_error_logging(self):
        """Test error logging"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test error logging"):
            # Test error logging
            assert (
                self.error_handling_testing.test_error_logging()
            ), "Error logging should work"

            # Test log levels
            assert (
                self.error_handling_testing.test_log_levels()
            ), "Log levels should be properly set"

        with allure.step("Test error monitoring"):
            # Test error monitoring
            assert (
                self.error_handling_testing.test_error_monitoring()
            ), "Error monitoring should work"

            # Test error alerting
            assert (
                self.error_handling_testing.test_error_alerting()
            ), "Error alerting should work"

        with allure.step("Test error analytics"):
            # Test error analytics
            analytics = self.error_handling_testing.collect_error_analytics()
            assert "error_count" in analytics, "Error count should be collected"
            assert "error_types" in analytics, "Error types should be collected"
            assert "error_frequency" in analytics, "Error frequency should be collected"
