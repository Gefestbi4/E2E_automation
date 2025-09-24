from .api_client import ApiClient
import allure


class UserApi(ApiClient):
    """API клиент для работы с пользователями через новый бэкенд"""
    
    def __init__(self, base_url, api_key=None):
        """
        Инициализирует API-клиент для работы с пользователями.
        :param base_url: Базовый URL бэкенда (например, http://localhost:5000).
        :param api_key: API-ключ (не используется в новом бэкенде).
        """
        super().__init__(base_url, api_key)
        self.session.headers['Content-Type'] = 'application/json'
    
    @allure.step("Авторизация пользователя")
    def login_user(self, email, password):
        """
        Авторизация пользователя через API.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: JSON-ответ с токеном авторизации.
        """
        login_data = {
            'email': email,
            'password': password
        }
        return self.post('/api/auth/login', data=login_data)
    
    @allure.step("Получение информации о текущем пользователе")
    def get_current_user(self, token):
        """
        Получение информации о текущем пользователе.
        :param token: JWT токен авторизации.
        :return: JSON-ответ с данными пользователя.
        """
        headers = {'Authorization': f'Bearer {token}'}
        return self.session.get(f"{self.base_url}/api/auth/me", headers=headers).json()
    
    @allure.step("Создание пользователя через авторизацию")
    def create_user(self, email, password, name=None):
        """
        Создает нового пользователя через авторизацию (автоматическая регистрация).
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param name: Имя пользователя (необязательно).
        :return: JSON-ответ с токеном авторизации.
        """
        # В новом бэкенде пользователь создается автоматически при авторизации
        try:
            return self.login_user(email, password)
        except Exception as e:
            # Если пользователь не существует, это нормально - он будет создан при первом логине
            allure.attach(f"Пользователь {email} не существует, будет создан при первом логине: {str(e)}", 
                         "Info", allure.attachment_type.TEXT)
            return None
    
    @allure.step("Проверка существования пользователя")
    def user_exists(self, email, password):
        """
        Проверяет, существует ли пользователь с данными учетными данными.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: True, если пользователь существует, False - если нет.
        """
        try:
            response = self.login_user(email, password)
            return 'access_token' in response
        except Exception:
            return False
    
    @allure.step("Удаление пользователя")
    def delete_user(self, email):
        """
        Удаление пользователя (в новом бэкенде не реализовано).
        :param email: Email пользователя.
        :return: None.
        """
        # В новом бэкенде нет эндпоинта для удаления пользователей
        # Это можно реализовать через прямую работу с БД или добавить эндпоинт
        allure.attach(f"Удаление пользователя {email} не реализовано в новом бэкенде", 
                     "Info", allure.attachment_type.TEXT)
        pass
    
    @allure.step("Проверка здоровья API")
    def health_check(self):
        """
        Проверка здоровья API.
        :return: JSON-ответ со статусом API.
        """
        return self.get('/api/health')
    
    @allure.step("Получение токена авторизации")
    def get_auth_token(self, email, password):
        """
        Получение токена авторизации для пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: JWT токен или None.
        """
        try:
            response = self.login_user(email, password)
            return response.get('access_token')
        except Exception as e:
            allure.attach(f"Ошибка получения токена: {str(e)}", "Error", allure.attachment_type.TEXT)
            return None