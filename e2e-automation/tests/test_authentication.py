"""
Authentication tests for the application
"""

import pytest
import allure
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.profile_page import ProfilePage
from pages.ecommerce_page import EcommercePage
from pages.social_page import SocialPage
from pages.tasks_page import TasksPage
from pages.content_page import ContentPage
from pages.analytics_page import AnalyticsPage
from utils.logger import TestLogger
from utils.auth_testing import AuthTesting


@allure.feature("Authentication Tests")
@allure.story("Authentication Testing")
class TestAuthentication(BaseTest):
    """Test class for authentication testing"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.logger = TestLogger("TestAuthentication")
        self.auth_testing = AuthTesting(self)
        self.login_page = LoginPage(self.driver, self)
        self.dashboard_page = DashboardPage(self.driver, self)
        self.profile_page = ProfilePage(self.driver, self)
        self.ecommerce_page = EcommercePage(self.driver, self)
        self.social_page = SocialPage(self.driver, self)
        self.tasks_page = TasksPage(self.driver, self)
        self.content_page = ContentPage(self.driver, self)
        self.analytics_page = AnalyticsPage(self.driver, self)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test successful login")
    @pytest.mark.authentication
    def test_successful_login(self):
        """Test successful login"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Check form elements are present
            assert self.login_page.is_element_present(
                *self.login_page.EMAIL_INPUT
            ), "Email input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.PASSWORD_INPUT
            ), "Password input should be present"
            assert self.login_page.is_element_present(
                *self.login_page.LOGIN_BUTTON
            ), "Login button should be present"

        with allure.step("Test login with valid credentials"):
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test redirect to dashboard"):
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test login with invalid credentials")
    @pytest.mark.authentication
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test login with invalid email"):
            self.login_page.login("invalid@example.com", "password")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid email"
            assert (
                "Invalid email or password" in self.login_page.get_error_message()
            ), "Should show correct error message"

        with allure.step("Test login with invalid password"):
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], "wrongpassword")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid password"
            assert (
                "Invalid email or password" in self.login_page.get_error_message()
            ), "Should show correct error message"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test login with empty fields")
    @pytest.mark.authentication
    def test_login_with_empty_fields(self):
        """Test login with empty fields"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test login with empty email"):
            self.login_page.login("", "password")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for empty email"
            assert (
                "Email is required" in self.login_page.get_email_error_message()
            ), "Should show email required error"

        with allure.step("Test login with empty password"):
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], "")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for empty password"
            assert (
                "Password is required" in self.login_page.get_password_error_message()
            ), "Should show password required error"

        with allure.step("Test login with both fields empty"):
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

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test login with invalid email format")
    @pytest.mark.authentication
    def test_login_with_invalid_email_format(self):
        """Test login with invalid email format"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test login with invalid email format"):
            invalid_emails = [
                "invalid-email",
                "invalid@",
                "@example.com",
                "invalid@.com",
                "invalid@example.",
                "invalid@.com.",
                "invalid@example..com",
            ]

            for email in invalid_emails:
                self.login_page.login(email, "password")
                assert (
                    self.login_page.wait_for_validation_error()
                ), f"Should show validation error for invalid email: {email}"
                assert (
                    "Invalid email format" in self.login_page.get_email_error_message()
                ), f"Should show email format error for: {email}"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test login with demo credentials")
    @pytest.mark.authentication
    def test_login_with_demo_credentials(self):
        """Test login with demo credentials"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test demo credentials are available"):
            assert self.login_page.is_element_present(
                *self.login_page.DEMO_EMAIL_VALUE
            ), "Demo email should be present"
            assert self.login_page.is_element_present(
                *self.login_page.DEMO_PASSWORD_VALUE
            ), "Demo password should be present"

        with allure.step("Test login with demo credentials"):
            self.login_page.fill_demo_credentials()
            demo_email = self.login_page.get_demo_email_value()
            demo_password = self.login_page.get_demo_password_value()

            self.login_page.login(demo_email, demo_password)
            assert (
                self.login_page.wait_for_login_success()
            ), "Login with demo credentials should succeed"

        with allure.step("Test redirect to dashboard with demo credentials"):
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert (
                self.dashboard_page.get_logged_in_username() != "Guest"
            ), "User should be logged in with demo credentials"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test login attempt limiting")
    @pytest.mark.authentication
    def test_login_attempt_limiting(self):
        """Test login attempt limiting"""
        with allure.step("Test login page loads"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

        with allure.step("Test multiple failed login attempts"):
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

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test session management")
    @pytest.mark.authentication
    def test_session_management(self):
        """Test session management"""
        with allure.step("Test session creation"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

            # Test session creation
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"
            assert self.dashboard_page.is_session_created(), "Session should be created"
            assert (
                self.dashboard_page.is_session_id_present()
            ), "Session ID should be present"

        with allure.step("Test session persistence"):
            # Test session persistence across page navigations
            self.ecommerce_page.navigate_to()
            assert (
                self.ecommerce_page.verify_page_loaded()
            ), "E-commerce page should load correctly"
            assert (
                self.ecommerce_page.get_logged_in_username() != "Guest"
            ), "User should remain logged in"

            self.social_page.navigate_to()
            assert (
                self.social_page.verify_page_loaded()
            ), "Social page should load correctly"
            assert (
                self.social_page.get_logged_in_username() != "Guest"
            ), "User should remain logged in"

        with allure.step("Test session timeout"):
            # Test session timeout
            assert (
                self.dashboard_page.is_session_timeout_configured()
            ), "Session timeout should be configured"
            assert (
                self.dashboard_page.is_session_timeout_enforced()
            ), "Session timeout should be enforced"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test logout functionality")
    @pytest.mark.authentication
    def test_logout_functionality(self):
        """Test logout functionality"""
        with allure.step("Test login first"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            assert self.login_page.wait_for_login_success(), "Login should succeed"

        with allure.step("Test logout from dashboard"):
            self.dashboard_page.navigate_to()
            assert (
                self.dashboard_page.verify_page_loaded()
            ), "Dashboard should load correctly"

            # Test logout
            self.dashboard_page.logout()
            assert (
                self.login_page.verify_page_loaded()
            ), "Should redirect to login page after logout"

        with allure.step("Test session invalidation"):
            # Test session invalidation
            self.dashboard_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Should redirect to login page when not logged in"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test password security")
    @pytest.mark.authentication
    def test_password_security(self):
        """Test password security"""
        with allure.step("Test password requirements"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test password requirements
            assert self.login_page.is_password_required(), "Password should be required"
            assert (
                self.login_page.is_password_minimum_length_enforced()
            ), "Password minimum length should be enforced"
            assert (
                self.login_page.is_password_complexity_enforced()
            ), "Password complexity should be enforced"

        with allure.step("Test password masking"):
            # Test password masking
            self.login_page.enter_password("password123")
            assert self.login_page.is_password_masked(), "Password should be masked"
            assert (
                self.login_page.get_password_value() == "password123"
            ), "Password value should be correct"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test authentication API")
    @pytest.mark.authentication
    def test_authentication_api(self):
        """Test authentication API"""
        with allure.step("Test login API"):
            user_data = self.settings.get_user_credentials("regular_user")
            response = self.api_client.post(
                "/api/auth/login",
                {"email": user_data["email"], "password": user_data["password"]},
            )
            assert response.status_code == 200, "Login API should return 200"
            assert "access_token" in response.json(), "Login should return access token"

        with allure.step("Test get current user API"):
            response = self.api_client.get("/api/auth/me")
            assert response.status_code == 200, "Get current user API should return 200"
            assert (
                response.json()["email"] == user_data["email"]
            ), "Should return correct user email"

        with allure.step("Test refresh token API"):
            response = self.api_client.post(
                "/api/auth/refresh", {"refresh_token": "test_refresh_token"}
            )
            assert response.status_code == 200, "Refresh token API should return 200"
            assert (
                "access_token" in response.json()
            ), "Refresh should return new access token"

        with allure.step("Test logout API"):
            response = self.api_client.post("/api/auth/logout")
            assert response.status_code == 200, "Logout API should return 200"
            assert (
                response.json()["message"] == "Successfully logged out"
            ), "Should return logout message"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test authentication error handling")
    @pytest.mark.authentication
    def test_authentication_error_handling(self):
        """Test authentication error handling"""
        with allure.step("Test login error handling"):
            self.login_page.navigate_to()
            assert (
                self.login_page.verify_page_loaded()
            ), "Login page should load correctly"

            # Test error handling
            self.login_page.login("invalid@example.com", "wrongpassword")
            assert (
                self.login_page.wait_for_error_message()
            ), "Should show error for invalid credentials"
            assert (
                self.login_page.is_error_message_helpful()
            ), "Error message should be helpful"

        with allure.step("Test form validation error handling"):
            # Test form validation error handling
            self.login_page.login("", "")
            assert (
                self.login_page.wait_for_validation_error()
            ), "Should show validation error for empty fields"
            assert (
                self.login_page.are_error_messages_clear()
            ), "Error messages should be clear"

        with allure.step("Test API error handling"):
            # Test API error handling
            response = self.api_client.post(
                "/api/auth/login",
                {"email": "invalid@example.com", "password": "wrongpassword"},
            )
            assert (
                response.status_code == 401
            ), "Should return 401 for invalid credentials"
            assert (
                "Invalid email or password" in response.json()["detail"]
            ), "Should return correct error message"

    # Profile Management Tests
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test viewing user profile")
    @pytest.mark.profile
    def test_view_user_profile(self):
        """Test viewing user profile"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()

            # Navigate to profile
            self.profile_page.load()
            assert (
                self.profile_page.is_profile_loaded()
            ), "Profile page should load correctly"

        with allure.step("Verify profile information is displayed"):
            assert (
                self.profile_page.get_user_name() != ""
            ), "User name should be displayed"
            assert (
                self.profile_page.get_user_email() == user_data["email"]
            ), "User email should match login email"
            assert (
                self.profile_page.get_registration_date() != ""
            ), "Registration date should be displayed"
            assert (
                self.profile_page.get_user_status() != ""
            ), "User status should be displayed"
            assert (
                self.profile_page.get_activity_stats() != ""
            ), "Activity stats should be displayed"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test editing user profile")
    @pytest.mark.profile
    def test_edit_user_profile(self):
        """Test editing user profile"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.profile_page.load()

        with allure.step("Edit profile information"):
            self.profile_page.click_edit_profile()
            profile_data = self.settings.get_test_data()["profile_data"][
                "profile_update"
            ]

            self.profile_page.edit_full_name(profile_data["full_name"])
            self.profile_page.edit_email(profile_data["email"])
            self.profile_page.save_profile_changes()

        with allure.step("Verify profile changes are saved"):
            assert (
                self.profile_page.get_success_message() != ""
            ), "Success message should be displayed"
            assert (
                self.profile_page.get_user_name() == profile_data["full_name"]
            ), "User name should be updated"
            assert (
                self.profile_page.get_user_email() == profile_data["email"]
            ), "User email should be updated"

    @allure.severity(allure.severity_level.HIGH)
    @allure.description("Test changing user password")
    @pytest.mark.profile
    def test_change_user_password(self):
        """Test changing user password"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.profile_page.load()

        with allure.step("Navigate to security settings"):
            self.profile_page.click_security_settings()

        with allure.step("Change password"):
            password_data = self.settings.get_test_data()["profile_data"][
                "password_change"
            ]
            self.profile_page.change_password(
                password_data["current_password"],
                password_data["new_password"],
                password_data["confirm_password"],
            )

        with allure.step("Verify password change success"):
            assert (
                self.profile_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test password recovery")
    @pytest.mark.profile
    def test_password_recovery(self):
        """Test password recovery"""
        with allure.step("Navigate to login page"):
            self.login_page.navigate_to()

        with allure.step("Click forgot password"):
            self.profile_page.click_forgot_password()

        with allure.step("Request password reset"):
            user_data = self.settings.get_user_credentials("regular_user")
            self.profile_page.request_password_reset(user_data["email"])

        with allure.step("Verify reset request success"):
            assert (
                self.profile_page.get_success_message() != ""
            ), "Reset request success message should be displayed"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test email verification")
    @pytest.mark.profile
    def test_email_verification(self):
        """Test email verification"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.profile_page.load()

        with allure.step("Check email verification status"):
            status = self.profile_page.get_email_verification_status()
            assert status != "", "Email verification status should be displayed"

        with allure.step("Click verify email if needed"):
            if "not verified" in status.lower():
                self.profile_page.click_verify_email()
                assert (
                    self.profile_page.is_email_verification_success()
                ), "Email verification should be successful"

    @allure.severity(allure.severity_level.MEDIUM)
    @allure.description("Test notification settings")
    @pytest.mark.profile
    def test_notification_settings(self):
        """Test notification settings"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.profile_page.load()

        with allure.step("Navigate to notification settings"):
            self.profile_page.click_notification_settings()

        with allure.step("Toggle email notifications"):
            self.profile_page.toggle_email_notifications()

        with allure.step("Toggle push notifications"):
            self.profile_page.toggle_push_notifications()

        with allure.step("Select notification types"):
            notification_types = ["likes", "comments", "mentions"]
            self.profile_page.select_notification_types(notification_types)

        with allure.step("Save notification settings"):
            self.profile_page.save_notification_settings()
            assert (
                self.profile_page.get_success_message() != ""
            ), "Success message should be displayed"

    @allure.severity(allure.severity_level.LOW)
    @allure.description("Test account deletion")
    @pytest.mark.profile
    def test_account_deletion(self):
        """Test account deletion"""
        with allure.step("Login and navigate to profile"):
            self.login_page.navigate_to()
            user_data = self.settings.get_user_credentials("regular_user")
            self.login_page.login(user_data["email"], user_data["password"])
            self.dashboard_page.wait_for_page_load()
            self.profile_page.load()

        with allure.step("Navigate to account settings"):
            self.profile_page.click_account_settings()

        with allure.step("Click delete account"):
            self.profile_page.click_delete_account()

        with allure.step("Confirm account deletion"):
            self.profile_page.confirm_account_deletion()

        with allure.step("Verify account deletion"):
            # Should be redirected to login page
            assert (
                self.login_page.verify_page_loaded()
            ), "Should be redirected to login page after account deletion"
