#!/usr/bin/env python3
"""
Утилита для безопасной загрузки переменных окружения
Использует python-dotenv для загрузки .env файла
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Загружает переменные окружения из .env файла
    """
    # Ищем .env файл в корне проекта
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Загружены переменные из {env_path}")
    else:
        print(f"⚠️ Файл .env не найден по пути: {env_path}")
        print("💡 Создайте файл .env на основе .env.example")
    
    return env_path.exists()

def get_required_env_vars():
    """
    Проверяет наличие обязательных переменных окружения
    """
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют обязательные переменные: {', '.join(missing_vars)}")
        return False
    
    print("✅ Все обязательные переменные окружения загружены")
    return True

if __name__ == "__main__":
    load_environment()
    get_required_env_vars()
