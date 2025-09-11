from base_page import BasePage
from Locators import LoginPageLocators
import allure


class LoginPage(BasePage):
    @allure.step("Enter login")
    def enter_login(self, email):
        self.send_keys_to_element(*LoginPageLocators.EMAIL, email)

    @allure.step("Enter password")
    def enter_password(self, password):
        self.send_keys_to_element(*LoginPageLocators.PASSWORD, password)

    @allure.step("Click on Sign In button")
    def submit_sign_in_btn(self):
        self.click_element_clickable(*LoginPageLocators.SIGN_IN)

    @allure.step("Sign in with given email and password")
    def sign_in(self, email, password):
        self.enter_login(email)
        self.enter_password(password)
        self.submit_sign_in_btn()