"""
Base test class for E2E automation tests  # Документация базового класса для E2E тестов
"""

import pytest  # Импорт фреймворка тестирования pytest
import allure  # Импорт библиотеки Allure для отчетности
import logging  # Импорт модуля логирования Python
from typing import Dict, Any, Optional  # Импорт типов для аннотаций типов
from selenium import webdriver  # Импорт основного модуля Selenium WebDriver
from selenium.webdriver.remote.webdriver import WebDriver  # Импорт класса WebDriver
from selenium.webdriver.support.ui import (
    WebDriverWait,
)  # Импорт класса WebDriverWait для ожиданий
from selenium.webdriver.support import (
    expected_conditions as EC,
)  # Импорт ожидаемых условий
from selenium.webdriver.common.by import By  # Импорт класса By для селекторов
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)  # Импорт исключений Selenium
from config.settings import Settings  # Импорт класса настроек
from utils.logger import TestLogger  # Импорт класса логгера тестов
from utils.screenshot import ScreenshotManager  # Импорт менеджера скриншотов
from utils.api_client import APIClient  # Импорт API клиента


class BaseTest:  # Определение базового класса для всех E2E тестов
    """Base class for all E2E tests with common functionality"""  # Документация класса

    def __init__(self):  # Конструктор класса BaseTest
        self.settings = Settings()  # Инициализация объекта настроек
        self.logger = TestLogger()  # Инициализация логгера для тестов
        self.screenshot_manager = (
            ScreenshotManager()
        )  # Инициализация менеджера скриншотов
        self.api_client = APIClient()  # Инициализация API клиента
        self.driver: Optional[WebDriver] = None  # Инициализация WebDriver как None
        self.wait: Optional[WebDriverWait] = (
            None  # Инициализация WebDriverWait как None
        )
        self.test_data = (
            self.settings.get_test_data()
        )  # Загрузка тестовых данных из настроек

    @pytest.fixture(
        autouse=True
    )  # Декоратор pytest для автоматического использования фикстуры
    def setup_and_teardown(
        self, request
    ):  # Метод настройки и очистки для каждого теста
        """Setup and teardown for each test"""  # Документация метода
        # Setup  # Комментарий о настройке
        self.setup_driver()  # Вызов метода настройки WebDriver
        self.setup_wait()  # Вызов метода настройки WebDriverWait
        self.logger.info(
            f"Starting test: {request.node.name}"
        )  # Логирование начала теста

        # Add test info to Allure  # Комментарий о добавлении информации в Allure
        allure.dynamic.description(
            f"Test: {request.node.name}"
        )  # Установка описания теста в Allure
        allure.dynamic.severity(
            allure.severity_level.NORMAL
        )  # Установка уровня серьезности теста

        yield  # Ключевое слово для разделения setup и teardown

        # Teardown  # Комментарий об очистке
        self.cleanup(request)  # Вызов метода очистки после теста

    def setup_driver(self):  # Метод настройки WebDriver с конфигурацией
        """Setup WebDriver with configuration"""  # Документация метода
        try:  # Начало блока обработки исключений
            from selenium.webdriver.chrome.options import (
                Options as ChromeOptions,
            )  # Импорт опций Chrome
            from selenium.webdriver.firefox.options import (
                Options as FirefoxOptions,
            )  # Импорт опций Firefox
            from selenium.webdriver.remote.webdriver import (
                WebDriver as RemoteWebDriver,
            )  # Импорт RemoteWebDriver

            if (
                self.settings.BROWSER_NAME.lower() == "chrome"
            ):  # Проверка если браузер Chrome
                options = ChromeOptions()  # Создание объекта опций Chrome
                browser_options = (
                    self.settings.get_browser_options()
                )  # Получение опций браузера из настроек

                for arg in browser_options.get(
                    "args", []
                ):  # Цикл по аргументам браузера
                    options.add_argument(arg)  # Добавление аргумента в опции Chrome

                for (
                    key,
                    value,
                ) in browser_options.get(  # Цикл по экспериментальным опциям
                    "experimental_options", {}  # Получение экспериментальных опций
                ).items():  # Итерация по ключам и значениям
                    options.add_experimental_option(
                        key, value
                    )  # Добавление экспериментальной опции

                for key, value in browser_options.get(
                    "prefs", {}
                ).items():  # Цикл по предпочтениям
                    options.add_experimental_option(
                        "prefs", {key: value}
                    )  # Добавление предпочтения

                self.driver = RemoteWebDriver(  # Создание RemoteWebDriver
                    command_executor=self.settings.SELENIUM_HUB_URL,
                    options=options,  # URL Selenium Hub и опции
                )

            elif (
                self.settings.BROWSER_NAME.lower() == "firefox"
            ):  # Проверка если браузер Firefox
                options = FirefoxOptions()  # Создание объекта опций Firefox
                browser_options = (
                    self.settings.get_browser_options()
                )  # Получение опций браузера

                for arg in browser_options.get(
                    "args", []
                ):  # Цикл по аргументам браузера
                    options.add_argument(arg)  # Добавление аргумента в опции Firefox

                for key, value in browser_options.get(
                    "prefs", {}
                ).items():  # Цикл по предпочтениям
                    options.set_preference(key, value)  # Установка предпочтения Firefox

                self.driver = RemoteWebDriver(  # Создание RemoteWebDriver
                    command_executor=self.settings.SELENIUM_HUB_URL,
                    options=options,  # URL Selenium Hub и опции
                )

            self.driver.implicitly_wait(
                self.settings.IMPLICIT_WAIT
            )  # Установка неявного ожидания
            self.driver.set_page_load_timeout(
                self.settings.PAGE_LOAD_TIMEOUT
            )  # Установка таймаута загрузки страницы

            self.logger.info(
                f"WebDriver initialized: {self.settings.BROWSER_NAME}"
            )  # Логирование инициализации WebDriver

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to setup WebDriver: {str(e)}"
            )  # Логирование ошибки
            raise  # Повторное возбуждение исключения

    def setup_wait(self):  # Метод настройки WebDriverWait
        """Setup WebDriverWait"""  # Документация метода
        if self.driver:  # Проверка если WebDriver инициализирован
            self.wait = WebDriverWait(
                self.driver, self.settings.EXPLICIT_WAIT
            )  # Создание WebDriverWait с таймаутом

    def cleanup(self, request):  # Метод очистки после выполнения теста
        """Cleanup after test execution"""  # Документация метода
        try:  # Начало блока обработки исключений
            # Take screenshot on failure  # Комментарий о создании скриншота при падении
            if (
                request.node.rep_call.failed and self.settings.SCREENSHOT_ON_FAILURE
            ):  # Проверка падения теста и настройки скриншотов
                self.take_screenshot(
                    f"failure_{request.node.name}"
                )  # Создание скриншота при падении

            # Close driver  # Комментарий о закрытии драйвера
            if self.driver:  # Проверка если WebDriver существует
                self.driver.quit()  # Закрытие WebDriver
                self.logger.info("WebDriver closed")  # Логирование закрытия WebDriver

        except Exception as e:  # Обработка исключений при очистке
            self.logger.error(
                f"Error during cleanup: {str(e)}"
            )  # Логирование ошибки очистки

    def take_screenshot(self, name: str = "screenshot"):  # Метод создания скриншота
        """Take screenshot and attach to Allure report"""  # Документация метода
        try:  # Начало блока обработки исключений
            if self.driver:  # Проверка если WebDriver существует
                screenshot_path = self.screenshot_manager.take_screenshot(  # Создание скриншота через менеджер
                    self.driver, name  # Передача WebDriver и имени файла
                )
                allure.attach.file(  # Прикрепление файла к Allure отчету
                    screenshot_path,  # Путь к скриншоту
                    name=f"Screenshot: {name}",  # Имя вложения
                    attachment_type=allure.attachment_type.PNG,  # Тип вложения PNG
                )
                self.logger.info(
                    f"Screenshot saved: {screenshot_path}"
                )  # Логирование сохранения скриншота
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to take screenshot: {str(e)}"
            )  # Логирование ошибки создания скриншота

    def navigate_to(self, url: str):  # Метод перехода по URL
        """Navigate to URL"""  # Документация метода
        try:  # Начало блока обработки исключений
            self.driver.get(url)  # Переход по URL
            self.logger.info(f"Navigated to: {url}")  # Логирование перехода
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to navigate to {url}: {str(e)}"
            )  # Логирование ошибки навигации
            raise  # Повторное возбуждение исключения

    def find_element(
        self, by: By, value: str, timeout: int = None
    ):  # Метод поиска элемента
        """Find element with explicit wait"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            element = wait.until(
                EC.presence_of_element_located((by, value))
            )  # Ожидание появления элемента
            return element  # Возврат найденного элемента
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Element not found: {by}={value}"
            )  # Логирование ошибки поиска элемента
            raise  # Повторное возбуждение исключения

    def find_elements(
        self, by: By, value: str, timeout: int = None
    ):  # Метод поиска элементов
        """Find elements with explicit wait"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            elements = wait.until(
                EC.presence_of_all_elements_located((by, value))
            )  # Ожидание появления всех элементов
            return elements  # Возврат найденных элементов
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Elements not found: {by}={value}"
            )  # Логирование ошибки поиска элементов
            return []  # Возврат пустого списка

    def click_element(
        self, by: By, value: str, timeout: int = None
    ):  # Метод клика по элементу
        """Click element with explicit wait"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            element = wait.until(
                EC.element_to_be_clickable((by, value))
            )  # Ожидание кликабельности элемента
            element.click()  # Клик по элементу
            self.logger.info(f"Clicked element: {by}={value}")  # Логирование клика
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Element not clickable: {by}={value}"
            )  # Логирование ошибки клика
            raise  # Повторное возбуждение исключения

    def send_keys(
        self, by: By, value: str, text: str, timeout: int = None
    ):  # Метод ввода текста
        """Send keys to element with explicit wait"""  # Документация метода
        try:  # Начало блока обработки исключений
            element = self.find_element(by, value, timeout)  # Поиск элемента
            element.clear()  # Очистка поля ввода
            element.send_keys(text)  # Ввод текста
            self.logger.info(
                f"Sent keys to element: {by}={value}"
            )  # Логирование ввода текста
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to send keys to {by}={value}: {str(e)}"
            )  # Логирование ошибки ввода
            raise  # Повторное возбуждение исключения

    def wait_for_element_visible(
        self, by: By, value: str, timeout: int = None
    ):  # Метод ожидания видимости элемента
        """Wait for element to be visible"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            element = wait.until(
                EC.visibility_of_element_located((by, value))
            )  # Ожидание видимости элемента
            return element  # Возврат видимого элемента
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Element not visible: {by}={value}"
            )  # Логирование ошибки видимости
            raise  # Повторное возбуждение исключения

    def wait_for_element_clickable(
        self, by: By, value: str, timeout: int = None
    ):  # Метод ожидания кликабельности элемента
        """Wait for element to be clickable"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            element = wait.until(
                EC.element_to_be_clickable((by, value))
            )  # Ожидание кликабельности элемента
            return element  # Возврат кликабельного элемента
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Element not clickable: {by}={value}"
            )  # Логирование ошибки кликабельности
            raise  # Повторное возбуждение исключения

    def get_element_text(
        self, by: By, value: str, timeout: int = None
    ) -> str:  # Метод получения текста элемента
        """Get element text"""  # Документация метода
        try:  # Начало блока обработки исключений
            element = self.find_element(by, value, timeout)  # Поиск элемента
            return element.text  # Возврат текста элемента
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get text from {by}={value}: {str(e)}"
            )  # Логирование ошибки получения текста
            raise  # Повторное возбуждение исключения

    def is_element_present(
        self, by: By, value: str, timeout: int = 5
    ) -> bool:  # Метод проверки наличия элемента
        """Check if element is present"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait = WebDriverWait(
                self.driver, timeout
            )  # Создание WebDriverWait с таймаутом
            wait.until(
                EC.presence_of_element_located((by, value))
            )  # Ожидание присутствия элемента
            return True  # Возврат True если элемент найден
        except TimeoutException:  # Обработка исключения таймаута
            return False  # Возврат False если элемент не найден

    def is_element_visible(
        self, by: By, value: str, timeout: int = 5
    ) -> bool:  # Метод проверки видимости элемента
        """Check if element is visible"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait = WebDriverWait(
                self.driver, timeout
            )  # Создание WebDriverWait с таймаутом
            wait.until(
                EC.visibility_of_element_located((by, value))
            )  # Ожидание видимости элемента
            return True  # Возврат True если элемент видим
        except TimeoutException:  # Обработка исключения таймаута
            return False  # Возврат False если элемент не видим

    def wait_for_page_load(
        self, timeout: int = None
    ):  # Метод ожидания загрузки страницы
        """Wait for page to load completely"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.PAGE_LOAD_TIMEOUT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            wait.until(  # Ожидание выполнения условия
                lambda driver: driver.execute_script(
                    "return document.readyState"
                )  # Выполнение JavaScript для проверки готовности
                == "complete"  # Проверка что страница полностью загружена
            )
            self.logger.info(
                "Page loaded completely"
            )  # Логирование полной загрузки страницы
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.warning(
                "Page load timeout"
            )  # Логирование предупреждения о таймауте

    def execute_javascript(self, script: str, *args):  # Метод выполнения JavaScript
        """Execute JavaScript"""  # Документация метода
        try:  # Начало блока обработки исключений
            result = self.driver.execute_script(
                script, *args
            )  # Выполнение JavaScript скрипта
            self.logger.info(
                f"JavaScript executed: {script}"
            )  # Логирование выполнения JavaScript
            return result  # Возврат результата выполнения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to execute JavaScript: {str(e)}"
            )  # Логирование ошибки выполнения JavaScript
            raise  # Повторное возбуждение исключения

    def get_current_url(self) -> str:  # Метод получения текущего URL
        """Get current URL"""  # Документация метода
        return self.driver.current_url  # Возврат текущего URL страницы

    def get_page_title(self) -> str:  # Метод получения заголовка страницы
        """Get page title"""  # Документация метода
        return self.driver.title  # Возврат заголовка страницы

    def refresh_page(self):  # Метод обновления страницы
        """Refresh current page"""  # Документация метода
        self.driver.refresh()  # Обновление страницы
        self.wait_for_page_load()  # Ожидание загрузки обновленной страницы
        self.logger.info("Page refreshed")  # Логирование обновления страницы

    def go_back(self):  # Метод возврата назад в истории браузера
        """Go back in browser history"""  # Документация метода
        self.driver.back()  # Возврат назад в истории браузера
        self.wait_for_page_load()  # Ожидание загрузки предыдущей страницы
        self.logger.info("Navigated back")  # Логирование возврата назад

    def go_forward(self):  # Метод перехода вперед в истории браузера
        """Go forward in browser history"""  # Документация метода
        self.driver.forward()  # Переход вперед в истории браузера
        self.wait_for_page_load()  # Ожидание загрузки следующей страницы
        self.logger.info("Navigated forward")  # Логирование перехода вперед

    def switch_to_window(self, window_handle: str):  # Метод переключения на окно
        """Switch to specific window"""  # Документация метода
        self.driver.switch_to.window(window_handle)  # Переключение на указанное окно
        self.logger.info(
            f"Switched to window: {window_handle}"
        )  # Логирование переключения окна

    def close_window(self):  # Метод закрытия текущего окна
        """Close current window"""  # Документация метода
        self.driver.close()  # Закрытие текущего окна
        self.logger.info("Window closed")  # Логирование закрытия окна

    def get_all_window_handles(self) -> list:  # Метод получения всех окон
        """Get all window handles"""  # Документация метода
        return self.driver.window_handles  # Возврат списка всех окон

    def get_current_window_handle(self) -> str:  # Метод получения текущего окна
        """Get current window handle"""  # Документация метода
        return self.driver.current_window_handle  # Возврат текущего окна

    def maximize_window(self):  # Метод максимизации окна браузера
        """Maximize browser window"""  # Документация метода
        self.driver.maximize_window()  # Максимизация окна браузера
        self.logger.info("Window maximized")  # Логирование максимизации окна

    def set_window_size(self, width: int, height: int):  # Метод установки размера окна
        """Set window size"""  # Документация метода
        self.driver.set_window_size(width, height)  # Установка размера окна
        self.logger.info(
            f"Window size set to: {width}x{height}"
        )  # Логирование установки размера

    def scroll_to_element(self, by: By, value: str):  # Метод прокрутки к элементу
        """Scroll to element"""  # Документация метода
        try:  # Начало блока обработки исключений
            element = self.find_element(by, value)  # Поиск элемента
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", element
            )  # Прокрутка к элементу через JavaScript
            self.logger.info(
                f"Scrolled to element: {by}={value}"
            )  # Логирование прокрутки к элементу
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to scroll to element: {str(e)}"
            )  # Логирование ошибки прокрутки
            raise  # Повторное возбуждение исключения

    def scroll_to_top(self):  # Метод прокрутки к началу страницы
        """Scroll to top of page"""  # Документация метода
        self.driver.execute_script(
            "window.scrollTo(0, 0);"
        )  # Прокрутка к началу страницы через JavaScript
        self.logger.info("Scrolled to top")  # Логирование прокрутки к началу

    def scroll_to_bottom(self):  # Метод прокрутки к концу страницы
        """Scroll to bottom of page"""  # Документация метода
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )  # Прокрутка к концу страницы через JavaScript
        self.logger.info("Scrolled to bottom")  # Логирование прокрутки к концу

    def hover_over_element(self, by: By, value: str):  # Метод наведения на элемент
        """Hover over element"""  # Документация метода
        try:  # Начало блока обработки исключений
            from selenium.webdriver.common.action_chains import (
                ActionChains,
            )  # Импорт ActionChains для действий мыши

            element = self.find_element(by, value)  # Поиск элемента
            ActionChains(self.driver).move_to_element(
                element
            ).perform()  # Наведение мыши на элемент
            self.logger.info(
                f"Hovered over element: {by}={value}"
            )  # Логирование наведения на элемент
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to hover over element: {str(e)}"
            )  # Логирование ошибки наведения
            raise  # Повторное возбуждение исключения

    def double_click_element(
        self, by: By, value: str
    ):  # Метод двойного клика по элементу
        """Double click element"""  # Документация метода
        try:  # Начало блока обработки исключений
            from selenium.webdriver.common.action_chains import (
                ActionChains,
            )  # Импорт ActionChains для действий мыши

            element = self.find_element(by, value)  # Поиск элемента
            ActionChains(self.driver).double_click(
                element
            ).perform()  # Двойной клик по элементу
            self.logger.info(
                f"Double clicked element: {by}={value}"
            )  # Логирование двойного клика
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to double click element: {str(e)}"
            )  # Логирование ошибки двойного клика
            raise  # Повторное возбуждение исключения

    def right_click_element(
        self, by: By, value: str
    ):  # Метод правого клика по элементу
        """Right click element"""  # Документация метода
        try:  # Начало блока обработки исключений
            from selenium.webdriver.common.action_chains import (
                ActionChains,
            )  # Импорт ActionChains для действий мыши

            element = self.find_element(by, value)  # Поиск элемента
            ActionChains(self.driver).context_click(
                element
            ).perform()  # Правый клик по элементу
            self.logger.info(
                f"Right clicked element: {by}={value}"
            )  # Логирование правого клика
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to right click element: {str(e)}"
            )  # Логирование ошибки правого клика
            raise  # Повторное возбуждение исключения

    def drag_and_drop(  # Метод перетаскивания элемента
        self, source_by: By, source_value: str, target_by: By, target_value: str
    ):
        """Drag and drop element"""  # Документация метода
        try:  # Начало блока обработки исключений
            from selenium.webdriver.common.action_chains import (
                ActionChains,
            )  # Импорт ActionChains для действий мыши

            source = self.find_element(
                source_by, source_value
            )  # Поиск исходного элемента
            target = self.find_element(
                target_by, target_value
            )  # Поиск целевого элемента
            ActionChains(self.driver).drag_and_drop(
                source, target
            ).perform()  # Перетаскивание элемента
            self.logger.info(
                f"Dragged and dropped element"
            )  # Логирование перетаскивания
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to drag and drop element: {str(e)}"
            )  # Логирование ошибки перетаскивания
            raise  # Повторное возбуждение исключения

    def get_element_attribute(
        self, by: By, value: str, attribute: str
    ) -> str:  # Метод получения атрибута элемента
        """Get element attribute"""  # Документация метода
        try:  # Начало блока обработки исключений
            element = self.find_element(by, value)  # Поиск элемента
            return element.get_attribute(attribute)  # Возврат значения атрибута
        except Exception as e:  # Обработка исключений
            self.logger.error(  # Логирование ошибки получения атрибута
                f"Failed to get attribute {attribute} from {by}={value}: {str(e)}"
            )
            raise  # Повторное возбуждение исключения

    def get_element_css_property(
        self, by: By, value: str, property_name: str
    ) -> str:  # Метод получения CSS свойства
        """Get element CSS property"""  # Документация метода
        try:  # Начало блока обработки исключений
            element = self.find_element(by, value)  # Поиск элемента
            return element.value_of_css_property(
                property_name
            )  # Возврат значения CSS свойства
        except Exception as e:  # Обработка исключений
            self.logger.error(  # Логирование ошибки получения CSS свойства
                f"Failed to get CSS property {property_name} from {by}={value}: {str(e)}"
            )
            raise  # Повторное возбуждение исключения

    def wait_for_text_in_element(  # Метод ожидания текста в элементе
        self, by: By, value: str, text: str, timeout: int = None
    ):
        """Wait for text to appear in element"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            wait.until(
                EC.text_to_be_present_in_element((by, value), text)
            )  # Ожидание появления текста в элементе
            self.logger.info(
                f"Text '{text}' found in element: {by}={value}"
            )  # Логирование найденного текста
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Text '{text}' not found in element: {by}={value}"
            )  # Логирование ошибки поиска текста
            raise  # Повторное возбуждение исключения

    def wait_for_url_contains(
        self, url_fragment: str, timeout: int = None
    ):  # Метод ожидания URL содержащего фрагмент
        """Wait for URL to contain specific text"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            wait.until(
                EC.url_contains(url_fragment)
            )  # Ожидание содержания URL фрагмента
            self.logger.info(
                f"URL contains: {url_fragment}"
            )  # Логирование содержания URL
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"URL does not contain: {url_fragment}"
            )  # Логирование ошибки URL
            raise  # Повторное возбуждение исключения

    def wait_for_title_contains(
        self, title_fragment: str, timeout: int = None
    ):  # Метод ожидания заголовка содержащего фрагмент
        """Wait for title to contain specific text"""  # Документация метода
        try:  # Начало блока обработки исключений
            wait_time = (
                timeout or self.settings.EXPLICIT_WAIT
            )  # Определение времени ожидания
            wait = WebDriverWait(self.driver, wait_time)  # Создание WebDriverWait
            wait.until(
                EC.title_contains(title_fragment)
            )  # Ожидание содержания заголовка фрагмента
            self.logger.info(
                f"Title contains: {title_fragment}"
            )  # Логирование содержания заголовка
        except TimeoutException:  # Обработка исключения таймаута
            self.logger.error(
                f"Title does not contain: {title_fragment}"
            )  # Логирование ошибки заголовка
            raise  # Повторное возбуждение исключения

    def get_console_logs(self) -> list:  # Метод получения логов консоли браузера
        """Get browser console logs"""  # Документация метода
        try:  # Начало блока обработки исключений
            logs = self.driver.get_log("browser")  # Получение логов браузера
            self.logger.info(
                f"Retrieved {len(logs)} console logs"
            )  # Логирование количества полученных логов
            return logs  # Возврат списка логов
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get console logs: {str(e)}"
            )  # Логирование ошибки получения логов
            return []  # Возврат пустого списка

    def get_network_logs(self) -> list:  # Метод получения сетевых логов
        """Get network logs"""  # Документация метода
        try:  # Начало блока обработки исключений
            logs = self.driver.get_log(
                "performance"
            )  # Получение логов производительности
            self.logger.info(
                f"Retrieved {len(logs)} network logs"
            )  # Логирование количества сетевых логов
            return logs  # Возврат списка сетевых логов
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get network logs: {str(e)}"
            )  # Логирование ошибки получения сетевых логов
            return []  # Возврат пустого списка

    def intercept_network_requests(self):  # Метод перехвата сетевых запросов
        """Enable network request interception"""  # Документация метода
        try:  # Начало блока обработки исключений
            self.driver.execute_cdp_cmd(
                "Network.enable", {}
            )  # Включение перехвата сетевых запросов через CDP
            self.logger.info(
                "Network request interception enabled"
            )  # Логирование включения перехвата
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to enable network interception: {str(e)}"
            )  # Логирование ошибки включения перехвата

    def get_intercepted_requests(
        self,
    ) -> list:  # Метод получения перехваченных запросов
        """Get intercepted network requests"""  # Документация метода
        try:  # Начало блока обработки исключений
            logs = self.driver.get_log(
                "performance"
            )  # Получение логов производительности
            requests = []  # Инициализация списка запросов
            for log in logs:  # Цикл по логам
                message = log["message"]  # Получение сообщения лога
                if "Network.requestWillBeSent" in message:  # Проверка на сетевой запрос
                    requests.append(message)  # Добавление запроса в список
            return requests  # Возврат списка запросов
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get intercepted requests: {str(e)}"
            )  # Логирование ошибки получения запросов
            return []  # Возврат пустого списка

    def add_allure_attachment(  # Метод добавления вложения в Allure отчет
        self, content: str, name: str, attachment_type: str = "text"
    ):
        """Add attachment to Allure report"""  # Документация метода
        try:  # Начало блока обработки исключений
            if attachment_type == "text":  # Проверка типа вложения - текст
                allure.attach(
                    content, name, allure.attachment_type.TEXT
                )  # Прикрепление текстового вложения
            elif attachment_type == "json":  # Проверка типа вложения - JSON
                allure.attach(
                    content, name, allure.attachment_type.JSON
                )  # Прикрепление JSON вложения
            elif attachment_type == "html":  # Проверка типа вложения - HTML
                allure.attach(
                    content, name, allure.attachment_type.HTML
                )  # Прикрепление HTML вложения
            self.logger.info(
                f"Added Allure attachment: {name}"
            )  # Логирование добавления вложения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to add Allure attachment: {str(e)}"
            )  # Логирование ошибки добавления вложения

    def add_allure_step(
        self, step_name: str, step_func
    ):  # Метод добавления шага в Allure отчет
        """Add step to Allure report"""  # Документация метода
        try:  # Начало блока обработки исключений
            with allure.step(step_name):  # Создание шага Allure
                return step_func()  # Выполнение функции шага
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to add Allure step: {str(e)}"
            )  # Логирование ошибки добавления шага
            raise  # Повторное возбуждение исключения
