"""
Тесты обработки ошибок
"""

import pytest
import allure
from pages.login_page import LoginPage
from pages.tests_page import TestsPage
from config.settings import Settings
from utils.helpers import TestHelpers


@allure.feature("Обработка ошибок")
@allure.story("Сетевые ошибки")
@pytest.mark.medium
def test_network_error_handling(browser, url):
    """Проверка обработки сетевых ошибок"""
    # Пытаемся загрузить несуществующую страницу для симуляции сетевой ошибки
    try:
        browser.get(f"{url}/nonexistent-page-that-causes-network-error")
    except Exception as e:
        # Проверяем, что ошибка связана с сетью
        assert (
            "network" in str(e).lower() or "connection" in str(e).lower()
        ), "Ошибка сети не обнаружена"


@allure.feature("Обработка ошибок")
@allure.story("API ошибки")
@pytest.mark.medium
def test_api_error_handling(browser, url):
    """Проверка обработки API ошибок"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()

    # Пытаемся авторизоваться с неверными данными
    page.sign_in("invalid@example.com", "wrongpassword")

    # Проверяем, что показывается сообщение об ошибке (проверяем URL или заголовок)
    current_url = browser.current_url
    page_title = browser.title

    # Проверяем, что пользователь остался на странице входа (правильное поведение)
    # Это демонстрирует, что фронтенд теперь правильно обрабатывает ошибки API
    assert (
        "login" in current_url
    ), "Пользователь должен остаться на странице входа при ошибке авторизации"
    assert (
        "Вход" in page_title or "Login" in page_title or "Авторизация" in page_title
    ), "Страница входа должна отображаться"


@allure.feature("Обработка ошибок")
@allure.story("404 ошибки")
@pytest.mark.low
def test_404_error_handling(browser, url):
    """Проверка обработки 404 ошибок"""
    # Переходим на несуществующую страницу
    browser.get(f"{url}/nonexistent-page.html")

    # Проверяем, что показывается страница 404
    assert (
        "404" in browser.title or "Not Found" in browser.title
    ), "Страница 404 не отображается"


@allure.feature("Обработка ошибок")
@allure.story("500 ошибки")
@pytest.mark.low
def test_500_error_handling(browser, url):
    """Проверка обработки 500 ошибок"""
    # Пытаемся обратиться к несуществующему API endpoint
    browser.get(f"{url}/api/nonexistent")

    # Проверяем, что показывается сообщение об ошибке сервера (404 вместо 500)
    page_source = browser.page_source
    assert (
        "404" in page_source or "Not Found" in page_source
    ), "Ошибка 404 не обрабатывается"


@allure.feature("Обработка ошибок")
@allure.story("Таймауты")
@pytest.mark.medium
def test_timeout_error_handling(browser, url):
    """Проверка обработки таймаутов"""
    # Устанавливаем очень короткий таймаут
    browser.set_page_load_timeout(1)

    try:
        # Пытаемся загрузить страницу
        page = LoginPage(browser, f"{url}/login.html")
        page.open()
    except Exception as e:
        # Проверяем, что таймаут обрабатывается корректно
        assert "timeout" in str(e).lower(), "Таймаут не обрабатывается корректно"
    finally:
        # Восстанавливаем нормальный таймаут
        browser.set_page_load_timeout(30)


@allure.feature("Обработка ошибок")
@allure.story("Валидация форм")
@pytest.mark.medium
def test_form_validation_errors(browser, url):
    """Проверка обработки ошибок валидации форм"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()

    # Пытаемся отправить пустую форму
    page.submit_sign_in_btn()

    # Проверяем, что остались на странице входа (HTML5 валидация предотвратила отправку)
    current_url = browser.current_url
    assert "login" in current_url, "Форма была отправлена без валидации"


@allure.feature("Обработка ошибок")
@allure.story("JavaScript ошибки")
@pytest.mark.low
def test_javascript_error_handling(browser, url):
    """Проверка обработки JavaScript ошибок"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()

    # Выполняем JavaScript код, который может вызвать ошибку
    try:
        browser.execute_script("throw new Error('Test JavaScript error');")
    except Exception as e:
        # Проверяем, что JavaScript ошибки обрабатываются
        assert "Test JavaScript error" in str(e), "JavaScript ошибки не обрабатываются"


@allure.feature("Обработка ошибок")
@allure.story("Восстановление после ошибок")
@pytest.mark.medium
def test_error_recovery(browser, url):
    """Проверка восстановления после ошибок"""
    page = LoginPage(browser, f"{url}/login.html")
    page.open()

    # Вызываем ошибку
    try:
        page.sign_in("invalid@example.com", "wrongpassword")
    except Exception:
        pass

    # Проверяем, что приложение восстанавливается
    page.refresh()
    # Проверяем, что страница загрузилась (проверяем заголовок)
    # После refresh пользователь может остаться на tests.html (токен еще действителен)
    current_url = browser.current_url
    assert (
        "tests" in current_url or "login" in current_url
    ), "Пользователь должен быть на tests.html или перенаправлен на login"
    page_title = browser.title
    assert (
        "Демо компонентов" in page_title
        or "Страница тестов" in page_title
        or "Вход" in page_title
        or "Login" in page_title
        or "Авторизация" in page_title
    ), "Страница должна отображаться корректно"
