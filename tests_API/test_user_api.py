
import os
import pytest
from dotenv import load_dotenv
from api.api_user import UserApi
import random
import string

# Загружаем переменные окружения
load_dotenv()
base_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')

def generate_random_email():
    """Генерирует случайный email."""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return f"{random_string}@example.com"

@pytest.fixture(scope="module")
def user_api_client():
    """Фикстура для создания клиента API."""
    return UserApi(base_url, api_key)

@pytest.fixture(scope="function")
def test_user(user_api_client):
    """Фикстура для создания и последующего удаления тестового пользователя."""
    email = generate_random_email()
    password = "testpassword123"
    name = "Test User"
    
    # Создаем пользователя
    response = user_api_client.create_user(email, password, name)
    user_id = response.get('id')
    assert user_id is not None, "Не удалось создать пользователя для теста"
    
    yield user_id, email, name
    
    # Очистка: удаляем пользователя после теста
    try:
        user_api_client.delete_user(user_id)
    except Exception as e:
        print(f"Не удалось удалить пользователя {user_id}: {e}")

def test_create_user(user_api_client):
    """Тест создания нового пользователя."""
    email = generate_random_email()
    password = "supersecret"
    name = "John Doe"
    
    response = user_api_client.create_user(email, password, name)
    
    assert 'id' in response, "В ответе отсутствует ID пользователя"
    user_id = response['id']
    
    # Проверяем, что пользователь действительно создан
    user_data = user_api_client.get_user_data(user_id)
    assert user_data['email'] == email
    assert user_data['name'] == name
    
    # Удаляем созданного пользователя
    user_api_client.delete_user(user_id)

def test_get_user_data(user_api_client, test_user):
    """Тест получения данных пользователя."""
    user_id, email, name = test_user
    
    user_data = user_api_client.get_user_data(user_id)
    
    assert user_data['id'] == user_id
    assert user_data['email'] == email
    assert user_data['name'] == name

def test_update_user(user_api_client, test_user):
    """Тест обновления данных пользователя."""
    user_id, _, _ = test_user
    new_name = "Jane Doe"
    new_email = generate_random_email()
    
    update_response = user_api_client.update_user(user_id, name=new_name, email=new_email)
    assert update_response is not None
    
    # Проверяем, что данные обновились
    updated_user_data = user_api_client.get_user_data(user_id)
    assert updated_user_data['name'] == new_name
    assert updated_user_data['email'] == new_email

def test_delete_user(user_api_client):
    """Тест удаления пользователя."""
    email = generate_random_email()
    password = "tobedeleted"
    name = "User To Delete"
    
    # Создаем пользователя для удаления
    response = user_api_client.create_user(email, password, name)
    user_id = response['id']
    
    # Удаляем пользователя
    delete_response = user_api_client.delete_user(user_id)
    assert delete_response is None # Метод delete возвращает None при успехе
    
    # Проверяем, что пользователь действительно удален (ожидаем ошибку)
    with pytest.raises(Exception) as e:
        user_api_client.get_user_data(user_id)
    
    assert "404" in str(e.value), "Ожидалась ошибка 404 Not Found при запросе удаленного пользователя"
