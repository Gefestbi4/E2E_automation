
import os
import pytest
from dotenv import load_dotenv
from database.mongo_client import MongoDBClient
from database.user_repository import UserRepository

# Загружаем переменные окружения
load_dotenv()

@pytest.fixture(scope="session")
def db_client():
    """
    Фикстура для создания клиента MongoDB.
    Соединение устанавливается один раз на всю тестовую сессию.
    """
    mongo_url = os.getenv("MONGO_URL") # Убедитесь, что MONGO_URL есть в .env
    db_name = os.getenv("MONGO_DB_NAME", "test_db") # Имя тестовой БД

    if not mongo_url:
        pytest.fail("Переменная окружения MONGO_URL не установлена.")

    client = MongoDBClient(mongo_url, db_name)
    yield client
    client.close()

@pytest.fixture(scope="function")
def user_repo(db_client):
    """
    Фикстура, которая предоставляет экземпляр UserRepository для каждого теста.
    """
    return UserRepository(db_client)
