# 🚀 E2E Автоматизация с Telegram интеграцией

Полноценный фреймворк для E2E тестирования с автоматической отправкой отчетов в Telegram.

## ✨ Что реализовано

### 🧪 E2E Тестирование
- **7 автоматизированных тестов** для страницы авторизации
- **Page Object Model** с структурированными локаторами
- **Allure интеграция** для детальной отчетности
- **Автоматическая регистрация** пользователей
- **JWT токен валидация**

### 📱 Telegram интеграция
- **Автоматическая отправка** отчетов в Telegram
- **ZIP архив** с полным Allure отчетом
- **Красивое форматирование** с эмодзи и статистикой
- **Проверка подключения** к Telegram API

### 🐳 Docker контейнеризация
- **Полная инфраструктура** в Docker Compose
- **Изолированное тестирование** в контейнерах
- **Автоматический запуск** всех сервисов
- **Масштабируемость** для CI/CD

## 🚀 Быстрый старт

### 1. Настройка Telegram бота

```bash
# Получите токен от @BotFather и ID чата от @userinfobot
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

### 2. Запуск демонстрации

```bash
# Главный скрипт (рекомендуется)
./run_tests.sh local    # Локальный запуск
./run_tests.sh docker   # Docker запуск
./run_tests.sh demo     # Демонстрация
./run_tests.sh report   # Открыть Allure отчет

# Или напрямую:
./scripts/demo_local.sh                    # Локальная демонстрация
python3 scripts/test_telegram.py          # Проверка Telegram
pytest tests_E2E/test_login_page.py -v    # Запуск тестов
allure generate allure-results -o allure-reports/latest  # Генерация отчета
python3 scripts/send_allure_report.py     # Отправка в Telegram
./scripts/open_allure_report.sh           # Открыть отчет
```

### 3. Docker запуск

```bash
# Запуск всей инфраструктуры
docker compose up -d

# Запуск E2E тестов в Docker
docker compose up --build e2e-tests
```

## 📊 Результат работы

После выполнения вы получите:

### В Telegram:
```
🧪 E2E Тесты завершены
📅 24.09.2025 18:45:30

✅ ВСЕ ТЕСТЫ ПРОШЛИ

📊 Статистика:
✅ Прошло: 7
❌ Упало: 0
💥 Сломано: 0
⏭️ Пропущено: 0

⏱️ Время выполнения: 22.6с
📈 Всего тестов: 7
```

### В браузере:
- **Allure отчет**: http://localhost:5050
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 🧪 Доступные тесты

| Тест | Описание | Статус |
|------|----------|--------|
| `test_successful_login` | Успешная авторизация | ✅ |
| `test_auto_registration_new_user` | Автоматическая регистрация | ✅ |
| `test_form_validation` | Валидация формы | ✅ |
| `test_invalid_credentials` | Обработка неверных данных | ✅ |
| `test_login_page_elements` | Проверка UI элементов | ✅ |
| `test_navigation_from_login_page` | Навигация | ✅ |
| `test_auth_token_storage` | Сохранение JWT токена | ✅ |

## 🏗️ Архитектура

```
├── 🧪 E2E Tests
│   ├── tests_E2E/test_login_page.py    # Тесты
│   ├── pages/                          # Page Objects
│   │   ├── Locators.py                 # Локаторы
│   │   ├── base_page.py                # Базовая страница
│   │   └── login_page.py               # Страница логина
│   └── conftest.py                     # Конфигурация pytest
├── 📁 Scripts (все скрипты в одной папке)
│   ├── send_allure_report.py           # ⭐ Отправка в Telegram
│   ├── run_e2e_tests.sh               # ⭐ Docker запуск
│   ├── demo_local.sh                  # Локальная демонстрация
│   ├── demo_e2e.sh                    # Docker демонстрация
│   ├── test_telegram.py               # Тест подключения
│   └── cleanup_scripts.sh             # Очистка файлов
├── 🐳 Docker
│   ├── Dockerfile.e2e                  # E2E контейнер
│   └── docker-compose.yml              # Инфраструктура
├── 🚀 Главные скрипты
│   └── run_tests.sh                    # ⭐ Главный скрипт запуска
└── 📊 Reports
    ├── allure-results/                 # Сырые данные
    └── allure-reports/                 # Сгенерированные отчеты
