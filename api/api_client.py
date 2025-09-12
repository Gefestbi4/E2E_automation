import requests
import allure

class ApiClient:
    def __init__(self, base_url, api_key=None):
        """
        Инициализирует API-клиент.
        :param base_url: Базовый URL для всех API-запросов (например, https://api.google.com/v1).
        :param api_key: API-ключ для авторизации (если требуется).
        """
        self.base_url = base_url
        self.session = requests.Session()  # Используем сессию для переиспользования соединения
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    @allure.step("API GET-запрос на эндпоинт: {endpoint}")
    def get(self, endpoint, params=None):
        """
        Отправляет GET-запрос.
        :param endpoint: Путь к эндпоинту (например, '/users').
        :param params: Параметры запроса.
        :return: Ответ сервера в формате JSON.
        """
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"GET {url} с параметрами: {params}"):
            response = self.session.get(url, params=params)
            response.raise_for_status()  # Проверяет, что запрос завершился успешно (код 2xx)
            allure.attach(response.text, 'Response Body', allure.attachment_type.JSON)
            return response.json()

    @allure.step("API POST-запрос на эндпоинт: {endpoint}")
    def post(self, endpoint, data=None):
        """
        Отправляет POST-запрос.
        :param endpoint: Путь к эндпоинту.
        :param data: Тело запроса в формате dict.
        :return: Ответ сервера в формате JSON.
        """
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"POST {url} с телом: {data}"):
            response = self.session.post(url, json=data)
            response.raise_for_status()
            allure.attach(response.text, 'Response Body', allure.attachment_type.JSON)
            return response.json()

    @allure.step("API PUT-запрос на эндпоинт: {endpoint}")
    def put(self, endpoint, data=None):
        """
        Отправляет PUT-запрос.
        :param endpoint: Путь к эндпоинту.
        :param data: Тело запроса в формате dict.
        :return: Ответ сервера в формате JSON.
        """
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"PUT {url} с телом: {data}"):
            response = self.session.put(url, json=data)
            response.raise_for_status()
            allure.attach(response.text, 'Response Body', allure.attachment_type.JSON)
            return response.json()

    @allure.step("API PATCH-запрос на эндпоинт: {endpoint}")
    def patch(self, endpoint, data=None):
        """
        Отправляет PATCH-запрос.
        :param endpoint: Путь к эндпоинту.
        :param data: Тело запроса в формате dict для частичного обновления.
        :return: Ответ сервера в формате JSON.
        """
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"PATCH {url} с телом: {data}"):
            response = self.session.patch(url, json=data)
            response.raise_for_status()
            allure.attach(response.text, 'Response Body', allure.attachment_type.JSON)
            return response.json()

    @allure.step("API DELETE-запрос на эндпоинт: {endpoint}")
    def delete(self, endpoint):
        """
        Отправляет DELETE-запрос.
        :param endpoint: Путь к эндпоинту.
        :return: Ответ сервера в формате JSON или None, если тело ответа пустое.
        """
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"DELETE {url}"):
            response = self.session.delete(url)
            response.raise_for_status()
            # Успешный DELETE-запрос может вернуть пустой ответ (статус 204)
            if response.status_code != 204 and response.text:
                allure.attach(response.text, 'Response Body', allure.attachment_type.JSON)
                return response.json()
            return None