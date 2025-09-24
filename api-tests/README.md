# 🔌 API Tests

Автоматизированное тестирование REST API с использованием pytest и Allure.

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
docker build -t api-tests .

# Запуск тестов
docker run --rm -v $(pwd)/allure-results:/app/allure-results api-tests
```

## 📁 Структура
```
api-tests/
├── tests/              # API тесты
├── requirements.txt    # Зависимости
├── .env               # Переменные окружения
├── Dockerfile         # Docker конфигурация
└── README.md          # Документация
```

## 🔧 Конфигурация

Основные переменные в `.env`:
- `API_BASE_URL` - Базовый URL API
- `API_KEY` - Ключ API
- `TELEGRAM_BOT_TOKEN` - Токен Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений
