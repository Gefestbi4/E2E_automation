
from bson import ObjectId

class UserRepository:
    def __init__(self, db_client):
        """
        Инициализирует репозиторий для работы с пользователями.
        :param db_client: Экземпляр MongoDBClient.
        """
        self.db_client = db_client
        self.collection_name = "users"

    def create_user(self, user_data):
        """
        Создает нового пользователя.
        :param user_data: Словарь с данными пользователя (например, email, name, password_hash).
        :return: ID созданного пользователя.
        """
        return self.db_client.insert_one(self.collection_name, user_data)

    def get_user_by_id(self, user_id):
        """
        Находит пользователя по его ID.
        :param user_id: ID пользователя (может быть строкой или ObjectId).
        :return: Документ пользователя или None.
        """
        # ObjectId необходим для корректного поиска по _id в MongoDB
        query = {"_id": ObjectId(user_id)}
        return self.db_client.find_one(self.collection_name, query)

    def get_user_by_email(self, email):
        """
        Находит пользователя по email.
        :param email: Email пользователя.
        :return: Документ пользователя или None.
        """
        query = {"email": email}
        return self.db_client.find_one(self.collection_name, query)

    def delete_user_by_id(self, user_id):
        """
        Удаляет пользователя по ID.
        :param user_id: ID пользователя.
        :return: Результат операции удаления.
        """
        query = {"_id": ObjectId(user_id)}
        return self.db_client.delete_one(self.collection_name, query)
