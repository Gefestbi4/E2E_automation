#!/bin/bash

# Умный запуск E2E тестов с проверкой Allure
echo "🚀 Starting E2E tests..."

# Запуск тестов
python -m pytest tests/ --alluredir=/app/allure-results -s
TEST_EXIT_CODE=$?

echo "📊 Tests completed with exit code: $TEST_EXIT_CODE"

# Ожидание обработки результатов Allure
echo "⏳ Waiting for Allure to process results..."

# Проверяем, что Allure сервер доступен
ALLURE_READY=false
for i in {1..30}; do
    if curl -s http://allure:5050/api/result > /dev/null 2>&1; then
        echo "✅ Allure server is ready"
        ALLURE_READY=true
        break
    fi
    echo "⏳ Waiting for Allure server... ($i/30)"
    sleep 2
done

if [ "$ALLURE_READY" = false ]; then
    echo "⚠️  Allure server not ready, but continuing..."
fi

# Проверка результатов
if [ -d "/app/allure-results" ] && [ "$(ls -A /app/allure-results)" ]; then
    echo "✅ Allure results found, processing complete"
    
    # Показываем статистику результатов
    RESULT_COUNT=$(find /app/allure-results -name "*.json" | wc -l)
    echo "📈 Found $RESULT_COUNT test result files"
else
    echo "⚠️  Warning: No Allure results found"
fi

# Логируем финальный статус
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests passed successfully!"
else
    echo "❌ Some tests failed. Check the logs above for details."
fi

echo "🏁 Container will now exit with code: $TEST_EXIT_CODE"

# Возвращаем код выхода тестов
exit $TEST_EXIT_CODE
