"""
API integration tests for the application
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
from utils.api_integration_testing import APIIntegrationTesting


@allure.feature("API Integration Tests")
@allure.story("API Integration Testing")
class TestAPIIntegration(BaseTest):
    """Test class for API integration testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestAPIIntegration")
        self.api_integration_testing = APIIntegrationTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test authentication API integration")
    @pytest.mark.api_integration
    def test_authentication_api_integration(self):
        """Test authentication API integration"""
        with allure.step("Test login API"):
            # Test login API
            response = self.api_client.post(
                "/api/auth/login",
                {"email": "test@example.com", "password": "testpassword123"},
            )
            assert response.status_code == 200, "Login API should return 200"
            assert "access_token" in response.json(), "Login should return access token"
            assert (
                "refresh_token" in response.json()
            ), "Login should return refresh token"

        with allure.step("Test get current user API"):
            # Test get current user API
            response = self.api_client.get("/api/auth/me")
            assert response.status_code == 200, "Get current user API should return 200"
            assert "email" in response.json(), "User should have email"
            assert "username" in response.json(), "User should have username"

        with allure.step("Test refresh token API"):
            # Test refresh token API
            response = self.api_client.post(
                "/api/auth/refresh", {"refresh_token": "test_refresh_token"}
            )
            assert response.status_code == 200, "Refresh token API should return 200"
            assert (
                "access_token" in response.json()
            ), "Refresh should return new access token"

        with allure.step("Test logout API"):
            # Test logout API
            response = self.api_client.post("/api/auth/logout")
            assert response.status_code == 200, "Logout API should return 200"
            assert "message" in response.json(), "Logout should return message"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test e-commerce API integration")
    @pytest.mark.api_integration
    def test_ecommerce_api_integration(self):
        """Test e-commerce API integration"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test products API"):
            # Test products API
            response = self.api_client.get("/api/ecommerce/products")
            assert response.status_code == 200, "Products API should return 200"
            assert len(response.json()) > 0, "Should have products"
            assert all(
                "id" in product for product in response.json()
            ), "All products should have ID"
            assert all(
                "name" in product for product in response.json()
            ), "All products should have name"

        with allure.step("Test product details API"):
            # Test product details API
            response = self.api_client.get("/api/ecommerce/products/1")
            assert response.status_code == 200, "Product details API should return 200"
            assert "id" in response.json(), "Product should have ID"
            assert "name" in response.json(), "Product should have name"
            assert "price" in response.json(), "Product should have price"

        with allure.step("Test cart API"):
            # Test cart API
            response = self.api_client.get("/api/ecommerce/cart")
            assert response.status_code == 200, "Cart API should return 200"
            assert "items" in response.json(), "Cart should have items"

        with allure.step("Test add to cart API"):
            # Test add to cart API
            response = self.api_client.post(
                "/api/ecommerce/cart/add", {"product_id": 1, "quantity": 1}
            )
            assert response.status_code == 200, "Add to cart API should return 200"
            assert "message" in response.json(), "Should return success message"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test social API integration")
    @pytest.mark.api_integration
    def test_social_api_integration(self):
        """Test social API integration"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test posts API"):
            # Test posts API
            response = self.api_client.get("/api/social/posts")
            assert response.status_code == 200, "Posts API should return 200"
            assert len(response.json()) > 0, "Should have posts"
            assert all(
                "id" in post for post in response.json()
            ), "All posts should have ID"
            assert all(
                "content" in post for post in response.json()
            ), "All posts should have content"

        with allure.step("Test create post API"):
            # Test create post API
            response = self.api_client.post(
                "/api/social/posts", {"content": "Test post content"}
            )
            assert response.status_code == 201, "Create post API should return 201"
            assert "id" in response.json(), "Post should have ID"
            assert (
                response.json()["content"] == "Test post content"
            ), "Post content should match"

        with allure.step("Test like post API"):
            # Test like post API
            response = self.api_client.post("/api/social/posts/1/like")
            assert response.status_code == 200, "Like post API should return 200"
            assert "message" in response.json(), "Should return success message"

        with allure.step("Test comment API"):
            # Test comment API
            response = self.api_client.post(
                "/api/social/posts/1/comments", {"content": "Test comment content"}
            )
            assert response.status_code == 201, "Comment API should return 201"
            assert "id" in response.json(), "Comment should have ID"
            assert (
                response.json()["content"] == "Test comment content"
            ), "Comment content should match"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test tasks API integration")
    @pytest.mark.api_integration
    def test_tasks_api_integration(self):
        """Test tasks API integration"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks API"):
            # Test tasks API
            response = self.api_client.get("/api/tasks")
            assert response.status_code == 200, "Tasks API should return 200"
            assert len(response.json()) > 0, "Should have tasks"
            assert all(
                "id" in task for task in response.json()
            ), "All tasks should have ID"
            assert all(
                "title" in task for task in response.json()
            ), "All tasks should have title"

        with allure.step("Test create task API"):
            # Test create task API
            response = self.api_client.post(
                "/api/tasks",
                {
                    "title": "Test task",
                    "description": "Test task description",
                    "priority": "high",
                },
            )
            assert response.status_code == 201, "Create task API should return 201"
            assert "id" in response.json(), "Task should have ID"
            assert response.json()["title"] == "Test task", "Task title should match"

        with allure.step("Test update task API"):
            # Test update task API
            response = self.api_client.put("/api/tasks/1", {"status": "in_progress"})
            assert response.status_code == 200, "Update task API should return 200"
            assert (
                response.json()["status"] == "in_progress"
            ), "Task status should be updated"

        with allure.step("Test assign task API"):
            # Test assign task API
            response = self.api_client.post(
                "/api/tasks/1/assign", {"assignee": "admin_user"}
            )
            assert response.status_code == 200, "Assign task API should return 200"
            assert "message" in response.json(), "Should return success message"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test content API integration")
    @pytest.mark.api_integration
    def test_content_api_integration(self):
        """Test content API integration"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test articles API"):
            # Test articles API
            response = self.api_client.get("/api/content/articles")
            assert response.status_code == 200, "Articles API should return 200"
            assert len(response.json()) > 0, "Should have articles"
            assert all(
                "id" in article for article in response.json()
            ), "All articles should have ID"
            assert all(
                "title" in article for article in response.json()
            ), "All articles should have title"

        with allure.step("Test create article API"):
            # Test create article API
            response = self.api_client.post(
                "/api/content/articles",
                {
                    "title": "Test article",
                    "content": "Test article content",
                    "category": "Technology",
                },
            )
            assert response.status_code == 201, "Create article API should return 201"
            assert "id" in response.json(), "Article should have ID"
            assert (
                response.json()["title"] == "Test article"
            ), "Article title should match"

        with allure.step("Test update article API"):
            # Test update article API
            response = self.api_client.put(
                "/api/content/articles/1", {"title": "Updated article title"}
            )
            assert response.status_code == 200, "Update article API should return 200"
            assert (
                response.json()["title"] == "Updated article title"
            ), "Article title should be updated"

        with allure.step("Test publish article API"):
            # Test publish article API
            response = self.api_client.post("/api/content/articles/1/publish")
            assert response.status_code == 200, "Publish article API should return 200"
            assert (
                response.json()["status"] == "published"
            ), "Article status should be published"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test analytics API integration")
    @pytest.mark.api_integration
    def test_analytics_api_integration(self):
        """Test analytics API integration"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test metrics API"):
            # Test metrics API
            response = self.api_client.get("/api/analytics/metrics")
            assert response.status_code == 200, "Metrics API should return 200"
            assert len(response.json()) > 0, "Should have metrics"
            assert all(
                "name" in metric for metric in response.json()
            ), "All metrics should have name"
            assert all(
                "value" in metric for metric in response.json()
            ), "All metrics should have value"

        with allure.step("Test charts API"):
            # Test charts API
            response = self.api_client.get("/api/analytics/charts")
            assert response.status_code == 200, "Charts API should return 200"
            assert len(response.json()) > 0, "Should have charts"
            assert all(
                "name" in chart for chart in response.json()
            ), "All charts should have name"
            assert all(
                "data" in chart for chart in response.json()
            ), "All charts should have data"

        with allure.step("Test reports API"):
            # Test reports API
            response = self.api_client.get("/api/analytics/reports")
            assert response.status_code == 200, "Reports API should return 200"
            assert len(response.json()) > 0, "Should have reports"
            assert all(
                "id" in report for report in response.json()
            ), "All reports should have ID"
            assert all(
                "title" in report for report in response.json()
            ), "All reports should have title"

        with allure.step("Test generate report API"):
            # Test generate report API
            response = self.api_client.post(
                "/api/analytics/reports/generate",
                {"title": "Test report", "metrics": ["total_users", "active_users"]},
            )
            assert response.status_code == 200, "Generate report API should return 200"
            assert "report_id" in response.json(), "Report should have ID"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test API error handling")
    @pytest.mark.api_integration
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
            # Test 400 Bad Request error
            response = self.api_client.post("/api/auth/login", {"invalid": "data"})
            assert response.status_code == 400, "Should return 400 for bad request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 401 Unauthorized error"):
            # Test 401 Unauthorized error
            response = self.api_client.get("/api/auth/me")
            assert (
                response.status_code == 401
            ), "Should return 401 for unauthorized request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 403 Forbidden error"):
            # Test 403 Forbidden error
            response = self.api_client.get("/api/admin/users")
            assert (
                response.status_code == 403
            ), "Should return 403 for forbidden request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 404 Not Found error"):
            # Test 404 Not Found error
            response = self.api_client.get("/api/nonexistent")
            assert (
                response.status_code == 404
            ), "Should return 404 for not found request"
            assert "error" in response.json(), "Should return error message"

        with allure.step("Test 500 Internal Server Error"):
            # Test 500 Internal Server Error
            response = self.api_client.get("/api/error")
            assert (
                response.status_code == 500
            ), "Should return 500 for internal server error"
            assert "error" in response.json(), "Should return error message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test API performance")
    @pytest.mark.api_integration
    def test_api_performance(self):
        """Test API performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test API response times"):
            # Test API response times
            api_response_times = (
                self.api_integration_testing.measure_api_response_times()
            )
            for endpoint, response_time in api_response_times.items():
                assert (
                    response_time < 2
                ), f"API {endpoint} should respond within 2 seconds, actual: {response_time}s"

        with allure.step("Test API throughput"):
            # Test API throughput
            throughput = self.api_integration_testing.measure_api_throughput()
            assert (
                throughput > 100
            ), f"API throughput should be at least 100 requests per second, actual: {throughput}"

        with allure.step("Test API concurrency"):
            # Test API concurrency
            concurrency_results = self.api_integration_testing.test_api_concurrency()
            assert (
                concurrency_results["success_rate"] > 0.95
            ), f"API concurrency success rate should be at least 95%, actual: {concurrency_results['success_rate']*100}%"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test API integration reporting")
    @pytest.mark.api_integration
    def test_api_integration_reporting(self):
        """Test API integration reporting"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test API integration report generation"):
            # Test API integration report generation
            report = self.api_integration_testing.generate_api_integration_report()
            assert (
                "endpoints" in report
            ), "API integration report should include endpoints"
            assert (
                "performance" in report
            ), "API integration report should include performance"
            assert "issues" in report, "API integration report should include issues"

        with allure.step("Test API integration metrics"):
            # Test API integration metrics
            metrics = self.api_integration_testing.collect_api_integration_metrics()
            assert (
                "total_requests" in metrics
            ), "API integration metrics should include total requests"
            assert (
                "success_rate" in metrics
            ), "API integration metrics should include success rate"
            assert (
                "average_response_time" in metrics
            ), "API integration metrics should include average response time"

        with allure.step("Test API integration recommendations"):
            # Test API integration recommendations
            recommendations = (
                self.api_integration_testing.get_api_integration_recommendations()
            )
            assert (
                len(recommendations) > 0
            ), "API integration recommendations should be provided"
            assert all(
                "endpoint" in rec for rec in recommendations
            ), "All recommendations should specify endpoint"
            assert all(
                "issue" in rec for rec in recommendations
            ), "All recommendations should specify issue"
