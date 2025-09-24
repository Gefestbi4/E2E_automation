import os
import pytest
import allure
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests_E2E.pages.login_page import LoginPage
from tests_E2E.pages.Locators import LoginPageLocators, TestsPageLocators, get_locator
from api.api_user import UserApi

load_dotenv()  # Загружает переменные из .env

# Получаем переменные окружения
api_key = os.getenv('API_KEY')
database_url = os.getenv('DATABASE_URL')
email = os.getenv('EMAIL', 'test@example.com')
password = os.getenv('PASSWORD', 'testpassword123')
name = os.getenv('USER_NAME', 'Test User')

# Генерируем уникальные email для тестов
import time
timestamp = int(time.time())
test_email = f"test{timestamp}@example.com"


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


@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
@pytest.mark.crit
def test_successful_login(login_page, api_client):
    """Проверка успешной авторизации пользователя"""
    with allure.step("Заполнение формы авторизации"):
        login_page.enter_login(test_email)
        login_page.enter_password(password)
    
    with allure.step("Отправка формы"):
        login_page.submit_sign_in_btn()
    
    with allure.step("Проверка статуса авторизации"):
        # Ждем появления статуса
        login_page.wait_for_element_visible(*LoginPageLocators.LOGIN_STATUS, timeout=10)
        
        # Проверяем статус
        status_text = login_page.get_status_message()
        allure.attach(f"Статус авторизации: {status_text}", "Status", allure.attachment_type.TEXT)
        
        # Если есть ошибка, выводим её
        if "ошибка" in status_text.lower() or "error" in status_text.lower():
            pytest.fail(f"Ошибка авторизации: {status_text}")
    
    with allure.step("Проверка перенаправления на страницу тестов"):
        # Ждем перенаправления на страницу тестов
        login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
        
        # Проверяем, что мы на странице тестов
        current_url = login_page.browser.current_url
        assert "/tests.html" in current_url, f"Ожидалось перенаправление на tests.html, получен URL: {current_url}"
        
        # Проверяем наличие элементов страницы тестов
        assert login_page.is_element_present(*TestsPageLocators.PAGE_TITLE), "Заголовок страницы тестов не найден"
        assert login_page.is_element_present(*TestsPageLocators.SIDEBAR), "Сайдбар не найден"


@allure.feature("Авторизация")
@allure.story("Автоматическая регистрация")
@pytest.mark.medium
def test_auto_registration_new_user(login_page, api_client):
    """Проверка автоматической регистрации нового пользователя"""
    new_email = "newuser@example.com"
    new_password = "newpassword123"
    
    with allure.step("Удаление пользователя если существует"):
        try:
            api_client.delete_user(new_email)
        except:
            pass  # Пользователь может не существовать
    
    with allure.step("Заполнение формы с новыми данными"):
        login_page.enter_login(new_email)
        login_page.enter_password(new_password)
    
    with allure.step("Отправка формы для регистрации"):
        login_page.submit_sign_in_btn()
    
    with allure.step("Проверка успешной регистрации и перенаправления"):
        login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
        
        current_url = login_page.browser.current_url
        assert "/tests.html" in current_url, f"Ожидалось перенаправление на tests.html, получен URL: {current_url}"


@allure.feature("Авторизация")
@allure.story("Валидация полей")
@pytest.mark.medium
def test_form_validation(login_page):
    """Проверка валидации формы авторизации"""
    with allure.step("Проверка обязательных полей"):
        # Проверяем, что поля помечены как обязательные
        email_field = login_page.find_element(*LoginPageLocators.EMAIL_INPUT)
        password_field = login_page.find_element(*LoginPageLocators.PASSWORD_INPUT)
        
        assert email_field.get_attribute("required") is not None, "Поле email должно быть обязательным"
        assert password_field.get_attribute("required") is not None, "Поле пароль должно быть обязательным"
    
    with allure.step("Проверка типов полей"):
        assert email_field.get_attribute("type") == "email", "Поле должно иметь тип email"
        assert password_field.get_attribute("type") == "password", "Поле должно иметь тип password"


