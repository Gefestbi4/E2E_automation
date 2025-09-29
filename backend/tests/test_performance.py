"""
Тесты производительности API
"""

import pytest
import time
import asyncio
import aiohttp
import json
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from models import Base, User
from auth import get_password_hash, get_db


# Тестовая база данных
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


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module")
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
        email="perf@example.com",
        username="perfuser",
        full_name="Performance User",
        hashed_password=get_password_hash("perfpass123"),
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()


@pytest.fixture
def auth_headers(test_user):
    """Получение заголовков аутентификации"""
    response = client.post(
        "/api/auth/login", json={"email": "perf@example.com", "password": "perfpass123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestAPIPerformance:
    """Тесты производительности API"""

    def test_basic_endpoint_performance(self, setup_database):
        """Тест производительности базовых endpoints"""
        # Тест главного endpoint
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()

        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000  # в миллисекундах
        assert response_time < 100  # Должен отвечать менее чем за 100ms
        print(f"GET / response time: {response_time:.2f}ms")

    def test_auth_performance(self, setup_database, test_user):
        """Тест производительности аутентификации"""
        # Тест логина
        start_time = time.time()
        response = client.post(
            "/api/auth/login",
            json={"email": "perf@example.com", "password": "perfpass123"},
        )
        end_time = time.time()

        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000
        assert response_time < 500  # Логин должен быть быстрым
        print(f"Login response time: {response_time:.2f}ms")

    def test_database_query_performance(self, setup_database, test_user, auth_headers):
        """Тест производительности запросов к БД"""
        # Создаем несколько товаров для тестирования
        products_data = [
            {
                "name": f"Product {i}",
                "description": f"Description for product {i}",
                "price": 10.0 + i,
                "category": "Test",
                "stock_quantity": 10,
            }
            for i in range(10)
        ]

        for product_data in products_data:
            client.post(
                "/api/ecommerce/products", json=product_data, headers=auth_headers
            )

        # Тест получения списка товаров
        start_time = time.time()
        response = client.get("/api/ecommerce/products")
        end_time = time.time()

        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000
        assert response_time < 200  # Список товаров должен загружаться быстро
        print(f"Products list response time: {response_time:.2f}ms")

    def test_concurrent_requests(self, setup_database, test_user, auth_headers):
        """Тест производительности при одновременных запросах"""

        def make_request():
            """Функция для выполнения запроса"""
            response = client.get("/api/ecommerce/products")
            return response.status_code == 200

        # Выполняем 10 одновременных запросов
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        end_time = time.time()

        # Все запросы должны быть успешными
        assert all(results)
        total_time = (end_time - start_time) * 1000
        print(f"10 concurrent requests completed in: {total_time:.2f}ms")
        assert (
            total_time < 1000
        )  # Все запросы должны завершиться менее чем за 1 секунду

    def test_large_data_handling(self, setup_database, test_user, auth_headers):
        """Тест обработки больших объемов данных"""
        # Создаем много товаров
        products_data = [
            {
                "name": f"Bulk Product {i}",
                "description": f"Description for bulk product {i}",
                "price": 1.0 + (i % 100),
                "category": f"Category {i % 5}",
                "stock_quantity": 1,
            }
            for i in range(100)
        ]

        # Создаем товары
        start_time = time.time()
        for product_data in products_data:
            response = client.post(
                "/api/ecommerce/products", json=product_data, headers=auth_headers
            )
            assert response.status_code == 200
        creation_time = (time.time() - start_time) * 1000
        print(f"Created 100 products in: {creation_time:.2f}ms")

        # Тест получения всех товаров с пагинацией
        start_time = time.time()
        response = client.get("/api/ecommerce/products?limit=50")
        end_time = time.time()

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 50
        response_time = (end_time - start_time) * 1000
        print(f"Retrieved 50 products in: {response_time:.2f}ms")
        assert response_time < 500

    def test_memory_usage(self, setup_database, test_user, auth_headers):
        """Тест использования памяти"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Создаем много данных
        for i in range(50):
            product_data = {
                "name": f"Memory Test Product {i}",
                "description": "x" * 1000,  # Большое описание
                "price": 10.0,
                "category": "Memory Test",
                "stock_quantity": 1,
            }
            client.post(
                "/api/ecommerce/products", json=product_data, headers=auth_headers
            )

        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = current_memory - initial_memory

        print(f"Memory usage increased by: {memory_increase:.2f}MB")
        assert memory_increase < 50  # Увеличение памяти не должно быть критическим

    def test_response_size_limits(self, setup_database, test_user, auth_headers):
        """Тест ограничений размера ответа"""
        # Создаем товар с большим описанием
        large_description = "x" * 10000  # 10KB описание
        product_data = {
            "name": "Large Product",
            "description": large_description,
            "price": 100.0,
            "category": "Large",
            "stock_quantity": 1,
        }

        response = client.post(
            "/api/ecommerce/products", json=product_data, headers=auth_headers
        )
        assert response.status_code == 200

        # Получаем товар
        response = client.get(f"/api/ecommerce/products/{response.json()['id']}")
        assert response.status_code == 200

        # Проверяем, что ответ не слишком большой
        response_size = len(response.content)
        print(f"Response size: {response_size} bytes")
        assert response_size < 50000  # Ответ не должен быть больше 50KB

    def test_error_handling_performance(self, setup_database, test_user, auth_headers):
        """Тест производительности обработки ошибок"""
        # Тест несуществующего товара
        start_time = time.time()
        response = client.get("/api/ecommerce/products/99999")
        end_time = time.time()

        assert response.status_code == 404
        error_response_time = (end_time - start_time) * 1000
        print(f"404 error response time: {error_response_time:.2f}ms")
        assert error_response_time < 200  # Ошибки должны обрабатываться быстро

        # Тест невалидных данных
        start_time = time.time()
        response = client.post(
            "/api/ecommerce/products", json={"invalid": "data"}, headers=auth_headers
        )
        end_time = time.time()

        assert response.status_code == 422
        validation_time = (end_time - start_time) * 1000
        print(f"Validation error response time: {validation_time:.2f}ms")
        assert validation_time < 200

    def test_caching_performance(self, setup_database, test_user, auth_headers):
        """Тест производительности кэширования (если реализовано)"""
        # Первый запрос
        start_time = time.time()
        response1 = client.get("/api/ecommerce/products")
        first_time = (time.time() - start_time) * 1000

        # Второй запрос (должен быть быстрее, если есть кэш)
        start_time = time.time()
        response2 = client.get("/api/ecommerce/products")
        second_time = (time.time() - start_time) * 1000

        assert response1.status_code == 200
        assert response2.status_code == 200

        print(f"First request: {first_time:.2f}ms")
        print(f"Second request: {second_time:.2f}ms")

        # Второй запрос может быть быстрее из-за кэширования
        # но не обязательно, так как кэш может быть не реализован


class TestDatabasePerformance:
    """Тесты производительности базы данных"""

    def test_database_connection_pool(self, setup_database):
        """Тест пула соединений с БД"""
        # Тест множественных соединений
        start_time = time.time()

        def db_operation():
            db = TestingSessionLocal()
            try:
                users = db.query(User).all()
                return len(users)
            finally:
                db.close()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(db_operation) for _ in range(10)]
            results = [future.result() for future in futures]

        end_time = time.time()
        total_time = (end_time - start_time) * 1000

        print(f"10 database operations completed in: {total_time:.2f}ms")
        assert all(result >= 0 for result in results)  # Все операции успешны
        assert total_time < 1000  # Операции должны быть быстрыми

    def test_query_optimization(self, setup_database, test_user, auth_headers):
        """Тест оптимизации запросов"""
        # Создаем данные для тестирования
        for i in range(20):
            product_data = {
                "name": f"Query Test Product {i}",
                "description": f"Description {i}",
                "price": 10.0 + i,
                "category": f"Category {i % 3}",
                "stock_quantity": 5,
            }
            client.post(
                "/api/ecommerce/products", json=product_data, headers=auth_headers
            )

        # Тест запроса с фильтрацией
        start_time = time.time()
        response = client.get("/api/ecommerce/products?category=Category 0&limit=10")
        end_time = time.time()

        assert response.status_code == 200
        filtered_time = (end_time - start_time) * 1000
        print(f"Filtered query time: {filtered_time:.2f}ms")
        assert filtered_time < 300

        # Тест запроса с поиском
        start_time = time.time()
        response = client.get("/api/ecommerce/products?search=Query Test&limit=10")
        end_time = time.time()

        assert response.status_code == 200
        search_time = (end_time - start_time) * 1000
        print(f"Search query time: {search_time:.2f}ms")
        assert search_time < 300


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
