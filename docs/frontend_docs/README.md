# Frontend Documentation

## Обзор архитектуры

Frontend построен как SPA (Single Page Application) с модульной архитектурой, обеспечивающей интерактивное обучение автоматизаторов различным типам веб-приложений.

## Структура проекта

```
frontend/
├── src/
│   ├── components/           # Переиспользуемые компоненты
│   │   ├── common/          # Общие компоненты
│   │   ├── forms/           # Формы
│   │   ├── modals/          # Модальные окна
│   │   ├── navigation/      # Навигация
│   │   └── widgets/         # Виджеты
│   ├── pages/               # Страницы приложения
│   │   ├── auth/           # Страницы авторизации
│   │   ├── ecommerce/      # E-commerce модуль
│   │   ├── social/         # Social Network модуль
│   │   ├── tasks/          # Task Management модуль
│   │   ├── content/        # Content Management модуль
│   │   └── analytics/      # Analytics модуль
│   ├── services/            # API сервисы
│   │   ├── api.js          # Базовый API клиент
│   │   ├── auth.js         # Аутентификация
│   │   ├── ecommerce.js    # E-commerce API
│   │   ├── social.js       # Social API
│   │   ├── tasks.js        # Tasks API
│   │   ├── content.js      # Content API
│   │   └── analytics.js    # Analytics API
│   ├── store/              # State management
│   │   ├── modules/        # Модули store
│   │   └── index.js        # Главный store
│   ├── utils/              # Утилиты
│   │   ├── auth.js         # Утилиты авторизации
│   │   ├── validation.js   # Валидация
│   │   ├── helpers.js      # Вспомогательные функции
│   │   └── constants.js    # Константы
│   ├── styles/             # Стили
│   │   ├── components/     # Стили компонентов
│   │   ├── pages/          # Стили страниц
│   │   └── themes/         # Темы оформления
│   └── assets/             # Статические ресурсы
│       ├── images/         # Изображения
│       ├── icons/          # Иконки
│       └── fonts/          # Шрифты
├── public/                 # Публичные файлы
│   ├── index.html         # Главная HTML
│   └── favicon.ico        # Иконка сайта
└── tests/                 # Тесты
    ├── unit/              # Юнит тесты
    ├── integration/       # Интеграционные тесты
    └── e2e/               # E2E тесты
```

## Модули приложения

### 1. Authentication Module
**Страницы:**
- `/login` - Страница входа
- `/register` - Регистрация
- `/forgot-password` - Восстановление пароля
- `/reset-password` - Сброс пароля

**Функциональность:**
- JWT токен управление
- Автоматическое обновление токенов
- Сохранение сессии
- 2FA поддержка
- OAuth2 интеграция

### 2. E-commerce Module
**Страницы:**
- `/shop` - Каталог товаров
- `/product/{id}` - Детали товара
- `/cart` - Корзина покупок
- `/checkout` - Оформление заказа
- `/orders` - История заказов
- `/profile` - Профиль пользователя

**Функциональность:**
- Фильтрация и поиск товаров
- Добавление в корзину
- Процесс оформления заказа
- Система отзывов
- Рекомендации товаров
- Избранное

### 3. Social Network Module
**Страницы:**
- `/feed` - Лента постов
- `/profile/{id}` - Профиль пользователя
- `/messages` - Чаты
- `/notifications` - Уведомления
- `/friends` - Друзья и подписки

**Функциональность:**
- Создание и редактирование постов
- Лайки и комментарии
- Система подписок
- Чаты в реальном времени
- Уведомления
- Поиск пользователей

### 4. Task Management Module
**Страницы:**
- `/boards` - Доски задач
- `/board/{id}` - Kanban доска
- `/projects` - Проекты
- `/team` - Команда
- `/reports` - Отчеты

**Функциональность:**
- Drag & drop задачи
- Создание и редактирование карточек
- Назначение исполнителей
- Комментарии к задачам
- Уведомления о дедлайнах
- Аналитика проектов