@allure.feature("Авторизация")
@allure.story("Ошибки авторизации")
@pytest.mark.medium
def test_invalid_credentials(login_page):
    """Проверка обработки неверных учетных данных"""
    with allure.step("Ввод неверных учетных данных"):
        login_page.enter_login("invalid@example.com")
        login_page.enter_password("wrongpassword")
    
    with allure.step("Отправка формы"):
        login_page.submit_sign_in_btn()
    
    with allure.step("Проверка результата авторизации"):
        # В новом бэкенде пользователи создаются автоматически, поэтому неверные данные
        # тоже приведут к успешной авторизации и перенаправлению
        # Проверяем, что происходит перенаправление (что означает успешную авторизацию)
        login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
        
        # Проверяем, что мы на странице тестов (автоматическая регистрация)
        current_url = login_page.browser.current_url
        assert "/tests.html" in current_url, f"Ожидалось перенаправление на tests.html, получен URL: {current_url}"
        
        # Проверяем, что токен сохранен (пользователь был создан)
        token = login_page.browser.execute_script("return localStorage.getItem('auth_token');")
        assert token is not None, "Токен авторизации должен быть сохранен (автоматическая регистрация)"
        assert len(token) > 0, "Токен авторизации не должен быть пустым"


@allure.feature("Авторизация")
@allure.story("UI элементы")
@pytest.mark.low
def test_login_page_elements(login_page):
    """Проверка наличия всех элементов на странице авторизации"""
    with allure.step("Проверка заголовка страницы"):
        assert login_page.is_element_present(*LoginPageLocators.PAGE_TITLE), "Заголовок страницы не найден"
        
        title_text = login_page.find_element(*LoginPageLocators.PAGE_TITLE).text
        assert "вход" in title_text.lower() or "login" in title_text.lower(), f"Неожиданный текст заголовка: {title_text}"
    
    with allure.step("Проверка формы авторизации"):
        assert login_page.is_element_present(*LoginPageLocators.LOGIN_FORM), "Форма авторизации не найдена"
        assert login_page.is_element_present(*LoginPageLocators.EMAIL_INPUT), "Поле email не найдено"
        assert login_page.is_element_present(*LoginPageLocators.PASSWORD_INPUT), "Поле пароль не найдено"
        assert login_page.is_element_present(*LoginPageLocators.LOGIN_SUBMIT_BUTTON), "Кнопка отправки не найдена"
        assert login_page.is_element_present(*LoginPageLocators.LOGIN_STATUS), "Элемент статуса не найден"
    
    with allure.step("Проверка плейсхолдеров"):
        email_input = login_page.find_element(*LoginPageLocators.EMAIL_INPUT)
        password_input = login_page.find_element(*LoginPageLocators.PASSWORD_INPUT)
        
        assert email_input.get_attribute("placeholder") is not None, "Поле email должно иметь плейсхолдер"
        assert password_input.get_attribute("placeholder") is not None, "Поле пароль должно иметь плейсхолдер"


@allure.feature("Авторизация")
@allure.story("Навигация")
@pytest.mark.low
def test_navigation_from_login_page(login_page):
    """Проверка навигации со страницы авторизации"""
    with allure.step("Проверка возможности возврата на главную страницу"):
        # Проверяем, что можно перейти на главную страницу
        login_page.browser.get(login_page.base_url)
        
        # Проверяем, что мы на главной странице
        current_url = login_page.browser.current_url
        assert current_url == login_page.base_url or current_url.endswith("/"), f"Ожидалась главная страница, получен URL: {current_url}"


@allure.feature("Авторизация")
@allure.story("Токен авторизации")
@pytest.mark.medium
def test_auth_token_storage(login_page, api_client):
    """Проверка сохранения токена авторизации в localStorage"""
    with allure.step("Авторизация пользователя"):
        login_page.enter_login(test_email)
        login_page.enter_password(password)
        login_page.submit_sign_in_btn()
    
    with allure.step("Ожидание перенаправления"):
        login_page.wait_for_url_change(f"{login_page.base_url}/tests.html", timeout=10)
    
    with allure.step("Проверка сохранения токена в localStorage"):
        # Проверяем, что токен сохранен в localStorage
        token = login_page.browser.execute_script("return localStorage.getItem('auth_token');")
        assert token is not None, "Токен авторизации не сохранен в localStorage"
        assert len(token) > 0, "Токен авторизации пустой"
        
        # Проверяем, что токен имеет правильный формат (JWT)
        assert token.count('.') == 2, f"Токен не имеет формат JWT: {token[:20]}..."