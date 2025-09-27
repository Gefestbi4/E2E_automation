from .base_page import BasePage
from .Locators import LoginPageLocators
import allure
import time


class LoginPage(BasePage):
    """Класс для работы со страницей авторизации"""

    def __init__(self, browser, url):
        super().__init__(browser, url)
        self.base_url = url.replace("/login.html", "")

    @allure.step("Enter login")
    def enter_login(self, email):
        """Ввод email в поле авторизации"""
        self.send_keys_to_element(*LoginPageLocators.EMAIL_INPUT, email)

    @allure.step("Enter password")
    def enter_password(self, password):
        """Ввод пароля в поле авторизации"""
        self.send_keys_to_element(*LoginPageLocators.PASSWORD_INPUT, password)

    @allure.step("Click on Sign In button")
    def submit_sign_in_btn(self):
        """Нажатие на кнопку авторизации"""
        self.click_element_clickable(*LoginPageLocators.LOGIN_SUBMIT_BUTTON)

    @allure.step("Sign in with given email and password")
    def sign_in(self, email, password):
        """Полный процесс авторизации"""
        self.enter_login(email)
        self.enter_password(password)
        self.submit_sign_in_btn()

        # Ждем появления статусного сообщения
        try:
            status_message = self.wait_for_status_message(timeout=5)
        except Exception:
            pass

    @allure.step("Get login status message")
    def get_status_message(self):
        """Получение сообщения о статусе авторизации"""
        status_element = self.find_element(*LoginPageLocators.LOGIN_STATUS)
        return status_element.text.strip()

    @allure.step("Wait for login status message")
    def wait_for_status_message(self, timeout=10):
        """Ожидание появления сообщения о статусе"""
        self.wait_for_element_visible(*LoginPageLocators.LOGIN_STATUS, timeout)
        return self.get_status_message()

    @allure.step("Check if form is valid")
    def is_form_valid(self):
        """Проверка валидности формы"""
        email_field = self.find_element(*LoginPageLocators.EMAIL_INPUT)
        password_field = self.find_element(*LoginPageLocators.PASSWORD_INPUT)

        # Проверяем, что поля заполнены
        email_filled = email_field.get_attribute("value") != ""
        password_filled = password_field.get_attribute("value") != ""

        # Проверяем валидность email через JavaScript
        email_valid = self.browser.execute_script(
            "return arguments[0].validity.valid;", email_field
        )

        return email_valid and email_filled and password_filled

    @allure.step("Wait for URL change")
    def wait_for_url_change(self, expected_url, timeout=10):
        """Ожидание изменения URL"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_url = self.browser.current_url
            if expected_url in current_url:
                return True
            time.sleep(0.5)
        return False

    @allure.step("Check if user is redirected to tests page")
    def is_redirected_to_tests(self):
        """Проверка перенаправления на страницу тестов"""
        current_url = self.browser.current_url
        return current_url.endswith("/tests.html") or "/tests.html" in current_url

    @allure.step("Wait for redirect to tests page")
    def wait_for_redirect_to_tests(self, timeout=10):
        """Ожидание перенаправления на страницу тестов"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.is_redirected_to_tests():
                return True
            time.sleep(0.5)

        return False

    @allure.step("Get current page title")
    def get_page_title(self):
        """Получение заголовка страницы"""
        title_element = self.find_element(*LoginPageLocators.PAGE_TITLE)
        return title_element.text

    @allure.step("Check if network error is displayed")
    def is_network_error_displayed(self):
        """Проверка отображения ошибки сети"""
        try:
            # Ищем сообщение об ошибке сети
            error_element = self.find_element(*LoginPageLocators.LOGIN_STATUS)
            return (
                "network" in error_element.text.lower()
                or "connection" in error_element.text.lower()
            )
        except:
            return False

    @allure.step("Check if validation error is displayed")
    def is_validation_error_displayed(self):
        """Проверка отображения ошибок валидации"""
        try:
            # Проверяем HTML5 валидацию
            email_field = self.find_element(*LoginPageLocators.EMAIL_INPUT)
            return not email_field.get_attribute("validity").get("valid", True)
        except:
            return False

    @allure.step("Refresh page")
    def refresh(self):
        """Обновление страницы"""
        self.browser.refresh()

    @allure.step("Check if page is loaded")
    def is_page_loaded(self):
        """Проверка загрузки страницы входа"""
        try:
            self.find_element(*LoginPageLocators.EMAIL_INPUT)
            return True
        except:
            return False

    @allure.step("Check if login button is enabled")
    def is_login_button_enabled(self):
        """Проверка активности кнопки авторизации"""
        button = self.find_element(*LoginPageLocators.LOGIN_SUBMIT_BUTTON)
        return not button.get_attribute("disabled")

    @allure.step("Get auth token from localStorage")
    def get_auth_token(self):
        """Получение токена авторизации из localStorage"""
        try:
            token = self.browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            return token
        except Exception:
            return None

    @allure.step("Fill form with test data")
    def fill_form_with_test_data(
        self, email="test@example.com", password="testpassword123"
    ):
        """Заполнение формы тестовыми данными"""
        self.enter_login(email)
        self.enter_password(password)
