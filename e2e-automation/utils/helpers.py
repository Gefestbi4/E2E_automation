"""
Helper utilities for E2E tests
"""

import time
import allure
from typing import Any, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestHelpers:
    """Helper methods for test execution"""

    @staticmethod
    def take_screenshot(driver: WebDriver, name: str = None) -> str:
        """Take screenshot and attach to Allure"""
        if not name:
            name = f"screenshot_{int(time.time())}"

        screenshot_path = f"/app/screenshots/{name}.png"
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name, allure.attachment_type.PNG)
        return screenshot_path

    @staticmethod
    def wait_for_page_load(driver: WebDriver, timeout: int = 10) -> bool:
        """Wait for page to fully load"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False

    @staticmethod
    def scroll_to_element(driver: WebDriver, element: Any) -> None:
        """Scroll to element"""
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        time.sleep(0.5)

    @staticmethod
    def highlight_element(
        driver: WebDriver, element: Any, duration: float = 1.0
    ) -> None:
        """Highlight element for debugging"""
        original_style = element.get_attribute("style")
        driver.execute_script(
            "arguments[0].style.border='3px solid red'; arguments[0].style.backgroundColor='yellow';",
            element,
        )
        time.sleep(duration)
        driver.execute_script(f"arguments[0].style='{original_style}';", element)

    @staticmethod
    def get_element_info(element: Any) -> dict:
        """Get comprehensive element information"""
        try:
            return {
                "tag": element.tag_name,
                "text": element.text[:100] if element.text else "",
                "location": element.location,
                "size": element.size,
                "is_displayed": element.is_displayed(),
                "is_enabled": element.is_enabled(),
                "attributes": {
                    attr: element.get_attribute(attr)
                    for attr in ["id", "class", "name", "type", "value", "href", "src"]
                    if element.get_attribute(attr)
                },
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
        """Decorator for retrying failed operations"""

        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_retries - 1:
                            raise e
                        time.sleep(delay)
                        allure.attach(
                            f"Retry attempt {attempt + 1}/{max_retries}",
                            "Retry Info",
                            allure.attachment_type.TEXT,
                        )
                return None

            return wrapper

        return decorator
