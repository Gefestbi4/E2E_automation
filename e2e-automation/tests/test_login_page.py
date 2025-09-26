import os
import sys
import pytest
import allure
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.Locators import LoginPageLocators, TestsPageLocators

# Добавляем путь к api модулю
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from api.api_user import UserApi

load_dotenv()

# Получаем переменные окружения
api_key = os.getenv("API_KEY")
email = os.getenv("EMAIL", "test@example.com")
password = os.getenv("PASSWORD", "test123")
url = os.getenv("URL", "http://localhost:3000")


@pytest.fixture(scope="function")
def login_page(browser, url):
    """Фикстура для создания страницы логина"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()
    return page


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""
    return UserApi("http://localhost:5000", api_key)


# ============================================== Тесты для страницы авторизации ==============================================


@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
@pytest.mark.crit
def test_successful_login(login_page):
    """Проверка успешной авторизации пользователя"""
    # Авторизация (шаг уже есть в sign_in())
    login_page.sign_in(email, password)

    # Проверка перенаправления (шаг уже есть в is_redirected_to_tests())
    login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
    assert (
        login_page.is_redirected_to_tests()
    ), "Ожидалось перенаправление на tests.html"

    # Проверка элементов страницы тестов
    assert login_page.is_element_present(
        *TestsPageLocators.PAGE_TITLE
    ), "Заголовок страницы тестов не найден"
    assert login_page.is_element_present(
        *TestsPageLocators.SIDEBAR
    ), "Сайдбар не найден"


@allure.feature("Авторизация")
@allure.story("Автоматическая регистрация")
@pytest.mark.medium
def test_auto_registration_new_user(login_page, api_client):
    """Проверка автоматической регистрации нового пользователя"""
    new_email = "newuser@example.com"
    new_password = "newpassword123"

    # Удаление пользователя если существует
    try:
        api_client.delete_user(new_email)
    except:
        pass

    # Авторизация (шаг уже есть в sign_in())
    login_page.sign_in(new_email, new_password)

    # Проверка перенаправления (шаг уже есть в is_redirected_to_tests())
    login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
    assert (
        login_page.is_redirected_to_tests()
    ), "Ожидалось перенаправление на tests.html"


@allure.feature("Авторизация")
@allure.story("Валидация полей")
@pytest.mark.medium
def test_form_validation(login_page):
    """Проверка валидации формы авторизации"""
    # Проверка обязательных полей
    email_field = login_page.find_element(*LoginPageLocators.EMAIL_INPUT)
    password_field = login_page.find_element(*LoginPageLocators.PASSWORD_INPUT)

    assert (
        email_field.get_attribute("required") is not None
    ), "Поле email должно быть обязательным"
    assert (
        password_field.get_attribute("required") is not None
    ), "Поле пароль должно быть обязательным"

    # Проверка типов полей
    assert email_field.get_attribute("type") == "email", "Поле должно иметь тип email"
    assert (
        password_field.get_attribute("type") == "password"
    ), "Поле должно иметь тип password"

    # Проверка валидности формы (шаг уже есть в fill_form_with_test_data() и is_form_valid())
    login_page.fill_form_with_test_data()
    assert (
        login_page.is_form_valid()
    ), "Форма должна быть валидной с корректными данными"


@allure.feature("Авторизация")
@allure.story("Ошибки авторизации")
@pytest.mark.medium
def test_invalid_credentials(login_page):
    """Проверка обработки неверных учетных данных"""
    # Авторизация (шаг уже есть в sign_in())
    login_page.sign_in("invalid@example.com", "wrongpassword")

    # Проверка результата (шаг уже есть в is_redirected_to_tests())
    login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
    assert (
        login_page.is_redirected_to_tests()
    ), "Ожидалось перенаправление на tests.html"

    # Проверка токена
    token = login_page.browser.execute_script(
        "return localStorage.getItem('auth_token');"
    )
    assert (
        token is not None
    ), "Токен авторизации должен быть сохранен (автоматическая регистрация)"
    assert len(token) > 0, "Токен авторизации не должен быть пустым"


@allure.feature("Авторизация")
@allure.story("UI элементы")
@pytest.mark.low
def test_login_page_elements(login_page):
    """Проверка наличия всех элементов на странице авторизации"""
    # Проверка заголовка (шаг уже есть в get_page_title())
    assert login_page.is_element_present(
        *LoginPageLocators.PAGE_TITLE
    ), "Заголовок страницы не найден"

    title_text = login_page.get_page_title()
    assert (
        "вход" in title_text.lower() or "login" in title_text.lower()
    ), f"Неожиданный текст заголовка: {title_text}"

    # Проверка формы авторизации
    assert login_page.is_element_present(
        *LoginPageLocators.LOGIN_FORM
    ), "Форма авторизации не найдена"
    assert login_page.is_element_present(
        *LoginPageLocators.EMAIL_INPUT
    ), "Поле email не найдено"
    assert login_page.is_element_present(
        *LoginPageLocators.PASSWORD_INPUT
    ), "Поле пароль не найдено"
    assert login_page.is_element_present(
        *LoginPageLocators.LOGIN_SUBMIT_BUTTON
    ), "Кнопка отправки не найдена"
    assert login_page.is_element_present(
        *LoginPageLocators.LOGIN_STATUS
    ), "Элемент статуса не найден"

    # Проверка активности кнопки (шаг уже есть в is_login_button_enabled())
    assert (
        login_page.is_login_button_enabled()
    ), "Кнопка авторизации должна быть активна"

    # Проверка плейсхолдеров
    email_input = login_page.find_element(*LoginPageLocators.EMAIL_INPUT)
    password_input = login_page.find_element(*LoginPageLocators.PASSWORD_INPUT)

    assert (
        email_input.get_attribute("placeholder") is not None
    ), "Поле email должно иметь плейсхолдер"
    assert (
        password_input.get_attribute("placeholder") is not None
    ), "Поле пароль должно иметь плейсхолдер"


@allure.feature("Авторизация")
@allure.story("Токен авторизации")
@pytest.mark.medium
def test_auth_token_storage(login_page, api_client):
    """Проверка сохранения токена авторизации в localStorage"""
    # Авторизация (шаг уже есть в sign_in())
    login_page.sign_in(email, password)

    # Ожидание перенаправления (шаг уже есть в wait_for_url_change())
    login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)

    # Проверка токена
    token = login_page.get_auth_token()
    assert token is not None, "Токен авторизации не сохранен в localStorage"
    assert len(token) > 0, "Токен авторизации пустой"
    assert token.count(".") == 2, f"Токен не имеет формат JWT: {token[:30]}..."


def test_fail_login(login_page):
    """Проверка обработки неверных учетных данных"""
    login_page.sign_in("invalid@example.com", "wrongssword1")
    assert login_page.is_redirected_to_tests()
    assert login_page.is_element_present(
        *LoginPageLocators.LOGIN_STATUS
    ), "Элемент статуса не найден"
    assert login_page.get_status_message() == "Неверный email или пароль"
