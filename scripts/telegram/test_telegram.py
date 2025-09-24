#!/usr/bin/env python3
"""
Тестовый скрипт для проверки отправки сообщений в Telegram
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv(Path(__file__).parent.parent / '.env')

def test_telegram_connection():
    """Тест подключения к Telegram API"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Ошибка: не заданы TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")
        return False
    
    # Проверка токена бота
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Бот подключен: @{bot_info['result']['username']}")
        else:
            print(f"❌ Ошибка проверки бота: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram API: {e}")
        return False
    
    # Отправка тестового сообщения
    try:
        message = "🧪 Тестовое сообщение от E2E тестов\n\n✅ Подключение к Telegram работает!"
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
        )
        
        if response.status_code == 200:
            print("✅ Тестовое сообщение отправлено успешно!")
            return True
        else:
            print(f"❌ Ошибка отправки сообщения: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Проверка подключения к Telegram...")
    success = test_telegram_connection()
    if success:
        print("🎉 Все работает! Можно запускать E2E тесты.")
    else:
        print("💥 Есть проблемы. Проверьте настройки.")
