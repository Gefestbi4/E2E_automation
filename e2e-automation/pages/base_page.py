"""
Base page class for Page Object Model
"""

from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from core.base_test import BaseTest
from utils.logger import TestLogger


class BasePage:
    """Base page class with common functionality for all pages"""

    def __init__(self, driver: WebDriver, base_test: BaseTest):
        self.driver = driver
        self.base_test = base_test
        self.logger = TestLogger(f"Page_{self.__class__.__name__}")
        self.wait = base_test.wait
        self.settings = base_test.settings
        self.test_data = base_test.test_data

    def navigate_to(self, url: str = None):
        """Navigate to page URL"""
        if url is None:
            url = self.url
        self.base_test.navigate_to(url)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.base_test.wait_for_page_load()

    def get_title(self) -> str:
        """Get page title"""
        return self.base_test.get_page_title()

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.base_test.get_current_url()

    def refresh_page(self):
        """Refresh current page"""
        self.base_test.refresh_page()

    def find_element(self, by: By, value: str, timeout: int = None) -> WebElement:
        """Find element on page"""
        return self.base_test.find_element(by, value, timeout)

    def find_elements(
        self, by: By, value: str, timeout: int = None
    ) -> List[WebElement]:
        """Find elements on page"""
        return self.base_test.find_elements(by, value, timeout)

    def click_element(self, by: By, value: str, timeout: int = None):
        """Click element on page"""
        self.base_test.click_element(by, value, timeout)

    def send_keys(self, by: By, value: str, text: str, timeout: int = None):
        """Send keys to element on page"""
        self.base_test.send_keys(by, value, text, timeout)

    def get_element_text(self, by: By, value: str, timeout: int = None) -> str:
        """Get element text"""
        return self.base_test.get_element_text(by, value, timeout)

    def is_element_present(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is present"""
        return self.base_test.is_element_present(by, value, timeout)

    def is_element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is visible"""
        return self.base_test.is_element_visible(by, value, timeout)

    def wait_for_element_visible(
        self, by: By, value: str, timeout: int = None
    ) -> WebElement:
        """Wait for element to be visible"""
        return self.base_test.wait_for_element_visible(by, value, timeout)

    def wait_for_element_clickable(
        self, by: By, value: str, timeout: int = None
    ) -> WebElement:
        """Wait for element to be clickable"""
        return self.base_test.wait_for_element_clickable(by, value, timeout)

    def scroll_to_element(self, by: By, value: str):
        """Scroll to element"""
        self.base_test.scroll_to_element(by, value)

    def hover_over_element(self, by: By, value: str):
        """Hover over element"""
        self.base_test.hover_over_element(by, value)

    def get_element_attribute(self, by: By, value: str, attribute: str) -> str:
        """Get element attribute"""
        return self.base_test.get_element_attribute(by, value, attribute)

    def wait_for_text_in_element(
        self, by: By, value: str, text: str, timeout: int = None
    ):
        """Wait for text to appear in element"""
        self.base_test.wait_for_text_in_element(by, value, text, timeout)

    def wait_for_url_contains(self, url_fragment: str, timeout: int = None):
        """Wait for URL to contain specific text"""
        self.base_test.wait_for_url_contains(url_fragment, timeout)

    def take_screenshot(self, name: str = None):
        """Take screenshot of current page"""
        if name is None:
            name = f"{self.__class__.__name__}_screenshot"
        self.base_test.take_screenshot(name)

    def execute_javascript(self, script: str, *args):
        """Execute JavaScript on page"""
        return self.base_test.execute_javascript(script, *args)

    def get_console_logs(self) -> List[dict]:
        """Get browser console logs"""
        return self.base_test.get_console_logs()

    def get_network_logs(self) -> List[dict]:
        """Get network logs"""
        return self.base_test.get_network_logs()

    def intercept_network_requests(self):
        """Enable network request interception"""
        self.base_test.intercept_network_requests()

    def get_intercepted_requests(self) -> List[dict]:
        """Get intercepted network requests"""
        return self.base_test.get_intercepted_requests()

    def add_allure_attachment(
        self, content: str, name: str, attachment_type: str = "text"
    ):
        """Add attachment to Allure report"""
        self.base_test.add_allure_attachment(content, name, attachment_type)

    def add_allure_step(self, step_name: str, step_func):
        """Add step to Allure report"""
        return self.base_test.add_allure_step(step_name, step_func)

    def log_page_action(self, action: str, element: str = None, value: str = None):
        """Log page action"""
        self.logger.browser_action(action, element, value)

    def verify_page_loaded(self) -> bool:
        """Verify that page has loaded correctly"""
        try:
            # Check if page title is not empty
            title = self.get_title()
            if not title:
                return False

            # Check if URL contains expected fragment
            if hasattr(self, "url_fragment"):
                current_url = self.get_current_url()
                if self.url_fragment not in current_url:
                    return False

            # Check if key elements are present
            if hasattr(self, "key_elements"):
                for element in self.key_elements:
                    if not self.is_element_present(element["by"], element["value"]):
                        return False

            return True
        except Exception as e:
            self.logger.error(f"Failed to verify page load: {str(e)}")
            return False

    def wait_for_ajax_complete(self, timeout: int = 10):
        """Wait for AJAX requests to complete"""
        try:
            self.execute_javascript(
                """
                return jQuery.active == 0;
            """
            )
            self.logger.info("AJAX requests completed")
        except Exception as e:
            self.logger.warning(f"AJAX wait failed: {str(e)}")

    def get_page_source(self) -> str:
        """Get page source"""
        return self.driver.page_source

    def get_window_size(self) -> dict:
        """Get window size"""
        size = self.driver.get_window_size()
        return {"width": size["width"], "height": size["height"]}

    def set_window_size(self, width: int, height: int):
        """Set window size"""
        self.driver.set_window_size(width, height)

    def maximize_window(self):
        """Maximize window"""
        self.driver.maximize_window()

    def get_cookies(self) -> List[dict]:
        """Get all cookies"""
        return self.driver.get_cookies()

    def add_cookie(self, cookie: dict):
        """Add cookie"""
        self.driver.add_cookie(cookie)

    def delete_cookie(self, name: str):
        """Delete cookie by name"""
        self.driver.delete_cookie(name)

    def clear_cookies(self):
        """Clear all cookies"""
        self.driver.delete_all_cookies()

    def get_local_storage(self, key: str = None) -> str:
        """Get local storage value"""
        if key:
            return self.execute_javascript(f"return localStorage.getItem('{key}');")
        else:
            return self.execute_javascript("return JSON.stringify(localStorage);")

    def set_local_storage(self, key: str, value: str):
        """Set local storage value"""
        self.execute_javascript(f"localStorage.setItem('{key}', '{value}');")

    def remove_local_storage(self, key: str):
        """Remove local storage value"""
        self.execute_javascript(f"localStorage.removeItem('{key}');")

    def clear_local_storage(self):
        """Clear all local storage"""
        self.execute_javascript("localStorage.clear();")

    def get_session_storage(self, key: str = None) -> str:
        """Get session storage value"""
        if key:
            return self.execute_javascript(f"return sessionStorage.getItem('{key}');")
        else:
            return self.execute_javascript("return JSON.stringify(sessionStorage);")

    def set_session_storage(self, key: str, value: str):
        """Set session storage value"""
        self.execute_javascript(f"sessionStorage.setItem('{key}', '{value}');")

    def remove_session_storage(self, key: str):
        """Remove session storage value"""
        self.execute_javascript(f"sessionStorage.removeItem('{key}');")

    def clear_session_storage(self):
        """Clear all session storage"""
        self.execute_javascript("sessionStorage.clear();")

    def switch_to_frame(self, frame_reference):
        """Switch to frame"""
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        """Switch to default content"""
        self.driver.switch_to.default_content()

    def switch_to_alert(self):
        """Switch to alert"""
        return self.driver.switch_to.alert

    def accept_alert(self):
        """Accept alert"""
        alert = self.switch_to_alert()
        alert.accept()

    def dismiss_alert(self):
        """Dismiss alert"""
        alert = self.switch_to_alert()
        alert.dismiss()

    def get_alert_text(self) -> str:
        """Get alert text"""
        alert = self.switch_to_alert()
        return alert.text

    def send_keys_to_alert(self, text: str):
        """Send keys to alert"""
        alert = self.switch_to_alert()
        alert.send_keys(text)

    def wait_for_alert(self, timeout: int = 10) -> bool:
        """Wait for alert to appear"""
        try:
            from selenium.webdriver.support import expected_conditions as EC

            wait = self.base_test.wait
            wait.until(EC.alert_is_present())
            return True
        except Exception:
            return False
