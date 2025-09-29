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

        db.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        return False


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
