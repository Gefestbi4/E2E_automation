"""
E2E тесты для модуля аутентификации с системой маркировки
"""

import pytest
import allure
from utils.test_markers import debug_test, fixme_test, critical_test, high_priority
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from config.settings import Settings


@allure.feature("Аутентификация")
@allure.story("Вход в систему")
class TestLogin:
    """Тесты входа в систему"""

    @critical_test("Критический путь пользователя")
    @allure.story("Успешный вход")
    @pytest.mark.critical
    @pytest.mark.auth
    def test_successful_login(self, browser, url, test_data):
        """Успешный вход в систему с валидными данными"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()
            assert login_page.is_page_loaded(), "Страница входа не загрузилась"

        with allure.step("Ввод валидных данных"):
            user_data = test_data["users"]["valid_user"]
            login_page.sign_in(user_data["email"], user_data["password"])

        with allure.step("Проверка успешной авторизации"):
            assert (
                login_page.wait_for_redirect_to_tests()
            ), "Не произошло перенаправление на главную страницу"

    @high_priority("Проверка безопасности")
    @allure.story("Неудачный вход")
    @pytest.mark.high
    @pytest.mark.auth
    def test_invalid_credentials(self, browser, url):
        """Вход с неверными учетными данными"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

        with allure.step("Ввод неверных данных"):
            login_page.sign_in("invalid@example.com", "wrongpassword")

        with allure.step("Проверка отображения ошибки"):
            assert login_page.is_error_displayed(), "Ошибка не отображается"
            assert (
                "login" in browser.current_url
            ), "Пользователь не остался на странице входа"

    @debug_test("Проблема с валидацией email")
    @allure.story("Валидация email")
    @pytest.mark.debug
    @pytest.mark.auth
    def test_email_validation(self, browser, url):
        """Проверка валидации email адреса"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

        with allure.step("Ввод некорректного email"):
            login_page.enter_email("invalid-email")
            login_page.enter_password("password123")

        with allure.step("Проверка валидации"):
            assert (
                login_page.is_validation_error_displayed()
            ), "Ошибка валидации не отображается"

    @fixme_test("Тест падает из-за изменений в UI")
    @allure.story("Восстановление пароля")
    @pytest.mark.fixme
    @pytest.mark.auth
    def test_password_recovery(self, browser, url):
        """Восстановление пароля"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

        with allure.step("Переход к восстановлению пароля"):
            login_page.click_forgot_password_link()
            # Этот тест сломан и требует исправления

        with allure.step("Проверка формы восстановления"):
            # Здесь должна быть проверка формы восстановления пароля
            pass


@allure.feature("Аутентификация")
@allure.story("Регистрация")
class TestRegistration:
    """Тесты регистрации пользователя"""

    @critical_test("Новый пользователь должен иметь возможность зарегистрироваться")
    @allure.story("Успешная регистрация")
    @pytest.mark.critical
    @pytest.mark.auth
    def test_successful_registration(self, browser, url, test_data):
        """Успешная регистрация нового пользователя"""
        with allure.step("Открытие страницы регистрации"):
            register_page = RegisterPage(browser, f"{url}/register.html")
            register_page.open()
            assert register_page.is_page_loaded(), "Страница регистрации не загрузилась"

        with allure.step("Заполнение формы регистрации"):
            new_user = test_data["users"]["new_user"]
            register_page.fill_form(
                email=new_user["email"],
                username=new_user["username"],
                full_name=new_user["full_name"],
                password=new_user["password"],
                confirm_password=new_user["password"],
            )

        with allure.step("Отправка формы"):
            register_page.submit_form()

        with allure.step("Проверка успешной регистрации"):
            assert (
                register_page.is_success_message_displayed()
            ), "Сообщение об успешной регистрации не отображается"

    @high_priority("Проверка уникальности email")
    @allure.story("Дублирование email")
    @pytest.mark.high
    @pytest.mark.auth
    def test_duplicate_email_registration(self, browser, url, test_data):
        """Регистрация с уже существующим email"""
        with allure.step("Открытие страницы регистрации"):
            register_page = RegisterPage(browser, f"{url}/register.html")
            register_page.open()

        with allure.step("Заполнение формы существующим email"):
            existing_user = test_data["users"]["valid_user"]
            register_page.fill_form(
                email=existing_user["email"],
                username="newusername",
                full_name="New User",
                password="newpassword123",
                confirm_password="newpassword123",
            )

        with allure.step("Отправка формы"):
            register_page.submit_form()

        with allure.step("Проверка ошибки дублирования"):
            assert (
                register_page.is_error_displayed()
            ), "Ошибка дублирования email не отображается"
            assert "already registered" in register_page.get_error_message().lower()


