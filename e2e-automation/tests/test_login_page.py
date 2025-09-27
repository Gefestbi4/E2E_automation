"""
E2E tests for login page using improved architecture
"""

import pytest
import allure
from pages.login_page import LoginPage
from config.settings import Settings
from utils.helpers import TestHelpers


@pytest.fixture(scope="function")
def login_page(browser, url):
    """Фикстура для создания страницы логина"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()
    return page


@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
@pytest.mark.crit
@pytest.mark.smoke
def test_successful_login(login_page, test_data):
    """Проверка успешной авторизации пользователя"""
    user_data = test_data["users"]["valid_user"]

    # Авторизация
    login_page.sign_in(user_data["email"], user_data["password"])

    # Ожидание перенаправления
    assert login_page.wait_for_redirect_to_tests(
        timeout=15
    ), "Ожидалось перенаправление на tests.html"

    # Проверка заголовка страницы
    assert (
        login_page.get_page_title() == "Демо компонентов"
    ), "Неверный заголовок страницы"


@allure.feature("Авторизация")
@allure.story("Неуспешная авторизация")
@pytest.mark.crit
@pytest.mark.smoke
def test_invalid_credentials(login_page, test_data):
    """Проверка авторизации с неверными данными"""
    user_data = test_data["users"]["invalid_user"]

    # Попытка авторизации с неверными данными
    login_page.sign_in(user_data["email"], user_data["password"])

    # Проверка сообщения об ошибке
    status_message = login_page.wait_for_status_message(timeout=10)
    assert (
        "Incorrect password" in status_message
    ), f"Ожидалось сообщение об ошибке пароля, получено: {status_message}"


@allure.feature("Авторизация")
@allure.story("Автоматическая регистрация")
@pytest.mark.medium
def test_auto_registration_new_user(login_page, test_data):
    """Проверка автоматической регистрации нового пользователя"""
    user_data = test_data["users"]["new_user"]

    # Авторизация нового пользователя
    login_page.sign_in(user_data["email"], user_data["password"])

    # Ожидание перенаправления
    assert login_page.wait_for_redirect_to_tests(
        timeout=15
    ), "Ожидалось перенаправление на tests.html"


@allure.feature("Валидация формы")
@allure.story("Проверка валидности формы")
@pytest.mark.medium
def test_form_validation(login_page, test_data):
    """Проверка валидности формы авторизации"""
    user_data = test_data["users"]["valid_user"]

    # Заполнение формы корректными данными
    login_page.fill_form_with_test_data(user_data["email"], user_data["password"])

    # Проверка валидности формы
    assert (
        login_page.is_form_valid()
    ), "Форма должна быть валидной с корректными данными"

    # Проверка активности кнопки
    assert login_page.is_login_button_enabled(), "Кнопка входа должна быть активной"


@allure.feature("Авторизация")
@allure.story("Хранение токена")
@pytest.mark.medium
def test_auth_token_storage(login_page, test_data):
    """Проверка сохранения токена авторизации"""
    user_data = test_data["users"]["valid_user"]

    # Авторизация
    login_page.sign_in(user_data["email"], user_data["password"])

    # Ожидание перенаправления
    assert login_page.wait_for_redirect_to_tests(
        timeout=15
    ), "Ожидалось перенаправление на tests.html"

    # Проверка наличия access токена
    token = login_page.get_auth_token()
    assert token is not None, "Access токен должен быть сохранен"
    assert len(token) > 0, "Access токен не должен быть пустым"

    # Проверка наличия refresh токена
    assert login_page.is_refresh_token_present(), "Refresh токен должен быть сохранен"

    # Проверка наличия информации об истечении токена
    assert (
        login_page.is_token_expires_present()
    ), "Информация об истечении токена должна быть сохранена"

    # Проверка времени истечения токена
    expires_time = login_page.get_token_expiration_time()
    assert expires_time is not None, "Время истечения токена должно быть установлено"
    current_time = login_page.browser.execute_script("return Date.now();")
    assert expires_time > current_time, "Время истечения токена должно быть в будущем"


@allure.feature("Авторизация")
@allure.story("Refresh токен")
@pytest.mark.medium
def test_refresh_token_functionality(browser, url, test_data):
    """Проверка функциональности refresh токена"""
    from pages.login_page import LoginPage

    user_data = test_data["users"]["valid_user"]
    login_page = LoginPage(browser, f"{url}/login.html")
    login_page.open()

    # Авторизация
    login_page.sign_in(user_data["email"], user_data["password"])
    assert login_page.wait_for_redirect_to_tests(), "Авторизация не удалась"

    # Получаем refresh токен
    refresh_token = browser.execute_script(
        "return localStorage.getItem('refresh_token');"
    )
    assert refresh_token is not None, "Refresh токен должен быть сохранен"

    # Симулируем истечение access токена, установив время истечения в прошлое
    browser.execute_script("localStorage.setItem('token_expires', '1000000000');")

    # Переходим на страницу tests.html - должна произойти проверка авторизации
    browser.get(f"{url}/tests.html")

    # Проверяем, что пользователь перенаправлен на страницу входа
    current_url = browser.current_url
    assert (
        "login" in current_url
    ), "Пользователь должен быть перенаправлен на страницу входа при истекшем токене"


@allure.feature("Авторизация")
@allure.story("Неуспешная авторизация")
@pytest.mark.low
def test_fail_login(login_page, test_data):
    """Тест, который должен упасть для демонстрации отчетности"""
    user_data = test_data["users"]["invalid_user"]

    # Попытка авторизации с неверными данными
    login_page.sign_in(user_data["email"], user_data["password"])

    # Намеренно неверная проверка для демонстрации падения теста
    assert login_page.wait_for_redirect_to_tests(
        timeout=5
    ), "Этот тест должен упасть для демонстрации отчетности"
