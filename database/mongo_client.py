
from pymongo import MongoClient
import allure
import json

class MongoDBClient:
    def __init__(self, connection_string, db_name):
        """
        Инициализирует клиент для подключения к MongoDB.
        :param connection_string: Строка подключения к MongoDB.
        :param db_name: Имя базы данных.
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def find_one(self, collection_name, query):
        """
        Находит один документ в коллекции.
        :param collection_name: Имя коллекции.
        :param query: Запрос для поиска.
        :return: Найденный документ или None.
        """
        with allure.step(f"MongoDB: Поиск одного документа в '{collection_name}'"):
            allure.attach(json.dumps(query, indent=2), "Query", allure.attachment_type.JSON)
            document = self.db[collection_name].find_one(query)
            if document:
                # ObjectId не сериализуется в JSON, поэтому преобразуем его в строку
                document['_id'] = str(document['_id'])
                allure.attach(json.dumps(document, indent=2), "Found Document", allure.attachment_type.JSON)
            return document

    def find(self, collection_name, query):
        """
        Находит все документы, соответствующие запросу.
        :param collection_name: Имя коллекции.
        :param query: Запрос для поиска.
        :return: Курсор с результатами.
        """
        with allure.step(f"MongoDB: Поиск документов в '{collection_name}'"):
            allure.attach(json.dumps(query, indent=2), "Query", allure.attachment_type.JSON)
            return self.db[collection_name].find(query)

    def insert_one(self, collection_name, document):
        """
        Вставляет один документ в коллекцию.
        :param collection_name: Имя коллекции.
        :param document: Документ для вставки.
        :return: ID вставленного документа.
        """
        with allure.step(f"MongoDB: Вставка документа в '{collection_name}'"):
            allure.attach(json.dumps(document, indent=2), "Document to Insert", allure.attachment_type.JSON)
            inserted_id = self.db[collection_name].insert_one(document).inserted_id
            allure.attach(str(inserted_id), "Inserted ID", allure.attachment_type.TEXT)
            return inserted_id

    def delete_one(self, collection_name, query):
        """
        Удаляет один документ из коллекции.
        :param collection_name: Имя коллекции.
        :param query: Запрос для удаления.
        :return: Результат операции удаления.
        """
        with allure.step(f"MongoDB: Удаление одного документа из '{collection_name}'"):
            allure.attach(json.dumps(query, indent=2), "Query", allure.attachment_type.JSON)
            return self.db[collection_name].delete_one(query)

    def close(self):
        """Закрывает соединение с базой данных."""
        with allure.step("Закрытие соединения с MongoDB"):
            self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
