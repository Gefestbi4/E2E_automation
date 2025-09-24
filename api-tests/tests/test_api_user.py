
import pytest
import os
from dotenv import load_dotenv
from faker import Faker
from requests import HTTPError

from api.api_user import UserApi

load_dotenv()
fake = Faker()

# --- Фикстуры ---

@pytest.fixture(scope="session")
def api_client():
    """Фикстура для инициализации API клиента."""
    base_url = os.getenv('DATABASE_URL')
    api_key = os.getenv('API_KEY')
    return UserApi(base_url, api_key)

@pytest.fixture
def new_user_payload():
    """Фикстура для генерации данных нового пользователя."""
    return {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }

@pytest.fixture
def created_user(api_client, new_user_payload):
    """Фикстура для создания пользователя и его последующего удаления."""
    # Создание пользователя
    response = api_client.create_user(**new_user_payload)
    # Предполагаем, что API возвращает id в ответе
    user_id = response.get('id')
    assert user_id is not None, "API не вернуло ID созданного пользователя"

    # Передаем созданного пользователя в тест
    yield response

    # Очистка (удаление пользователя после теста)
    try:
        api_client.delete_user(user_id)
    except HTTPError as e:
        # Игнорируем ошибку 404, если пользователь уже был удален в самом тесте
        if e.response.status_code != 404:
            raise

# --- Тесты ---

@pytest.mark.api
def test_create_user_success(created_user, new_user_payload):
    """
    Тест успешного создания пользователя.
    Проверяет, что пользователь создается с корректными данными.
    Фикстура created_user уже выполнила создание, здесь мы проверяем результат.
    """
    assert 'id' in created_user
    assert created_user['email'] == new_user_payload['email']
    assert created_user['name'] == new_user_payload['name']
    # Пароль обычно не возвращается в ответе, поэтому его не проверяем

@pytest.mark.api
def test_get_user_success(api_client, created_user):
    """
    Тест успешного получения пользователя по ID.
    Проверяет, что можно получить созданного пользователя и данные совпадают.
    """
    user_id = created_user['id']
    get_response = api_client.get_user(user_id)

    assert get_response['id'] == user_id
    assert get_response['email'] == created_user['email']
    assert get_response['name'] == created_user['name']

@pytest.mark.api
def test_update_user_success(api_client, created_user):
    """
    Тест успешного обновления данных пользователя.
    Проверяет, что имя и email пользователя можно изменить.
    """
    user_id = created_user['id']
    new_name = fake.name()
    new_email = fake.email()
    update_payload = {
        "name": new_name,
        "email": new_email
    }

    update_response = api_client.update_user(user_id, update_payload)

    assert update_response['id'] == user_id
    assert update_response['name'] == new_name
    assert update_response['email'] == new_email

    # Проверяем, что данные действительно сохранились, запросив пользователя еще раз
    get_response = api_client.get_user(user_id)
    assert get_response['name'] == new_name
    assert get_response['email'] == new_email

@pytest.mark.api
def test_delete_user_success(api_client, created_user):
    """
    Тест успешного удаления пользователя.
    Проверяет, что после удаления пользователь становится недоступен.
    """
    user_id = created_user['id']

    # Удаляем пользователя
    delete_response = api_client.delete_user(user_id)
    assert delete_response is None  # Метод delete ничего не возвращает при успехе

    # Проверяем, что пользователь действительно удален (ожидаем ошибку 404)
    with pytest.raises(HTTPError) as e:
        api_client.get_user(user_id)
    assert e.value.response.status_code == 404
