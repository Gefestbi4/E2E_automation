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

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        """Setup and teardown for each test"""
        # Setup
        self.setup_driver()
        self.setup_wait()
        self.logger.info(f"Starting test: {request.node.name}")

        # Add test info to Allure
        allure.dynamic.description(f"Test: {request.node.name}")
        allure.dynamic.severity(allure.severity_level.NORMAL)

        yield

        # Teardown
        self.cleanup(request)

    def setup_driver(self):
        """Setup WebDriver with configuration"""
        try:
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

            if self.settings.BROWSER_NAME.lower() == "chrome":
                options = ChromeOptions()
                browser_options = self.settings.get_browser_options()

                for arg in browser_options.get("args", []):
                    options.add_argument(arg)

                for key, value in browser_options.get(
                    "experimental_options", {}
                ).items():
                    options.add_experimental_option(key, value)

                for key, value in browser_options.get("prefs", {}).items():
                    options.add_experimental_option("prefs", {key: value})

                self.driver = RemoteWebDriver(
                    command_executor=self.settings.SELENIUM_HUB_URL, options=options
                )

            elif self.settings.BROWSER_NAME.lower() == "firefox":
                options = FirefoxOptions()
                browser_options = self.settings.get_browser_options()

                for arg in browser_options.get("args", []):
                    options.add_argument(arg)

                for key, value in browser_options.get("prefs", {}).items():
                    options.set_preference(key, value)

                self.driver = RemoteWebDriver(
                    command_executor=self.settings.SELENIUM_HUB_URL, options=options
                )

            self.driver.implicitly_wait(self.settings.IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(self.settings.PAGE_LOAD_TIMEOUT)

            self.logger.info(f"WebDriver initialized: {self.settings.BROWSER_NAME}")

        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise

    def setup_wait(self):
        """Setup WebDriverWait"""
        if self.driver:
            self.wait = WebDriverWait(self.driver, self.settings.EXPLICIT_WAIT)

    def cleanup(self, request):
        """Cleanup after test execution"""
        try:
            # Take screenshot on failure
            if request.node.rep_call.failed and self.settings.SCREENSHOT_ON_FAILURE:
                self.take_screenshot(f"failure_{request.node.name}")

            # Close driver
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver closed")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

    def take_screenshot(self, name: str = "screenshot"):
        """Take screenshot and attach to Allure report"""
        try:
            if self.driver:
                screenshot_path = self.screenshot_manager.take_screenshot(
                    self.driver, name
                )
                allure.attach.file(
                    screenshot_path,
                    name=f"Screenshot: {name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                self.logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")

    def navigate_to(self, url: str):
        """Navigate to URL"""
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise

    def find_element(self, by: By, value: str, timeout: int = None):
        """Find element with explicit wait"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {by}={value}")
            raise

    def find_elements(self, by: By, value: str, timeout: int = None):
        """Find elements with explicit wait"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {by}={value}")
            return []

    def click_element(self, by: By, value: str, timeout: int = None):
        """Click element with explicit wait"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            self.logger.info(f"Clicked element: {by}={value}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {by}={value}")
            raise

    def send_keys(self, by: By, value: str, text: str, timeout: int = None):
        """Send keys to element with explicit wait"""
        try:
            element = self.find_element(by, value, timeout)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys to element: {by}={value}")
        except Exception as e:
            self.logger.error(f"Failed to send keys to {by}={value}: {str(e)}")
            raise

    def wait_for_element_visible(self, by: By, value: str, timeout: int = None):
        """Wait for element to be visible"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {by}={value}")
            raise

    def wait_for_element_clickable(self, by: By, value: str, timeout: int = None):
        """Wait for element to be clickable"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {by}={value}")
            raise

    def get_element_text(self, by: By, value: str, timeout: int = None) -> str:
        """Get element text"""
        try:
            element = self.find_element(by, value, timeout)
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text from {by}={value}: {str(e)}")
            raise

    def is_element_present(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is present"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to load completely"""
        try:
            wait_time = timeout or self.settings.PAGE_LOAD_TIMEOUT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            self.logger.info("Page loaded completely")
        except TimeoutException:
            self.logger.warning("Page load timeout")

    def execute_javascript(self, script: str, *args):
        """Execute JavaScript"""
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.info(f"JavaScript executed: {script}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to execute JavaScript: {str(e)}")
            raise

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()
        self.logger.info("Page refreshed")

    def go_back(self):
        """Go back in browser history"""
        self.driver.back()
        self.wait_for_page_load()
        self.logger.info("Navigated back")

    def go_forward(self):
        """Go forward in browser history"""
        self.driver.forward()
        self.wait_for_page_load()
        self.logger.info("Navigated forward")

    def switch_to_window(self, window_handle: str):
        """Switch to specific window"""
        self.driver.switch_to.window(window_handle)
        self.logger.info(f"Switched to window: {window_handle}")

    def close_window(self):
        """Close current window"""
        self.driver.close()
        self.logger.info("Window closed")

    def get_all_window_handles(self) -> list:
        """Get all window handles"""
        return self.driver.window_handles

    def get_current_window_handle(self) -> str:
        """Get current window handle"""
        return self.driver.current_window_handle

    def maximize_window(self):
        """Maximize browser window"""
        self.driver.maximize_window()
        self.logger.info("Window maximized")

    def set_window_size(self, width: int, height: int):
        """Set window size"""
        self.driver.set_window_size(width, height)
        self.logger.info(f"Window size set to: {width}x{height}")

    def scroll_to_element(self, by: By, value: str):
        """Scroll to element"""
        try:
            element = self.find_element(by, value)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to element: {by}={value}")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            raise

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.logger.info("Scrolled to top")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.info("Scrolled to bottom")

    def hover_over_element(self, by: By, value: str):
        """Hover over element"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            element = self.find_element(by, value)
            ActionChains(self.driver).move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {by}={value}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element: {str(e)}")
            raise

    def double_click_element(self, by: By, value: str):
        """Double click element"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            element = self.find_element(by, value)
            ActionChains(self.driver).double_click(element).perform()
            self.logger.info(f"Double clicked element: {by}={value}")
        except Exception as e:
            self.logger.error(f"Failed to double click element: {str(e)}")
            raise

    def right_click_element(self, by: By, value: str):
        """Right click element"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            element = self.find_element(by, value)
            ActionChains(self.driver).context_click(element).perform()
            self.logger.info(f"Right clicked element: {by}={value}")
        except Exception as e:
            self.logger.error(f"Failed to right click element: {str(e)}")
            raise

    def drag_and_drop(
        self, source_by: By, source_value: str, target_by: By, target_value: str
    ):
        """Drag and drop element"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains

            source = self.find_element(source_by, source_value)
            target = self.find_element(target_by, target_value)
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            self.logger.info(f"Dragged and dropped element")
        except Exception as e:
            self.logger.error(f"Failed to drag and drop element: {str(e)}")
            raise

    def get_element_attribute(self, by: By, value: str, attribute: str) -> str:
        """Get element attribute"""
        try:
            element = self.find_element(by, value)
            return element.get_attribute(attribute)
        except Exception as e:
            self.logger.error(
                f"Failed to get attribute {attribute} from {by}={value}: {str(e)}"
            )
            raise

    def get_element_css_property(self, by: By, value: str, property_name: str) -> str:
        """Get element CSS property"""
        try:
            element = self.find_element(by, value)
            return element.value_of_css_property(property_name)
        except Exception as e:
            self.logger.error(
                f"Failed to get CSS property {property_name} from {by}={value}: {str(e)}"
            )
            raise

    def wait_for_text_in_element(
        self, by: By, value: str, text: str, timeout: int = None
    ):
        """Wait for text to appear in element"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.text_to_be_present_in_element((by, value), text))
            self.logger.info(f"Text '{text}' found in element: {by}={value}")
        except TimeoutException:
            self.logger.error(f"Text '{text}' not found in element: {by}={value}")
            raise

    def wait_for_url_contains(self, url_fragment: str, timeout: int = None):
        """Wait for URL to contain specific text"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.url_contains(url_fragment))
            self.logger.info(f"URL contains: {url_fragment}")
        except TimeoutException:
            self.logger.error(f"URL does not contain: {url_fragment}")
            raise

    def wait_for_title_contains(self, title_fragment: str, timeout: int = None):
        """Wait for title to contain specific text"""
        try:
            wait_time = timeout or self.settings.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.title_contains(title_fragment))
            self.logger.info(f"Title contains: {title_fragment}")
        except TimeoutException:
            self.logger.error(f"Title does not contain: {title_fragment}")
            raise

    def get_console_logs(self) -> list:
        """Get browser console logs"""
        try:
            logs = self.driver.get_log("browser")
            self.logger.info(f"Retrieved {len(logs)} console logs")
            return logs
        except Exception as e:
            self.logger.error(f"Failed to get console logs: {str(e)}")
            return []

    def get_network_logs(self) -> list:
        """Get network logs"""
        try:
            logs = self.driver.get_log("performance")
            self.logger.info(f"Retrieved {len(logs)} network logs")
            return logs
        except Exception as e:
            self.logger.error(f"Failed to get network logs: {str(e)}")
            return []

    def intercept_network_requests(self):
        """Enable network request interception"""
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.logger.info("Network request interception enabled")
        except Exception as e:
            self.logger.error(f"Failed to enable network interception: {str(e)}")

    def get_intercepted_requests(self) -> list:
        """Get intercepted network requests"""
        try:
            logs = self.driver.get_log("performance")
            requests = []
            for log in logs:
                message = log["message"]
                if "Network.requestWillBeSent" in message:
                    requests.append(message)
            return requests
        except Exception as e:
            self.logger.error(f"Failed to get intercepted requests: {str(e)}")
            return []

    def add_allure_attachment(
        self, content: str, name: str, attachment_type: str = "text"
    ):
        """Add attachment to Allure report"""
        try:
            if attachment_type == "text":
                allure.attach(content, name, allure.attachment_type.TEXT)
            elif attachment_type == "json":
                allure.attach(content, name, allure.attachment_type.JSON)
            elif attachment_type == "html":
                allure.attach(content, name, allure.attachment_type.HTML)
            self.logger.info(f"Added Allure attachment: {name}")
        except Exception as e:
            self.logger.error(f"Failed to add Allure attachment: {str(e)}")

    def add_allure_step(self, step_name: str, step_func):
        """Add step to Allure report"""
        try:
            with allure.step(step_name):
                return step_func()
        except Exception as e:
            self.logger.error(f"Failed to add Allure step: {str(e)}")
            raise
