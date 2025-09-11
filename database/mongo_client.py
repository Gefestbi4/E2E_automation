
from pymongo import MongoClient
import allure

class MongoDBClient:
    def __init__(self, connection_string, db_name):
        """
        Инициализирует клиент для подключения к MongoDB.
        :param connection_string: Строка подключения к MongoDB.
        :param db_name: Имя базы данных.
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    @allure.step("Поиск одного документа в коллекции '{collection_name}'")
    def find_one(self, collection_name, query):
        """
        Находит один документ в коллекции.
        :param collection_name: Имя коллекции.
        :param query: Запрос для поиска.
        :return: Найденный документ или None.
        """
        return self.db[collection_name].find_one(query)

    @allure.step("Поиск нескольких документов в коллекции '{collection_name}'")
    def find(self, collection_name, query):
        """
        Находит все документы, соответствующие запросу.
        :param collection_name: Имя коллекции.
        :param query: Запрос для поиска.
        :return: Курсор с результатами.
        """
        return self.db[collection_name].find(query)

    @allure.step("Вставка документа в коллекцию '{collection_name}'")
    def insert_one(self, collection_name, document):
        """
        Вставляет один документ в коллекцию.
        :param collection_name: Имя коллекции.
        :param document: Документ для вставки.
        :return: ID вставленного документа.
        """
        return self.db[collection_name].insert_one(document).inserted_id

    @allure.step("Удаление одного документа из коллекции '{collection_name}'")
    def delete_one(self, collection_name, query):
        """
        Удаляет один документ из коллекции.
        :param collection_name: Имя коллекции.
        :param query: Запрос для удаления.
        :return: Результат операции удаления.
        """
        return self.db[collection_name].delete_one(query)

    @allure.step("Закрытие соединения с MongoDB")
    def close(self):
        """Закрывает соединение с базой данных."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
