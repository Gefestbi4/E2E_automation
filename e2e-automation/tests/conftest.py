"""
Pytest configuration and fixtures for E2E tests
"""

import os
import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

# Add project root to Python path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from config.settings import Settings
from utils.helpers import TestHelpers


@pytest.fixture(scope="session")
def url():
    """Base URL for testing"""
    return Settings.FRONTEND_URL


@pytest.fixture(scope="function")
def browser(request):
    """Browser fixture with Selenium Grid support"""
    browser_name = request.config.getoption(
        "--browser-name", default=Settings.BROWSER_NAME
    )
    options = None

    if browser_name == "chrome":
        options = ChromeOptions()
        browser_options = Settings.get_browser_options()

        for arg in browser_options.get("args", []):
            options.add_argument(arg)

        for key, value in browser_options.get("experimental_options", {}).items():
            options.add_experimental_option(key, value)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        browser_options = Settings.get_browser_options()

        for arg in browser_options.get("args", []):
            options.add_argument(arg)
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")

    # Connect to Selenium Grid
    browser = webdriver.Remote(
        command_executor=Settings.SELENIUM_HUB_URL, options=options
    )

    browser.implicitly_wait(Settings.IMPLICIT_WAIT)
    browser.set_page_load_timeout(Settings.PAGE_LOAD_TIMEOUT)

    yield browser

    # Cleanup
    try:
        browser.execute_script("window.localStorage.clear();")
        browser.execute_script("window.sessionStorage.clear();")
    except Exception as e:
        print(f"Warning: Could not clear storage: {e}")

    time.sleep(1)
    browser.quit()


@pytest.fixture(scope="function")
def api_client():
    """API client fixture"""
    from utils.api_client import ApiClient

    return ApiClient()


@pytest.fixture(scope="function")
def test_data():
    """Test data fixture"""
    import json

    data_file = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.json")
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--browser-name",
        action="store",
        default=Settings.BROWSER_NAME,
        help="Browser name for testing (chrome/firefox)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=Settings.HEADLESS,
        help="Run tests in headless mode",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook for taking screenshots on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Get browser instance from test
        browser = None
        for fixture_name in item.fixturenames:
            if fixture_name == "browser":
                browser = item.funcargs.get(fixture_name)
                break

        if browser and Settings.SCREENSHOT_ON_FAILURE:
            screenshot_name = f"{item.name}_{int(time.time())}"
            TestHelpers.take_screenshot(browser, screenshot_name)


@pytest.fixture(autouse=True)
def test_info(request):
    """Auto fixture for test information"""
    test_name = request.node.name
    test_markers = [mark.name for mark in request.node.iter_markers()]

    allure.dynamic.feature("E2E Automation")
    allure.dynamic.story(test_name)
    allure.dynamic.severity(allure.severity_level.NORMAL)

    # Add markers as tags
    for marker in test_markers:
        allure.dynamic.tag(marker)

    yield
