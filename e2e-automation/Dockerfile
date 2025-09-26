# E2E Automation Dockerfile
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY ./e2e-automation/requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода E2E
COPY ./e2e-automation/ .

# Копирование API модулей из корневой директории
COPY ./api ./api

# Делаем скрипт исполняемым
RUN chmod +x run_tests_with_delay.sh

# Команда по умолчанию
CMD ["./run_tests_with_delay.sh"]