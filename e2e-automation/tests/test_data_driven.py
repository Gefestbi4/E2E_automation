"""
Data-driven tests for the application
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
from utils.data_driven_testing import DataDrivenTesting


@allure.feature("Data-Driven Tests")
@allure.story("Data-Driven Testing")
class TestDataDriven(BaseTest):
    """Test class for data-driven testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestDataDriven")
        self.data_driven_testing = DataDrivenTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test login with multiple user credentials")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "user_data",
        [
            {
                "email": "test1@example.com",
                "password": "password123",
                "expected_result": "success",
            },
            {
                "email": "test2@example.com",
                "password": "password456",
                "expected_result": "success",
            },
            {
                "email": "test3@example.com",
                "password": "password789",
                "expected_result": "success",
            },
            {
                "email": "invalid@example.com",
                "password": "wrongpassword",
                "expected_result": "failure",
            },
            {
                "email": "test4@example.com",
                "password": "wrongpassword",
                "expected_result": "failure",
            },
            {
                "email": "",
                "password": "password123",
                "expected_result": "validation_error",
            },
            {
                "email": "test5@example.com",
                "password": "",
                "expected_result": "validation_error",
            },
            {
                "email": "invalid-email",
                "password": "password123",
                "expected_result": "validation_error",
            },
        ],
    )
    def test_login_with_multiple_credentials(self, user_data):
        """Test login with multiple user credentials"""
        with allure.step(f"Test login with email: {user_data['email']}"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            self.login_page.login(user_data["email"], user_data["password"])

            if user_data["expected_result"] == "success":
                assert self.login_page.wait_for_login_success(), "Login should succeed"
                assert (
                    self.dashboard_page.verify_page_loaded()
                ), "Dashboard should load correctly"
            elif user_data["expected_result"] == "failure":
                assert (
                    self.login_page.wait_for_error_message()
                ), "Should show error for invalid credentials"
                assert (
                    "Invalid email or password" in self.login_page.get_error_message()
                ), "Should show correct error message"
            elif user_data["expected_result"] == "validation_error":
                assert (
                    self.login_page.wait_for_validation_error()
                ), "Should show validation error"
                if not user_data["email"]:
                    assert (
                        "Email is required" in self.login_page.get_email_error_message()
                    ), "Should show email required error"
                if not user_data["password"]:
                    assert (
                        "Password is required"
                        in self.login_page.get_password_error_message()
                    ), "Should show password required error"
                if user_data["email"] == "invalid-email":
                    assert (
                        "Invalid email format"
                        in self.login_page.get_email_error_message()
                    ), "Should show email format error"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test e-commerce with multiple products")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "product_data",
        [
            {
                "name": "Laptop",
                "category": "Electronics",
                "price": 999.99,
                "expected_result": "success",
            },
            {
                "name": "Smartphone",
                "category": "Electronics",
                "price": 699.99,
                "expected_result": "success",
            },
            {
                "name": "Headphones",
                "category": "Electronics",
                "price": 199.99,
                "expected_result": "success",
            },
            {
                "name": "Book",
                "category": "Books",
                "price": 29.99,
                "expected_result": "success",
            },
            {
                "name": "Clothing",
                "category": "Fashion",
                "price": 49.99,
                "expected_result": "success",
            },
            {
                "name": "",
                "category": "Electronics",
                "price": 999.99,
                "expected_result": "validation_error",
            },
            {
                "name": "Product",
                "category": "",
                "price": 999.99,
                "expected_result": "validation_error",
            },
            {
                "name": "Product",
                "category": "Electronics",
                "price": -100,
                "expected_result": "validation_error",
            },
        ],
    )
    def test_ecommerce_with_multiple_products(self, product_data):
        """Test e-commerce with multiple products"""
        with allure.step(f"Test e-commerce with product: {product_data['name']}"):
            # Login first
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Navigate to e-commerce
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            if product_data["expected_result"] == "success":
                # Test product search
                self.ecommerce_page.search_products(product_data["name"])
                assert (
                    self.ecommerce_page.wait_for_search_results()
                ), "Search results should load"

                # Test add to cart
                product = self.ecommerce_page.get_first_product()
                self.ecommerce_page.add_to_cart(product)
                assert self.ecommerce_page.wait_for_cart_update(), "Cart should update"
                assert (
                    self.ecommerce_page.get_cart_count() > 0
                ), "Cart should have items"
            elif product_data["expected_result"] == "validation_error":
                # Test validation errors
                if not product_data["name"]:
                    self.ecommerce_page.search_products("")
                    assert (
                        self.ecommerce_page.wait_for_validation_error()
                    ), "Should show validation error for empty search"
                    assert (
                        "Search term is required"
                        in self.ecommerce_page.get_validation_error()
                    ), "Should show search required error"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test social with multiple posts")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "post_data",
        [
            {"content": "This is a test post", "expected_result": "success"},
            {
                "content": "Another test post with more content",
                "expected_result": "success",
            },
            {"content": "Short post", "expected_result": "success"},
            {
                "content": "A very long post with lots of content that should still work fine and be accepted by the system",
                "expected_result": "success",
            },
            {"content": "", "expected_result": "validation_error"},
            {"content": "x" * 1001, "expected_result": "validation_error"},
        ],
    )
    def test_social_with_multiple_posts(self, post_data):
        """Test social with multiple posts"""
        with allure.step(
            f"Test social with post content: {post_data['content'][:50]}..."
        ):
            # Login first
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Navigate to social
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            if post_data["expected_result"] == "success":
                # Test post creation
                self.social_page.create_post(post_data)
                assert (
                    self.social_page.wait_for_post_created()
                ), "Post should be created"
                assert self.social_page.is_post_displayed(
                    post_data
                ), "Post should be displayed"
            elif post_data["expected_result"] == "validation_error":
                # Test validation errors
                self.social_page.create_post(post_data)
                assert (
                    self.social_page.wait_for_validation_error()
                ), "Should show validation error"
                if not post_data["content"]:
                    assert (
                        "Content is required" in self.social_page.get_validation_error()
                    ), "Should show content required error"
                elif len(post_data["content"]) > 1000:
                    assert (
                        "Content too long" in self.social_page.get_validation_error()
                    ), "Should show content too long error"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test tasks with multiple task data")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "task_data",
        [
            {
                "title": "Task 1",
                "description": "Description for task 1",
                "priority": "high",
                "expected_result": "success",
            },
            {
                "title": "Task 2",
                "description": "Description for task 2",
                "priority": "medium",
                "expected_result": "success",
            },
            {
                "title": "Task 3",
                "description": "Description for task 3",
                "priority": "low",
                "expected_result": "success",
            },
            {
                "title": "",
                "description": "Description for task",
                "priority": "high",
                "expected_result": "validation_error",
            },
            {
                "title": "Task",
                "description": "",
                "priority": "high",
                "expected_result": "validation_error",
            },
            {
                "title": "Task",
                "description": "Description",
                "priority": "invalid",
                "expected_result": "validation_error",
            },
        ],
    )
    def test_tasks_with_multiple_task_data(self, task_data):
        """Test tasks with multiple task data"""
        with allure.step(f"Test tasks with title: {task_data['title']}"):
            # Login first
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Navigate to tasks
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            if task_data["expected_result"] == "success":
                # Test task creation
                self.tasks_page.create_task(task_data)
                assert self.tasks_page.wait_for_task_created(), "Task should be created"
                assert self.tasks_page.is_task_displayed(
                    task_data
                ), "Task should be displayed"
            elif task_data["expected_result"] == "validation_error":
                # Test validation errors
                self.tasks_page.create_task(task_data)
                assert (
                    self.tasks_page.wait_for_validation_error()
                ), "Should show validation error"
                if not task_data["title"]:
                    assert (
                        "Title is required" in self.tasks_page.get_validation_error()
                    ), "Should show title required error"
                if not task_data["description"]:
                    assert (
                        "Description is required"
                        in self.tasks_page.get_validation_error()
                    ), "Should show description required error"
                if task_data["priority"] == "invalid":
                    assert (
                        "Invalid priority" in self.tasks_page.get_validation_error()
                    ), "Should show invalid priority error"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test content with multiple articles")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "article_data",
        [
            {
                "title": "Article 1",
                "content": "Content for article 1",
                "category": "Technology",
                "expected_result": "success",
            },
            {
                "title": "Article 2",
                "content": "Content for article 2",
                "category": "Science",
                "expected_result": "success",
            },
            {
                "title": "Article 3",
                "content": "Content for article 3",
                "category": "Business",
                "expected_result": "success",
            },
            {
                "title": "",
                "content": "Content for article",
                "category": "Technology",
                "expected_result": "validation_error",
            },
            {
                "title": "Article",
                "content": "",
                "category": "Technology",
                "expected_result": "validation_error",
            },
            {
                "title": "Article",
                "content": "Content",
                "category": "",
                "expected_result": "validation_error",
            },
        ],
    )
    def test_content_with_multiple_articles(self, article_data):
        """Test content with multiple articles"""
        with allure.step(f"Test content with article title: {article_data['title']}"):
            # Login first
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Navigate to content
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            if article_data["expected_result"] == "success":
                # Test article creation
                self.content_page.create_article(article_data)
                assert (
                    self.content_page.wait_for_article_created()
                ), "Article should be created"
                assert self.content_page.is_article_displayed(
                    article_data
                ), "Article should be displayed"
            elif article_data["expected_result"] == "validation_error":
                # Test validation errors
                self.content_page.create_article(article_data)
                assert (
                    self.content_page.wait_for_validation_error()
                ), "Should show validation error"
                if not article_data["title"]:
                    assert (
                        "Title is required" in self.content_page.get_validation_error()
                    ), "Should show title required error"
                if not article_data["content"]:
                    assert (
                        "Content is required"
                        in self.content_page.get_validation_error()
                    ), "Should show content required error"
                if not article_data["category"]:
                    assert (
                        "Category is required"
                        in self.content_page.get_validation_error()
                    ), "Should show category required error"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test analytics with multiple metrics")
    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "metric_data",
        [
            {"name": "total_users", "value": 1000, "expected_result": "success"},
            {"name": "active_users", "value": 750, "expected_result": "success"},
            {"name": "total_revenue", "value": 50000.50, "expected_result": "success"},
            {"name": "conversion_rate", "value": 0.15, "expected_result": "success"},
            {"name": "", "value": 1000, "expected_result": "validation_error"},
            {"name": "metric", "value": -100, "expected_result": "validation_error"},
            {
                "name": "metric",
                "value": "invalid",
                "expected_result": "validation_error",
            },
        ],
    )
    def test_analytics_with_multiple_metrics(self, metric_data):
        """Test analytics with multiple metrics"""
        with allure.step(f"Test analytics with metric: {metric_data['name']}"):
            # Login first
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Navigate to analytics
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            if metric_data["expected_result"] == "success":
                # Test metric display
                assert self.analytics_page.is_metric_displayed(
                    metric_data["name"]
                ), f"Metric {metric_data['name']} should be displayed"
                assert (
                    self.analytics_page.get_metric_value(metric_data["name"])
                    == metric_data["value"]
                ), f"Metric {metric_data['name']} value should match"
            elif metric_data["expected_result"] == "validation_error":
                # Test validation errors
                if not metric_data["name"]:
                    assert (
                        self.analytics_page.wait_for_validation_error()
                    ), "Should show validation error for empty metric name"
                    assert (
                        "Metric name is required"
                        in self.analytics_page.get_validation_error()
                    ), "Should show metric name required error"
                elif metric_data["value"] < 0:
                    assert (
                        self.analytics_page.wait_for_validation_error()
                    ), "Should show validation error for negative value"
                    assert (
                        "Value must be positive"
                        in self.analytics_page.get_validation_error()
                    ), "Should show positive value error"
                elif metric_data["value"] == "invalid":
                    assert (
                        self.analytics_page.wait_for_validation_error()
                    ), "Should show validation error for invalid value"
                    assert (
                        "Invalid value format"
                        in self.analytics_page.get_validation_error()
                    ), "Should show invalid value format error"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test data-driven test reporting")
    @pytest.mark.data_driven
    def test_data_driven_test_reporting(self):
        """Test data-driven test reporting"""
        with allure.step("Test data-driven test report generation"):
            # Test data-driven test report generation
            report = self.data_driven_testing.generate_data_driven_report()
            assert (
                "test_cases" in report
            ), "Data-driven report should include test cases"
            assert "data_sets" in report, "Data-driven report should include data sets"
            assert "results" in report, "Data-driven report should include results"

        with allure.step("Test data-driven test metrics"):
            # Test data-driven test metrics
            metrics = self.data_driven_testing.collect_data_driven_metrics()
            assert (
                "total_test_cases" in metrics
            ), "Data-driven metrics should include total test cases"
            assert (
                "passed_test_cases" in metrics
            ), "Data-driven metrics should include passed test cases"
            assert (
                "failed_test_cases" in metrics
            ), "Data-driven metrics should include failed test cases"
            assert (
                "success_rate" in metrics
            ), "Data-driven metrics should include success rate"

        with allure.step("Test data-driven test recommendations"):
            # Test data-driven test recommendations
            recommendations = self.data_driven_testing.get_data_driven_recommendations()
            assert (
                len(recommendations) > 0
            ), "Data-driven recommendations should be provided"
            assert all(
                "test_case" in rec for rec in recommendations
            ), "All recommendations should specify test case"
            assert all(
                "issue" in rec for rec in recommendations
            ), "All recommendations should specify issue"
