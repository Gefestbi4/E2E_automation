#!/bin/bash

# Скрипт для открытия Allure отчета

echo "🧪 Открытие Allure отчета..."
echo "============================="

# Проверяем, что Allure сервер запущен
if ! curl -s http://localhost:5050/allure-docker-service/version > /dev/null; then
    echo "❌ Allure сервер не запущен на localhost:5050"
    echo "Запустите: docker compose up -d allure"
    exit 1
fi

# URL отчета
REPORT_URL="http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html"

echo "📊 Отчет доступен по адресу:"
echo "$REPORT_URL"
echo ""

# Пытаемся открыть в браузере
if command -v open > /dev/null; then
    echo "🌐 Открываем в браузере..."
    open "$REPORT_URL"
elif command -v xdg-open > /dev/null; then
    echo "🌐 Открываем в браузере..."
    xdg-open "$REPORT_URL"
elif command -v start > /dev/null; then
    echo "🌐 Открываем в браузере..."
    start "$REPORT_URL"
else
    echo "⚠️  Не удалось автоматически открыть браузер"
    echo "Скопируйте и вставьте URL в браузер:"
    echo "$REPORT_URL"
fi

echo ""
echo "✅ Готово!"
