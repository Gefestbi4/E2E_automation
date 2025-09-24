#!/bin/bash

# Скрипт для запуска E2E тестов с отправкой отчета в Telegram

set -e

echo "🚀 Запуск E2E тестов в Docker..."

# Проверка наличия переменных окружения
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ Ошибка: не заданы переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID"
    echo "Создайте файл .env с этими переменными или экспортируйте их:"
    echo "export TELEGRAM_BOT_TOKEN='your_bot_token'"
    echo "export TELEGRAM_CHAT_ID='your_chat_id'"
    exit 1
fi

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cat > .env << EOF
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
EOF
fi

# Запуск E2E тестов
echo "🧪 Запуск E2E тестов..."
docker compose up --build e2e-tests

# Получение логов
echo "📋 Получение логов..."
docker compose logs e2e-tests

echo "✅ E2E тесты завершены!"
echo "📊 Отчет отправлен в Telegram"
echo "🌐 Allure отчет доступен по адресу: http://localhost:5050"
