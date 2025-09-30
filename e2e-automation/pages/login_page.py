"""
Login page object model
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import TestLogger


class LoginPage(BasePage):
    """Page object for login page"""

    # Page URL
    url = "/login.html"
    url_fragment = "login"

    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[test-id='email-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[test-id='password-input']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[test-id='login-submit-btn']")
    LOGIN_FORM = (By.CSS_SELECTOR, "form[test-id='login-form']")
    LOGIN_STATUS = (By.CSS_SELECTOR, "[test-id='login-status']")
    EMAIL_ERROR = (By.CSS_SELECTOR, "[test-id='email-error']")
    PASSWORD_ERROR = (By.CSS_SELECTOR, "[test-id='password-error']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[test-id='register-link']")
    DEMO_EMAIL = (By.CSS_SELECTOR, "[test-id='demo-email']")
    DEMO_PASSWORD = (By.CSS_SELECTOR, "[test-id='demo-password']")

    # Key elements for page verification
    key_elements = [
        {"by": EMAIL_INPUT[0], "value": EMAIL_INPUT[1]},
        {"by": PASSWORD_INPUT[0], "value": PASSWORD_INPUT[1]},
        {"by": LOGIN_BUTTON[0], "value": LOGIN_BUTTON[1]},
    ]

    def __init__(self, driver, base_test):
        super().__init__(driver, base_test)
        self.logger = TestLogger("LoginPage")

    def enter_email(self, email: str):
        """Enter email in email field"""
        self.log_page_action("Enter email", "email input", email)
        self.send_keys(*self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Enter password in password field"""
        self.log_page_action("Enter password", "password input", "***")
        self.send_keys(*self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click login button"""
        self.log_page_action("Click login button")
        self.click_element(*self.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """Complete login process"""
        self.logger.step("Login with credentials", {"email": email})
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def login_with_demo_credentials(self):
        """Login using demo credentials"""
        self.logger.step("Login with demo credentials")
        self.click_element(*self.DEMO_EMAIL)
        self.click_element(*self.DEMO_PASSWORD)
        self.click_login_button()

    def get_email_error(self) -> str:
        """Get email validation error message"""
        if self.is_element_visible(*self.EMAIL_ERROR):
            return self.get_element_text(*self.EMAIL_ERROR)
        return ""

    def get_password_error(self) -> str:
        """Get password validation error message"""
        if self.is_element_visible(*self.PASSWORD_ERROR):
            return self.get_element_text(*self.PASSWORD_ERROR)
        return ""

    def get_login_status(self) -> str:
        """Get login status message"""
        if self.is_element_visible(*self.LOGIN_STATUS):
            return self.get_element_text(*self.LOGIN_STATUS)
        return ""

    def is_login_form_present(self) -> bool:
        """Check if login form is present"""
        return self.is_element_present(*self.LOGIN_FORM)

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        try:
            button = self.find_element(*self.LOGIN_BUTTON)
            return button.is_enabled()
        except Exception:
            return False

    def is_login_button_loading(self) -> bool:
        """Check if login button is in loading state"""
        try:
            loading_element = self.find_element(By.CSS_SELECTOR, "#login-loading")
            return loading_element.is_displayed()
        except Exception:
            return False

    def wait_for_login_success(self, timeout: int = 10) -> bool:
        """Wait for successful login (redirect to main page)"""
        try:
            self.wait_for_url_contains("index.html", timeout)
            return True
        except Exception:
            return False

    def wait_for_login_error(self, timeout: int = 5) -> bool:
        """Wait for login error message"""
        try:
            self.wait_for_element_visible(*self.LOGIN_STATUS, timeout)
            return True
        except Exception:
            return False

    def clear_form(self):
        """Clear login form"""
        self.log_page_action("Clear login form")
        self.find_element(*self.EMAIL_INPUT).clear()
        self.find_element(*self.PASSWORD_INPUT).clear()

    def is_email_field_focused(self) -> bool:
        """Check if email field is focused"""
        try:
            email_field = self.find_element(*self.EMAIL_INPUT)
            return email_field == self.driver.switch_to.active_element
        except Exception:
            return False

    def is_password_field_focused(self) -> bool:
        """Check if password field is focused"""
        try:
            password_field = self.find_element(*self.PASSWORD_INPUT)
            return password_field == self.driver.switch_to.active_element
        except Exception:
            return False

    def get_email_placeholder(self) -> str:
        """Get email field placeholder text"""
        return self.get_element_attribute(*self.EMAIL_INPUT, "placeholder")

    def get_password_placeholder(self) -> str:
        """Get password field placeholder text"""
        return self.get_element_attribute(*self.PASSWORD_INPUT, "placeholder")

    def get_login_button_text(self) -> str:
        """Get login button text"""
        return self.get_element_text(*self.LOGIN_BUTTON)

    def click_register_link(self):
        """Click register link"""
        self.log_page_action("Click register link")
        self.click_element(*self.REGISTER_LINK)

    def is_demo_credentials_visible(self) -> bool:
        """Check if demo credentials are visible"""
        return self.is_element_visible(*self.DEMO_EMAIL) and self.is_element_visible(
            *self.DEMO_PASSWORD
        )

    def get_demo_email_text(self) -> str:
        """Get demo email text"""
        if self.is_element_visible(*self.DEMO_EMAIL):
            return self.get_element_text(*self.DEMO_EMAIL)
        return ""

    def get_demo_password_text(self) -> str:
        """Get demo password text"""
        if self.is_element_visible(*self.DEMO_PASSWORD):
            return self.get_element_text(*self.DEMO_PASSWORD)
        return ""

    def validate_email_format(self, email: str) -> bool:
        """Validate email format using frontend validation"""
        self.enter_email(email)
        self.click_login_button()

        # Check if email error appears
        email_error = self.get_email_error()
        return "email" in email_error.lower() if email_error else True

    def validate_password_required(self, password: str) -> bool:
        """Validate password is required"""
        self.enter_password(password)
        self.click_login_button()

        # Check if password error appears
        password_error = self.get_password_error()
        return "password" in password_error.lower() if password_error else True

    def submit_form_with_enter_key(self):
        """Submit form using Enter key"""
        from selenium.webdriver.common.keys import Keys

        self.log_page_action("Submit form with Enter key")
        password_field = self.find_element(*self.PASSWORD_INPUT)
        password_field.send_keys(Keys.RETURN)

    def get_form_validation_errors(self) -> dict:
        """Get all form validation errors"""
        return {
            "email_error": self.get_email_error(),
            "password_error": self.get_password_error(),
            "login_status": self.get_login_status(),
        }

    def is_form_valid(self) -> bool:
        """Check if form is valid (no validation errors)"""
        errors = self.get_form_validation_errors()
        return not any(errors.values())

    def wait_for_page_load_complete(self):
        """Wait for page to load completely including all resources"""
        self.wait_for_page_load()
        self.wait_for_ajax_complete()

        # Wait for key elements to be visible
        self.wait_for_element_visible(*self.EMAIL_INPUT)
        self.wait_for_element_visible(*self.PASSWORD_INPUT)
        self.wait_for_element_visible(*self.LOGIN_BUTTON)

    def get_page_title(self) -> str:
        """Get page title"""
        return super().get_title()

    def verify_page_elements(self) -> bool:
        """Verify all required page elements are present"""
        required_elements = [
            self.EMAIL_INPUT,
            self.PASSWORD_INPUT,
            self.LOGIN_BUTTON,
            self.LOGIN_FORM,
        ]

        for element in required_elements:
            if not self.is_element_present(*element):
                self.logger.error(f"Required element not found: {element}")
                return False

        return True

    def get_login_form_data(self) -> dict:
        """Get current form data"""
        return {
            "email": self.get_element_attribute(*self.EMAIL_INPUT, "value"),
            "password": self.get_element_attribute(*self.PASSWORD_INPUT, "value"),
        }

    def is_remember_me_available(self) -> bool:
        """Check if remember me checkbox is available"""
        try:
            remember_me = self.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            return remember_me.is_displayed()
        except Exception:
            return False

    def click_remember_me(self):
        """Click remember me checkbox if available"""
        if self.is_remember_me_available():
            self.log_page_action("Click remember me checkbox")
            self.click_element(By.CSS_SELECTOR, "input[type='checkbox']")

    def is_forgot_password_available(self) -> bool:
        """Check if forgot password link is available"""
        try:
            forgot_link = self.find_element(By.CSS_SELECTOR, "a[href*='forgot']")
            return forgot_link.is_displayed()
        except Exception:
            return False

    def click_forgot_password(self):
        """Click forgot password link if available"""
        if self.is_forgot_password_available():
            self.log_page_action("Click forgot password link")
            self.click_element(By.CSS_SELECTOR, "a[href*='forgot']")
