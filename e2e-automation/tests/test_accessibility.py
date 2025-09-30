"""
Accessibility tests for the application
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
from utils.accessibility_testing import AccessibilityTesting


@allure.feature("Accessibility Tests")
@allure.story("Accessibility Testing")
class TestAccessibility(BaseTest):
    """Test class for accessibility testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestAccessibility")
        self.accessibility_testing = AccessibilityTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test keyboard navigation")
    @pytest.mark.accessibility
    def test_keyboard_navigation(self):
        """Test keyboard navigation"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test keyboard navigation on dashboard"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test Tab navigation
            assert (
                self.accessibility_testing.test_tab_navigation()
            ), "Tab navigation should work"

            # Test Enter key activation
            assert (
                self.accessibility_testing.test_enter_key_activation()
            ), "Enter key activation should work"

            # Test Escape key functionality
            assert (
                self.accessibility_testing.test_escape_key_functionality()
            ), "Escape key functionality should work"

        with allure.step("Test keyboard navigation on e-commerce"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test Tab navigation
            assert (
                self.accessibility_testing.test_tab_navigation()
            ), "Tab navigation should work"

            # Test arrow key navigation
            assert (
                self.accessibility_testing.test_arrow_key_navigation()
            ), "Arrow key navigation should work"

        with allure.step("Test keyboard navigation on social"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test Tab navigation
            assert (
                self.accessibility_testing.test_tab_navigation()
            ), "Tab navigation should work"

            # Test Space key activation
            assert (
                self.accessibility_testing.test_space_key_activation()
            ), "Space key activation should work"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test screen reader compatibility")
    @pytest.mark.accessibility
    def test_screen_reader_compatibility(self):
        """Test screen reader compatibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test ARIA labels on dashboard"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test ARIA labels
            assert (
                self.accessibility_testing.test_aria_labels()
            ), "ARIA labels should be present"

            # Test ARIA roles
            assert (
                self.accessibility_testing.test_aria_roles()
            ), "ARIA roles should be present"

            # Test ARIA descriptions
            assert (
                self.accessibility_testing.test_aria_descriptions()
            ), "ARIA descriptions should be present"

        with allure.step("Test screen reader announcements"):
            # Test screen reader announcements
            assert (
                self.accessibility_testing.test_screen_reader_announcements()
            ), "Screen reader announcements should work"

            # Test live regions
            assert (
                self.accessibility_testing.test_live_regions()
            ), "Live regions should work"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test color contrast")
    @pytest.mark.accessibility
    def test_color_contrast(self):
        """Test color contrast"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test color contrast on dashboard"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test text contrast
            assert (
                self.accessibility_testing.test_text_contrast()
            ), "Text contrast should meet WCAG standards"

            # Test background contrast
            assert (
                self.accessibility_testing.test_background_contrast()
            ), "Background contrast should meet WCAG standards"

            # Test button contrast
            assert (
                self.accessibility_testing.test_button_contrast()
            ), "Button contrast should meet WCAG standards"

        with allure.step("Test color contrast on e-commerce"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test product card contrast
            assert (
                self.accessibility_testing.test_product_card_contrast()
            ), "Product card contrast should meet WCAG standards"

            # Test price contrast
            assert (
                self.accessibility_testing.test_price_contrast()
            ), "Price contrast should meet WCAG standards"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test focus management")
    @pytest.mark.accessibility
    def test_focus_management(self):
        """Test focus management"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test focus management on dashboard"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test focus visibility
            assert (
                self.accessibility_testing.test_focus_visibility()
            ), "Focus should be visible"

            # Test focus order
            assert (
                self.accessibility_testing.test_focus_order()
            ), "Focus order should be logical"

            # Test focus trapping
            assert (
                self.accessibility_testing.test_focus_trapping()
            ), "Focus trapping should work"

        with allure.step("Test focus management on modals"):
            # Test focus management in modals
            assert (
                self.accessibility_testing.test_modal_focus_management()
            ), "Modal focus management should work"

            # Test focus return after modal close
            assert (
                self.accessibility_testing.test_focus_return_after_modal_close()
            ), "Focus should return after modal close"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test form accessibility")
    @pytest.mark.accessibility
    def test_form_accessibility(self):
        """Test form accessibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test form accessibility on e-commerce"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test form labels
            assert (
                self.accessibility_testing.test_form_labels()
            ), "Form labels should be present"

            # Test form validation messages
            assert (
                self.accessibility_testing.test_form_validation_messages()
            ), "Form validation messages should be accessible"

            # Test form error handling
            assert (
                self.accessibility_testing.test_form_error_handling()
            ), "Form error handling should be accessible"

        with allure.step("Test form accessibility on social"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test post creation form
            assert (
                self.accessibility_testing.test_post_creation_form()
            ), "Post creation form should be accessible"

            # Test comment form
            assert (
                self.accessibility_testing.test_comment_form()
            ), "Comment form should be accessible"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test image accessibility")
    @pytest.mark.accessibility
    def test_image_accessibility(self):
        """Test image accessibility"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test image accessibility on e-commerce"):
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"

            # Test product images
            assert (
                self.accessibility_testing.test_product_images()
            ), "Product images should have alt text"

            # Test decorative images
            assert (
                self.accessibility_testing.test_decorative_images()
            ), "Decorative images should be marked as decorative"

        with allure.step("Test image accessibility on social"):
            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"

            # Test post images
            assert (
                self.accessibility_testing.test_post_images()
            ), "Post images should have alt text"

            # Test user avatars
            assert (
                self.accessibility_testing.test_user_avatars()
            ), "User avatars should have alt text"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test accessibility compliance")
    @pytest.mark.accessibility
    def test_accessibility_compliance(self):
        """Test accessibility compliance"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test WCAG 2.1 AA compliance"):
            # Test WCAG 2.1 AA compliance
            compliance_results = self.accessibility_testing.test_wcag_compliance()
            assert (
                compliance_results["level"] == "AA"
            ), f"Should meet WCAG 2.1 AA level, actual: {compliance_results['level']}"
            assert (
                compliance_results["score"] >= 90
            ), f"Accessibility score should be at least 90, actual: {compliance_results['score']}"

        with allure.step("Test accessibility violations"):
            # Test accessibility violations
            violations = self.accessibility_testing.test_accessibility_violations()
            assert (
                len(violations) == 0
            ), f"No accessibility violations should be found, actual: {violations}"

        with allure.step("Test accessibility recommendations"):
            # Test accessibility recommendations
            recommendations = (
                self.accessibility_testing.get_accessibility_recommendations()
            )
            assert (
                len(recommendations) > 0
            ), "Accessibility recommendations should be provided"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test accessibility testing tools")
    @pytest.mark.accessibility
    def test_accessibility_testing_tools(self):
        """Test accessibility testing tools"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test axe-core integration"):
            # Test axe-core integration
            axe_results = self.accessibility_testing.run_axe_analysis()
            assert (
                axe_results["violations"] == 0
            ), f"No axe violations should be found, actual: {axe_results['violations']}"
            assert axe_results["passes"] > 0, "Axe should find passing tests"

        with allure.step("Test WAVE integration"):
            # Test WAVE integration
            wave_results = self.accessibility_testing.run_wave_analysis()
            assert (
                wave_results["errors"] == 0
            ), f"No WAVE errors should be found, actual: {wave_results['errors']}"
            assert (
                wave_results["warnings"] == 0
            ), f"No WAVE warnings should be found, actual: {wave_results['warnings']}"

        with allure.step("Test Lighthouse accessibility audit"):
            # Test Lighthouse accessibility audit
            lighthouse_results = (
                self.accessibility_testing.run_lighthouse_accessibility_audit()
            )
            assert (
                lighthouse_results["score"] >= 90
            ), f"Lighthouse accessibility score should be at least 90, actual: {lighthouse_results['score']}"
