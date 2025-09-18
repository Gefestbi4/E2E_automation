from .api_client import ApiClient


class UserApi(ApiClient):
    def create_user(self, email, password, name):
        """
        Создает нового пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param name: Имя пользователя.
        :return: JSON-ответ с данными созданного пользователя.
        """
        user_data = {
            'email': email,
            'password': password,
            'name': name
        }
        return self.post('/users', data=user_data)

    def get_user(self, user_id):
        """
        Получает данные пользователя по ID.
        :param user_id: ID пользователя.
        :return: JSON-ответ с данными пользователя.
        """
        return self.get(f'/users/{user_id}')

    def update_user(self, user_id, data):
        """
        Обновляет данные пользователя.
        :param user_id: ID пользователя.
        :param data: Словарь с обновляемыми полями.
        :return: JSON-ответ с обновленными данными пользователя.
        """
        return self.put(f'/users/{user_id}', data=data)

    def delete_user(self, user_id):
        """
        Удаляет пользователя по ID.
        :param user_id: ID пользователя.
        :return: None.
        """
        return self.delete(f'/users/{user_id}')


