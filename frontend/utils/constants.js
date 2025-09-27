/**
 * Константы приложения
 */

// API конфигурация
const API_CONFIG = {
    BASE_URL: document.querySelector('meta[name="api-base"]')?.content || 'http://localhost:5000',
    ENDPOINTS: {
        AUTH: {
            LOGIN: '/api/auth/login',
            REGISTER: '/api/auth/register',
            REFRESH: '/api/auth/refresh',
            LOGOUT: '/api/auth/logout',
            ME: '/api/auth/me'
        },
        ECOMMERCE: {
            PRODUCTS: '/api/ecommerce/products',
            CATEGORIES: '/api/ecommerce/categories',
            CART: '/api/ecommerce/cart',
            ORDERS: '/api/ecommerce/orders'
        },
        SOCIAL: {
            POSTS: '/api/social/posts',
            COMMENTS: '/api/social/comments',
            USERS: '/api/social/users',
            FOLLOWS: '/api/social/follows',
            MESSAGES: '/api/social/messages'
        },
        TASKS: {
            PROJECTS: '/api/tasks/projects',
            BOARDS: '/api/tasks/boards',
            TASKS: '/api/tasks/tasks',
            TIME_ENTRIES: '/api/tasks/time-entries'
        },
        CONTENT: {
            ARTICLES: '/api/content/articles',
            CATEGORIES: '/api/content/categories',
            MEDIA: '/api/content/media',
            COMMENTS: '/api/content/comments'
        },
        ANALYTICS: {
            DASHBOARD: '/api/analytics/dashboard',
            METRICS: '/api/analytics/metrics',
            REPORTS: '/api/analytics/reports'
        }
    },
    TIMEOUT: 10000,
    RETRY_ATTEMPTS: 3
};

// Статусы и типы
const STATUS = {
    LOADING: 'loading',
    SUCCESS: 'success',
    ERROR: 'error',
    IDLE: 'idle'
};

const TASK_STATUS = {
    TODO: 'todo',
    IN_PROGRESS: 'in_progress',
    IN_REVIEW: 'in_review',
    DONE: 'done',
    CANCELLED: 'cancelled'
};

const TASK_PRIORITY = {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    URGENT: 'urgent'
};

const CONTENT_STATUS = {
    DRAFT: 'draft',
    PUBLISHED: 'published',
    ARCHIVED: 'archived',
    SCHEDULED: 'scheduled'
};

// Сообщения
const MESSAGES = {
    SUCCESS: {
        LOGIN: 'Успешный вход в систему',
        LOGOUT: 'Успешный выход из системы',
        SAVE: 'Данные успешно сохранены',
        DELETE: 'Успешно удалено',
        UPDATE: 'Данные обновлены'
    },
    ERROR: {
        LOGIN: 'Ошибка входа в систему',
        LOGOUT: 'Ошибка выхода из системы',
        SAVE: 'Ошибка сохранения данных',
        DELETE: 'Ошибка удаления',
        UPDATE: 'Ошибка обновления данных',
        NETWORK: 'Ошибка сети',
        UNAUTHORIZED: 'Необходима авторизация',
        FORBIDDEN: 'Доступ запрещен',
        NOT_FOUND: 'Ресурс не найден',
        SERVER_ERROR: 'Ошибка сервера'
    },
    VALIDATION: {
        REQUIRED: 'Поле обязательно для заполнения',
        EMAIL: 'Некорректный email',
        PASSWORD: 'Пароль должен содержать минимум 8 символов',
        CONFIRM_PASSWORD: 'Пароли не совпадают',
        MIN_LENGTH: 'Минимальная длина',
        MAX_LENGTH: 'Максимальная длина'
    }
};

// Локализация
const LOCALE = {
    DATE_FORMAT: 'DD.MM.YYYY',
    TIME_FORMAT: 'HH:mm',
    DATETIME_FORMAT: 'DD.MM.YYYY HH:mm',
    CURRENCY: '₽',
    DECIMAL_SEPARATOR: ',',
    THOUSANDS_SEPARATOR: ' '
};

// Настройки пагинации
const PAGINATION = {
    DEFAULT_PAGE_SIZE: 20,
    PAGE_SIZES: [10, 20, 50, 100],
    MAX_PAGES_SHOWN: 7
};

// Настройки файлов
const FILE_CONFIG = {
    MAX_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_TYPES: {
        IMAGE: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
        DOCUMENT: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        TEXT: ['text/plain', 'text/csv'],
        ALL: ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'text/plain', 'text/csv']
    }
};

// Настройки уведомлений
const TOAST_CONFIG = {
    DEFAULT_DURATION: 3000,
    SUCCESS_DURATION: 2000,
    ERROR_DURATION: 5000,
    POSITION: 'top-right'
};

// Настройки анимации
const ANIMATION = {
    DURATION: {
        FAST: 150,
        NORMAL: 300,
        SLOW: 500
    },
    EASING: {
        EASE: 'ease',
        EASE_IN: 'ease-in',
        EASE_OUT: 'ease-out',
        EASE_IN_OUT: 'ease-in-out'
    }
};

// Клавиши
const KEYS = {
    ENTER: 13,
    ESCAPE: 27,
    SPACE: 32,
    ARROW_UP: 38,
    ARROW_DOWN: 40,
    ARROW_LEFT: 37,
    ARROW_RIGHT: 39,
    TAB: 9,
    BACKSPACE: 8,
    DELETE: 46
};

// Регулярные выражения
const REGEX = {
    EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    PHONE: /^[\+]?[1-9][\d]{0,15}$/,
    URL: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
    SLUG: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
    PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/
};

// Экспорт констант
window.Constants = {
    API_CONFIG,
    STATUS,
    TASK_STATUS,
    TASK_PRIORITY,
    CONTENT_STATUS,
    MESSAGES,
    LOCALE,
    PAGINATION,
    FILE_CONFIG,
    TOAST_CONFIG,
    ANIMATION,
    KEYS,
    REGEX
};
