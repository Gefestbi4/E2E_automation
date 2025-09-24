#!/usr/bin/env python3
"""
Финальный упрощенный скрипт для отправки отчетов в Telegram
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv(Path(__file__).parent.parent / '.env')


def get_test_summary(allure_reports_dir):
    """Получение сводки тестов из allure-reports"""
    summary_file = Path(allure_reports_dir) / "widgets" / "summary.json"
    
    if not summary_file.exists():
        print(f"Файл summary.json не найден: {summary_file}")
        return None
    
    try:
        with open(summary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Преобразование структуры данных
        summary = {
            'passed': data['statistic']['passed'],
            'failed': data['statistic']['failed'],
            'broken': data['statistic']['broken'],
            'skipped': data['statistic']['skipped'],
            'total': data['statistic']['total'],
            'duration': data['time']['duration']
        }
        return summary
    except Exception as e:
        print(f"Ошибка чтения summary.json: {e}")
        return None


def send_telegram_message(bot_token, chat_id, message, photo_paths=None):
    """Отправка сообщения в Telegram"""
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    # Отправка текстового сообщения
    send_url = f"{base_url}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(send_url, data=data, timeout=30)
        if response.status_code == 200:
            print("📱 Текстовое сообщение отправлено в Telegram")
        else:
            print(f"❌ Ошибка отправки текстового сообщения: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка отправки текстового сообщения: {e}")
        return False
    
    # Отправка скриншота, если есть
    if photo_paths:
        for photo_path in photo_paths:
            if os.path.exists(photo_path):
                send_photo_url = f"{base_url}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {'chat_id': chat_id, 'caption': '📊 Скриншот Allure отчета'}
                    response = requests.post(send_photo_url, files=files, data=data, timeout=60)
                    
                    if response.status_code == 200:
                        print(f"📸 Скриншот отправлен: {photo_path}")
                    else:
                        print(f"❌ Ошибка отправки скриншота: {response.status_code}")
    
    return True


def format_duration(seconds):
    """Форматирование времени выполнения"""
    if seconds < 60:
        return f"{seconds:.1f}с"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}м {secs}с"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}ч {minutes}м"


def main():
    """Основная функция"""
    # Получение переменных окружения
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    allure_results_dir = os.getenv('ALLURE_RESULTS_DIR', 'allure-results')
    allure_reports_dir = os.getenv('ALLURE_REPORTS_DIR', 'allure-reports/latest')
    allure_url = os.getenv('ALLURE_URL', 'http://localhost:5050')
    
    if not bot_token or not chat_id:
        print("❌ Ошибка: не заданы TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")
        return 1
    
    # Получение сводки тестов
    summary = get_test_summary(allure_reports_dir)
    if not summary:
        print("❌ Не удалось получить сводку тестов")
        return 1
    
    # Создание скриншота Allure отчета
    print("📸 Создание скриншота Allure отчета...")
    try:
        import subprocess
        result = subprocess.run(['python3', 'scripts/screenshot_local_allure.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("✅ Скриншот Allure отчета создан")
        else:
            print(f"❌ Ошибка создания скриншота: {result.stderr}")
    except Exception as e:
        print(f"❌ Ошибка запуска скриншота: {e}")
    
    # Формирование сообщения
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # Эмодзи для статусов
    status_emoji = {
        'passed': '✅',
        'failed': '❌',
        'broken': '💥',
        'skipped': '⏭️'
    }
    
    # Определение общего статуса
    if summary['failed'] > 0 or summary['broken'] > 0:
        overall_status = "❌ ЕСТЬ ОШИБКИ"
    elif summary['skipped'] > 0:
        overall_status = "⚠️ ЕСТЬ ПРОПУЩЕННЫЕ"
    else:
        overall_status = "✅ ВСЕ ТЕСТЫ ПРОШЛИ"
    
    message = f"""
🧪 *E2E Тесты завершены*
📅 {timestamp}

{overall_status}

⏱️ Время выполнения: {format_duration(summary['duration'] / 1000)}
📈 Всего тестов: {summary['total']}

🔗 *Кликабельные ссылки:*
📊 [Allure отчет - localhost:8080](http://localhost:8080)
🌐 [Frontend - localhost:3000](http://localhost:3000)
🔧 [Backend API - localhost:5000](http://localhost:5000)

💡 *Совет:* Нажмите на ссылки выше для быстрого перехода к отчетам
"""
    
    # Поиск скриншотов для отправки
    photo_paths = []
    screenshots_dir = Path(allure_reports_dir) / "screenshots"
    if screenshots_dir.exists():
        for screenshot_file in screenshots_dir.glob("*.png"):
            photo_paths.append(str(screenshot_file))
            print(f"📸 Найден скриншот: {screenshot_file}")
    
    # Отправка сообщения
    success = send_telegram_message(bot_token, chat_id, message, photo_paths)
    
    if success:
        print("✅ Отчет успешно отправлен в Telegram")
        return 0
    else:
        print("❌ Ошибка отправки отчета в Telegram")
        return 1


if __name__ == "__main__":
    exit(main())
