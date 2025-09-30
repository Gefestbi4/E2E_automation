"""
Visual regression tests for the application
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
from utils.visual_testing import VisualTesting


@allure.feature("Visual Regression Tests")
@allure.story("Visual Regression Testing")
class TestVisual(BaseTest):
    """Test class for visual regression testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestVisual")
        self.visual_testing = VisualTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test login page visual regression")
    @pytest.mark.visual
    def test_login_page_visual_regression(self):
        """Test login page visual regression"""
        with allure.step("Test login page visual comparison"):
            # Test login page visual comparison
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("login_page")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "login_page", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Login page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test login page responsive visual regression"):
            # Test login page responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "login_page",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test login page element visual regression"):
            # Test login page element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "login_page",
                ["email_input", "password_input", "login_button", "register_link"],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test dashboard visual regression")
    @pytest.mark.visual
    def test_dashboard_visual_regression(self):
        """Test dashboard visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard visual comparison"):
            # Test dashboard visual comparison
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("dashboard")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "dashboard", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Dashboard should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test dashboard responsive visual regression"):
            # Test dashboard responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "dashboard",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test dashboard element visual regression"):
            # Test dashboard element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "dashboard",
                [
                    "header",
                    "navigation",
                    "ecommerce_card",
                    "social_card",
                    "tasks_card",
                    "content_card",
                    "analytics_card",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test e-commerce visual regression")
    @pytest.mark.visual
    def test_ecommerce_visual_regression(self):
        """Test e-commerce visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test e-commerce visual comparison"):
            # Test e-commerce visual comparison
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("ecommerce")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "ecommerce", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"E-commerce page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test e-commerce responsive visual regression"):
            # Test e-commerce responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "ecommerce",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test e-commerce element visual regression"):
            # Test e-commerce element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "ecommerce",
                [
                    "product_grid",
                    "product_card",
                    "search_bar",
                    "filters",
                    "cart_button",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test social visual regression")
    @pytest.mark.visual
    def test_social_visual_regression(self):
        """Test social visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test social visual comparison"):
            # Test social visual comparison
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("social")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "social", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Social page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test social responsive visual regression"):
            # Test social responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "social",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test social element visual regression"):
            # Test social element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "social",
                [
                    "post_feed",
                    "post_card",
                    "create_post_form",
                    "like_button",
                    "comment_section",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test tasks visual regression")
    @pytest.mark.visual
    def test_tasks_visual_regression(self):
        """Test tasks visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test tasks visual comparison"):
            # Test tasks visual comparison
            self.tasks_page.navigate_to()
            assert (
                self.tasks_page.verify_page_loaded()
            ), "Tasks page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("tasks")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "tasks", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Tasks page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test tasks responsive visual regression"):
            # Test tasks responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "tasks",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test tasks element visual regression"):
            # Test tasks element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "tasks",
                [
                    "task_list",
                    "task_card",
                    "create_task_form",
                    "task_filters",
                    "task_status",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test content visual regression")
    @pytest.mark.visual
    def test_content_visual_regression(self):
        """Test content visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test content visual comparison"):
            # Test content visual comparison
            self.content_page.navigate_to()
            assert (
                self.content_page.verify_page_loaded()
            ), "Content page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("content")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "content", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Content page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test content responsive visual regression"):
            # Test content responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "content",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test content element visual regression"):
            # Test content element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "content",
                [
                    "article_list",
                    "article_card",
                    "create_article_form",
                    "article_filters",
                    "publish_button",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test analytics visual regression")
    @pytest.mark.visual
    def test_analytics_visual_regression(self):
        """Test analytics visual regression"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test analytics visual comparison"):
            # Test analytics visual comparison
            self.analytics_page.navigate_to()
            assert (
                self.analytics_page.verify_page_loaded()
            ), "Analytics page should load correctly"

            # Capture screenshot
            screenshot_path = self.visual_testing.capture_screenshot("analytics")
            assert screenshot_path is not None, "Screenshot should be captured"

            # Compare with baseline
            comparison_result = self.visual_testing.compare_with_baseline(
                "analytics", screenshot_path
            )
            assert comparison_result[
                "match"
            ], f"Analytics page should match baseline, actual: {comparison_result['difference_percentage']}% difference"

        with allure.step("Test analytics responsive visual regression"):
            # Test analytics responsive visual regression
            responsive_results = self.visual_testing.test_responsive_visual_regression(
                "analytics",
                [
                    {"width": 1920, "height": 1080},
                    {"width": 1366, "height": 768},
                    {"width": 768, "height": 1024},
                    {"width": 375, "height": 667},
                ],
            )
            assert all(
                result["match"] for result in responsive_results
            ), "All responsive breakpoints should match baseline"

        with allure.step("Test analytics element visual regression"):
            # Test analytics element visual regression
            element_results = self.visual_testing.test_element_visual_regression(
                "analytics",
                [
                    "metrics_dashboard",
                    "chart_container",
                    "filters",
                    "report_generator",
                    "export_button",
                ],
            )
            assert all(
                result["match"] for result in element_results
            ), "All elements should match baseline"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test visual regression reporting")
    @pytest.mark.visual
    def test_visual_regression_reporting(self):
        """Test visual regression reporting"""
        with allure.step("Test visual regression report generation"):
            # Test visual regression report generation
            report = self.visual_testing.generate_visual_regression_report()
            assert "page_comparisons" in report, "Should have page comparisons"
            assert "element_comparisons" in report, "Should have element comparisons"
            assert "responsive_tests" in report, "Should have responsive tests"
            assert "differences" in report, "Should have differences"

        with allure.step("Test visual regression metrics"):
            # Test visual regression metrics
            metrics = self.visual_testing.collect_visual_regression_metrics()
            assert "total_pages_tested" in metrics, "Should have total pages tested"
            assert (
                "pages_with_differences" in metrics
            ), "Should have pages with differences"
            assert (
                "average_difference_percentage" in metrics
            ), "Should have average difference percentage"
            assert (
                "visual_regression_score" in metrics
            ), "Should have visual regression score"

        with allure.step("Test visual regression recommendations"):
            # Test visual regression recommendations
            recommendations = (
                self.visual_testing.get_visual_regression_recommendations()
            )
            assert len(recommendations) > 0, "Should have recommendations"
            assert all(
                "page" in rec for rec in recommendations
            ), "All recommendations should specify page"
            assert all(
                "issue" in rec for rec in recommendations
            ), "All recommendations should specify issue"
            assert all(
                "priority" in rec for rec in recommendations
            ), "All recommendations should specify priority"
