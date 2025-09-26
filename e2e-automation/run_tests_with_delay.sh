#!/bin/bash

# Запуск E2E тестов с задержкой для Allure
echo "Starting E2E tests..."

# Запуск тестов
python -m pytest tests/ --alluredir=/app/allure-results -s

# Получение кода выхода тестов
TEST_EXIT_CODE=$?

echo "Tests completed with exit code: $TEST_EXIT_CODE"

# Ожидание обработки результатов Allure
echo "Waiting for Allure to process results..."
sleep 10

# Проверка, что результаты обработаны
if [ -d "/app/allure-results" ] && [ "$(ls -A /app/allure-results)" ]; then
    echo "✅ Allure results found, processing complete"
else
    echo "⚠️  Warning: No Allure results found"
fi

# Логируем финальный статус
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests passed successfully!"
else
    echo "❌ Some tests failed. Check the logs above for details."
fi

echo "Container will now exit with code: $TEST_EXIT_CODE"

# Возвращаем код выхода тестов
exit $TEST_EXIT_CODE
