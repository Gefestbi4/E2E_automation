import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

SELENIUM_HUB_URL = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")

@pytest.fixture(scope="function")
def bowser(request):
    """
    Фикстура для инициализации сеанса Selenium с передачей нужного браузера.
    Поддерживаемые браузеры: Chrome, Firefox, Safari.
    """
    # Получаем имя браузера из командной строки lower - приведение к нижнему регистру
    browser_name = request.config.getoption("--browser-name").lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-fullscreen")  # Используем аргумент для полного экрана
        # options.add_argument("--disable-gpu")  # Отключаем GPU ускорение
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')  # отключает использование /dev/shm ограничивающее использованную память для запуска контейнера
        options.add_argument('disable-infobars')  # отключает инфобар у браузера
        options.add_argument("--disable-extensions")  # отключает установленные надстроки для браузера
        # options.page_load_strategy = 'eager'  # change behavior page load strategy to waiting only when DOM is loaded
        # options.page_load_strategy = 'none'  # Does not block WebDriver at all

        # Можно установить путь к бинарнику Chrome (если это необходимо)
        # options.binary_location = '/usr/bin/google-chrome-stable'

        # Запуск на удаленном хабе с браузерами
        #bowser = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с Хром браузером
        bowser = webdriver.Chrome(options=options)
        bowser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.headless = False  # Включаем видимый интерфейс браузера
        options.accept_insecure_certs = True  # Принятие небезопасных сертификатов

        # Запуск на удаленном хабе с браузерами
        #bowser = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с FireFox браузером
        bowser = webdriver.Firefox(options=options)
        bowser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    elif browser_name == "safari":
        options = SafariOptions()
        options.set_capability("allowAllWebViewScripts", True)

        # Запуск на удаленном хабе с браузерами
        #bowser = webdriver.Remote( command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с Safari браузером
        bowser = webdriver.Safari(options=options)
        bowser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    yield bowser

    bowser.execute_script('window.localStorage.clear();') # очистка токена из локалстораджа
    time.sleep(1)
    bowser.quit()


def pytest_addoption(parser):
    """
    Добавляет опцию в pytest для выбора браузера для тестирования.
    """
    parser.addoption("--browser-name", action="store", default="chrome",
                     help="Имя браузера для тестирования (chrome/firefox/safari)")
