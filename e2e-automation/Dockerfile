# E2E Automation Dockerfile
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY ./e2e-automation/requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Создание директорий для отчетов
RUN mkdir -p /app/allure-results /app/screenshots

# Копирование кода E2E
COPY ./e2e-automation/ .

# Установка curl только для health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Делаем скрипты исполняемыми
RUN chmod +x run_tests_with_delay.sh run_tests_smart.sh

# Команда по умолчанию
CMD ["pytest", "tests/test_login_page.py"]