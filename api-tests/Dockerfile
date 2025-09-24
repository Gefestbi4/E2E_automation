# API Tests Dockerfile
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Allure
RUN curl -o allure-2.13.8.tgz -Ls https://github.com/allure-framework/allure2/releases/download/2.13.8/allure-2.13.8.tgz \
    && tar -zxf allure-2.13.8.tgz -C /opt/ \
    && ln -s /opt/allure-2.13.8/bin/allure /usr/local/bin/allure \
    && rm allure-2.13.8.tgz

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Команда по умолчанию
CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]
