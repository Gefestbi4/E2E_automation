
import pytest
from dotenv import load_dotenv
from faker import Faker
from database.postgres_client import PostgresClient
import os

# Загружаем переменные окружения для доступа к БД
load_dotenv()
fake = Faker()

# --- Фикстуры ---

@pytest.fixture(scope="module")
def db_client():
    """Фикстура для подключения к базе данных. Выполняется один раз для всех тестов в модуле."""
    # Предполагается, что у вас есть эти переменные в .env файле
    with PostgresClient(
        db_host=os.getenv('DB_HOST'),
        db_port=os.getenv('DB_PORT'),
        db_user=os.getenv('DB_USER'),
        db_password=os.getenv('DB_PASSWORD'),
        db_name=os.getenv('DB_NAME')
    ) as client:
        yield client

@pytest.fixture
def new_user_data():
    """Фикстура для генерации данных нового пользователя."""
    return {
        "email": fake.email(),
        "password": fake.password(),  # В реальном проекте пароль бы хэшировался
        "name": fake.name()
    }

@pytest.fixture
def created_user_in_db(db_client, new_user_data):
    """
    Фикстура для создания пользователя в БД перед тестом и его удаления после.
    """
    # Создаем пользователя и получаем его ID
    query = """
        INSERT INTO users (email, password, name) 
        VALUES (%(email)s, %(password)s, %(name)s) 
        RETURNING id;
    """
    result = db_client.execute_query(query, new_user_data, fetch="one")
    assert result is not None, "Не удалось создать пользователя в БД"
    user_id = result[0]
    
    # Передаем ID и данные в тест
    yield user_id, new_user_data

    # Очистка: удаляем пользователя после теста
    db_client.execute_query("DELETE FROM users WHERE id = %s;", (user_id,))

# --- Тесты ---

@pytest.mark.db
def test_create_and_get_user(db_client, created_user_in_db):
    """
    Тест: проверяет, что пользователь корректно создается и его можно получить из БД.
    """
    user_id, new_user_data = created_user_in_db
    
    # Проверяем, что пользователь существует в БД и данные совпадают
    query = "SELECT id, email, name, password FROM users WHERE id = %s;"
    user_from_db = db_client.execute_query(query, (user_id,), fetch="one")

    assert user_from_db is not None
    assert user_from_db[0] == user_id
    assert user_from_db[1] == new_user_data['email']
    assert user_from_db[2] == new_user_data['name']
    assert user_from_db[3] == new_user_data['password']

@pytest.mark.db
def test_update_user(db_client, created_user_in_db):
    """
    Тест: проверяет, что данные пользователя можно обновить в БД.
    """
    user_id, _ = created_user_in_db
    new_name = fake.name()
    
    # Обновляем имя пользователя
    update_query = "UPDATE users SET name = %s WHERE id = %s;"
    db_client.execute_query(update_query, (new_name, user_id))

    # Проверяем, что имя обновилось
    select_query = "SELECT name FROM users WHERE id = %s;"
    updated_name_tuple = db_client.execute_query(select_query, (user_id,), fetch="one")
    assert updated_name_tuple is not None, "Не удалось найти пользователя после обновления"
    updated_name = updated_name_tuple[0]

    assert updated_name == new_name

@pytest.mark.db
def test_delete_user(db_client, created_user_in_db):
    """
    Тест: проверяет, что пользователь удаляется из БД.
    """
    user_id, _ = created_user_in_db

    # Удаляем пользователя (этот код выполнится после yield в фикстуре)
    # Здесь мы просто проверяем, что после удаления его нет
    
    # Сначала удаляем
    delete_query = "DELETE FROM users WHERE id = %s;"
    db_client.execute_query(delete_query, (user_id,))
    
    # Проверяем, что пользователя больше нет
    select_query = "SELECT id FROM users WHERE id = %s;"
    user_from_db = db_client.execute_query(select_query, (user_id,), fetch="one")
    assert user_from_db is None, "Пользователь не был удален из БД"
