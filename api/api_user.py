from api_client import ApiClient

class UserApi(ApiClient):
    def create_user(self, email, password, name):
        """
        Создает нового пользователя.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param name: Имя пользователя.
        :return: ID созданного пользователя.
        """
        user_data = {
            'email': email,
            'password': password,
            'name': name
        }
        return self.post('/users', data=user_data)

    def update_user(self, user_id, email=None, password=None, name=None):
        """
        Обновляет данные пользователя.
        :param user_id: ID пользователя.
        :param email: Новый email пользователя (optional).
        :param password: Новый пароль пользователя (optional).
        :param name: Новое имя пользователя (optional).
        :return: Ответ сервера в формате JSON.
        """
        user_data = {}
        if email:
            user_data['email'] = email
        if password:
            user_data['password'] = password
        if name:
            user_data['name'] = name
        return self.patch(f'/users/{user_id}', data=user_data)

    def get_user_data(self, user_id):
        """
        Получает данные пользователя по ID.
        :param user_id: ID пользователя.
        :return: Ответ сервера в формате JSON.
        """
        return self.get(f'/users/{user_id}')

    def delete_user(self, user_id):
        """
        Удаляет пользователя по ID.
        :param user_id: ID пользователя.
        :return: Ответ сервера в формате JSON или None, если тело ответа пустое.
        """
        return self.delete(f'/users/{user_id}')


