"""
Authentication tests for the application  # Документация тестов аутентификации для приложения
"""

import pytest  # Импорт фреймворка тестирования pytest
import allure  # Импорт библиотеки Allure для отчетности
from core.base_test import BaseTest  # Импорт базового класса тестов
from pages.login_page import LoginPage  # Импорт страницы входа
from pages.dashboard_page import DashboardPage  # Импорт страницы дашборда
from pages.profile_page import ProfilePage  # Импорт страницы профиля
from pages.ecommerce_page import EcommercePage  # Импорт страницы e-commerce
from pages.social_page import SocialPage  # Импорт страницы социальной сети
from pages.tasks_page import TasksPage  # Импорт страницы задач
from pages.content_page import ContentPage  # Импорт страницы контента
from pages.analytics_page import AnalyticsPage  # Импорт страницы аналитики
from utils.logger import TestLogger  # Импорт класса логгера тестов
from utils.auth_testing import AuthTesting  # Импорт утилиты тестирования аутентификации


@allure.feature(
    "Authentication Tests"
)  # Декоратор Allure для группировки тестов по функциональности
@allure.story(
    "Authentication Testing"
)  # Декоратор Allure для группировки тестов по истории
class TestAuthentication(BaseTest):  # Определение класса тестов аутентификации
    """Test class for authentication testing"""  # Документация класса

    @pytest.fixture(
        autouse=True
    )  # Декоратор pytest для автоматического использования фикстуры
    def setup(self):  # Метод настройки для каждого теста
        """Setup for each test"""  # Документация метода
        self.logger = TestLogger(
            "TestAuthentication"
        )  # Инициализация логгера для тестов аутентификации
        self.auth_testing = AuthTesting(
            self
        )  # Инициализация утилиты тестирования аутентификации
        self.login_page = LoginPage(self.driver, self)  # Инициализация страницы входа
        self.dashboard_page = DashboardPage(
            self.driver, self
        )  # Инициализация страницы дашборда
        self.profile_page = ProfilePage(
            self.driver, self
        )  # Инициализация страницы профиля
        self.ecommerce_page = EcommercePage(
            self.driver, self
        )  # Инициализация страницы e-commerce
        self.social_page = SocialPage(
            self.driver, self
        )  # Инициализация страницы социальной сети
        self.tasks_page = TasksPage(self.driver, self)  # Инициализация страницы задач
        self.content_page = ContentPage(
            self.driver, self
        )  # Инициализация страницы контента
        self.analytics_page = AnalyticsPage(
            self.driver, self
        )  # Инициализация страницы аналитики

    @allure.severity(
        allure.severity_level.CRITICAL
    )  # Декоратор Allure для установки критического уровня серьезности
    @allure.description("Test successful login")  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_successful_login(self):  # Тест успешного входа в систему
        """Test successful login"""  # Документация теста
        with allure.step(
            "Test login page loads"
        ):  # Шаг Allure для загрузки страницы входа
            self.login_page.navigate_to()  # Переход на страницу входа
            assert (  # Проверка загрузки страницы входа
                self.login_page.verify_page_loaded()  # Верификация загрузки страницы
            ), "Login page should load correctly"  # Сообщение об ошибке если страница не загрузилась

            # Check form elements are present  # Комментарий о проверке наличия элементов формы
            assert (
                self.login_page.is_email_field_present()
            ), "Email field should be present"  # Проверка наличия поля email
            assert (
                self.login_page.is_password_field_present()
            ), "Password field should be present"  # Проверка наличия поля пароля
            assert (
                self.login_page.is_login_button_present()
            ), "Login button should be present"  # Проверка наличия кнопки входа

        with allure.step(
            "Enter valid credentials"
        ):  # Шаг Allure для ввода валидных учетных данных
            test_data = self.test_data.get(
                "profile_data", {}
            )  # Получение тестовых данных профиля
            email = test_data.get(
                "email", "test@example.com"
            )  # Получение email из тестовых данных
            password = test_data.get(
                "password", "testpassword123"
            )  # Получение пароля из тестовых данных

            self.login_page.enter_email(email)  # Ввод email
            self.login_page.enter_password(password)  # Ввод пароля

        with allure.step("Submit login form"):  # Шаг Allure для отправки формы входа
            self.login_page.click_login_button()  # Клик по кнопке входа

        with allure.step(
            "Verify successful login"
        ):  # Шаг Allure для проверки успешного входа
            self.dashboard_page.wait_for_page_load()  # Ожидание загрузки страницы дашборда
            assert (  # Проверка успешного входа
                self.dashboard_page.verify_page_loaded()  # Верификация загрузки дашборда
            ), "Dashboard should load after successful login"  # Сообщение об ошибке если дашборд не загрузился

            # Verify user is logged in  # Комментарий о проверке входа пользователя
            assert (
                self.dashboard_page.is_user_logged_in()
            ), "User should be logged in"  # Проверка что пользователь вошел в систему

    @allure.severity(
        allure.severity_level.CRITICAL
    )  # Декоратор Allure для установки критического уровня серьезности
    @allure.description(
        "Test login with invalid credentials"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_login_invalid_credentials(self):  # Тест входа с неверными учетными данными
        """Test login with invalid credentials"""  # Документация теста
        with allure.step(
            "Navigate to login page"
        ):  # Шаг Allure для перехода на страницу входа
            self.login_page.navigate_to()  # Переход на страницу входа
            assert (  # Проверка загрузки страницы входа
                self.login_page.verify_page_loaded()  # Верификация загрузки страницы
            ), "Login page should load correctly"  # Сообщение об ошибке если страница не загрузилась

        with allure.step(
            "Enter invalid credentials"
        ):  # Шаг Allure для ввода неверных учетных данных
            self.login_page.enter_email("invalid@example.com")  # Ввод неверного email
            self.login_page.enter_password("wrongpassword")  # Ввод неверного пароля

        with allure.step("Submit login form"):  # Шаг Allure для отправки формы входа
            self.login_page.click_login_button()  # Клик по кнопке входа

        with allure.step(
            "Verify error message is displayed"
        ):  # Шаг Allure для проверки отображения сообщения об ошибке
            assert (  # Проверка отображения сообщения об ошибке
                self.login_page.is_error_message_displayed()  # Проверка наличия сообщения об ошибке
            ), "Error message should be displayed for invalid credentials"  # Сообщение об ошибке если сообщение не отображается

            # Verify user is not logged in  # Комментарий о проверке что пользователь не вошел в систему
            assert (
                not self.dashboard_page.is_user_logged_in()
            ), "User should not be logged in"  # Проверка что пользователь не вошел в систему

    @allure.severity(
        allure.severity_level.HIGH
    )  # Декоратор Allure для установки высокого уровня серьезности
    @allure.description(
        "Test profile management functionality"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_profile_management(self):  # Тест управления профилем
        """Test profile management functionality"""  # Документация теста
        with allure.step("Login to application"):  # Шаг Allure для входа в приложение
            self.auth_testing.login_with_valid_credentials()  # Вход с валидными учетными данными

        with allure.step(
            "Navigate to profile page"
        ):  # Шаг Allure для перехода на страницу профиля
            self.profile_page.navigate_to()  # Переход на страницу профиля
            assert (  # Проверка загрузки страницы профиля
                self.profile_page.verify_page_loaded()  # Верификация загрузки страницы
            ), "Profile page should load correctly"  # Сообщение об ошибке если страница не загрузилась

        with allure.step(
            "Update profile information"
        ):  # Шаг Allure для обновления информации профиля
            test_data = self.test_data.get(
                "profile_data", {}
            )  # Получение тестовых данных профиля
            updated_name = test_data.get(
                "full_name", "Updated Test User"
            )  # Получение обновленного имени
            updated_email = test_data.get(
                "email", "updated@example.com"
            )  # Получение обновленного email

            self.profile_page.update_full_name(updated_name)  # Обновление полного имени
            self.profile_page.update_email(updated_email)  # Обновление email

        with allure.step(
            "Save profile changes"
        ):  # Шаг Allure для сохранения изменений профиля
            self.profile_page.click_save_button()  # Клик по кнопке сохранения

        with allure.step(
            "Verify profile updated successfully"
        ):  # Шаг Allure для проверки успешного обновления профиля
            assert (  # Проверка успешного обновления профиля
                self.profile_page.is_success_message_displayed()  # Проверка отображения сообщения об успехе
            ), "Success message should be displayed after profile update"  # Сообщение об ошибке если сообщение не отображается

    @allure.severity(
        allure.severity_level.HIGH
    )  # Декоратор Allure для установки высокого уровня серьезности
    @allure.description(
        "Test password change functionality"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_password_change(self):  # Тест смены пароля
        """Test password change functionality"""  # Документация теста
        with allure.step("Login to application"):  # Шаг Allure для входа в приложение
            self.auth_testing.login_with_valid_credentials()  # Вход с валидными учетными данными

        with allure.step(
            "Navigate to profile page"
        ):  # Шаг Allure для перехода на страницу профиля
            self.profile_page.navigate_to()  # Переход на страницу профиля
            assert (  # Проверка загрузки страницы профиля
                self.profile_page.verify_page_loaded()  # Верификация загрузки страницы
            ), "Profile page should load correctly"  # Сообщение об ошибке если страница не загрузилась

        with allure.step(
            "Open password change form"
        ):  # Шаг Allure для открытия формы смены пароля
            self.profile_page.click_change_password_button()  # Клик по кнопке смены пароля

        with allure.step(
            "Enter password change details"
        ):  # Шаг Allure для ввода деталей смены пароля
            test_data = self.test_data.get(
                "profile_data", {}
            )  # Получение тестовых данных профиля
            current_password = test_data.get(
                "password", "testpassword123"
            )  # Получение текущего пароля
            new_password = test_data.get(
                "new_password", "newpassword123"
            )  # Получение нового пароля

            self.profile_page.enter_current_password(
                current_password
            )  # Ввод текущего пароля
            self.profile_page.enter_new_password(new_password)  # Ввод нового пароля
            self.profile_page.confirm_new_password(
                new_password
            )  # Подтверждение нового пароля

        with allure.step(
            "Submit password change"
        ):  # Шаг Allure для отправки смены пароля
            self.profile_page.click_save_password_button()  # Клик по кнопке сохранения пароля

        with allure.step(
            "Verify password changed successfully"
        ):  # Шаг Allure для проверки успешной смены пароля
            assert (  # Проверка успешной смены пароля
                self.profile_page.is_success_message_displayed()  # Проверка отображения сообщения об успехе
            ), "Success message should be displayed after password change"  # Сообщение об ошибке если сообщение не отображается

    @allure.severity(
        allure.severity_level.MEDIUM
    )  # Декоратор Allure для установки среднего уровня серьезности
    @allure.description(
        "Test logout functionality"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_logout(self):  # Тест выхода из системы
        """Test logout functionality"""  # Документация теста
        with allure.step("Login to application"):  # Шаг Allure для входа в приложение
            self.auth_testing.login_with_valid_credentials()  # Вход с валидными учетными данными

        with allure.step(
            "Verify user is logged in"
        ):  # Шаг Allure для проверки входа пользователя
            assert (  # Проверка входа пользователя
                self.dashboard_page.is_user_logged_in()  # Проверка что пользователь вошел в систему
            ), "User should be logged in"  # Сообщение об ошибке если пользователь не вошел в систему

        with allure.step(
            "Click logout button"
        ):  # Шаг Allure для клика по кнопке выхода
            self.dashboard_page.click_logout_button()  # Клик по кнопке выхода

        with allure.step(
            "Verify user is logged out"
        ):  # Шаг Allure для проверки выхода пользователя
            assert (  # Проверка выхода пользователя
                self.login_page.verify_page_loaded()  # Проверка загрузки страницы входа
            ), "Login page should load after logout"  # Сообщение об ошибке если страница входа не загрузилась

            # Verify user is not logged in  # Комментарий о проверке что пользователь не вошел в систему
            assert (
                not self.dashboard_page.is_user_logged_in()
            ), "User should be logged out"  # Проверка что пользователь вышел из системы

    @allure.severity(
        allure.severity_level.MEDIUM
    )  # Декоратор Allure для установки среднего уровня серьезности
    @allure.description(
        "Test session timeout functionality"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_session_timeout(self):  # Тест таймаута сессии
        """Test session timeout functionality"""  # Документация теста
        with allure.step("Login to application"):  # Шаг Allure для входа в приложение
            self.auth_testing.login_with_valid_credentials()  # Вход с валидными учетными данными

        with allure.step(
            "Wait for session timeout"
        ):  # Шаг Allure для ожидания таймаута сессии
            # Simulate session timeout by clearing cookies  # Комментарий о симуляции таймаута сессии
            self.driver.delete_all_cookies()  # Удаление всех cookies

        with allure.step(
            "Try to access protected page"
        ):  # Шаг Allure для попытки доступа к защищенной странице
            self.dashboard_page.navigate_to()  # Переход на страницу дашборда

        with allure.step(
            "Verify redirect to login page"
        ):  # Шаг Allure для проверки перенаправления на страницу входа
            assert (  # Проверка перенаправления на страницу входа
                self.login_page.verify_page_loaded()  # Проверка загрузки страницы входа
            ), "User should be redirected to login page after session timeout"  # Сообщение об ошибке если перенаправление не произошло

    @allure.severity(
        allure.severity_level.LOW
    )  # Декоратор Allure для установки низкого уровня серьезности
    @allure.description(
        "Test remember me functionality"
    )  # Декоратор Allure для описания теста
    @pytest.mark.authentication  # Маркер pytest для группировки тестов аутентификации
    def test_remember_me(self):  # Тест функции "Запомнить меня"
        """Test remember me functionality"""  # Документация теста
        with allure.step(
            "Navigate to login page"
        ):  # Шаг Allure для перехода на страницу входа
            self.login_page.navigate_to()  # Переход на страницу входа
            assert (  # Проверка загрузки страницы входа
                self.login_page.verify_page_loaded()  # Верификация загрузки страницы
            ), "Login page should load correctly"  # Сообщение об ошибке если страница не загрузилась

        with allure.step(
            "Enter credentials and check remember me"
        ):  # Шаг Allure для ввода учетных данных и отметки "Запомнить меня"
            test_data = self.test_data.get(
                "profile_data", {}
            )  # Получение тестовых данных профиля
            email = test_data.get(
                "email", "test@example.com"
            )  # Получение email из тестовых данных
            password = test_data.get(
                "password", "testpassword123"
            )  # Получение пароля из тестовых данных

            self.login_page.enter_email(email)  # Ввод email
            self.login_page.enter_password(password)  # Ввод пароля
            self.login_page.check_remember_me()  # Отметка "Запомнить меня"

        with allure.step("Submit login form"):  # Шаг Allure для отправки формы входа
            self.login_page.click_login_button()  # Клик по кнопке входа

        with allure.step(
            "Verify successful login"
        ):  # Шаг Allure для проверки успешного входа
            self.dashboard_page.wait_for_page_load()  # Ожидание загрузки страницы дашборда
            assert (  # Проверка успешного входа
                self.dashboard_page.verify_page_loaded()  # Верификация загрузки дашборда
            ), "Dashboard should load after successful login"  # Сообщение об ошибке если дашборд не загрузился

        with allure.step(
            "Logout and verify remember me works"
        ):  # Шаг Allure для выхода и проверки работы "Запомнить меня"
            self.dashboard_page.click_logout_button()  # Клик по кнопке выхода
            self.login_page.navigate_to()  # Переход на страницу входа

            # Check if email is remembered  # Комментарий о проверке запоминания email
            assert (  # Проверка запоминания email
                self.login_page.is_email_remembered()  # Проверка что email запомнен
            ), "Email should be remembered after logout"  # Сообщение об ошибке если email не запомнен
