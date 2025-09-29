#!/usr/bin/env python3
"""
Скрипт для создания пользователя в базе данных
"""
import sys
import os

# Добавляем путь к backend в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy.orm import Session
from models import User, SessionLocal
from security import get_password_hash


def create_user(email: str, password: str, username: str = None):
    """Создает пользователя в базе данных"""
    if not username:
        username = email.split("@")[0]

    # Создаем сессию базы данных
    db = SessionLocal()

    try:
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ Пользователь с email {email} уже существует!")
            return False

        # Хешируем пароль
        hashed_password = get_password_hash(password)

        # Создаем нового пользователя
        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True,
        )

        # Добавляем в базу данных
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"✅ Пользователь успешно создан!")
        print(f"   ID: {new_user.id}")
        print(f"   Email: {new_user.email}")
        print(f"   Username: {new_user.username}")
        print(f"   Active: {new_user.is_active}")
        print(f"   Verified: {new_user.is_verified}")

        return True

    except Exception as e:
        print(f"❌ Ошибка при создании пользователя: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Создаем пользователя с указанными данными
    email = "test@example.com"
    password = "testpassword123"
    username = "testuser"

    print("🔧 Создание пользователя в базе данных...")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Username: {username}")
    print()

    success = create_user(email, password, username)

    if success:
        print("\n🎉 Пользователь готов к использованию!")
        print("   Теперь можно войти в систему через http://localhost:3000/login.html")
    else:
        print("\n💥 Не удалось создать пользователя")
        sys.exit(1)
