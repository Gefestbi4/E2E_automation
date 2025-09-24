# 🧪 E2E Automation

Автоматизированное E2E тестирование веб-приложений с использованием Selenium и Allure.

## 🚀 Быстрый старт

### Локальный запуск
```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл

# Запуск тестов
pytest tests/ -v --alluredir=allure-results

# Генерация отчета
allure generate allure-results --clean -o allure-reports/latest
allure serve allure-results
```

### Docker запуск
```bash
# Сборка образа
docker build -t e2e-automation .

# Запуск тестов
docker run --rm -v $(pwd)/allure-results:/app/allure-results e2e-automation
```

## 📁 Структура
```
e2e-automation/
├── tests/              # Тесты
├── pages/              # Page Object Model
├── screenshots/        # Скриншоты
├── requirements.txt    # Зависимости
├── .env               # Переменные окружения
├── Dockerfile         # Docker конфигурация
└── README.md          # Документация
```

## 🔧 Конфигурация

Основные переменные в `.env`:
- `TEST_URL` - URL тестируемого приложения
- `EMAIL` - Email для тестов
- `PASSWORD` - Пароль для тестов
- `TELEGRAM_BOT_TOKEN` - Токен Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений
