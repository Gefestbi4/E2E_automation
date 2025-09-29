#!/usr/bin/env python3
"""
Простой скрипт инициализации базы данных
Создает необходимые базы данных, enum'ы и тестовые данные
"""

import os
import sys
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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


def create_test_database():
    """Создаем тестовую базу данных"""
    print("🗄️ Создание тестовой базы данных...")

    try:
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
        return True

    except Exception as e:
        print(f"❌ Ошибка при создании тестовой базы данных: {e}")
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


def main():
    """Основная функция инициализации"""
    print("🚀 Начинаем инициализацию базы данных...")

    # Ждем PostgreSQL
    if not wait_for_postgres():
        sys.exit(1)

    # Создаем тестовую базу данных
    if not create_test_database():
        sys.exit(1)

    # Создаем enum'ы в основной базе
    if not create_enums("my_database"):
        sys.exit(1)

    # Создаем enum'ы в тестовой базе
    if not create_enums("test_database"):
        sys.exit(1)

    print("🎉 Инициализация базы данных завершена успешно!")


if __name__ == "__main__":
    main()
