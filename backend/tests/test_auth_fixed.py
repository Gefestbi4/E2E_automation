"""
Исправленные тесты для модуля аутентификации
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from models import Base, User
from auth import get_password_hash, get_db

# Создаем тестовую БД
SQLALCHEMY_DATABASE_URL = (
    "postgresql://my_user:my_password@localhost:5432/test_database"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Импортируем все модели для создания таблиц
import models_package.ecommerce
import models_package.social
import models_package.tasks
import models_package.content
import models_package.analytics

# Создаем таблицы
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Переопределяем get_db для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def db_session():
    """Фикстура для сессии БД"""
    # Очищаем БД перед каждым тестом
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: Session):
    """Фикстура для тестового пользователя"""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestUserRegistration:
    """Тесты регистрации пользователя"""

    def test_successful_registration(self):
        """Успешная регистрация пользователя"""
        # Используем уникальный email для каждого теста
        import time

        timestamp = int(time.time())
        unique_email = f"newuser{timestamp}@example.com"

        user_data = {
            "email": unique_email,
            "password": "newpassword123",
            "confirm_password": "newpassword123",
            "full_name": "New User",
        }

        response = client.post("/api/auth/register", json=user_data)

        # Отладочная информация
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code != 200:
            # Если ошибка валидации, выводим детали
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                pass

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert (
            data["username"] == f"newuser{timestamp}"
        )  # Автоматически создается из email
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert data["is_active"] is True
        assert data["is_verified"] is False

    def test_registration_with_existing_email(self, test_user):
        """Регистрация с существующим email"""
        user_data = {
            "email": test_user.email,
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Another User",
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 409
        assert "уже существует" in response.json()["detail"]

    def test_registration_with_invalid_email(self):
        """Регистрация с невалидным email"""
        user_data = {
            "email": "invalid-email",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Test User",
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 422


class TestUserLogin:
    """Тесты входа пользователя"""

    def test_successful_login(self, test_user):
        """Успешный вход пользователя"""
        login_data = {"email": test_user.email, "password": "testpassword123"}

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_with_wrong_password(self, test_user):
        """Вход с неверным паролем"""
        login_data = {"email": test_user.email, "password": "wrongpassword"}

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 401
        assert "Неверный email или пароль" in response.json()["detail"]

    def test_login_with_nonexistent_email(self):
        """Вход с несуществующим email"""
        login_data = {"email": "nonexistent@example.com", "password": "password123"}

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 401
        assert "Неверный email или пароль" in response.json()["detail"]

    def test_login_with_inactive_user(self, db_session: Session):
        """Вход неактивного пользователя"""
        inactive_user = User(
            email="inactive@example.com",
            username="inactive",
            hashed_password=get_password_hash("password123"),
            is_active=False,
        )
        db_session.add(inactive_user)
        db_session.commit()

        login_data = {"email": inactive_user.email, "password": "password123"}

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 403
        assert "деактивирован" in response.json()["detail"]


class TestTokenRefresh:
    """Тесты обновления токенов"""

    def test_successful_token_refresh(self, test_user):
        """Успешное обновление токена"""
        # Сначала получаем токены
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]

        # Обновляем токен
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/auth/refresh", json=refresh_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_with_invalid_token(self):
        """Обновление с невалидным токеном"""
        refresh_data = {"refresh_token": "invalid_token"}
        response = client.post("/api/auth/refresh", json=refresh_data)

        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]


class TestProtectedEndpoints:
    """Тесты защищенных endpoints"""

    def test_get_current_user_success(self, test_user):
        """Успешное получение информации о пользователе"""
        # Получаем токен
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # Получаем информацию о пользователе
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username

    def test_get_current_user_without_token(self):
        """Получение информации без токена"""
        response = client.get("/api/auth/me")

        assert response.status_code == 403

    def test_get_current_user_with_invalid_token(self):
        """Получение информации с невалидным токеном"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == 401


class TestUserUpdate:
    """Тесты обновления пользователя"""

    def test_update_user_success(self, test_user):
        """Успешное обновление пользователя"""
        # Получаем токен
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # Обновляем пользователя
        update_data = {"full_name": "Updated Name", "username": "updateduser"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/api/auth/me", json=update_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["username"] == "updateduser"

    def test_update_user_without_token(self):
        """Обновление пользователя без токена"""
        update_data = {"full_name": "New Name"}
        response = client.put("/api/auth/me", json=update_data)

        assert response.status_code == 403


class TestPasswordChange:
    """Тесты смены пароля"""

    def test_change_password_success(self, test_user):
        """Успешная смена пароля"""
        # Получаем токен
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # Меняем пароль
        password_data = {
            "current_password": "testpassword123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post(
            "/api/auth/change-password", json=password_data, headers=headers
        )

        assert response.status_code == 200
        assert "успешно изменен" in response.json()["message"]

    def test_change_password_wrong_current(self, test_user):
        """Смена пароля с неверным текущим паролем"""
        # Получаем токен
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # Меняем пароль с неверным текущим
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123",
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post(
            "/api/auth/change-password", json=password_data, headers=headers
        )

        assert response.status_code == 401
        assert "Неверный текущий пароль" in response.json()["detail"]


class TestEmailVerification:
    """Тесты подтверждения email"""

    def test_verify_email_success(self):
        """Успешное подтверждение email"""
        verification_data = {"token": "test_token"}
        response = client.post("/api/auth/verify-email", json=verification_data)

        assert response.status_code == 200
        assert "успешно подтвержден" in response.json()["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
