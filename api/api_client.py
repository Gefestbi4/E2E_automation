import allure
import requests


class ApiClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    @allure.step("API GET-запрос на эндпоинт: {endpoint}")
    def get(self, endpoint, params=None):
        response = self.session.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP (4xx или 5xx)
        if response.status_code != 204:  # No Content
            return response.json()
        return None

    @allure.step("API POST-запрос на эндпоинт: {endpoint}")
    def post(self, endpoint, data=None):
        response = self.session.post(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
        return None

    @allure.step("API PUT-запрос на эндпоинт: {endpoint}")
    def put(self, endpoint, data=None):
        response = self.session.put(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
        return None

    @allure.step("API PATCH-запрос на эндпоинт: {endpoint}")
    def patch(self, endpoint, data=None):
        response = self.session.patch(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        if response.status_code != 204:
            return response.json()
        return None

    @allure.step("API DELETE-запрос на эндпоинт: {endpoint}")
    def delete(self, endpoint):
        response = self.session.delete(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return None