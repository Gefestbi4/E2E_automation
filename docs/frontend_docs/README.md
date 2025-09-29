# Frontend Documentation

## Обзор архитектуры

Frontend построен как SPA (Single Page Application) с модульной архитектурой, обеспечивающей интерактивное обучение автоматизаторов различным типам веб-приложений.

## Структура проекта

```
frontend/
├── components/             # Переиспользуемые компоненты
│   ├── forms.js           # Формы
│   ├── modals.js          # Модальные окна
│   ├── advanced_forms.js  # Продвинутые формы
│   ├── advanced_modals.js # Продвинутые модальные окна
│   ├── advanced_tables.js # Продвинутые таблицы
│   └── toast.js           # Уведомления
├── pages/                 # Страницы приложения
│   ├── analytics.js       # Analytics модуль
│   ├── content.js         # Content Management модуль
│   ├── dashboard.js       # Главная панель
│   ├── ecommerce.js       # E-commerce модуль
│   ├── social.js          # Social Network модуль
│   └── tasks.js           # Task Management модуль
├── services/              # API сервисы
│   ├── api.js             # Базовый API клиент
│   ├── auth.js            # Аутентификация
│   ├── analytics.js       # Analytics API
│   ├── content.js         # Content API
│   ├── ecommerce.js       # E-commerce API
│   ├── social.js          # Social API
│   └── tasks.js           # Tasks API
├── styles/                # Стили
│   ├── accessibility.css  # Стили доступности
│   ├── advanced-components.css # Продвинутые компоненты
│   ├── components.css     # Стили компонентов
│   ├── fix.css            # Исправления
│   ├── interactions.css   # Взаимодействия
│   ├── main.css           # Основные стили
│   ├── notifications.css  # Уведомления
│   ├── performance.css    # Производительность
│   ├── realtime.css       # Реальное время
│   ├── responsive.css     # Адаптивность
│   ├── social_connections.css # Социальные связи
│   ├── testing.css        # Тестирование
│   └── themes.css         # Темы оформления
├── utils/                 # Утилиты
│   ├── accessibility.js   # Доступность
│   ├── advanced_analytics_manager.js # Продвинутая аналитика
│   ├── advanced_notifications_manager.js # Продвинутые уведомления
│   ├── ai_manager.js      # AI менеджер
│   ├── animations.js      # Анимации
│   ├── auth.js            # Утилиты авторизации
│   ├── avatar.js          # Аватары
│   ├── common.js          # Общие утилиты
│   ├── constants.js       # Константы
│   ├── error_handler.js   # Обработка ошибок
│   ├── form_validator.js  # Валидация форм
│   ├── helpers.js         # Вспомогательные функции
│   ├── integrations_manager.js # Менеджер интеграций
│   ├── interactions.js    # Взаимодействия
│   ├── loading_indicators.js # Индикаторы загрузки
│   ├── logger.js          # Логирование
│   ├── media_upload.js    # Загрузка медиа
│   ├── mobile_navigation.js # Мобильная навигация
│   ├── monitoring_dashboard.js # Мониторинг
│   ├── notifications.js   # Уведомления
│   ├── performance_optimizer.js # Оптимизация производительности
│   ├── performance.js     # Производительность
│   ├── realtime.js        # Реальное время
│   ├── roles_manager.js   # Менеджер ролей
│   ├── search_filter.js   # Поиск и фильтрация
│   ├── security_manager.js # Менеджер безопасности
│   ├── settings_manager.js # Менеджер настроек
│   ├── social_connections.js # Социальные связи
│   ├── social_feed.js     # Социальная лента
│   ├── testing_manager.js # Менеджер тестирования
│   ├── toast.js           # Уведомления
│   ├── touch_gestures.js  # Жесты
│   └── validation.js      # Валидация
├── index.html             # Главная HTML страница
├── login.html             # Страница входа
├── tests.html             # Страница тестов
├── app.js                 # Главный JavaScript файл
├── style.css              # Основные стили
├── sw.js                  # Service Worker
└── default-avatar.*       # Аватары по умолчанию
```

## Модули приложения

### 1. Authentication Module
**Страницы:**
- `login.html` - Страница входа
- `index.html` - Главная страница с профилем

**Файлы:**
- `components/forms.js` - Формы входа и регистрации
- `services/auth.js` - API авторизации
- `utils/auth.js` - Утилиты авторизации

**Функциональность:**
- JWT токен управление
- Автоматическое обновление токенов
- Сохранение сессии
- Управление профилем
- Восстановление пароля

### 2. E-commerce Module
**Страницы:**
- `pages/ecommerce.js` - Каталог товаров, корзина, оформление заказа

**Файлы:**
- `components/forms.js` - Формы заказа
- `components/modals.js` - Модальные окна товаров
- `services/ecommerce.js` - API E-commerce

