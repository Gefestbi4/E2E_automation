"""
Page Object для страницы тестов (tests.html)
"""

from .base_page import BasePage
from .Locators import TestsPageLocators
import allure
import time


class TestsPage(BasePage):
    """Класс для работы со страницей тестов"""

    def __init__(self, browser, url):
        super().__init__(browser, url)
        self.base_url = url.replace("/tests.html", "")

    @allure.step("Check if page is loaded")
    def is_page_loaded(self):
        """Проверка загрузки страницы"""
        try:
            self.find_element(*TestsPageLocators.PAGE_TITLE)
            return True
        except:
            return False

    @allure.step("Get page title")
    def get_page_title(self):
        """Получение заголовка страницы"""
        title_element = self.find_element(*TestsPageLocators.PAGE_TITLE)
        return title_element.text

    @allure.step("Check if sidebar is present")
    def is_navigation_menu_present(self):
        """Проверка наличия сайдбара с навигацией"""
        try:
            self.find_element(*TestsPageLocators.SIDEBAR)
            return True
        except:
            return False

    @allure.step("Check if inputs tab is present")
    def is_files_button_present(self):
        """Проверка наличия таба 'Поля ввода'"""
        try:
            self.find_element(*TestsPageLocators.INPUTS_TAB)
            return True
        except:
            return False

    @allure.step("Check if checkboxes tab is present")
    def is_folders_button_present(self):
        """Проверка наличия таба 'Чекбоксы'"""
        try:
            self.find_element(*TestsPageLocators.CHECKBOXES_TAB)
            return True
        except:
            return False

    @allure.step("Check if buttons tab is present")
    def is_settings_button_present(self):
        """Проверка наличия таба 'Кнопки'"""
        try:
            self.find_element(*TestsPageLocators.BUTTONS_TAB)
            return True
        except:
            return False

    @allure.step("Check if images tab is present")
    def is_logout_button_present(self):
        """Проверка наличия таба 'Картинки'"""
        try:
            self.find_element(*TestsPageLocators.IMAGES_TAB)
            return True
        except:
            return False

    @allure.step("Navigate to inputs section")
    def navigate_to_files(self):
        """Переход в раздел полей ввода"""
        self.click_element_clickable(*TestsPageLocators.INPUTS_TAB)

    @allure.step("Navigate to checkboxes section")
    def navigate_to_folders(self):
        """Переход в раздел чекбоксов"""
        self.click_element_clickable(*TestsPageLocators.CHECKBOXES_TAB)

    @allure.step("Navigate to buttons section")
    def navigate_to_settings(self):
        """Переход в раздел кнопок"""
        self.click_element_clickable(*TestsPageLocators.BUTTONS_TAB)

    @allure.step("Navigate to images section")
    def logout_user(self):
        """Переход в раздел картинок"""
        self.click_element_clickable(*TestsPageLocators.IMAGES_TAB)

    @allure.step("Check if inputs section is active")
    def is_files_section_active(self):
        """Проверка активности раздела полей ввода"""
        try:
            # Проверяем, что демо элементы полей ввода присутствуют
            self.find_element(*TestsPageLocators.DEMO_EMAIL_INPUT)
            return True
        except:
            return False

    @allure.step("Check if checkboxes section is active")
    def is_folders_section_active(self):
        """Проверка активности раздела чекбоксов"""
        try:
            # Проверяем, что демо элементы чекбоксов присутствуют
            self.find_element(*TestsPageLocators.CHECKBOXES_TAB)
            return True
        except:
            return False

    @allure.step("Check if buttons section is active")
    def is_settings_section_active(self):
        """Проверка активности раздела кнопок"""
        try:
            # Проверяем, что демо элементы кнопок присутствуют
            self.find_element(*TestsPageLocators.NORMAL_BUTTON)
            return True
        except:
            return False

    @allure.step("Check if redirected to login")
    def is_redirected_to_login(self):
        """Проверка перенаправления на страницу входа"""
        current_url = self.browser.current_url
        return "/login.html" in current_url

    @allure.step("Check if auth token is present")
    def is_auth_token_present(self):
        """Проверка наличия токена авторизации"""
        try:
            token = self.browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            return token is not None
        except:
            return False

    @allure.step("Refresh page")
    def refresh_page(self):
        """Обновление страницы"""
        self.browser.refresh()

    @allure.step("Check if page is loaded after refresh")
    def is_page_loaded_after_refresh(self):
        """Проверка загрузки страницы после обновления"""
        try:
            self.find_element(*TestsPageLocators.PAGE_TITLE)
            return True
        except:
            return False

    @allure.step("Check if user is authenticated")
    def is_user_authenticated(self):
        """Проверка авторизации пользователя"""
        return self.is_auth_token_present()

    @allure.step("Check if main page is active")
    def is_main_page_active(self):
        """Проверка активности главной страницы"""
        try:
            # Проверяем, что мы на странице тестов
            return "tests" in self.browser.current_url
        except:
            return False

    @allure.step("Browser back navigation")
    def browser_back(self):
        """Навигация назад в браузере"""
        self.browser.back()

    @allure.step("Browser forward navigation")
    def browser_forward(self):
        """Навигация вперед в браузере"""
        self.browser.forward()

    @allure.step("Interact with demo inputs")
    def interact_with_demo_inputs(self):
        """Взаимодействие с демо полями ввода"""
        try:
            # Проверяем, что демо элементы присутствуют
            email_input = self.find_element(*TestsPageLocators.DEMO_EMAIL_INPUT)
            login_input = self.find_element(*TestsPageLocators.DEMO_LOGIN_INPUT)
            password_input = self.find_element(*TestsPageLocators.DEMO_PASSWORD_INPUT)

            # Заполняем поля
            email_input.send_keys("test@example.com")
            login_input.send_keys("testuser")
            password_input.send_keys("testpassword")

            return True
        except:
            return False

    @allure.step("Interact with demo checkboxes")
    def interact_with_demo_checkboxes(self):
        """Взаимодействие с демо чекбоксами"""
        try:
            # Ищем кнопки управления чекбоксами
            check_all_btn = self.find_element(*TestsPageLocators.CHECK_ALL_BTN)
            uncheck_all_btn = self.find_element(*TestsPageLocators.UNCHECK_ALL_BTN)

            # Кликаем на "Выбрать все"
            check_all_btn.click()
            time.sleep(0.5)

            # Кликаем на "Снять все"
            uncheck_all_btn.click()

            return True
        except:
            return False

    @allure.step("Interact with demo buttons")
    def interact_with_demo_buttons(self):
        """Взаимодействие с демо кнопками"""
        try:
            # Ищем демо кнопки
            normal_button = self.find_element(*TestsPageLocators.NORMAL_BUTTON)
            primary_button = self.find_element(*TestsPageLocators.PRIMARY_BUTTON)

            # Кликаем на кнопки
            normal_button.click()
            time.sleep(0.5)
            primary_button.click()

            return True
        except:
            return False

    @allure.step("Check if user is authenticated")
    def is_user_authenticated(self):
        """Проверка авторизации пользователя"""
        try:
            # Проверяем наличие токена в localStorage
            token = self.browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            return token is not None
        except:
            return False

    @allure.step("Check if auth token is present")
    def is_auth_token_present(self):
        """Проверка наличия токена авторизации"""
        try:
            # Проверяем наличие токена в localStorage
            token = self.browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            return token is not None and len(token) > 0
        except:
            return False
