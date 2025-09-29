#!/usr/bin/env python3
"""
Скрипт инициализации базы данных
Создает необходимые базы данных, enum'ы и тестовые данные
"""

import os
import sys
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к backend в PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

from models import Base, User
from security import get_password_hash
import models_package.ecommerce
import models_package.social
import models_package.tasks
import models_package.content
import models_package.analytics


def wait_for_postgres(max_retries=30, delay=2):
    """Ждем пока PostgreSQL станет доступен"""
    print("⏳ Ожидание подключения к PostgreSQL...")

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "postgres"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                user=os.getenv("POSTGRES_USER", "my_user"),
                password=os.getenv("POSTGRES_PASSWORD", "my_password"),
                database=os.getenv("POSTGRES_DB", "my_database"),
            )
            conn.close()
            print("✅ PostgreSQL подключен!")
            return True
        except psycopg2.OperationalError:
            if attempt < max_retries - 1:
                print(
                    f"⏳ Попытка {attempt + 1}/{max_retries} - PostgreSQL еще не готов, ждем {delay}с..."
                )
                time.sleep(delay)
            else:
                print("❌ Не удалось подключиться к PostgreSQL")
                return False
    return False


def create_databases():
    """Создаем необходимые базы данных"""
    print("🗄️ Создание баз данных...")

    try:
        # Подключаемся к основной базе данных
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER", "my_user"),
            password=os.getenv("POSTGRES_PASSWORD", "my_password"),
            database=os.getenv("POSTGRES_DB", "my_database"),
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Создаем тестовую базу данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'test_database'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE test_database")
            print("✅ Создана база данных test_database")
        else:
            print("ℹ️ База данных test_database уже существует")

        cursor.close()
        conn.close()

        # Создаем enum'ы в основной базе
        create_enums("my_database")

        # Создаем enum'ы в тестовой базе
        create_enums("test_database")

        return True

    except Exception as e:
        print(f"❌ Ошибка при создании баз данных: {e}")
        return False


