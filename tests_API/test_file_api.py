
import os
import pytest
from dotenv import load_dotenv
from api.api_file import FileApi

# Загружаем переменные окружения
load_dotenv()
base_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')

@pytest.fixture(scope="module")
def file_api_client():
    """Фикстура для создания клиента FileApi."""
    return FileApi(base_url, api_key)

@pytest.fixture(scope="function")
def temp_file():
    """Фикстура для создания временного файла для тестов."""
    file_path = "test_file.txt"
    file_content = "Hello, this is a test file."
    with open(file_path, "w") as f:
        f.write(file_content)
    
    yield file_path, file_content
    
    # Очистка: удаляем файл после теста
    os.remove(file_path)

def test_file_upload_download_delete_workflow(file_api_client, temp_file):
    """
    Комплексный тест: загрузка, проверка, скачивание, сравнение и удаление файла.
    """
    file_path, file_content = temp_file

    # 1. Загрузка файла
    upload_response = file_api_client.upload_file(file_path)
    assert 'id' in upload_response, "Ответ на загрузку не содержит ID файла"
    file_id = upload_response['id']

    # 2. Получение URL файла (неявная проверка)
    # Этот шаг выполняется внутри download_file, но можно и явно проверить
    file_url = file_api_client.get_file_url(file_id)
    assert file_url is not None, "Не удалось получить URL для скачивания файла"

    # 3. Скачивание файла
    downloaded_content = file_api_client.download_file(file_id)
    assert downloaded_content.decode('utf-8') == file_content, "Содержимое скачанного файла не совпадает с оригиналом"

    # 4. Удаление файла
    delete_response = file_api_client.delete_file(file_id)
    assert delete_response is None, "Ответ на удаление файла не пустой"

    # 5. Проверка, что файл действительно удален
    with pytest.raises(Exception) as e:
        file_api_client.get_file_url(file_id)
    assert "404" in str(e.value), "Ожидалась ошибка 404 Not Found при запросе удаленного файла"
