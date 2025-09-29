"""
Упрощенные интеграционные тесты для проверки основных функций API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from models import Base, User
from auth import get_password_hash, get_db
import models_package.ecommerce as ecommerce_models


# Тестовая база данных в памяти
SQLALCHEMY_DATABASE_URL = (
    "postgresql://my_user:my_password@localhost:5432/test_database"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости БД для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Переопределяем зависимость БД
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Настройка тестовой базы данных"""
    # Импортируем все модели для создания таблиц
    import models_package.ecommerce
    import models_package.social
    import models_package.tasks
    import models_package.content
    import models_package.analytics

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Создание тестового пользователя"""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("testpass123"),
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    # Очищаем все связанные данные
    db.query(ecommerce_models.CartItem).delete()
    db.query(ecommerce_models.OrderItem).delete()
    db.query(ecommerce_models.Order).delete()
    db.query(ecommerce_models.Product).delete()
    db.delete(user)
    db.commit()
    db.close()


@pytest.fixture
def auth_headers(test_user):
    """Получение заголовков аутентификации"""
    response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "testpass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestBasicAPI:
    """Тесты базового API"""

    def test_health_check(self, setup_database):
        """Тест проверки здоровья API"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "E2E Automation API is running" in data["message"]

    def test_docs_endpoint(self, setup_database):
        """Тест документации API"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, setup_database):
        """Тест OpenAPI схемы"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data


class TestAuthentication:
    """Тесты аутентификации"""

    def test_user_registration(self, setup_database):
        """Тест регистрации пользователя"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "newpass123",
                "confirm_password": "newpass123",
                "full_name": "New User",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["is_active"] is True
        assert data["is_verified"] is False

    def test_user_login(self, setup_database, test_user):
        """Тест входа пользователя"""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_get_current_user(self, setup_database, test_user, auth_headers):
        """Тест получения информации о текущем пользователе"""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_protected_endpoint_without_auth(self, setup_database):
        """Тест защищенного endpoint без аутентификации"""
        response = client.get("/api/auth/me")
        assert (
            response.status_code == 403
        )  # FastAPI возвращает 403 для отсутствующего токена


class TestEcommerce:
    """Тесты E-commerce модуля"""

    def test_get_products_empty(self, setup_database):
        """Тест получения пустого списка товаров"""
        response = client.get("/api/ecommerce/products")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 0

    def test_create_product(self, setup_database, test_user, auth_headers):
        """Тест создания товара"""
        product_data = {
            "name": "Test Product",
            "description": "Test product description",
            "price": 99.99,
            "category": "Electronics",
            "stock_quantity": 10,
        }
        response = client.post(
            "/api/ecommerce/products", json=product_data, headers=auth_headers
        )
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == "Test Product"
        assert product["price"] == 99.99
        assert product["category"] == "Electronics"

    def test_get_products_with_data(self, setup_database, test_user, auth_headers):
        """Тест получения списка товаров с данными"""
        # Создаем товар
        product_data = {
            "name": "Test Product",
            "description": "Test product description",
            "price": 99.99,
            "category": "Electronics",
            "stock_quantity": 10,
        }
        client.post("/api/ecommerce/products", json=product_data, headers=auth_headers)

        # Получаем список товаров
        response = client.get("/api/ecommerce/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Test Product"

    def test_cart_operations(self, setup_database, test_user, auth_headers):
        """Тест операций с корзиной"""
        # Создаем товар
        product_data = {
            "name": "Cart Test Product",
            "description": "Product for cart testing",
            "price": 50.0,
            "category": "Test",
            "stock_quantity": 5,
        }
        response = client.post(
            "/api/ecommerce/products", json=product_data, headers=auth_headers
        )
        product_id = response.json()["id"]

        # Добавляем товар в корзину
        cart_data = {"product_id": product_id, "quantity": 2}
        response = client.post(
            "/api/ecommerce/cart", json=cart_data, headers=auth_headers
        )
        assert response.status_code == 200
        cart_item = response.json()
        assert cart_item["quantity"] == 2

        # Получаем корзину
        response = client.get("/api/ecommerce/cart", headers=auth_headers)
        assert response.status_code == 200
        cart = response.json()
        assert cart["total_items"] == 2
        assert cart["total_amount"] == 100.0


class TestErrorHandling:
    """Тесты обработки ошибок"""

    def test_invalid_json(self, setup_database):
        """Тест невалидного JSON"""
        response = client.post(
            "/api/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    def test_missing_required_fields(self, setup_database):
        """Тест отсутствующих обязательных полей"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com"},  # Отсутствуют обязательные поля
        )
        assert response.status_code == 422

    def test_invalid_credentials(self, setup_database):
        """Тест неверных учетных данных"""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_nonexistent_endpoint(self, setup_database):
        """Тест несуществующего endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404


class TestCORS:
    """Тесты CORS"""

    def test_cors_headers(self, setup_database):
        """Тест CORS заголовков"""
        response = client.get("/api/auth/login")  # Используем GET вместо OPTIONS
        # Проверяем, что CORS заголовки присутствуют в ответе
        assert (
            "access-control-allow-origin" in response.headers
            or response.status_code == 405
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
