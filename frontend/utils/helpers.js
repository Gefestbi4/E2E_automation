/**
 * Вспомогательные функции
 */

// Утилиты для работы с датами
const DateUtils = {
    // Форматирование даты
    format(date, format = 'DD.MM.YYYY') {
        if (!date) return '';

        const d = new Date(date);
        if (isNaN(d.getTime())) return '';

        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');

        return format
            .replace('DD', day)
            .replace('MM', month)
            .replace('YYYY', year)
            .replace('HH', hours)
            .replace('mm', minutes);
    },

    // Относительное время
    timeAgo(date) {
        if (!date) return '';

        const now = new Date();
        const past = new Date(date);
        const diffInSeconds = Math.floor((now - past) / 1000);

        if (diffInSeconds < 60) return 'только что';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} мин назад`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} ч назад`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} дн назад`;

        return this.format(date);
    },

    // Проверка, сегодня ли дата
    isToday(date) {
        if (!date) return false;

        const today = new Date();
        const checkDate = new Date(date);

        return today.toDateString() === checkDate.toDateString();
    },

    // Добавление дней к дате
    addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    },

    // Разница между датами в днях
    daysDifference(date1, date2) {
        const d1 = new Date(date1);
        const d2 = new Date(date2);
        const diffTime = Math.abs(d2 - d1);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
};

// Утилиты для работы с числами
const NumberUtils = {
    // Форматирование валюты
    formatCurrency(amount, currency = '₽') {
        if (amount === null || amount === undefined) return '0 ' + currency;

        return new Intl.NumberFormat('ru-RU', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        }).format(amount) + ' ' + currency;
    },

    // Форматирование числа
    formatNumber(number, decimals = 0) {
        if (number === null || number === undefined) return '0';

        return new Intl.NumberFormat('ru-RU', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);
    },

    // Сокращение больших чисел
    abbreviateNumber(number) {
        if (number < 1000) return String(number);
        if (number < 1000000) return (number / 1000).toFixed(1) + 'K';
        if (number < 1000000000) return (number / 1000000).toFixed(1) + 'M';
        return (number / 1000000000).toFixed(1) + 'B';
    },

    // Проверка, является ли число четным
    isEven(number) {
        return number % 2 === 0;
    },

    // Генерация случайного числа в диапазоне
    random(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    // Округление до указанного количества знаков
    round(number, decimals = 2) {
        return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
    }
};

// Утилиты для работы со строками
const StringUtils = {
    // Обрезка строки
    truncate(str, length = 100, suffix = '...') {
        if (!str || str.length <= length) return str;
        return str.substring(0, length) + suffix;
    },

    // Заглавная первая буква
    capitalize(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    },

    // Создание slug из строки
    slugify(str) {
        if (!str) return '';
        return str
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, '-')
            .replace(/^-+|-+$/g, '');
    },

    // Проверка, является ли строка email
    isEmail(str) {
        return Constants.REGEX.EMAIL.test(str);
    },

    // Проверка, является ли строка URL
    isUrl(str) {
        return Constants.REGEX.URL.test(str);
    },

    // Экранирование HTML
    escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    },

    // Подсветка поискового запроса
    highlight(str, query) {
        if (!query || !str) return str;

        const regex = new RegExp(`(${query})`, 'gi');
        return str.replace(regex, '<mark>$1</mark>');
    }
};

// Утилиты для работы с DOM
const DOMUtils = {
    // Создание элемента
    createElement(tag, className = '', content = '') {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (content) element.innerHTML = content;
        return element;
    },

    // Поиск элемента
    $(selector, parent = document) {
        return parent.querySelector(selector);
    },

    // Поиск всех элементов
    $$(selector, parent = document) {
        return Array.from(parent.querySelectorAll(selector));
    },

    // Добавление класса
    addClass(element, className) {
        if (element) element.classList.add(className);
    },

    // Удаление класса
    removeClass(element, className) {
        if (element) element.classList.remove(className);
    },

    // Переключение класса
    toggleClass(element, className) {
        if (element) element.classList.toggle(className);
    },

    // Проверка наличия класса
    hasClass(element, className) {
        return element ? element.classList.contains(className) : false;
    },

    // Показать элемент
    show(element) {
        if (element) element.style.display = '';
    },

    // Скрыть элемент
    hide(element) {
        if (element) element.style.display = 'none';
    },

    // Анимация появления
    fadeIn(element, duration = 300) {
        if (!element) return;

        element.style.opacity = '0';
        element.style.display = '';

        let start = performance.now();

        function animate(time) {
            const elapsed = time - start;
            const progress = Math.min(elapsed / duration, 1);

            element.style.opacity = progress;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    },

    // Анимация исчезновения
    fadeOut(element, duration = 300) {
        if (!element) return;

        let start = performance.now();

        function animate(time) {
            const elapsed = time - start;
            const progress = Math.min(elapsed / duration, 1);

            element.style.opacity = 1 - progress;

            if (progress >= 1) {
                element.style.display = 'none';
            } else {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    }
};

// Утилиты для работы с локальным хранилищем
const StorageUtils = {
    // Сохранение данных
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Ошибка сохранения в localStorage:', error);
            return false;
        }
    },

    // Получение данных
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Ошибка чтения из localStorage:', error);
            return defaultValue;
        }
    },

    // Удаление данных
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Ошибка удаления из localStorage:', error);
            return false;
        }
    },

    // Очистка всех данных
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Ошибка очистки localStorage:', error);
            return false;
        }
    },

    // Проверка поддержки localStorage
    isSupported() {
        try {
            const test = '__localStorage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (error) {
            return false;
        }
    }
};

// Утилиты для работы с файлами
const FileUtils = {
    // Проверка типа файла
    isValidType(file, allowedTypes) {
        return allowedTypes.includes(file.type);
    },

    // Проверка размера файла
    isValidSize(file, maxSize = Constants.FILE_CONFIG.MAX_SIZE) {
        return file.size <= maxSize;
    },

    // Форматирование размера файла
    formatSize(bytes) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Чтение файла как текста
    readAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    },

    // Чтение файла как URL
    readAsURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    },

    // Скачивание файла
    download(data, filename, type = 'application/octet-stream') {
        const blob = new Blob([data], { type });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }
};

// Утилиты для работы с URL
const URLUtils = {
    // Получение параметров URL
    getParams() {
        const params = new URLSearchParams(window.location.search);
        const result = {};

        for (const [key, value] of params) {
            result[key] = value;
        }

        return result;
    },

    // Установка параметра URL
    setParam(key, value) {
        const url = new URL(window.location);
        url.searchParams.set(key, value);
        window.history.pushState({}, '', url);
    },

    // Удаление параметра URL
    removeParam(key) {
        const url = new URL(window.location);
        url.searchParams.delete(key);
        window.history.pushState({}, '', url);
    },

    // Построение URL с параметрами
    buildURL(base, params = {}) {
        const url = new URL(base);

        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                url.searchParams.set(key, value);
            }
        });

        return url.toString();
    }
};

// Утилиты для работы с событиями
const EventUtils = {
    // Дебаунс
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Тротлинг
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Обработчик клавиш
    onKeyPress(element, key, handler) {
        element.addEventListener('keydown', (event) => {
            if (event.keyCode === key || event.key === key) {
                handler(event);
            }
        });
    },

    // Обработчик клика вне элемента
    onClickOutside(element, handler) {
        document.addEventListener('click', (event) => {
            if (!element.contains(event.target)) {
                handler(event);
            }
        });
    }
};

// Экспорт утилит
window.Utils = {
    Date: DateUtils,
    Number: NumberUtils,
    String: StringUtils,
    DOM: DOMUtils,
    Storage: StorageUtils,
    File: FileUtils,
    URL: URLUtils,
    Event: EventUtils
};