**Функциональность:**
- Фильтрация и поиск товаров
- Добавление в корзину
- Процесс оформления заказа
- Система отзывов
- Рекомендации товаров
- Избранное

### 3. Social Network Module
**Страницы:**
- `pages/social.js` - Лента постов, профили, связи

**Файлы:**
- `components/forms.js` - Формы постов и комментариев
- `components/modals.js` - Модальные окна постов
- `services/social.js` - API Social Network
- `utils/social_feed.js` - Утилиты социальной ленты
- `utils/social_connections.js` - Утилиты связей

**Функциональность:**
- Создание и редактирование постов
- Лайки и комментарии
- Система подписок
- Чаты в реальном времени
- Уведомления
- Поиск пользователей

### 4. Task Management Module
**Страницы:**
- `pages/tasks.js` - Доски задач, Kanban интерфейс

**Файлы:**
- `components/forms.js` - Формы задач
- `components/modals.js` - Модальные окна задач
- `services/tasks.js` - API Task Management

**Функциональность:**
- Drag & drop задачи
- Создание и редактирование карточек
- Назначение исполнителей
- Комментарии к задачам
- Уведомления о дедлайнах
- Аналитика проектов

### 5. Content Management Module
**Страницы:**
- `pages/content.js` - Статьи, редактор, медиа

**Файлы:**
- `components/forms.js` - Формы статей
- `components/modals.js` - Модальные окна контента
- `services/content.js` - API Content Management
- `utils/media_upload.js` - Утилиты загрузки медиа

**Функциональность:**
- Rich text редактор
- Загрузка медиа файлов
- Система категорий и тегов
- Модерация контента
- Поиск по статьям
- Комментарии к статьям

### 6. Analytics & Dashboard Module
**Страницы:**
- `pages/analytics.js` - Главная панель, отчеты, метрики

**Файлы:**
- `components/forms.js` - Формы отчетов
- `components/modals.js` - Модальные окна аналитики
- `services/analytics.js` - API Analytics
- `utils/advanced_analytics_manager.js` - Продвинутая аналитика

**Функциональность:**
- Интерактивные графики
- Настраиваемые виджеты
- Экспорт данных
- Фильтры и даты
- Уведомления о метриках
- Шаблоны дашбордов

## Технологический стек

- **HTML5** - разметка
- **CSS3** - стили с модульной архитектурой
- **Vanilla JavaScript (ES6+)** - логика без фреймворков
- **Fetch API** - HTTP запросы
- **Local Storage** - локальное хранилище
- **Service Worker** - PWA функциональность
- **WebSockets** - реальное время
- **Chart.js** - графики и диаграммы
- **Quill.js** - rich text редактор
- **Sortable.js** - drag & drop для Kanban досок
- **Intersection Observer API** - ленивая загрузка
- **Web Workers** - фоновые задачи
- **IndexedDB** - клиентская база данных

## Компоненты

### Общие компоненты (components/)
- `forms.js` - Формы входа, регистрации, профиля
- `modals.js` - Модальные окна для всех модулей
- `advanced_forms.js` - Продвинутые формы с валидацией
- `advanced_modals.js` - Продвинутые модальные окна
- `advanced_tables.js` - Продвинутые таблицы с сортировкой
- `toast.js` - Система уведомлений

### E-commerce компоненты
- Формы заказа в `components/forms.js`
- Модальные окна товаров в `components/modals.js`
- Карточки товаров в `pages/ecommerce.js`

### Social Network компоненты
- Формы постов в `components/forms.js`
- Модальные окна постов в `components/modals.js`
- Лента постов в `pages/social.js`
- Утилиты социальных связей в `utils/social_connections.js`

### Task Management компоненты
- Формы задач в `components/forms.js`
- Kanban доски в `pages/tasks.js`
- Drag & drop функциональность

### Content Management компоненты
- Формы статей в `components/forms.js`
- Rich text редактор
- Загрузка медиа в `utils/media_upload.js`

### Analytics компоненты
- Формы отчетов в `components/forms.js`
- Графики и диаграммы в `pages/analytics.js`
- Продвинутая аналитика в `utils/advanced_analytics_manager.js`

## State Management

### Глобальное состояние (utils/)
- `auth.js` - Аутентификация и управление токенами
- `common.js` - Общие утилиты состояния
- `constants.js` - Константы приложения
- `notifications.js` - Система уведомлений
- `settings_manager.js` - Менеджер настроек

### Модульное состояние
- `services/ecommerce.js` - E-commerce данные и API
- `services/social.js` - Social network данные и API
- `services/tasks.js` - Task management данные и API
- `services/content.js` - Content management данные и API
- `services/analytics.js` - Analytics данные и API

### Специализированные менеджеры
- `utils/advanced_analytics_manager.js` - Продвинутая аналитика
- `utils/advanced_notifications_manager.js` - Продвинутые уведомления
- `utils/roles_manager.js` - Менеджер ролей
- `utils/security_manager.js` - Менеджер безопасности

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