def create_enums(database_name):
    """Создаем enum'ы в указанной базе данных"""
    print(f"🔧 Создание enum'ов в базе {database_name}...")

    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER", "my_user"),
            password=os.getenv("POSTGRES_PASSWORD", "my_password"),
            database=database_name,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Создаем enum'ы если они не существуют
        enums = [
            ("taskstatus", "('todo', 'in_progress', 'review', 'done')"),
            ("taskpriority", "('low', 'medium', 'high', 'urgent')"),
            ("articlestatus", "('draft', 'published', 'archived')"),
        ]

        for enum_name, enum_values in enums:
            # Проверяем, существует ли enum
            cursor.execute("SELECT 1 FROM pg_type WHERE typname = %s", (enum_name,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE TYPE {enum_name} AS ENUM {enum_values}")
                print(f"✅ Создан enum {enum_name}")
            else:
                print(f"ℹ️ Enum {enum_name} уже существует")

        print(f"✅ Enum'ы созданы в базе {database_name}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании enum'ов в {database_name}: {e}")
        return False


def create_tables(database_url):
    """Создаем таблицы в базе данных"""
    print(f"📋 Создание таблиц в базе данных...")

    try:
        engine = create_engine(database_url)
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False


def create_test_data(database_url):
    """Создаем тестовые данные"""
    print("👤 Создание тестовых данных...")

    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Проверяем, есть ли уже пользователь
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if not existing_user:
            # Создаем тестового пользователя
            test_user = User(
                email="test@example.com",
                username="testuser",
                full_name="Test User",
                hashed_password=get_password_hash("testpassword123"),
                is_active=True,
                is_verified=True,
            )
            db.add(test_user)
            db.commit()
            print("✅ Создан тестовый пользователь: test@example.com")
        else:
            print("ℹ️ Тестовый пользователь уже существует")
            test_user = existing_user

        # Создаем тестовые данные для E-commerce
        create_ecommerce_test_data(db, test_user)

        # Создаем тестовые данные для Social Network
        create_social_test_data(db, test_user)

        # Создаем тестовые данные для Task Management
        create_tasks_test_data(db, test_user)

        # Создаем тестовые данные для Content Management
        create_content_test_data(db, test_user)

        # Создаем тестовые данные для Analytics
        create_analytics_test_data(db, test_user)

        db.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        return False


def create_ecommerce_test_data(db, user):
    """Создаем тестовые данные для E-commerce"""
    print("🛒 Создание тестовых данных E-commerce...")

    from models_package.ecommerce import Product, Order, OrderItem

    # Создаем товары
    products_data = [
        {
            "name": "Laptop Pro 15",
            "description": "High-performance laptop for professionals",
            "price": 1299.99,
            "category": "Electronics",
            "image_url": "https://via.placeholder.com/300x200?text=Laptop+Pro+15",
            "stock_quantity": 10,
        },
        {
            "name": "Wireless Headphones",
            "description": "Premium wireless headphones with noise cancellation",
            "price": 199.99,
            "category": "Audio",
            "image_url": "https://via.placeholder.com/300x200?text=Headphones",
            "stock_quantity": 25,
        },
        {
            "name": "Smartphone X",
            "description": "Latest smartphone with advanced features",
            "price": 899.99,
            "category": "Electronics",
            "image_url": "https://via.placeholder.com/300x200?text=Smartphone+X",
            "stock_quantity": 15,
        },
        {
            "name": "Coffee Maker",
            "description": "Automatic coffee maker for home use",
            "price": 149.99,
            "category": "Appliances",
            "image_url": "https://via.placeholder.com/300x200?text=Coffee+Maker",
            "stock_quantity": 8,
        },
        {
            "name": "Running Shoes",
            "description": "Comfortable running shoes for athletes",
            "price": 129.99,
            "category": "Sports",
            "image_url": "https://via.placeholder.com/300x200?text=Running+Shoes",
            "stock_quantity": 20,
        },
    ]

    for product_data in products_data:
        existing_product = (
            db.query(Product).filter(Product.name == product_data["name"]).first()
        )
        if not existing_product:
            product = Product(**product_data)
            db.add(product)

    db.commit()
    print("✅ Созданы тестовые товары")


def create_social_test_data(db, user):
    """Создаем тестовые данные для Social Network"""
    print("👥 Создание тестовых данных Social Network...")

    from models_package.social import Post, Comment, PostLike

    # Создаем посты
    posts_data = [
        {
            "content": "Привет всем! Добро пожаловать в нашу социальную сеть! 🎉",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "content": "Только что закончил работу над новым проектом. Очень доволен результатом! 💪",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "content": "Кто-нибудь знает хорошие курсы по автоматизации тестирования? 🤔",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "content": "Сегодня отличная погода для прогулки! ☀️",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "content": "Поделитесь опытом работы с Selenium WebDriver, пожалуйста! 🚀",
            "user_id": user.id,
            "is_public": True,
        },
    ]

    for post_data in posts_data:
        existing_post = (
            db.query(Post).filter(Post.content == post_data["content"]).first()
        )
        if not existing_post:
            post = Post(**post_data)
            db.add(post)

    db.commit()
    print("✅ Созданы тестовые посты")


def create_tasks_test_data(db, user):
    """Создаем тестовые данные для Task Management"""
    print("📋 Создание тестовых данных Task Management...")

    from models_package.tasks import Board, Card, TaskStatus, TaskPriority

    # Создаем доски
    boards_data = [
        {
            "name": "Веб-приложение для тестирования",
            "description": "Разработка полноценного веб-приложения для обучения автоматизаторов",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "name": "Документация API",
            "description": "Создание подробной документации для всех API эндпоинтов",
            "user_id": user.id,
            "is_public": True,
        },
        {
            "name": "Тестирование производительности",
            "description": "Проведение нагрузочного тестирования системы",
            "user_id": user.id,
            "is_public": True,
        },
    ]

    for board_data in boards_data:
        existing_board = (
            db.query(Board).filter(Board.name == board_data["name"]).first()
        )
        if not existing_board:
            board = Board(**board_data)
            db.add(board)
            db.flush()  # Получаем ID доски

            # Создаем карточки для доски
            cards_data = [
                {
                    "title": f"Задача 1 для {board.name}",
                    "description": f"Описание первой задачи доски {board.name}",
                    "board_id": board.id,
                    "assigned_to_id": user.id,
                    "status": "todo",
                    "priority": "high",
                },
                {
                    "title": f"Задача 2 для {board.name}",
                    "description": f"Описание второй задачи доски {board.name}",
                    "board_id": board.id,
                    "assigned_to_id": user.id,
                    "status": "in_progress",
                    "priority": "medium",
                },
                {
                    "title": f"Задача 3 для {board.name}",
                    "description": f"Описание третьей задачи доски {board.name}",
                    "board_id": board.id,
                    "assigned_to_id": user.id,
                    "status": "done",
                    "priority": "low",
                },
            ]

            for card_data in cards_data:
                existing_card = (
                    db.query(Card).filter(Card.title == card_data["title"]).first()
                )
                if not existing_card:
                    card = Card(**card_data)
                    db.add(card)

    db.commit()
    print("✅ Созданы тестовые доски и карточки")


def create_content_test_data(db, user):
    """Создаем тестовые данные для Content Management"""
    print("📝 Создание тестовых данных Content Management...")

    from models_package.content import Article, Category

    # Создаем категории
    categories_data = [
        {
            "name": "Технологии",
            "description": "Статьи о современных технологиях",
            "slug": "tehnologii",
        },
        {
            "name": "Тестирование",
            "description": "Материалы по автоматизации тестирования",
            "slug": "testirovanie",
        },
        {
            "name": "Программирование",
            "description": "Статьи о программировании и разработке",
            "slug": "programmirovanie",
        },
        {
            "name": "Обучение",
            "description": "Обучающие материалы и руководства",
            "slug": "obuchenie",
        },
    ]

    for category_data in categories_data:
        existing_category = (
            db.query(Category).filter(Category.name == category_data["name"]).first()
        )
        if not existing_category:
            category = Category(**category_data)
            db.add(category)

    db.flush()  # Получаем ID категорий

    # Получаем ID категорий для ссылок в статьях
    tech_category = db.query(Category).filter(Category.name == "Технологии").first()
    testing_category = (
        db.query(Category).filter(Category.name == "Тестирование").first()
    )
    programming_category = (
        db.query(Category).filter(Category.name == "Программирование").first()
    )

    # Создаем статьи
    articles_data = [
        {
            "title": "Введение в автоматизацию тестирования",
            "content": "Автоматизация тестирования - это процесс использования специальных инструментов для выполнения тестов без участия человека...",
            "author_id": user.id,
            "category_id": testing_category.id,
            "status": "published",
            "slug": "vvedenie-v-avtomatizaciyu-testirovaniya",
            "views_count": 150,
        },
        {
            "title": "Selenium WebDriver: основы работы",
            "content": "Selenium WebDriver - это мощный инструмент для автоматизации веб-приложений...",
            "author_id": user.id,
            "category_id": testing_category.id,
            "status": "published",
            "slug": "selenium-webdriver-osnovy-raboty",
            "views_count": 89,
        },
        {
            "title": "Современные подходы к тестированию API",
            "content": "Тестирование API является важной частью процесса разработки...",
            "author_id": user.id,
            "category_id": testing_category.id,
            "status": "published",
            "slug": "sovremennye-podhody-k-testirovaniyu-api",
            "views_count": 67,
        },
        {
            "title": "Python для автоматизации тестирования",
            "content": "Python - один из самых популярных языков для автоматизации тестирования...",
            "author_id": user.id,
            "category_id": programming_category.id,
            "status": "published",
            "slug": "python-dlya-avtomatizacii-testirovaniya",
            "views_count": 203,
        },
        {
            "title": "Docker в тестировании: лучшие практики",
            "content": "Использование Docker в тестировании позволяет создавать изолированные среды...",
            "author_id": user.id,
            "category_id": tech_category.id,
            "status": "published",
            "slug": "docker-v-testirovanii-luchshie-praktiki",
            "views_count": 134,
        },
    ]

    for article_data in articles_data:
        existing_article = (
            db.query(Article).filter(Article.title == article_data["title"]).first()
        )
        if not existing_article:
            article = Article(**article_data)
            db.add(article)

    db.commit()
    print("✅ Созданы тестовые статьи и категории")


def create_analytics_test_data(db, user):
    """Создаем тестовые данные для Analytics"""
    print("📊 Создание тестовых данных Analytics...")

    from models_package.analytics import (
        Metric,
        MetricData,
        Report,
        Dashboard,
        DashboardWidget,
    )

    # Создаем метрики
    metrics_data = [
        {
            "name": "page_views",
            "description": "Общее количество просмотров страниц",
            "metric_type": "counter",
            "unit": "views",
        },
        {
            "name": "unique_users",
            "description": "Количество уникальных пользователей",
            "metric_type": "gauge",
            "unit": "users",
        },
        {
            "name": "orders_count",
            "description": "Количество заказов",
            "metric_type": "counter",
            "unit": "orders",
        },
        {
            "name": "revenue",
            "description": "Общая выручка",
            "metric_type": "gauge",
            "unit": "currency",
        },
        {
            "name": "posts_count",
            "description": "Количество постов в социальной сети",
            "metric_type": "counter",
            "unit": "posts",
        },
        {
            "name": "tasks_completed",
            "description": "Количество выполненных задач",
            "metric_type": "counter",
            "unit": "tasks",
        },
    ]

    created_metrics = []
    for metric_data in metrics_data:
        existing_metric = (
            db.query(Metric).filter(Metric.name == metric_data["name"]).first()
        )
        if not existing_metric:
            metric = Metric(**metric_data)
            db.add(metric)
            created_metrics.append(metric)
        else:
            created_metrics.append(existing_metric)

    db.flush()  # Получаем ID метрик

    # Создаем данные для метрик
    metric_values = [
        {
            "metric": created_metrics[0],
            "value": 1250.0,
            "labels": {"page": "dashboard"},
        },
        {"metric": created_metrics[1], "value": 89.0, "labels": {"period": "daily"}},
        {
            "metric": created_metrics[2],
            "value": 456.0,
            "labels": {"status": "completed"},
        },
        {
            "metric": created_metrics[3],
            "value": 125000.0,
            "labels": {"currency": "USD"},
        },
        {"metric": created_metrics[4], "value": 234.0, "labels": {"type": "public"}},
        {"metric": created_metrics[5], "value": 156.0, "labels": {"priority": "high"}},
    ]

    for value_data in metric_values:
        metric_data = MetricData(
            metric_id=value_data["metric"].id,
            value=value_data["value"],
            labels=value_data["labels"],
        )
        db.add(metric_data)

    # Создаем отчет
    report = Report(
        name="Еженедельный отчет",
        description="Сводка по основным метрикам за неделю",
        report_type="weekly_summary",
        parameters={
            "period": "7d",
            "metrics": ["page_views", "unique_users", "revenue"],
        },
        created_by_id=user.id,
        is_public=True,
    )
    db.add(report)

    # Создаем дашборд
    dashboard = Dashboard(
        name="Основной дашборд",
        description="Главный дашборд с ключевыми метриками",
        created_by_id=user.id,
        is_public=True,
        layout_config={"columns": 4, "rows": 3},
    )
    db.add(dashboard)
    db.flush()  # Получаем ID дашборда

    # Создаем виджеты для дашборда
    widgets_data = [
        {
            "widget_type": "metric_card",
            "title": "Просмотры страниц",
            "config": {"metric_id": created_metrics[0].id, "format": "number"},
            "position_x": 0,
            "position_y": 0,
            "width": 2,
            "height": 1,
        },
        {
            "widget_type": "metric_card",
            "title": "Уникальные пользователи",
            "config": {"metric_id": created_metrics[1].id, "format": "number"},
            "position_x": 2,
            "position_y": 0,
            "width": 2,
            "height": 1,
        },
        {
            "widget_type": "chart",
            "title": "Выручка по дням",
            "config": {"metric_id": created_metrics[3].id, "chart_type": "line"},
            "position_x": 0,
            "position_y": 1,
            "width": 4,
            "height": 2,
        },
    ]

    for widget_data in widgets_data:
        widget = DashboardWidget(dashboard_id=dashboard.id, **widget_data)
        db.add(widget)

    db.commit()
    print("✅ Созданы тестовые метрики, отчеты и дашборды")


def main():
    """Основная функция инициализации"""
    print("🚀 Начинаем инициализацию базы данных...")

    # Ждем PostgreSQL
    if not wait_for_postgres():
        sys.exit(1)

    # Создаем базы данных и enum'ы
    if not create_databases():
        sys.exit(1)

    # Создаем таблицы в основной базе
    main_db_url = f"postgresql://{os.getenv('POSTGRES_USER', 'my_user')}:{os.getenv('POSTGRES_PASSWORD', 'my_password')}@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'my_database')}"
    if not create_tables(main_db_url):
        sys.exit(1)

    # Создаем тестовые данные в основной базе
    if not create_test_data(main_db_url):
        sys.exit(1)

    # Создаем таблицы в тестовой базе
    test_db_url = f"postgresql://{os.getenv('POSTGRES_USER', 'my_user')}:{os.getenv('POSTGRES_PASSWORD', 'my_password')}@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}/test_database"
    if not create_tables(test_db_url):
        sys.exit(1)

    print("🎉 Инициализация базы данных завершена успешно!")


if __name__ == "__main__":
    main()
