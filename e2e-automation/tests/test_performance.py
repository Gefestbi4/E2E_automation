"""
Performance tests for the application
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
from utils.performance_testing import PerformanceTesting


@allure.feature("Performance Tests")
@allure.story("Performance Testing")
class TestPerformance(BaseTest):
    """Test class for performance testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestPerformance")
        self.performance_testing = PerformanceTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test page load performance")
    @pytest.mark.performance
    def test_page_load_performance(self):
        """Test page load performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard load performance"):
            start_time = self.performance_testing.get_current_time()
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"Dashboard should load within 3 seconds, actual: {load_time}s"

        with allure.step("Test e-commerce load performance"):
            start_time = self.performance_testing.get_current_time()
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"E-commerce page should load within 3 seconds, actual: {load_time}s"

        with allure.step("Test social load performance"):
            start_time = self.performance_testing.get_current_time()
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"Social page should load within 3 seconds, actual: {load_time}s"

        with allure.step("Test tasks load performance"):
            start_time = self.performance_testing.get_current_time()
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"Tasks page should load within 3 seconds, actual: {load_time}s"

        with allure.step("Test content load performance"):
            start_time = self.performance_testing.get_current_time()
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"Content page should load within 3 seconds, actual: {load_time}s"

        with allure.step("Test analytics load performance"):
            start_time = self.performance_testing.get_current_time()
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"
            load_time = self.performance_testing.get_current_time() - start_time
            assert (
                load_time < 3
            ), f"Analytics page should load within 3 seconds, actual: {load_time}s"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test API response performance")
    @pytest.mark.performance
    def test_api_response_performance(self):
        """Test API response performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test authentication API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/auth/me")
            assert response.status_code == 200, "Auth API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"Auth API should respond within 1 second, actual: {response_time}s"

        with allure.step("Test e-commerce API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/ecommerce/products")
            assert response.status_code == 200, "E-commerce API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"E-commerce API should respond within 1 second, actual: {response_time}s"

        with allure.step("Test social API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/social/posts")
            assert response.status_code == 200, "Social API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"Social API should respond within 1 second, actual: {response_time}s"

        with allure.step("Test tasks API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/tasks")
            assert response.status_code == 200, "Tasks API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"Tasks API should respond within 1 second, actual: {response_time}s"

        with allure.step("Test content API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Content API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"Content API should respond within 1 second, actual: {response_time}s"

        with allure.step("Test analytics API performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/analytics/metrics")
            assert response.status_code == 200, "Analytics API should return 200"
            response_time = self.performance_testing.get_current_time() - start_time
            assert (
                response_time < 1
            ), f"Analytics API should respond within 1 second, actual: {response_time}s"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test database query performance")
    @pytest.mark.performance
    def test_database_query_performance(self):
        """Test database query performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test user data query performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/auth/me")
            assert response.status_code == 200, "User data API should return 200"
            query_time = self.performance_testing.get_current_time() - start_time
            assert (
                query_time < 0.5
            ), f"User data query should complete within 0.5 seconds, actual: {query_time}s"

        with allure.step("Test products query performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/ecommerce/products")
            assert response.status_code == 200, "Products API should return 200"
            query_time = self.performance_testing.get_current_time() - start_time
            assert (
                query_time < 0.5
            ), f"Products query should complete within 0.5 seconds, actual: {query_time}s"

        with allure.step("Test posts query performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/social/posts")
            assert response.status_code == 200, "Posts API should return 200"
            query_time = self.performance_testing.get_current_time() - start_time
            assert (
                query_time < 0.5
            ), f"Posts query should complete within 0.5 seconds, actual: {query_time}s"

        with allure.step("Test tasks query performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/tasks")
            assert response.status_code == 200, "Tasks API should return 200"
            query_time = self.performance_testing.get_current_time() - start_time
            assert (
                query_time < 0.5
            ), f"Tasks query should complete within 0.5 seconds, actual: {query_time}s"

        with allure.step("Test articles query performance"):
            start_time = self.performance_testing.get_current_time()
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Articles API should return 200"
            query_time = self.performance_testing.get_current_time() - start_time
            assert (
                query_time < 0.5
            ), f"Articles query should complete within 0.5 seconds, actual: {query_time}s"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test memory usage performance")
    @pytest.mark.performance
    def test_memory_usage_performance(self):
        """Test memory usage performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test initial memory usage"):
            initial_memory = self.performance_testing.get_memory_usage()
            assert (
                initial_memory < 100
            ), f"Initial memory usage should be less than 100MB, actual: {initial_memory}MB"

        with allure.step("Test memory usage after navigation"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            memory_after_navigation = self.performance_testing.get_memory_usage()
            assert (
                memory_after_navigation < 200
            ), f"Memory usage after navigation should be less than 200MB, actual: {memory_after_navigation}MB"

        with allure.step("Test memory usage after data operations"):
            # Perform data operations
            self.ecommerce_page.add_to_cart(self.ecommerce_page.get_first_product())
            assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"

            self.social_page.create_post(self.settings.get_post_data())
            assert self.social_page.wait_for_post_created(), "Post should be created"

            memory_after_operations = self.performance_testing.get_memory_usage()
            assert (
                memory_after_operations < 300
            ), f"Memory usage after operations should be less than 300MB, actual: {memory_after_operations}MB"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test concurrent user performance")
    @pytest.mark.performance
    def test_concurrent_user_performance(self):
        """Test concurrent user performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test concurrent API calls"):
            # Simulate concurrent API calls
            concurrent_calls = 10
            start_time = self.performance_testing.get_current_time()

            for i in range(concurrent_calls):
                response = self.api_client.get("/api/auth/me")
                assert (
                    response.status_code == 200
                ), f"Concurrent API call {i+1} should return 200"

            total_time = self.performance_testing.get_current_time() - start_time
            avg_time_per_call = total_time / concurrent_calls
            assert (
                avg_time_per_call < 1
            ), f"Average time per concurrent API call should be less than 1 second, actual: {avg_time_per_call}s"

        with allure.step("Test concurrent page loads"):
            # Simulate concurrent page loads
            concurrent_loads = 5
            start_time = self.performance_testing.get_current_time()

            for i in range(concurrent_loads):
                self.dashboard_page.navigate_to()
                assert (
                    self.dashboard_page.verify_page_loaded()
                ), f"Concurrent page load {i+1} should succeed"

            total_time = self.performance_testing.get_current_time() - start_time
            avg_time_per_load = total_time / concurrent_loads
            assert (
                avg_time_per_load < 3
            ), f"Average time per concurrent page load should be less than 3 seconds, actual: {avg_time_per_load}s"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test performance under load")
    @pytest.mark.performance
    def test_performance_under_load(self):
        """Test performance under load"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test performance under high load"):
            # Simulate high load
            high_load_operations = 50
            start_time = self.performance_testing.get_current_time()

            for i in range(high_load_operations):
                response = self.api_client.get("/api/auth/me")
                assert (
                    response.status_code == 200
                ), f"High load API call {i+1} should return 200"

            total_time = self.performance_testing.get_current_time() - start_time
            avg_time_per_operation = total_time / high_load_operations
            assert (
                avg_time_per_operation < 2
            ), f"Average time per high load operation should be less than 2 seconds, actual: {avg_time_per_operation}s"

        with allure.step("Test performance degradation under load"):
            # Test performance degradation
            initial_response_time = self.performance_testing.measure_api_response_time(
                "/api/auth/me"
            )

            # Apply load
            for i in range(20):
                self.api_client.get("/api/auth/me")

            # Measure response time under load
            loaded_response_time = self.performance_testing.measure_api_response_time(
                "/api/auth/me"
            )

            # Performance should not degrade significantly
            performance_degradation = (
                loaded_response_time - initial_response_time
            ) / initial_response_time
            assert (
                performance_degradation < 0.5
            ), f"Performance degradation should be less than 50%, actual: {performance_degradation*100}%"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test performance monitoring")
    @pytest.mark.performance
    def test_performance_monitoring(self):
        """Test performance monitoring"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test performance metrics collection"):
            # Test performance metrics collection
            metrics = self.performance_testing.collect_performance_metrics()
            assert "page_load_times" in metrics, "Page load times should be collected"
            assert (
                "api_response_times" in metrics
            ), "API response times should be collected"
            assert "memory_usage" in metrics, "Memory usage should be collected"
            assert "cpu_usage" in metrics, "CPU usage should be collected"

        with allure.step("Test performance alerts"):
            # Test performance alerts
            alerts = self.performance_testing.check_performance_alerts()
            assert (
                len(alerts) == 0
            ), f"No performance alerts should be triggered, actual: {alerts}"

        with allure.step("Test performance reporting"):
            # Test performance reporting
            report = self.performance_testing.generate_performance_report()
            assert "summary" in report, "Performance report should have summary"
            assert "metrics" in report, "Performance report should have metrics"
            assert (
                "recommendations" in report
            ), "Performance report should have recommendations"
