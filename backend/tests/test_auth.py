"""
Тесты для модуля аутентификации
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app_new import app
from core.database import Base, get_db
from core.security import get_password_hash
from models.user import User

# Создаем тестовую БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "newpassword123",
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert data["is_active"] is True

    def test_registration_with_existing_email(self, test_user):
        """Регистрация с существующим email"""
        user_data = {
            "email": test_user.email,
            "username": "anotheruser",
            "password": "password123",
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_registration_with_existing_username(self, test_user):
        """Регистрация с существующим username"""
        user_data = {
            "email": "another@example.com",
            "username": test_user.username,
            "password": "password123",
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_registration_with_invalid_email(self):
        """Регистрация с невалидным email"""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "password123",
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
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_with_nonexistent_email(self):
        """Вход с несуществующим email"""
        login_data = {"email": "nonexistent@example.com", "password": "password123"}

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

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

        assert response.status_code == 400
        assert "Inactive user" in response.json()["detail"]


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


class TestPasswordReset:
    """Тесты сброса пароля"""

    def test_forgot_password_success(self, test_user):
        """Успешный запрос сброса пароля"""
        reset_data = {"email": test_user.email}
        response = client.post("/api/auth/forgot-password", json=reset_data)

        assert response.status_code == 200
        assert "Password reset email sent" in response.json()["message"]

    def test_forgot_password_nonexistent_email(self):
        """Запрос сброса пароля для несуществующего email"""
        reset_data = {"email": "nonexistent@example.com"}
        response = client.post("/api/auth/forgot-password", json=reset_data)

        # Должен вернуть успех для безопасности
        assert response.status_code == 200
        assert "Password reset email sent" in response.json()["message"]


class TestUserUpdate:
    """Тесты обновления пользователя"""

    def test_update_user_success(self, test_user):
        """Успешное обновление пользователя"""
        # Получаем токен
        login_data = {"email": test_user.email, "password": "testpassword123"}
        login_response = client.post("/api/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]

        # Обновляем пользователя
        update_data = {"full_name": "Updated Name", "bio": "Updated bio"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.put("/api/auth/me", json=update_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["bio"] == "Updated bio"

    def test_update_user_without_token(self):
        """Обновление пользователя без токена"""
        update_data = {"full_name": "New Name"}
        response = client.put("/api/auth/me", json=update_data)

        assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__])
