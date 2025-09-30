"""
API client for E2E automation tests
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import TestLogger


class APIClient:
    """HTTP client for API testing and backend communication"""

    def __init__(self, base_url: str = None, timeout: int = 30):
        self.logger = TestLogger("APIClient")
        self.base_url = base_url or "http://backend:5000"
        self.timeout = timeout
        self.session = self._create_session()
        self.auth_token = None
        self.response_logs = []

    def _create_session(self) -> requests.Session:
        """Create configured requests session with retry strategy"""
        session = requests.Session()

        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Default headers
        session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "E2E-Automation-Test/1.0",
            }
        )

        return session

    def set_auth_token(self, token: str):
        """Set authentication token for requests"""
        self.auth_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.logger.info("Authentication token set")

    def clear_auth_token(self):
        """Clear authentication token"""
        self.auth_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        self.logger.info("Authentication token cleared")

    def _log_request(self, method: str, url: str, **kwargs):
        """Log API request"""
        start_time = time.time()
        self.logger.api_request(method, url)

        # Store request info for response logging
        self._current_request = {
            "method": method,
            "url": url,
            "start_time": start_time,
            "kwargs": kwargs,
        }

    def _log_response(self, response: requests.Response):
        """Log API response"""
        if hasattr(self, "_current_request"):
            duration = (time.time() - self._current_request["start_time"]) * 1000
            self.logger.api_request(
                self._current_request["method"],
                self._current_request["url"],
                response.status_code,
                duration,
            )

            # Store response log
            response_log = {
                "method": self._current_request["method"],
                "url": self._current_request["url"],
                "status_code": response.status_code,
                "response_time": duration,
                "timestamp": time.time(),
                "request_data": self._current_request["kwargs"].get("json", {}),
                "response_data": (
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json"
                    )
                    else response.text
                ),
            }
            self.response_logs.append(response_log)

    def get(self, endpoint: str, params: Dict = None, **kwargs) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url, params=params, **kwargs)

        try:
            response = self.session.get(
                url, params=params, timeout=self.timeout, **kwargs
            )
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"GET request failed: {str(e)}")
            raise

    def post(
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("POST", url, json=json_data or data, **kwargs)

        try:
            response = self.session.post(
                url, data=data, json=json_data, timeout=self.timeout, **kwargs
            )
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"POST request failed: {str(e)}")
            raise

    def put(
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("PUT", url, json=json_data or data, **kwargs)

        try:
            response = self.session.put(
                url, data=data, json=json_data, timeout=self.timeout, **kwargs
            )
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"PUT request failed: {str(e)}")
            raise

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("DELETE", url, **kwargs)

        try:
            response = self.session.delete(url, timeout=self.timeout, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"DELETE request failed: {str(e)}")
            raise

    def patch(
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """PATCH request"""
        url = f"{self.base_url}{endpoint}"
        self._log_request("PATCH", url, json=json_data or data, **kwargs)

        try:
            response = self.session.patch(
                url, data=data, json=json_data, timeout=self.timeout, **kwargs
            )
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"PATCH request failed: {str(e)}")
            raise

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and get authentication token"""
        try:
            response = self.post(
                "/api/auth/login", json_data={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    self.set_auth_token(token)
                    self.logger.info(f"Successfully logged in as: {email}")
                    return data
                else:
                    raise Exception("No access token in response")
            else:
                error_msg = response.json().get("detail", "Login failed")
                raise Exception(f"Login failed: {error_msg}")

        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            raise

    def logout(self) -> bool:
        """Logout and clear authentication token"""
        try:
            response = self.post("/api/auth/logout")
            self.clear_auth_token()
            self.logger.info("Successfully logged out")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            return False

    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        try:
            response = self.get("/api/auth/me")
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get user info: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to get current user: {str(e)}")
            raise

    def register_user(
        self, email: str, password: str, full_name: str
    ) -> Dict[str, Any]:
        """Register new user"""
        try:
            response = self.post(
                "/api/auth/register",
                json_data={
                    "email": email,
                    "password": password,
                    "confirm_password": password,
                    "full_name": full_name,
                },
            )

            if response.status_code == 200:
                self.logger.info(f"Successfully registered user: {email}")
                return response.json()
            else:
                error_msg = response.json().get("detail", "Registration failed")
                raise Exception(f"Registration failed: {error_msg}")

        except Exception as e:
            self.logger.error(f"Registration failed: {str(e)}")
            raise

    def get_products(self, params: Dict = None) -> Dict[str, Any]:
        """Get products list"""
        try:
            response = self.get("/api/ecommerce/products", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get products: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to get products: {str(e)}")
            raise

    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new product"""
        try:
            response = self.post("/api/ecommerce/products", json_data=product_data)
            if response.status_code == 200:
                self.logger.info("Successfully created product")
                return response.json()
            else:
                error_msg = response.json().get("detail", "Product creation failed")
                raise Exception(f"Product creation failed: {error_msg}")
        except Exception as e:
            self.logger.error(f"Failed to create product: {str(e)}")
            raise

    def get_posts(self, params: Dict = None) -> Dict[str, Any]:
        """Get social posts"""
        try:
            response = self.get("/api/social/posts", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get posts: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to get posts: {str(e)}")
            raise

    def create_post(self, content: str) -> Dict[str, Any]:
        """Create new social post"""
        try:
            response = self.post("/api/social/posts", json_data={"content": content})
            if response.status_code == 200:
                self.logger.info("Successfully created post")
                return response.json()
            else:
                error_msg = response.json().get("detail", "Post creation failed")
                raise Exception(f"Post creation failed: {error_msg}")
        except Exception as e:
            self.logger.error(f"Failed to create post: {str(e)}")
            raise

    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get analytics dashboard data"""
        try:
            response = self.get("/api/analytics/dashboard")
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get analytics: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to get analytics: {str(e)}")
            raise

    def health_check(self) -> bool:
        """Check API health"""
        try:
            response = self.get("/api/health")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

    def get_response_logs(self) -> List[Dict[str, Any]]:
        """Get all response logs"""
        return self.response_logs.copy()

    def clear_response_logs(self):
        """Clear response logs"""
        self.response_logs.clear()
        self.logger.info("Response logs cleared")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from response logs"""
        if not self.response_logs:
            return {}

        response_times = [log["response_time"] for log in self.response_logs]

        return {
            "total_requests": len(self.response_logs),
            "avg_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "success_rate": len(
                [log for log in self.response_logs if 200 <= log["status_code"] < 300]
            )
            / len(self.response_logs)
            * 100,
        }

    def wait_for_api_availability(self, timeout: int = 60) -> bool:
        """Wait for API to become available"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.health_check():
                self.logger.info("API is available")
                return True
            time.sleep(5)

        self.logger.error("API is not available after timeout")
        return False
