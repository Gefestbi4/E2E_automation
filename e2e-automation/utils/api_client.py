"""
API client for E2E tests
"""

import requests
import allure
from typing import Dict, Any, Optional
from config.settings import Settings


class ApiClient:
    """API client for backend communication"""

    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or Settings.BACKEND_URL
        self.api_key = api_key or Settings.API_KEY
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    @allure.step("API: Login user")
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user via API"""
        url = f"{self.base_url}/api/auth/login"
        data = {"email": email, "password": password}

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            allure.attach(
                f"API Error: {str(e)}", "API Error", allure.attachment_type.TEXT
            )
            raise

    @allure.step("API: Get user info")
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get user information"""
        url = f"{self.base_url}/api/users/{user_id}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            allure.attach(
                f"API Error: {str(e)}", "API Error", allure.attachment_type.TEXT
            )
            raise

    @allure.step("API: Check health")
    def health_check(self) -> bool:
        """Check if API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