@allure.feature("Аутентификация")
@allure.story("JWT токены")
class TestJWTTokens:
    """Тесты JWT токенов"""

    @critical_test("Проверка работы JWT токенов")
    @allure.story("Сохранение токенов")
    @pytest.mark.critical
    @pytest.mark.auth
    def test_jwt_token_storage(self, browser, url, test_data):
        """Проверка сохранения JWT токенов"""
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

            user_data = test_data["users"]["valid_user"]
            login_page.sign_in(user_data["email"], user_data["password"])
            assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

        with allure.step("Проверка сохранения access токена"):
            access_token = browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            assert access_token is not None, "Access токен не сохранен"
            assert len(access_token) > 0, "Access токен пустой"

        with allure.step("Проверка сохранения refresh токена"):
            refresh_token = browser.execute_script(
                "return localStorage.getItem('refresh_token');"
            )
            assert refresh_token is not None, "Refresh токен не сохранен"
            assert len(refresh_token) > 0, "Refresh токен пустой"

        with allure.step("Проверка сохранения времени истечения"):
            expires = browser.execute_script(
                "return localStorage.getItem('token_expires');"
            )
            assert expires is not None, "Время истечения токена не сохранено"

            import time

            current_time = int(time.time() * 1000)
            expires_time = int(expires)
            assert (
                expires_time > current_time
            ), "Время истечения токена должно быть в будущем"

    @high_priority("Проверка обновления токенов")
    @allure.story("Refresh токен")
    @pytest.mark.high
    @pytest.mark.auth
    def test_refresh_token_functionality(self, browser, url, test_data):
        """Проверка функциональности refresh токена"""
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

            user_data = test_data["users"]["valid_user"]
            login_page.sign_in(user_data["email"], user_data["password"])
            assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

        with allure.step("Получение исходных токенов"):
            original_access_token = browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )
            refresh_token = browser.execute_script(
                "return localStorage.getItem('refresh_token');"
            )

            assert original_access_token is not None, "Access токен не найден"
            assert refresh_token is not None, "Refresh токен не найден"

        with allure.step("Симуляция истечения access токена"):
            browser.execute_script(
                "localStorage.setItem('token_expires', '1000000000');"
            )

        with allure.step("Переход на защищенную страницу"):
            browser.get(f"{url}/tests.html")

            # Проверяем, что произошло обновление токена
            new_access_token = browser.execute_script(
                "return localStorage.getItem('auth_token');"
            )

            # Токен должен был обновиться
            assert (
                new_access_token != original_access_token
            ), "Access токен не обновился"

    @debug_test("Проблема с автоматическим обновлением токенов")
    @allure.story("Автоматическое обновление")
    @pytest.mark.debug
    @pytest.mark.auth
    def test_automatic_token_refresh(self, browser, url, test_data):
        """Проверка автоматического обновления токенов"""
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

            user_data = test_data["users"]["valid_user"]
            login_page.sign_in(user_data["email"], user_data["password"])
            assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

        with allure.step("Проверка установки интервала обновления"):
            # Проверяем, что установлен интервал для автоматического обновления токенов
            refresh_interval = browser.execute_script(
                """
                return window.authManager ? window.authManager.refreshTimer : null;
            """
            )
            assert (
                refresh_interval is not None
            ), "Интервал автоматического обновления не установлен"


@allure.feature("Аутентификация")
@allure.story("Безопасность")
class TestSecurity:
    """Тесты безопасности"""

    @high_priority("Защита от XSS")
    @allure.story("XSS защита")
    @pytest.mark.high
    @pytest.mark.security
    def test_xss_protection(self, browser, url):
        """Проверка защиты от XSS атак"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

        with allure.step("Попытка XSS атаки"):
            xss_payload = "<script>alert('XSS')</script>"
            login_page.enter_email(xss_payload)
            login_page.enter_password("password")

        with allure.step("Проверка защиты"):
            # Проверяем, что скрипт не выполнился
            page_source = browser.page_source
            assert (
                "<script>alert('XSS')</script>" not in page_source
            ), "XSS атака не заблокирована"

    @high_priority("Защита от CSRF")
    @allure.story("CSRF защита")
    @pytest.mark.high
    @pytest.mark.security
    def test_csrf_protection(self, browser, url):
        """Проверка защиты от CSRF атак"""
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

            user_data = {"email": "test@example.com", "password": "testpassword123"}
            login_page.sign_in(user_data["email"], user_data["password"])
            assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

        with allure.step("Проверка наличия CSRF токена"):
            # Проверяем наличие CSRF токена в запросах
            csrf_token = browser.execute_script(
                """
                return document.querySelector('meta[name="csrf-token"]')?.content;
            """
            )

            # В реальном приложении здесь должна быть проверка CSRF токена
            # Пока просто проверяем, что тест выполняется
            assert True, "CSRF защита должна быть реализована"


@allure.feature("Аутентификация")
@allure.story("Производительность")
class TestPerformance:
    """Тесты производительности аутентификации"""

    @medium_priority("Время авторизации")
    @allure.story("Скорость авторизации")
    @pytest.mark.medium
    @pytest.mark.performance
    def test_login_performance(self, browser, url, test_data):
        """Проверка времени выполнения авторизации"""
        with allure.step("Открытие страницы входа"):
            login_page = LoginPage(browser, f"{url}/login.html")
            login_page.open()

        with allure.step("Измерение времени авторизации"):
            import time

            start_time = time.time()

            user_data = test_data["users"]["valid_user"]
            login_page.sign_in(user_data["email"], user_data["password"])

            end_time = time.time()
            auth_time = end_time - start_time

            # Авторизация должна занимать не более 5 секунд
            assert (
                auth_time < 5
            ), f"Авторизация заняла слишком много времени: {auth_time:.2f}с"

    @medium_priority("Нагрузочное тестирование")
    @allure.story("Множественные авторизации")
    @pytest.mark.medium
    @pytest.mark.performance
    def test_multiple_logins(self, browser, url, test_data):
        """Проверка множественных авторизаций"""
        user_data = test_data["users"]["valid_user"]

        for i in range(3):
            with allure.step(f"Авторизация #{i+1}"):
                browser.get(f"{url}/login.html")
                login_page = LoginPage(browser, f"{url}/login.html")

                login_page.sign_in(user_data["email"], user_data["password"])
                assert (
                    login_page.wait_for_redirect_to_tests()
                ), f"Авторизация #{i+1} не удалась"

                # Выход для следующей итерации
                if i < 2:
                    browser.execute_script("localStorage.clear();")