### 5. Content Management Module
**Страницы:**
- `/articles` - Статьи
- `/article/{id}` - Чтение статьи
- `/create-article` - Создание статьи
- `/edit-article/{id}` - Редактирование
- `/media` - Медиа библиотека

**Функциональность:**
- Rich text редактор
- Загрузка медиа файлов
- Система категорий и тегов
- Модерация контента
- Поиск по статьям
- Комментарии к статьям

### 6. Analytics & Dashboard Module
**Страницы:**
- `/dashboard` - Главная панель
- `/analytics` - Аналитика
- `/reports` - Отчеты
- `/settings` - Настройки

**Функциональность:**
- Интерактивные графики
- Настраиваемые виджеты
- Экспорт данных
- Фильтры и даты
- Уведомления о метриках
- Шаблоны дашбордов

## Технологический стек

- **HTML5** - разметка
- **CSS3** - стили
- **JavaScript ES6+** - логика
- **Fetch API** - HTTP запросы
- **Local Storage** - локальное хранилище
- **WebSockets** - реальное время
- **Chart.js** - графики
- **Quill.js** - rich text редактор
- **Sortable.js** - drag & drop

## Компоненты

### Общие компоненты
- `Header` - Шапка сайта
- `Navigation` - Навигационное меню
- `Sidebar` - Боковая панель
- `Footer` - Подвал
- `Modal` - Модальные окна
- `Toast` - Уведомления
- `Loading` - Индикаторы загрузки
- `Pagination` - Пагинация

### Формы
- `LoginForm` - Форма входа
- `RegisterForm` - Форма регистрации
- `ProductForm` - Форма товара
- `ArticleForm` - Форма статьи
- `TaskForm` - Форма задачи
- `UserProfileForm` - Форма профиля

### Виджеты
- `ProductCard` - Карточка товара
- `PostCard` - Карточка поста
- `TaskCard` - Карточка задачи
- `ChartWidget` - Виджет графика
- `StatsWidget` - Виджет статистики
- `NotificationWidget` - Виджет уведомлений

## State Management

### Глобальное состояние
- `auth` - Аутентификация
- `user` - Данные пользователя
- `notifications` - Уведомления
- `theme` - Тема оформления

### Модульное состояние
- `ecommerce` - E-commerce данные
- `social` - Social network данные
- `tasks` - Task management данные
- `content` - Content management данные
- `analytics` - Analytics данные

## API Integration

### Базовый API клиент
```javascript
class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }
  
  async request(endpoint, options = {}) {
    // Базовая логика запросов
  }
}
```

### Сервисы по модулям
- `AuthService` - Аутентификация
- `EcommerceService` - E-commerce
- `SocialService` - Social network
- `TasksService` - Task management
- `ContentService` - Content management
- `AnalyticsService` - Analytics

## Стилизация

### CSS архитектура
- **BEM методология** - именование классов
- **CSS Variables** - переменные
- **Flexbox/Grid** - раскладка
- **Responsive Design** - адаптивность
- **Dark/Light themes** - темы

### Компонентная стилизация
- Каждый компонент имеет свои стили
- Переиспользуемые миксины
- Анимации и переходы
- Медиа запросы для адаптивности

## Производительность

### Оптимизации
- Lazy loading изображений
- Код сплиттинг по модулям
- Кэширование API запросов
- Минификация ресурсов
- Gzip сжатие

### Мониторинг
- Метрики загрузки страниц
- Ошибки JavaScript
- API запросы
- Пользовательские действия

## Тестирование

### Типы тестов
- **Unit тесты** - отдельные компоненты
- **Integration тесты** - взаимодействие компонентов
- **E2E тесты** - полные пользовательские сценарии

### Инструменты
- **Jest** - unit тестирование
- **Cypress** - E2E тестирование
- **Testing Library** - тестирование компонентов

## Доступность (Accessibility)

- ARIA атрибуты
- Клавиатурная навигация
- Screen reader поддержка
- Контрастность цветов
- Семантическая разметка
- Test_data_id - во всех елементах уникальные, для тестировщиков

## Браузерная поддержка

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Мобильные браузеры
