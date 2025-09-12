
import os
import pytest
from dotenv import load_dotenv
from api.api_folder import FolderApi

# Загружаем переменные окружения
load_dotenv()
base_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')

@pytest.fixture(scope="module")
def folder_api_client():
    """Фикстура для создания клиента FolderApi."""
    return FolderApi(base_url, api_key)

@pytest.fixture(scope="function")
def test_folder(folder_api_client):
    """Фикстура для создания и последующего удаления тестовой папки."""
    folder_name = "My Test Folder"
    folder_id = folder_api_client.create_folder(folder_name)
    
    yield folder_id, folder_name
    
    # Очистка: удаляем папку после теста
    try:
        folder_api_client.delete_folder(folder_id)
    except Exception as e:
        # Игнорируем ошибку, если папка уже была удалена в тесте
        print(f"Не удалось удалить папку {folder_id} при очистке: {e}")

def test_create_folder(folder_api_client):
    """Тест создания новой папки."""
    folder_name = "New Unique Folder"
    
    # Создаем папку
    folder_id = folder_api_client.create_folder(folder_name)
    assert folder_id is not None, "Не удалось создать папку"
    
    # Проверяем, что папка действительно создана
    folder_data = folder_api_client.get_folder(folder_id)
    assert folder_data['name'] == folder_name
    assert folder_data['id'] == folder_id
    
    # Удаляем созданную папку
    folder_api_client.delete_folder(folder_id)

def test_get_folder_data(folder_api_client, test_folder):
    """Тест получения данных папки."""
    folder_id, folder_name = test_folder
    
    folder_data = folder_api_client.get_folder(folder_id)
    
    assert folder_data['id'] == folder_id
    assert folder_data['name'] == folder_name

def test_update_folder(folder_api_client, test_folder):
    """Тест обновления данных папки."""
    folder_id, _ = test_folder
    new_name = "Updated Folder Name"
    
    update_response = folder_api_client.update_folder(folder_id, new_name)
    assert update_response['name'] == new_name
    
    # Проверяем, что имя действительно изменилось
    updated_folder_data = folder_api_client.get_folder(folder_id)
    assert updated_folder_data['name'] == new_name

def test_delete_folder(folder_api_client):
    """Тест удаления папки."""
    folder_name = "Folder to be deleted"
    folder_id = folder_api_client.create_folder(folder_name)
    
    # Удаляем папку
    delete_response = folder_api_client.delete_folder(folder_id)
    assert delete_response is None, "Ответ на удаление папки должен быть пустым"
    
    # Проверяем, что папка действительно удалена
    with pytest.raises(Exception) as e:
        folder_api_client.get_folder(folder_id)
    assert "404" in str(e.value), "Ожидалась ошибка 404 Not Found при запросе удаленной папки"
