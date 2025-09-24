#!/bin/bash

# Главный скрипт запуска E2E тестов
# Использует скрипты из папки scripts/

set -e

echo "🚀 E2E Автоматизация с Telegram интеграцией"
echo "============================================="
echo ""

# Загрузка переменных окружения из файла
if [ -f ".env" ]; then
    echo "📋 Загрузка переменных окружения из .env..."
    export $(grep -v '^#' .env | xargs)
elif [ -f "Environments.env" ]; then
    echo "📋 Загрузка переменных окружения из Environments.env..."
    export $(grep -v '^#' Environments.env | xargs)
else
    echo "⚠️ Файл .env не найден. Создайте его на основе .env.example"
    exit 1
fi

# Определение режима запуска
MODE=${1:-local}

# Проверка наличия переменных окружения (только для режимов, требующих Telegram)
if [ "$MODE" != "report" ] && ([ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]); then
    echo "❌ Ошибка: не заданы переменные окружения"
    echo ""
    echo "Для запуска выполните:"
    echo "export TELEGRAM_BOT_TOKEN='your_bot_token'"
    echo "export TELEGRAM_CHAT_ID='your_chat_id'"
    echo "./run_tests.sh [local|docker|demo|report]"
    echo ""
    echo "Доступные режимы:"
    echo "  local  - Локальный запуск тестов (по умолчанию)"
    echo "  docker - Запуск в Docker контейнерах"
    echo "  demo   - Демонстрация с проверкой Telegram"
    echo "  report - Открыть Allure отчет в браузере"
    echo ""
    exit 1
fi

case $MODE in
    "local")
        echo "🧪 Локальный запуск E2E тестов..."
        ./scripts/demo_local.sh
        ;;
    "docker")
        echo "🐳 Запуск E2E тестов в Docker..."
        ./scripts/run_e2e_tests.sh
        ;;
    "demo")
        echo "🎬 Демонстрация системы..."
        ./scripts/demo_e2e.sh
        ;;
    "report")
        echo "📊 Отправка Allure отчета в Telegram..."
        python3 scripts/send_final_report.py
        ;;
    *)
        echo "❌ Неизвестный режим: $MODE"
        echo "Доступные режимы: local, docker, demo, report"
        exit 1
        ;;
esac

echo ""
echo "✅ Готово! Проверьте Telegram для получения отчета."
