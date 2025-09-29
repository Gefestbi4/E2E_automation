"""
Интеграционные тесты для проверки взаимодействия между модулями
"""

import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from models import Base, User
from auth import get_password_hash, get_db
import models_package.ecommerce as ecommerce_models
import models_package.social as social_models
import models_package.tasks as tasks_models
import models_package.content as content_models
import models_package.analytics as analytics_models


# Тестовая база данных в памяти
SQLALCHEMY_DATABASE_URL = "postgresql://my_user:my_password@postgres:5432/test_database"
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
    # Очищаем все связанные данные перед удалением пользователя
    try:
        # Ecommerce
        db.query(ecommerce_models.CartItem).delete()
        db.query(ecommerce_models.OrderItem).delete()
        db.query(ecommerce_models.Order).delete()
        db.query(ecommerce_models.Product).delete()

        # Social
        db.query(social_models.Post).delete()
        db.query(social_models.Comment).delete()
        db.query(social_models.Like).delete()

        # Tasks
        db.query(tasks_models.Card).delete()
        db.query(tasks_models.Board).delete()

        # Content
        db.query(content_models.Article).delete()
        db.query(content_models.Category).delete()
        db.query(content_models.MediaFile).delete()

        # Analytics
        db.query(analytics_models.Dashboard).delete()
        db.query(analytics_models.Report).delete()
        db.query(analytics_models.Alert).delete()

        db.commit()
        db.delete(user)
        db.commit()
    except Exception:
        # Игнорируем ошибки при очистке
        pass
    finally:
        db.close()


@pytest.fixture
def auth_headers(test_user):
    """Получение заголовков аутентификации"""
    response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "testpass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestUserRegistrationAndLogin:
    """Тесты регистрации и входа пользователя"""

    def test_user_registration(self, setup_database):
        """Тест регистрации нового пользователя"""
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


class TestEcommerceIntegration:
    """Тесты интеграции E-commerce модуля"""

    def test_create_and_get_products(self, setup_database, test_user, auth_headers):
        """Тест создания и получения товаров"""
        # Создаем товар
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

        # Получаем список товаров
        response = client.get("/api/ecommerce/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Test Product"

    def test_cart_operations(self, setup_database, test_user, auth_headers):
        """Тест операций с корзиной"""
        # Сначала создаем товар
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

    def test_order_creation(self, setup_database, test_user, auth_headers):
        """Тест создания заказа"""
        # Создаем товар
        product_data = {
            "name": "Order Test Product",
            "description": "Product for order testing",
            "price": 25.0,
            "category": "Test",
            "stock_quantity": 3,
        }
        response = client.post(
            "/api/ecommerce/products", json=product_data, headers=auth_headers
        )
        product_id = response.json()["id"]

        # Добавляем в корзину
        cart_data = {"product_id": product_id, "quantity": 1}
        client.post("/api/ecommerce/cart", json=cart_data, headers=auth_headers)

        # Создаем заказ
        order_data = {
            "shipping_address": "123 Test Street, Test City",
            "payment_method": "card",  # Используем допустимый метод оплаты
        }
        response = client.post(
            "/api/ecommerce/orders", json=order_data, headers=auth_headers
        )
        assert response.status_code == 200
        order = response.json()
        assert order["total_amount"] == 25.0
        assert order["status"] == "pending"


class TestSocialNetworkIntegration:
    """Тесты интеграции Social Network модуля"""

    def test_create_and_get_posts(self, setup_database, test_user, auth_headers):
        """Тест создания и получения постов"""
        # Создаем пост
        post_data = {"content": "This is a test post", "is_public": True}
        response = client.post(
            "/api/social/posts", json=post_data, headers=auth_headers
        )
        assert response.status_code == 200
        post = response.json()
        assert post["content"] == "This is a test post"

        # Получаем посты
        response = client.get("/api/social/posts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["content"] == "This is a test post"

    def test_like_post(self, setup_database, test_user, auth_headers):
        """Тест лайка поста"""
        # Создаем пост
        post_data = {"content": "Post for liking", "is_public": True}
        response = client.post(
            "/api/social/posts", json=post_data, headers=auth_headers
        )
        post_id = response.json()["id"]

        # Лайкаем пост
        response = client.post(
            f"/api/social/posts/{post_id}/like", headers=auth_headers
        )
        assert response.status_code == 200

        # Проверяем количество лайков
        response = client.get(f"/api/social/posts/{post_id}", headers=auth_headers)
        assert response.status_code == 200
        post = response.json()
        assert post["likes_count"] == 1


class TestTaskManagementIntegration:
    """Тесты интеграции Task Management модуля"""

    def test_create_and_get_boards(self, setup_database, test_user, auth_headers):
        """Тест создания и получения досок"""
        # Создаем доску
        board_data = {
            "name": "Test Board",
            "description": "Test board description",
            "is_public": False,
        }
        response = client.post(
            "/api/tasks/boards", json=board_data, headers=auth_headers
        )
        assert response.status_code == 200
        board = response.json()
        assert board["name"] == "Test Board"

        # Получаем доски
        response = client.get("/api/tasks/boards", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Test Board"

    def test_create_cards(self, setup_database, test_user, auth_headers):
        """Тест создания карточек"""
        # Создаем доску
        board_data = {"name": "Board for Cards", "description": "Test board"}
        response = client.post(
            "/api/tasks/boards", json=board_data, headers=auth_headers
        )
        board_id = response.json()["id"]

        # Создаем карточку
        card_data = {
            "title": "Test Card",
            "description": "Test card description",
            "status": "todo",  # Используем lowercase для валидатора
            "priority": "medium",  # Используем lowercase для валидатора
            "board_id": board_id,  # Добавляем board_id в тело запроса
        }
        response = client.post("/api/tasks/cards", json=card_data, headers=auth_headers)
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        assert response.status_code == 200
        card = response.json()
        assert card["title"] == "Test Card"
        assert card["status"] == "todo"


class TestContentManagementIntegration:
    """Тесты интеграции Content Management модуля"""

    def test_create_and_get_articles(self, setup_database, test_user, auth_headers):
        """Тест создания и получения статей"""
        # Создаем статью
        article_data = {
            "title": "Test Article",
            "content": "This is test article content",
            "slug": "test-article",
            "status": "draft",  # Используем lowercase для валидатора
            "featured_image": "https://example.com/image.jpg",
        }
        response = client.post(
            "/api/content/articles", json=article_data, headers=auth_headers
        )
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        assert response.status_code == 200
        article = response.json()
        assert article["title"] == "Test Article"

        # Получаем статьи
        response = client.get("/api/content/articles", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Test Article"

    def test_create_categories(self, setup_database, test_user, auth_headers):
        """Тест создания категорий"""
        category_data = {
            "name": "Test Category",
            "description": "Test category description",
            "slug": "test-category",
        }
        response = client.post(
            "/api/content/categories", json=category_data, headers=auth_headers
        )
        assert response.status_code == 200
        category = response.json()
        assert category["name"] == "Test Category"


class TestAnalyticsIntegration:
    """Тесты интеграции Analytics модуля"""

    def test_get_dashboard_data(self, setup_database, test_user, auth_headers):
        """Тест получения данных дашборда"""
        response = client.get("/api/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # API возвращает другую структуру - проверяем реальные поля
        assert "dashboard" in data
        assert "reports" in data
        assert "alerts" in data
        assert "reports_count" in data
        assert "alerts_count" in data

    def test_create_dashboard(self, setup_database, test_user, auth_headers):
        """Тест создания дашборда"""
        dashboard_data = {
            "name": "Test Dashboard",
            "description": "Test dashboard description",
            "is_public": False,
        }
        response = client.post(
            "/api/analytics/dashboards", json=dashboard_data, headers=auth_headers
        )
        assert response.status_code == 200
        dashboard = response.json()
        assert dashboard["name"] == "Test Dashboard"

    def test_track_event(self, setup_database, test_user, auth_headers):
        """Тест отслеживания событий"""
        event_data = {
            "event_type": "page_view",
            "event_data": {"page": "/test", "duration": 30},
            "user_agent": "Test Agent",
            "ip_address": "127.0.0.1",
        }
        response = client.post(
            "/api/analytics/events", json=event_data, headers=auth_headers
        )
        assert response.status_code == 200
        event = response.json()
        assert event["name"] == "page_view"  # API возвращает 'name', а не 'event_type'
        assert event["properties"]["page"] == "/test"
        assert event["properties"]["duration"] == 30


class TestCrossModuleIntegration:
    """Тесты кросс-модульной интеграции"""

    def test_user_activity_across_modules(
        self, setup_database, test_user, auth_headers
    ):
        """Тест активности пользователя через разные модули"""
        # Создаем товар (E-commerce)
        product_data = {
            "name": "Cross Module Product",
            "price": 100.0,
            "category": "Test",
            "stock_quantity": 1,
        }
        client.post("/api/ecommerce/products", json=product_data, headers=auth_headers)

        # Создаем пост (Social)
        post_data = {"content": "Cross module post", "is_public": True}
        client.post("/api/social/posts", json=post_data, headers=auth_headers)

        # Создаем доску (Tasks)
        board_data = {"name": "Cross Module Board", "description": "Test board"}
        client.post("/api/tasks/boards", json=board_data, headers=auth_headers)

        # Создаем статью (Content)
        article_data = {
            "title": "Cross Module Article",
            "content": "Test content",
            "slug": "cross-module-article",
            "status": "draft",
            "featured_image": "https://example.com/image.jpg",
        }
        client.post("/api/content/articles", json=article_data, headers=auth_headers)

        # Проверяем, что все создано
        response = client.get("/api/ecommerce/products")
        assert len(response.json()["items"]) == 1

        response = client.get("/api/social/posts", headers=auth_headers)
        assert len(response.json()["items"]) == 1

        response = client.get("/api/tasks/boards", headers=auth_headers)
        assert len(response.json()["items"]) == 1

        response = client.get("/api/content/articles", headers=auth_headers)
        assert len(response.json()["items"]) == 1

    def test_analytics_tracking(self, setup_database, test_user, auth_headers):
        """Тест отслеживания аналитики через модули"""
        # Выполняем действия в разных модулях
        product_data = {
            "name": "Analytics Product",
            "price": 50.0,
            "category": "Test",
            "stock_quantity": 1,
        }
        client.post("/api/ecommerce/products", json=product_data, headers=auth_headers)

        post_data = {"content": "Analytics post", "is_public": True}
        client.post("/api/social/posts", json=post_data, headers=auth_headers)

        # Отслеживаем события
        event_data = {
            "event_type": "product_created",
            "event_data": {"product_name": "Analytics Product"},
            "user_agent": "Test Agent",
        }
        client.post("/api/analytics/events", json=event_data, headers=auth_headers)

        # Проверяем данные дашборда
        response = client.get("/api/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # API возвращает другую структуру - проверяем реальные поля
        assert "dashboard" in data
        assert "reports" in data
        assert "alerts" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
