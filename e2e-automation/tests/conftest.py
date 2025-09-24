import os
import time
import pytest
import random
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

SELENIUM_HUB_URL = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")

@pytest.fixture(scope="function")
def browser(request):
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
        options.add_argument('--disable-background-timer-throttling')  # отключает ограничения таймеров в фоне
        options.add_argument('--disable-backgrounding-occluded-windows')  # отключает фоновую обработку скрытых окон
        options.add_argument('--disable-renderer-backgrounding')  # отключает фоновую обработку рендерера
        options.add_argument('--disable-features=TranslateUI')  # отключает переводы
        options.add_argument('--disable-ipc-flooding-protection')  # отключает защиту от IPC флудинга
        options.add_argument('--disable-hang-monitor')  # отключает мониторинг зависаний
        options.add_argument('--disable-prompt-on-repost')  # отключает запросы на повторную отправку
        options.add_argument('--disable-sync')  # отключает синхронизацию
        options.add_argument('--disable-web-security')  # отключает веб-безопасность для тестов
        options.add_argument('--disable-features=VizDisplayCompositor')  # отключает композитор дисплея
        # options.page_load_strategy = 'eager'  # change behavior page load strategy to waiting only when DOM is loaded
        # options.page_load_strategy = 'none'  # Does not block WebDriver at all

        # Для локального запуска используем Selenium Manager
        # Для Docker контейнера раскомментируйте следующие строки:
        # options.binary_location = '/usr/bin/chromium'
        # service = ChromeService(executable_path='/usr/bin/chromedriver')
        
        # Для локального запуска
        service = ChromeService()

        # Запуск на удаленном хабе с браузерами
        #bowser = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с Хром браузером
        browser = webdriver.Chrome(service=service, options=options)
        browser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.headless = False  # Включаем видимый интерфейс браузера
        options.accept_insecure_certs = True  # Принятие небезопасных сертификатов

        # Запуск на удаленном хабе с браузерами
        #bowser = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с FireFox браузером
        browser = webdriver.Firefox(options=options)
        browser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    elif browser_name == "safari":
        options = SafariOptions()
        options.set_capability("allowAllWebViewScripts", True)

        # Запуск на удаленном хабе с браузерами
        #browser = webdriver.Remote( command_executor=SELENIUM_HUB_URL, options=options)

        # Запуск на локальной машине с Safari браузером
        browser = webdriver.Safari(options=options)
        browser.implicitly_wait(15) # Устанавливаем не явное ожидание обнаружения элементов на странице

    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    yield browser

    browser.execute_script('window.localStorage.clear();') # очистка токена из локалстораджа
    time.sleep(1)
    browser.quit()


@pytest.fixture(scope="function")
def url():
    """
    Фикстура для получения URL тестируемого приложения.
    """
    return os.getenv("TEST_URL", "http://localhost:3000")


def pytest_addoption(parser):
    """
    Добавляет опцию в pytest для выбора браузера для тестирования.
    """
    parser.addoption("--browser-name", action="store", default="chrome",
                     help="Имя браузера для тестирования (chrome/firefox/safari)")