```

## 🔧 Конфигурация

### Переменные окружения

```bash
# Обязательные для Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Настройки тестов
TEST_URL=http://localhost:3000
EMAIL=test@example.com
PASSWORD=testpassword123
USER_NAME=Test User
API_KEY=test_api_key
DATABASE_URL=postgresql://my_user:my_password@localhost:5432/my_database
```

### Настройка pytest

```ini
[tool:pytest]
testpaths = tests_E2E
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --alluredir=allure-results
markers =
    crit: critical tests
    medium: medium priority tests
    low: low priority tests
```

## 📱 Telegram Bot API

### Создание бота
1. Напишите [@BotFather](https://t.me/BotFather)
2. Создайте нового бота командой `/newbot`
3. Получите токен бота
4. Узнайте ID чата через [@userinfobot](https://t.me/userinfobot)

### Формат сообщений
- **HTML разметка** для красивого отображения
- **Эмодзи** для визуального разделения
- **ZIP архивы** с полными отчетами
- **Статистика** в реальном времени

## 🐳 Docker сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| `frontend` | 3000 | React приложение |
| `backend` | 5000 | FastAPI сервер |
| `postgres` | 5432 | База данных |
| `redis` | 6379 | Кеширование |
| `allure` | 5050 | Allure сервер |
| `e2e-tests` | - | E2E тесты |

## 🔍 Отладка

### Проверка сервисов
```bash
# Статус всех сервисов
docker compose ps

# Логи конкретного сервиса
docker compose logs e2e-tests
docker compose logs frontend
docker compose logs backend
```

### Проверка Telegram
```bash
# Тест подключения
python3 test_telegram.py

# Проверка токена
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

### Локальный запуск тестов
```bash
# Установка зависимостей
pip install -r requirements_test.txt

# Запуск тестов
pytest tests_E2E/test_login_page.py --browser-name=chrome -v
```

## 📈 Расширение

### Добавление новых тестов
1. Создайте файл в `tests_E2E/`
2. Добавьте локаторы в `pages/Locators.py`
3. Создайте Page Object в `pages/`
4. Обновите скрипты при необходимости

### Настройка уведомлений
Отредактируйте `scripts/send_allure_report.py` для изменения:
- Формата сообщений
- Условий отправки
- Дополнительной логики

### CI/CD интеграция
```yaml
# GitHub Actions пример
- name: Run E2E Tests
  run: |
    export TELEGRAM_BOT_TOKEN=${{ secrets.TELEGRAM_BOT_TOKEN }}
    export TELEGRAM_CHAT_ID=${{ secrets.TELEGRAM_CHAT_ID }}
    ./demo_local.sh
```

## 🎯 Ключевые особенности

### ✅ Надежность
- **Автоматическая регистрация** пользователей
- **Уникальные email** для каждого теста
- **Обработка ошибок** и retry логика
- **Валидация** всех входных данных

### 🚀 Производительность
- **Параллельный запуск** тестов
- **Кеширование** зависимостей
- **Оптимизированные** Docker образы
- **Быстрая генерация** отчетов

### 🔧 Удобство
- **Простой запуск** одной командой
- **Подробная документация**
- **Демо скрипты** для быстрого старта
- **Гибкая конфигурация**

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker compose logs`
2. Убедитесь в правильности переменных окружения
3. Проверьте доступность всех сервисов
4. Создайте issue с подробным описанием

## 📞 Контакты

- **Автор**: Николай Кияшко
- **Email**: gefestbi4@gmail.com
- **Telegram**: @NikolayKiyashko
- **GitHub**: [Репозиторий проекта]

---

🎉 **Готово к использованию!** Запускайте `./demo_local.sh` и наслаждайтесь автоматизированным тестированием с уведомлениями в Telegram!
