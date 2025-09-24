# 🗄️ Database Tests

Автоматизированное тестирование баз данных (PostgreSQL, MongoDB) с использованием pytest и Allure.

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
docker build -t db-tests .

# Запуск тестов
docker run --rm -v $(pwd)/allure-results:/app/allure-results db-tests
```

## 📁 Структура
```
db-tests/
├── tests/              # DB тесты
├── requirements.txt    # Зависимости
├── .env               # Переменные окружения
├── Dockerfile         # Docker конфигурация
└── README.md          # Документация
```

## 🔧 Конфигурация

Основные переменные в `.env`:
- `DATABASE_URL` - URL PostgreSQL базы данных
- `MONGO_URL` - URL MongoDB базы данных
- `TELEGRAM_BOT_TOKEN` - Токен Telegram бота
- `TELEGRAM_CHAT_ID` - ID чата для уведомлений
