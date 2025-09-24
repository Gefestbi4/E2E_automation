
import pytest

def test_create_and_get_user(user_repo):
    """
    Тест создания и последующего получения пользователя из БД.
    """
    user_data = {
        "email": "test.user@example.com",
        "name": "Test User",
        "password_hash": "some_secure_hash"
    }

    # 1. Создание пользователя
    user_id = user_repo.create_user(user_data)
    assert user_id is not None, "Не удалось создать пользователя"

    # 2. Получение пользователя по ID
    retrieved_user = user_repo.get_user_by_id(user_id)
    assert retrieved_user is not None, "Не удалось найти пользователя по ID"
    assert retrieved_user['email'] == user_data['email']
    assert retrieved_user['name'] == user_data['name']

    # 3. Получение пользователя по email
    retrieved_user_by_email = user_repo.get_user_by_email(user_data['email'])
    assert retrieved_user_by_email is not None, "Не удалось найти пользователя по email"
    assert str(retrieved_user_by_email['_id']) == str(user_id)

    # 4. Очистка
    result = user_repo.delete_user_by_id(user_id)
    assert result.deleted_count == 1, "Пользователь не был удален"

    # 5. Проверка, что пользователь действительно удален
    assert user_repo.get_user_by_id(user_id) is None, "Пользователь все еще существует после удаления"

def test_get_non_existent_user(user_repo):
    """
    Тест запроса несуществующего пользователя.
    """
    # Попытка найти пользователя с заведомо несуществующим ID
    non_existent_id = "60c72b2f9b1e8b3b3c8b4567" # Пример валидного, но несуществующего
    assert user_repo.get_user_by_id(non_existent_id) is None, "Поиск несуществующего пользователя должен вернуть None"

