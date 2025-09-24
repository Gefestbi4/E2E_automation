# E2E Automation Dockerfile
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Chrome для ARM64
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=arm64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver
RUN CHROME_VERSION=$(chromium-browser --version | grep -oP '\d+\.\d+\.\d+') \
    && CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*}") \
    && wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

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
