"""
Browser compatibility tests for the application
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
from utils.browser_compatibility_testing import BrowserCompatibilityTesting


@allure.feature("Browser Compatibility Tests")
@allure.story("Browser Compatibility Testing")
class TestBrowserCompatibility(BaseTest):
    """Test class for browser compatibility testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestBrowserCompatibility")
        self.browser_compatibility_testing = BrowserCompatibilityTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Chrome compatibility")
    @pytest.mark.browser_compatibility
    def test_chrome_compatibility(self):
        """Test Chrome compatibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard in Chrome"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.browser_compatibility_testing.test_chrome_features()
            ), "Chrome features should work"

        with allure.step("Test e-commerce in Chrome"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.browser_compatibility_testing.test_chrome_ecommerce()
            ), "E-commerce should work in Chrome"

        with allure.step("Test social in Chrome"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.browser_compatibility_testing.test_chrome_social()
            ), "Social features should work in Chrome"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test Firefox compatibility")
    @pytest.mark.browser_compatibility
    def test_firefox_compatibility(self):
        """Test Firefox compatibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard in Firefox"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.browser_compatibility_testing.test_firefox_features()
            ), "Firefox features should work"

        with allure.step("Test e-commerce in Firefox"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.browser_compatibility_testing.test_firefox_ecommerce()
            ), "E-commerce should work in Firefox"

        with allure.step("Test social in Firefox"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.browser_compatibility_testing.test_firefox_social()
            ), "Social features should work in Firefox"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test Safari compatibility")
    @pytest.mark.browser_compatibility
    def test_safari_compatibility(self):
        """Test Safari compatibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard in Safari"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.browser_compatibility_testing.test_safari_features()
            ), "Safari features should work"

        with allure.step("Test e-commerce in Safari"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.browser_compatibility_testing.test_safari_ecommerce()
            ), "E-commerce should work in Safari"

        with allure.step("Test social in Safari"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.browser_compatibility_testing.test_safari_social()
            ), "Social features should work in Safari"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test Edge compatibility")
    @pytest.mark.browser_compatibility
    def test_edge_compatibility(self):
        """Test Edge compatibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test dashboard in Edge"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.browser_compatibility_testing.test_edge_features()
            ), "Edge features should work"

        with allure.step("Test e-commerce in Edge"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.browser_compatibility_testing.test_edge_ecommerce()
            ), "E-commerce should work in Edge"

        with allure.step("Test social in Edge"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.browser_compatibility_testing.test_edge_social()
            ), "Social features should work in Edge"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test cross-browser functionality")
    @pytest.mark.browser_compatibility
    def test_cross_browser_functionality(self):
        """Test cross-browser functionality"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test cross-browser authentication"):
            # Test authentication across browsers
            assert (
                self.browser_compatibility_testing.test_cross_browser_authentication()
            ), "Authentication should work across browsers"

        with allure.step("Test cross-browser navigation"):
            # Test navigation across browsers
            assert (
                self.browser_compatibility_testing.test_cross_browser_navigation()
            ), "Navigation should work across browsers"

        with allure.step("Test cross-browser data persistence"):
            # Test data persistence across browsers
            assert (
                self.browser_compatibility_testing.test_cross_browser_data_persistence()
            ), "Data persistence should work across browsers"

        with allure.step("Test cross-browser API calls"):
            # Test API calls across browsers
            assert (
                self.browser_compatibility_testing.test_cross_browser_api_calls()
            ), "API calls should work across browsers"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test browser-specific features")
    @pytest.mark.browser_compatibility
    def test_browser_specific_features(self):
        """Test browser-specific features"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test Chrome-specific features"):
            # Test Chrome-specific features
            assert (
                self.browser_compatibility_testing.test_chrome_specific_features()
            ), "Chrome-specific features should work"

        with allure.step("Test Firefox-specific features"):
            # Test Firefox-specific features
            assert (
                self.browser_compatibility_testing.test_firefox_specific_features()
            ), "Firefox-specific features should work"

        with allure.step("Test Safari-specific features"):
            # Test Safari-specific features
            assert (
                self.browser_compatibility_testing.test_safari_specific_features()
            ), "Safari-specific features should work"

        with allure.step("Test Edge-specific features"):
            # Test Edge-specific features
            assert (
                self.browser_compatibility_testing.test_edge_specific_features()
            ), "Edge-specific features should work"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test browser performance")
    @pytest.mark.browser_compatibility
    def test_browser_performance(self):
        """Test browser performance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test Chrome performance"):
            # Test Chrome performance
            chrome_performance = (
                self.browser_compatibility_testing.test_chrome_performance()
            )
            assert (
                chrome_performance["page_load_time"] < 3
            ), f"Chrome page load time should be less than 3 seconds, actual: {chrome_performance['page_load_time']}s"
            assert (
                chrome_performance["memory_usage"] < 200
            ), f"Chrome memory usage should be less than 200MB, actual: {chrome_performance['memory_usage']}MB"

        with allure.step("Test Firefox performance"):
            # Test Firefox performance
            firefox_performance = (
                self.browser_compatibility_testing.test_firefox_performance()
            )
            assert (
                firefox_performance["page_load_time"] < 3
            ), f"Firefox page load time should be less than 3 seconds, actual: {firefox_performance['page_load_time']}s"
            assert (
                firefox_performance["memory_usage"] < 200
            ), f"Firefox memory usage should be less than 200MB, actual: {firefox_performance['memory_usage']}MB"

        with allure.step("Test Safari performance"):
            # Test Safari performance
            safari_performance = (
                self.browser_compatibility_testing.test_safari_performance()
            )
            assert (
                safari_performance["page_load_time"] < 3
            ), f"Safari page load time should be less than 3 seconds, actual: {safari_performance['page_load_time']}s"
            assert (
                safari_performance["memory_usage"] < 200
            ), f"Safari memory usage should be less than 200MB, actual: {safari_performance['memory_usage']}MB"

        with allure.step("Test Edge performance"):
            # Test Edge performance
            edge_performance = (
                self.browser_compatibility_testing.test_edge_performance()
            )
            assert (
                edge_performance["page_load_time"] < 3
            ), f"Edge page load time should be less than 3 seconds, actual: {edge_performance['page_load_time']}s"
            assert (
                edge_performance["memory_usage"] < 200
            ), f"Edge memory usage should be less than 200MB, actual: {edge_performance['memory_usage']}MB"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test browser compatibility reporting")
    @pytest.mark.browser_compatibility
    def test_browser_compatibility_reporting(self):
        """Test browser compatibility reporting"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test compatibility report generation"):
            # Test compatibility report generation
            report = self.browser_compatibility_testing.generate_compatibility_report()
            assert "browsers" in report, "Compatibility report should include browsers"
            assert "features" in report, "Compatibility report should include features"
            assert "issues" in report, "Compatibility report should include issues"

        with allure.step("Test compatibility metrics"):
            # Test compatibility metrics
            metrics = self.browser_compatibility_testing.collect_compatibility_metrics()
            assert (
                "supported_browsers" in metrics
            ), "Compatibility metrics should include supported browsers"
            assert (
                "feature_coverage" in metrics
            ), "Compatibility metrics should include feature coverage"
            assert (
                "performance_scores" in metrics
            ), "Compatibility metrics should include performance scores"

        with allure.step("Test compatibility recommendations"):
            # Test compatibility recommendations
            recommendations = (
                self.browser_compatibility_testing.get_compatibility_recommendations()
            )
            assert (
                len(recommendations) > 0
            ), "Compatibility recommendations should be provided"
            assert all(
                "browser" in rec for rec in recommendations
            ), "All recommendations should specify browser"
            assert all(
                "issue" in rec for rec in recommendations
            ), "All recommendations should specify issue"
