# Automation Learning Platform

Полноценное веб-приложение для обучения автоматизаторов с широким спектром функциональности, включающей различные типы веб-приложений.

## 🎯 Описание проекта

Это комплексная платформа для обучения QA автоматизаторов, включающая:

- **E-commerce модуль** - интернет-магазин с полным функционалом
- **Social Network модуль** - социальная сеть с постами и чатами
- **Task Management модуль** - система управления задачами (Kanban)
- **Content Management модуль** - система управления контентом
- **Analytics модуль** - аналитика и дашборды

## 🏗️ Архитектура

### Backend (FastAPI)
```
backend/
├── api/                    # API endpoints по модулям
├── core/                  # Основная конфигурация
├── models/                # SQLAlchemy модели
├── schemas/               # Pydantic схемы
├── services/              # Бизнес-логика
├── utils/                 # Утилиты
└── tests/                 # Тесты
```

### Frontend (Vanilla JS + CSS)
```
frontend/
├── src/
│   ├── components/        # Переиспользуемые компоненты
│   ├── pages/            # Страницы приложения
│   ├── services/         # API сервисы
│   ├── utils/            # Утилиты
│   ├── styles/           # Стили
│   └── assets/           # Статические ресурсы
└── index_new.html        # Главная страница
```

### E2E Testing (Playwright + Pytest)
```
e2e-automation/
├── tests/                # Тесты
│   ├── auth/            # Тесты авторизации
│   ├── ecommerce/       # Тесты e-commerce
│   ├── social/          # Тесты social network
│   ├── tasks/           # Тесты task management
│   ├── content/         # Тесты content management
│   └── analytics/       # Тесты analytics
├── pages/               # Page Objects
├── utils/               # Утилиты тестирования
└── config/              # Конфигурация
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Python 3.8+
- Node.js 16+ (для разработки frontend)

### Запуск через Docker Compose

```bash
# Клонирование репозитория
git clone <repository-url>
cd E2E_automation

# Запуск всех сервисов
docker-compose up --build

# Запуск только E2E тестов
docker-compose --profile testing up --build --abort-on-container-exit e2e-tests
```

### Локальная разработка

```bash
# Backend
cd backend
pip install -r requirements_new.txt
python app_new.py

# Frontend
cd frontend
# Открыть index_new.html в браузере

# E2E тесты
cd e2e-automation
pip install -r requirements_new.txt
pytest
```

## 📚 Документация

### Основная документация

- [Backend Documentation](docs/backend_docs/README.md)
- [Frontend Documentation](docs/frontend_docs/README.md)
- [QA Documentation](docs/qa/README.md)
- [Testing Guide](docs/qa/TESTING_GUIDE.md)

### API Endpoints

#### Аутентификация
- `POST /api/auth/login` - Вход в систему
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/refresh` - Обновление токена
- `POST /api/auth/logout` - Выход

#### E-commerce
- `GET /api/ecommerce/products` - Список товаров
- `POST /api/ecommerce/cart` - Добавить в корзину
- `POST /api/ecommerce/orders` - Создать заказ

#### Social Network
- `GET /api/social/posts` - Лента постов
- `POST /api/social/posts` - Создать пост
- `POST /api/social/users/{id}/follow` - Подписка

#### Task Management
- `GET /api/tasks/boards` - Доски задач
- `POST /api/tasks/cards` - Создать задачу
- `PUT /api/tasks/cards/{id}` - Обновить задачу

#### Content Management
- `GET /api/content/articles` - Статьи
- `POST /api/content/articles` - Создать статью
- `POST /api/content/upload` - Загрузка файлов

#### Analytics
- `GET /api/analytics/dashboard` - Данные дашборда
- `GET /api/analytics/metrics` - Метрики
- `POST /api/analytics/reports` - Создать отчет

## 🧪 Тестирование

### Система маркировки тестов

Проект включает продвинутую систему маркировки для эффективной отладки:

```python
@debug_test("Проблема с загрузкой страницы")
@pytest.mark.debug
def test_problematic():
    """Тест, требующий отладки"""
    pass

@fixme_test("Тест падает из-за изменений в API")
@pytest.mark.fixme
def test_broken():
    """Сломанный тест"""
    pass
```

### Запуск тестов

```bash
# Только тесты для отладки
pytest --debug-only

# Только сломанные тесты
pytest --fixme-only

# Критические тесты
pytest -m critical

# Интерактивный запуск
python run_debug_tests.py
```

### Типы тестов

- **E2E тесты** - Полные пользовательские сценарии
- **API тесты** - Тестирование REST API
- **Database тесты** - Тестирование моделей данных
- **Performance тесты** - Нагрузочное тестирование
- **Security тесты** - Тестирование безопасности

### Отчеты

- **Allure отчеты** - Детальная отчетность
- **Screenshots** - Скриншоты при падении
- **HTML отчеты** - Быстрый просмотр результатов

## 🛠️ Технологический стек

### Backend
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - основная БД
- **Redis** - кэширование
- **JWT** - аутентификация
- **Pydantic** - валидация данных

### Frontend
- **Vanilla JavaScript** - основная логика
- **CSS3** - стилизация
- **Chart.js** - графики
- **Quill.js** - rich text редактор
- **Fetch API** - HTTP запросы

### Testing
- **Playwright** - E2E тестирование
- **Pytest** - test runner
- **Allure** - отчетность
- **Requests** - API тестирование

## 📊 Модули приложения

### 1. E-commerce
- Каталог товаров с фильтрацией
- Корзина покупок
- Оформление заказа
- Система отзывов
- Управление категориями

### 2. Social Network
- Лента постов
- Комментарии и лайки
- Система подписок
- Чаты в реальном времени
- Уведомления

### 3. Task Management
- Kanban доски
- Проекты и команды
- Уведомления о дедлайнах
- Отчеты и аналитика
- Учет времени

### 4. Content Management
- Статьи и блоги
- Rich text редактор
- Медиа библиотека
- Категории и теги
- Модерация контента

### 5. Analytics
- Интерактивные дашборды
- Графики и диаграммы
- Экспорт данных
- Настраиваемые виджеты
- Алерты и уведомления

## 🔒 Безопасность

- JWT токены с коротким временем жизни
- Refresh токены для продления сессии
- CORS настройки
- Rate limiting
- Валидация входных данных
- Хеширование паролей (bcrypt)
- Защита от SQL инъекций

## 📈 Мониторинг

- Логирование запросов
- Метрики производительности
- Ошибки и исключения
- Health checks
- Prometheus метрики

## 🤝 Участие в разработке

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [документацию](docs/)
2. Изучите [руководство по тестированию](docs/qa/TESTING_GUIDE.md)
3. Создайте [Issue](https://github.com/your-repo/issues)

## 🎓 Обучение

Этот проект предназначен для обучения автоматизаторов и включает:

- Различные типы веб-приложений
- Современные паттерны тестирования
- Систему маркировки для отладки
- Comprehensive документацию
- Best practices для E2E тестирования

---

**Создано командой QA Automation Engineers для обучения и развития навыков автоматизации тестирования.**
