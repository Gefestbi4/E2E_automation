import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("--browser-name")
    browser = None

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Подключение к Selenium Grid
        browser = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub", options=options
        )

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Подключение к Selenium Grid
        browser = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub", options=options
        )

    else:
        raise ValueError(f"Браузер '{browser_name}' не поддерживается.")

    browser.implicitly_wait(15)
    yield browser

    try:
        browser.execute_script("window.localStorage.clear();")
    except Exception as e:
        print(f"Warning: Could not clear localStorage: {e}")
    time.sleep(1)
    browser.quit()


def pytest_addoption(parser):
    """Добавляет опции в pytest для выбора браузера и режима запуска."""
    parser.addoption(
        "--browser-name",
        action="store",
        default="chrome",
        help="Имя браузера для тестирования (chrome/firefox/safari)",
    )


@pytest.fixture(scope="session")
def url():
    """Базовый URL для тестирования"""
    return "http://frontend:80"
