"""
API client for E2E automation tests  # Документация API клиента для E2E автоматизации
"""

import requests  # Импорт библиотеки requests для HTTP запросов
import json  # Импорт модуля для работы с JSON
import time  # Импорт модуля для работы со временем
from typing import Dict, Any, Optional, List  # Импорт типов для аннотаций типов
from requests.adapters import HTTPAdapter  # Импорт HTTPAdapter для настройки сессии
from urllib3.util.retry import Retry  # Импорт Retry для стратегии повторных попыток
from utils.logger import TestLogger  # Импорт класса TestLogger


class APIClient:  # Определение класса API клиента
    """HTTP client for API testing and backend communication"""  # Документация класса

    def __init__(
        self, base_url: str = None, timeout: int = 30
    ):  # Конструктор класса APIClient
        self.logger = TestLogger("APIClient")  # Инициализация логгера для API клиента
        self.base_url = base_url or "http://backend:5000"  # Установка базового URL API
        self.timeout = timeout  # Установка таймаута запросов
        self.session = self._create_session()  # Создание HTTP сессии
        self.auth_token = None  # Инициализация токена аутентификации
        self.response_logs = []  # Инициализация списка логов ответов

    def _create_session(
        self,
    ) -> requests.Session:  # Приватный метод создания HTTP сессии
        """Create configured requests session with retry strategy"""  # Документация метода
        session = requests.Session()  # Создание новой HTTP сессии

        # Retry strategy  # Комментарий о стратегии повторных попыток
        retry_strategy = Retry(  # Создание стратегии повторных попыток
            total=3,  # Максимальное количество попыток
            backoff_factor=1,  # Коэффициент задержки между попытками
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],  # HTTP коды для повторных попыток
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )  # Создание HTTP адаптера с стратегией повторов
        session.mount("http://", adapter)  # Установка адаптера для HTTP
        session.mount("https://", adapter)  # Установка адаптера для HTTPS

        # Default headers  # Комментарий о заголовках по умолчанию
        session.headers.update(  # Обновление заголовков сессии
            {
                "Content-Type": "application/json",  # Тип контента JSON
                "Accept": "application/json",  # Принимаемый тип контента JSON
                "User-Agent": "E2E-Automation-Test/1.0",  # Идентификатор пользовательского агента
            }
        )

        return session  # Возврат настроенной сессии

    def set_auth_token(self, token: str):  # Метод установки токена аутентификации
        """Set authentication token for requests"""  # Документация метода
        self.auth_token = token  # Сохранение токена аутентификации
        self.session.headers.update(
            {"Authorization": f"Bearer {token}"}
        )  # Добавление заголовка авторизации
        self.logger.info("Authentication token set")  # Логирование установки токена

    def clear_auth_token(self):  # Метод очистки токена аутентификации
        """Clear authentication token"""  # Документация метода
        self.auth_token = None  # Очистка токена аутентификации
        if (
            "Authorization" in self.session.headers
        ):  # Проверка наличия заголовка авторизации
            del self.session.headers["Authorization"]  # Удаление заголовка авторизации
        self.logger.info("Authentication token cleared")  # Логирование очистки токена

    def _log_request(
        self, method: str, url: str, **kwargs
    ):  # Приватный метод логирования запроса
        """Log API request"""  # Документация метода
        start_time = time.time()  # Запись времени начала запроса
        self.logger.api_request(method, url)  # Логирование API запроса

        # Store request info for response logging  # Комментарий о сохранении информации о запросе
        self._current_request = {  # Сохранение информации о текущем запросе
            "method": method,  # HTTP метод
            "url": url,  # URL запроса
            "start_time": start_time,  # Время начала запроса
            "kwargs": kwargs,  # Дополнительные параметры запроса
        }

    def _log_response(
        self, response: requests.Response
    ):  # Приватный метод логирования ответа
        """Log API response"""  # Документация метода
        if hasattr(
            self, "_current_request"
        ):  # Проверка наличия информации о текущем запросе
            duration = (
                time.time() - self._current_request["start_time"]
            ) * 1000  # Вычисление длительности запроса в миллисекундах
            self.logger.api_request(  # Логирование API запроса с результатами
                self._current_request["method"],  # HTTP метод
                self._current_request["url"],  # URL запроса
                response.status_code,  # Статус код ответа
                duration,  # Длительность запроса
            )

            # Store response log  # Комментарий о сохранении лога ответа
            response_log = {  # Создание лога ответа
                "method": self._current_request["method"],  # HTTP метод
                "url": self._current_request["url"],  # URL запроса
                "status_code": response.status_code,  # Статус код ответа
                "response_time": duration,  # Время ответа
                "timestamp": time.time(),  # Временная метка
                "request_data": self._current_request["kwargs"].get(
                    "json", {}
                ),  # Данные запроса
                "response_data": (  # Данные ответа
                    response.json()  # JSON ответ если контент JSON
                    if response.headers.get(
                        "content-type", ""
                    ).startswith(  # Проверка типа контента
                        "application/json"  # JSON тип контента
                    )
                    else response.text  # Текстовый ответ иначе
                ),
            }
            self.response_logs.append(response_log)  # Добавление лога ответа в список

    def get(
        self, endpoint: str, params: Dict = None, **kwargs
    ) -> requests.Response:  # Метод GET запроса
        """GET request"""  # Документация метода
        url = f"{self.base_url}{endpoint}"  # Создание полного URL
        self._log_request("GET", url, params=params, **kwargs)  # Логирование запроса

        try:  # Начало блока обработки исключений
            response = self.session.get(  # Выполнение GET запроса
                url, params=params, timeout=self.timeout, **kwargs  # Параметры запроса
            )
            self._log_response(response)  # Логирование ответа
            return response  # Возврат ответа
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"GET request failed: {str(e)}"
            )  # Логирование ошибки GET запроса
            raise  # Повторное возбуждение исключения

    def post(  # Метод POST запроса
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """POST request"""  # Документация метода
        url = f"{self.base_url}{endpoint}"  # Создание полного URL
        self._log_request(
            "POST", url, json=json_data or data, **kwargs
        )  # Логирование запроса

        try:  # Начало блока обработки исключений
            response = self.session.post(  # Выполнение POST запроса
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                **kwargs,  # Параметры запроса
            )
            self._log_response(response)  # Логирование ответа
            return response  # Возврат ответа
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"POST request failed: {str(e)}"
            )  # Логирование ошибки POST запроса
            raise  # Повторное возбуждение исключения

    def put(  # Метод PUT запроса
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """PUT request"""  # Документация метода
        url = f"{self.base_url}{endpoint}"  # Создание полного URL
        self._log_request(
            "PUT", url, json=json_data or data, **kwargs
        )  # Логирование запроса

        try:  # Начало блока обработки исключений
            response = self.session.put(  # Выполнение PUT запроса
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                **kwargs,  # Параметры запроса
            )
            self._log_response(response)  # Логирование ответа
            return response  # Возврат ответа
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"PUT request failed: {str(e)}"
            )  # Логирование ошибки PUT запроса
            raise  # Повторное возбуждение исключения

    def delete(
        self, endpoint: str, **kwargs
    ) -> requests.Response:  # Метод DELETE запроса
        """DELETE request"""  # Документация метода
        url = f"{self.base_url}{endpoint}"  # Создание полного URL
        self._log_request("DELETE", url, **kwargs)  # Логирование запроса

        try:  # Начало блока обработки исключений
            response = self.session.delete(
                url, timeout=self.timeout, **kwargs
            )  # Выполнение DELETE запроса
            self._log_response(response)  # Логирование ответа
            return response  # Возврат ответа
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"DELETE request failed: {str(e)}"
            )  # Логирование ошибки DELETE запроса
            raise  # Повторное возбуждение исключения

    def patch(  # Метод PATCH запроса
        self, endpoint: str, data: Dict = None, json_data: Dict = None, **kwargs
    ) -> requests.Response:
        """PATCH request"""  # Документация метода
        url = f"{self.base_url}{endpoint}"  # Создание полного URL
        self._log_request(
            "PATCH", url, json=json_data or data, **kwargs
        )  # Логирование запроса

        try:  # Начало блока обработки исключений
            response = self.session.patch(  # Выполнение PATCH запроса
                url,
                data=data,
                json=json_data,
                timeout=self.timeout,
                **kwargs,  # Параметры запроса
            )
            self._log_response(response)  # Логирование ответа
            return response  # Возврат ответа
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"PATCH request failed: {str(e)}"
            )  # Логирование ошибки PATCH запроса
            raise  # Повторное возбуждение исключения

    def login(
        self, email: str, password: str
    ) -> Dict[str, Any]:  # Метод входа в систему
        """Login and get authentication token"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.post(  # Выполнение POST запроса для входа
                "/api/auth/login",
                json_data={"email": email, "password": password},  # Данные для входа
            )

            if response.status_code == 200:  # Проверка успешного входа
                data = response.json()  # Получение данных ответа
                token = data.get("access_token")  # Извлечение токена доступа
                if token:  # Проверка наличия токена
                    self.set_auth_token(token)  # Установка токена аутентификации
                    self.logger.info(
                        f"Successfully logged in as: {email}"
                    )  # Логирование успешного входа
                    return data  # Возврат данных ответа
                else:  # Если токен отсутствует
                    raise Exception(
                        "No access token in response"
                    )  # Возбуждение исключения
            else:  # Если вход не удался
                error_msg = response.json().get(
                    "detail", "Login failed"
                )  # Получение сообщения об ошибке
                raise Exception(
                    f"Login failed: {error_msg}"
                )  # Возбуждение исключения с сообщением об ошибке

        except Exception as e:  # Обработка исключений
            self.logger.error(f"Login failed: {str(e)}")  # Логирование ошибки входа
            raise  # Повторное возбуждение исключения

    def logout(self) -> bool:  # Метод выхода из системы
        """Logout and clear authentication token"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.post(
                "/api/auth/logout"
            )  # Выполнение POST запроса для выхода
            self.clear_auth_token()  # Очистка токена аутентификации
            self.logger.info("Successfully logged out")  # Логирование успешного выхода
            return response.status_code == 200  # Возврат результата выхода
        except Exception as e:  # Обработка исключений
            self.logger.error(f"Logout failed: {str(e)}")  # Логирование ошибки выхода
            return False  # Возврат False при ошибке

    def get_current_user(
        self,
    ) -> Dict[str, Any]:  # Метод получения информации о текущем пользователе
        """Get current user information"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.get(
                "/api/auth/me"
            )  # Выполнение GET запроса для получения информации о пользователе
            if response.status_code == 200:  # Проверка успешного запроса
                return response.json()  # Возврат данных пользователя
            else:  # Если запрос не удался
                raise Exception(
                    f"Failed to get user info: {response.status_code}"
                )  # Возбуждение исключения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get current user: {str(e)}"
            )  # Логирование ошибки получения пользователя
            raise  # Повторное возбуждение исключения

    def register_user(  # Метод регистрации пользователя
        self, email: str, password: str, full_name: str
    ) -> Dict[str, Any]:
        """Register new user"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.post(  # Выполнение POST запроса для регистрации
                "/api/auth/register",  # Endpoint регистрации
                json_data={  # Данные для регистрации
                    "email": email,  # Email пользователя
                    "password": password,  # Пароль пользователя
                    "confirm_password": password,  # Подтверждение пароля
                    "full_name": full_name,  # Полное имя пользователя
                },
            )

            if response.status_code == 200:  # Проверка успешной регистрации
                self.logger.info(
                    f"Successfully registered user: {email}"
                )  # Логирование успешной регистрации
                return response.json()  # Возврат данных ответа
            else:  # Если регистрация не удалась
                error_msg = response.json().get(
                    "detail", "Registration failed"
                )  # Получение сообщения об ошибке
                raise Exception(
                    f"Registration failed: {error_msg}"
                )  # Возбуждение исключения с сообщением об ошибке

        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Registration failed: {str(e)}"
            )  # Логирование ошибки регистрации
            raise  # Повторное возбуждение исключения

    def get_products(
        self, params: Dict = None
    ) -> Dict[str, Any]:  # Метод получения списка товаров
        """Get products list"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.get(
                "/api/ecommerce/products", params=params
            )  # Выполнение GET запроса для получения товаров
            if response.status_code == 200:  # Проверка успешного запроса
                return response.json()  # Возврат данных товаров
            else:  # Если запрос не удался
                raise Exception(
                    f"Failed to get products: {response.status_code}"
                )  # Возбуждение исключения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get products: {str(e)}"
            )  # Логирование ошибки получения товаров
            raise  # Повторное возбуждение исключения

    def create_product(
        self, product_data: Dict[str, Any]
    ) -> Dict[str, Any]:  # Метод создания товара
        """Create new product"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.post(
                "/api/ecommerce/products", json_data=product_data
            )  # Выполнение POST запроса для создания товара
            if response.status_code == 200:  # Проверка успешного создания
                self.logger.info(
                    "Successfully created product"
                )  # Логирование успешного создания товара
                return response.json()  # Возврат данных созданного товара
            else:  # Если создание не удалось
                error_msg = response.json().get(
                    "detail", "Product creation failed"
                )  # Получение сообщения об ошибке
                raise Exception(
                    f"Product creation failed: {error_msg}"
                )  # Возбуждение исключения с сообщением об ошибке
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to create product: {str(e)}"
            )  # Логирование ошибки создания товара
            raise  # Повторное возбуждение исключения

    def get_posts(
        self, params: Dict = None
    ) -> Dict[str, Any]:  # Метод получения социальных постов
        """Get social posts"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.get(
                "/api/social/posts", params=params
            )  # Выполнение GET запроса для получения постов
            if response.status_code == 200:  # Проверка успешного запроса
                return response.json()  # Возврат данных постов
            else:  # Если запрос не удался
                raise Exception(
                    f"Failed to get posts: {response.status_code}"
                )  # Возбуждение исключения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get posts: {str(e)}"
            )  # Логирование ошибки получения постов
            raise  # Повторное возбуждение исключения

    def create_post(
        self, content: str
    ) -> Dict[str, Any]:  # Метод создания социального поста
        """Create new social post"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.post(
                "/api/social/posts", json_data={"content": content}
            )  # Выполнение POST запроса для создания поста
            if response.status_code == 200:  # Проверка успешного создания
                self.logger.info(
                    "Successfully created post"
                )  # Логирование успешного создания поста
                return response.json()  # Возврат данных созданного поста
            else:  # Если создание не удалось
                error_msg = response.json().get(
                    "detail", "Post creation failed"
                )  # Получение сообщения об ошибке
                raise Exception(
                    f"Post creation failed: {error_msg}"
                )  # Возбуждение исключения с сообщением об ошибке
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to create post: {str(e)}"
            )  # Логирование ошибки создания поста
            raise  # Повторное возбуждение исключения

    def get_analytics_dashboard(
        self,
    ) -> Dict[str, Any]:  # Метод получения данных аналитического дашборда
        """Get analytics dashboard data"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.get(
                "/api/analytics/dashboard"
            )  # Выполнение GET запроса для получения аналитики
            if response.status_code == 200:  # Проверка успешного запроса
                return response.json()  # Возврат данных аналитики
            else:  # Если запрос не удался
                raise Exception(
                    f"Failed to get analytics: {response.status_code}"
                )  # Возбуждение исключения
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Failed to get analytics: {str(e)}"
            )  # Логирование ошибки получения аналитики
            raise  # Повторное возбуждение исключения

    def health_check(self) -> bool:  # Метод проверки здоровья API
        """Check API health"""  # Документация метода
        try:  # Начало блока обработки исключений
            response = self.get(
                "/api/health"
            )  # Выполнение GET запроса для проверки здоровья
            return response.status_code == 200  # Возврат результата проверки здоровья
        except Exception as e:  # Обработка исключений
            self.logger.error(
                f"Health check failed: {str(e)}"
            )  # Логирование ошибки проверки здоровья
            return False  # Возврат False при ошибке

    def get_response_logs(
        self,
    ) -> List[Dict[str, Any]]:  # Метод получения логов ответов
        """Get all response logs"""  # Документация метода
        return self.response_logs.copy()  # Возврат копии логов ответов

    def clear_response_logs(self):  # Метод очистки логов ответов
        """Clear response logs"""  # Документация метода
        self.response_logs.clear()  # Очистка списка логов ответов
        self.logger.info("Response logs cleared")  # Логирование очистки логов

    def get_performance_metrics(
        self,
    ) -> Dict[str, Any]:  # Метод получения метрик производительности
        """Get performance metrics from response logs"""  # Документация метода
        if not self.response_logs:  # Проверка наличия логов ответов
            return {}  # Возврат пустого словаря если логов нет

        response_times = [
            log["response_time"] for log in self.response_logs
        ]  # Извлечение времен ответов

        return {  # Возврат словаря с метриками производительности
            "total_requests": len(self.response_logs),  # Общее количество запросов
            "avg_response_time": sum(response_times)
            / len(response_times),  # Среднее время ответа
            "min_response_time": min(response_times),  # Минимальное время ответа
            "max_response_time": max(response_times),  # Максимальное время ответа
            "success_rate": len(  # Процент успешных запросов
                [
                    log for log in self.response_logs if 200 <= log["status_code"] < 300
                ]  # Фильтрация успешных запросов
            )
            / len(self.response_logs)  # Деление на общее количество запросов
            * 100,  # Умножение на 100 для получения процента
        }

    def wait_for_api_availability(
        self, timeout: int = 60
    ) -> bool:  # Метод ожидания доступности API
        """Wait for API to become available"""  # Документация метода
        start_time = time.time()  # Запись времени начала ожидания

        while time.time() - start_time < timeout:  # Цикл пока не истек таймаут
            if self.health_check():  # Проверка здоровья API
                self.logger.info("API is available")  # Логирование доступности API
                return True  # Возврат True если API доступен
            time.sleep(5)  # Ожидание 5 секунд перед следующей проверкой

        self.logger.error(
            "API is not available after timeout"
        )  # Логирование недоступности API после таймаута
        return False  # Возврат False если API недоступен
