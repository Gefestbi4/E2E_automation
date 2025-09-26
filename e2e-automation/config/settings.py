"""
Configuration settings for E2E automation tests
"""

import os
from typing import Dict, Any


class Settings:
    """Centralized configuration for E2E tests"""

    # Base URLs
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://frontend:80")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000")
    SELENIUM_HUB_URL = os.getenv("SELENIUM_HUB_URL", "http://selenium-hub:4444/wd/hub")

    # Test data
    TEST_EMAIL = os.getenv("EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("PASSWORD", "test123")
    API_KEY = os.getenv("API_KEY", "")

    # Browser settings
    BROWSER_NAME = os.getenv("BROWSER_NAME", "chrome")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "15"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # Test execution
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    VIDEO_RECORDING = os.getenv("VIDEO_RECORDING", "false").lower() == "true"

    # Allure settings
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "/app/allure-results")
    ALLURE_REPORTS_DIR = os.getenv("ALLURE_REPORTS_DIR", "/app/allure-reports")

    # Retry settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))

    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """Get browser-specific options"""
        options = {
            "chrome": {
                "args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-images",
                    "--disable-javascript",
                ],
                "experimental_options": {
                    "excludeSwitches": ["enable-automation"],
                    "useAutomationExtension": False,
                },
            },
            "firefox": {
                "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
            },
        }

        if cls.HEADLESS:
            options["chrome"]["args"].extend(["--headless", "--window-size=1920,1080"])
            options["firefox"]["args"].extend(
                ["--headless", "--width=1920", "--height=1080"]
            )

        return options.get(cls.BROWSER_NAME, {})

    @classmethod
    def get_test_data(cls) -> Dict[str, Any]:
        """Get test data configuration"""
        return {
            "valid_user": {"email": cls.TEST_EMAIL, "password": cls.TEST_PASSWORD},
            "invalid_user": {
                "email": "invalid@example.com",
                "password": "wrongpassword",
            },
            "test_urls": {
                "login": f"{cls.FRONTEND_URL}/login.html",
                "tests": f"{cls.FRONTEND_URL}/tests.html",
                "api_login": f"{cls.BACKEND_URL}/api/auth/login",
            },
        }
