"""
Configuration settings for E2E automation tests  # Документация конфигурации E2E тестов
"""

import os  # Импорт модуля для работы с переменными окружения
import json  # Импорт модуля для работы с JSON
from typing import Dict, Any, List  # Импорт типов для аннотаций типов
from pathlib import Path  # Импорт Path для работы с путями файлов


class Settings:  # Определение класса настроек
    """Centralized configuration for E2E tests"""  # Документация класса

    # Base URLs  # Комментарий о базовых URL
    FRONTEND_URL = os.getenv(
        "FRONTEND_URL", "http://frontend:80"
    )  # URL фронтенд приложения из переменной окружения
    BACKEND_URL = os.getenv(
        "BACKEND_URL", "http://backend:5000"
    )  # URL backend приложения из переменной окружения
    SELENIUM_HUB_URL = os.getenv(
        "SELENIUM_HUB_URL", "http://selenium-hub:4444/wd/hub"
    )  # URL Selenium Hub из переменной окружения
    ALLURE_SERVER_URL = os.getenv(
        "ALLURE_SERVER_URL", "http://allure:5050"
    )  # URL Allure сервера из переменной окружения

    # Test data  # Комментарий о тестовых данных
    TEST_EMAIL = os.getenv(
        "TEST_EMAIL", "test@example.com"
    )  # Email тестового пользователя из переменной окружения
    TEST_PASSWORD = os.getenv(
        "TEST_PASSWORD", "testpassword123"
    )  # Пароль тестового пользователя из переменной окружения
    ADMIN_EMAIL = os.getenv(
        "ADMIN_EMAIL", "admin@example.com"
    )  # Email администратора из переменной окружения
    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD", "adminpassword123"
    )  # Пароль администратора из переменной окружения
    API_KEY = os.getenv("API_KEY", "")  # API ключ из переменной окружения

    # Browser settings  # Комментарий о настройках браузера
    BROWSER_NAME = os.getenv(
        "BROWSER_NAME", "chrome"
    )  # Название браузера из переменной окружения
    IMPLICIT_WAIT = int(
        os.getenv("IMPLICIT_WAIT", "15")
    )  # Неявное ожидание в секундах из переменной окружения
    PAGE_LOAD_TIMEOUT = int(
        os.getenv("PAGE_LOAD_TIMEOUT", "30")
    )  # Таймаут загрузки страницы в секундах из переменной окружения
    EXPLICIT_WAIT = int(
        os.getenv("EXPLICIT_WAIT", "10")
    )  # Явное ожидание в секундах из переменной окружения

    # Test execution  # Комментарий о выполнении тестов
    HEADLESS = (
        os.getenv("HEADLESS", "false").lower() == "true"
    )  # Режим headless из переменной окружения
    SCREENSHOT_ON_FAILURE = (
        os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    )  # Скриншоты при падении из переменной окружения
    VIDEO_RECORDING = (
        os.getenv("VIDEO_RECORDING", "false").lower() == "true"
    )  # Запись видео из переменной окружения
    PARALLEL_EXECUTION = (
        os.getenv("PARALLEL_EXECUTION", "false").lower() == "true"
    )  # Параллельное выполнение из переменной окружения
    MAX_WORKERS = int(
        os.getenv("MAX_WORKERS", "4")
    )  # Максимальное количество воркеров из переменной окружения

    # Allure settings  # Комментарий о настройках Allure
    ALLURE_RESULTS_DIR = os.getenv(
        "ALLURE_RESULTS_DIR", "/app/allure-results"
    )  # Папка результатов Allure из переменной окружения
    ALLURE_REPORTS_DIR = os.getenv(
        "ALLURE_REPORTS_DIR", "/app/allure-reports"
    )  # Папка отчетов Allure из переменной окружения
    ALLURE_SERVER_TOKEN = os.getenv(
        "ALLURE_SERVER_TOKEN", ""
    )  # Токен Allure сервера из переменной окружения

    # Telegram settings  # Комментарий о настройках Telegram
    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN", ""
    )  # Токен Telegram бота из переменной окружения
    TELEGRAM_CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID", ""
    )  # ID чата Telegram из переменной окружения

    # Retry settings  # Комментарий о настройках повторов
    MAX_RETRIES = int(
        os.getenv("MAX_RETRIES", "2")
    )  # Максимальное количество повторов из переменной окружения
    RETRY_DELAY = int(
        os.getenv("RETRY_DELAY", "1")
    )  # Задержка между повторами в секундах из переменной окружения

    # Test data file  # Комментарий о файле тестовых данных
    TEST_DATA_FILE = os.getenv(
        "TEST_DATA_FILE", "/app/data/test_data.json"
    )  # Путь к файлу тестовых данных из переменной окружения

    @classmethod  # Декоратор для создания метода класса
    def load_test_data(
        cls,
    ) -> Dict[str, Any]:  # Метод загрузки тестовых данных из JSON файла
        """Load test data from JSON file"""  # Документация метода
        try:  # Начало блока обработки исключений
            with open(
                cls.TEST_DATA_FILE, "r", encoding="utf-8"
            ) as f:  # Открытие файла тестовых данных для чтения
                return json.load(f)  # Загрузка JSON данных из файла
        except FileNotFoundError:  # Обработка исключения файл не найден
            print(  # Вывод предупреждения в консоль
                f"Warning: Test data file {cls.TEST_DATA_FILE} not found, using defaults"
            )
            return cls.get_default_test_data()  # Возврат данных по умолчанию

    @classmethod  # Декоратор для создания метода класса
    def get_default_test_data(
        cls,
    ) -> Dict[str, Any]:  # Метод получения тестовых данных по умолчанию
        """Get default test data"""  # Документация метода
        return {  # Возврат словаря с тестовыми данными
            "users": {  # Секция пользователей
                "regular_user": {  # Обычный пользователь
                    "email": cls.TEST_EMAIL,  # Email из настроек
                    "password": cls.TEST_PASSWORD,  # Пароль из настроек
                    "username": "test",  # Имя пользователя
                    "full_name": "Test User",  # Полное имя
                },
                "admin_user": {  # Администратор
                    "email": cls.ADMIN_EMAIL,  # Email администратора из настроек
                    "password": cls.ADMIN_PASSWORD,  # Пароль администратора из настроек
                    "username": "admin",  # Имя администратора
                    "full_name": "Admin User",  # Полное имя администратора
                },
            },
            "products": {  # Секция товаров
                "sample_products": [  # Список примеров товаров
                    {  # Пример товара
                        "id": 1,  # ID товара
                        "name": "Laptop Pro 15",  # Название товара
                        "price": 1299.99,  # Цена товара
                        "category": "Electronics",  # Категория товара
                        "description": "High-performance laptop for professionals",  # Описание товара
                    }
                ]
            },
            "api_endpoints": {  # Секция API endpoints
                "authentication": [  # Endpoints аутентификации
                    "POST /api/auth/register",  # Регистрация пользователя
                    "POST /api/auth/login",  # Вход в систему
                    "GET /api/auth/me",  # Получение информации о текущем пользователе
                ],
                "ecommerce": [  # Endpoints e-commerce
                    "GET /api/ecommerce/products",  # Получение списка товаров
                    "POST /api/ecommerce/products",  # Создание товара
                    "GET /api/ecommerce/cart",  # Получение корзины
                ],
            },
        }

    @classmethod  # Декоратор для создания метода класса
    def get_browser_options(cls) -> Dict[str, Any]:  # Метод получения опций браузера
        """Get browser-specific options"""  # Документация метода
        options = {  # Словарь с опциями браузеров
            "chrome": {  # Опции для Chrome
                "args": [  # Аргументы командной строки Chrome
                    "--no-sandbox",  # Отключение sandbox режима
                    "--disable-dev-shm-usage",  # Отключение использования /dev/shm
                    "--disable-gpu",  # Отключение GPU ускорения
                    "--disable-blink-features=AutomationControlled",  # Отключение автоматизации
                    "--disable-extensions",  # Отключение расширений
                    "--disable-plugins",  # Отключение плагинов
                    "--disable-web-security",  # Отключение веб безопасности
                    "--allow-running-insecure-content",  # Разрешение небезопасного контента
                    "--ignore-certificate-errors",  # Игнорирование ошибок сертификатов
                    "--ignore-ssl-errors",  # Игнорирование SSL ошибок
                    "--ignore-certificate-errors-spki-list",  # Игнорирование ошибок SPKI
                    "--disable-features=VizDisplayCompositor",  # Отключение VizDisplayCompositor
                    "--window-size=1920,1080",  # Размер окна браузера
                ],
                "experimental_options": {  # Экспериментальные опции Chrome
                    "excludeSwitches": [
                        "enable-automation"
                    ],  # Исключение переключателей автоматизации
                    "useAutomationExtension": False,  # Отключение расширения автоматизации
                },
                "prefs": {  # Предпочтения Chrome
                    "profile.default_content_setting_values.notifications": 2,  # Отключение уведомлений
                    "profile.default_content_settings.popups": 0,  # Отключение всплывающих окон
                    "profile.managed_default_content_settings.images": 2,  # Отключение изображений
                },
            },
            "firefox": {  # Опции для Firefox
                "args": [  # Аргументы командной строки Firefox
                    "--no-sandbox",  # Отключение sandbox режима
                    "--disable-dev-shm-usage",  # Отключение использования /dev/shm
                    "--disable-gpu",  # Отключение GPU ускорения
                    "--width=1920",  # Ширина окна браузера
                    "--height=1080",  # Высота окна браузера
                ],
                "prefs": {  # Предпочтения Firefox
                    "dom.webnotifications.enabled": False,  # Отключение веб уведомлений
                    "dom.push.enabled": False,  # Отключение push уведомлений
                },
            },
        }

        if cls.HEADLESS:  # Проверка режима headless
            options["chrome"]["args"].extend(
                ["--headless=new"]
            )  # Добавление headless режима для Chrome
            options["firefox"]["args"].extend(
                ["--headless"]
            )  # Добавление headless режима для Firefox

        return options.get(
            cls.BROWSER_NAME, {}
        )  # Возврат опций для выбранного браузера

    @classmethod  # Декоратор для создания метода класса
    def get_test_data(cls) -> Dict[str, Any]:  # Метод получения тестовых данных
        """Get test data configuration"""  # Документация метода
        return cls.load_test_data()  # Возврат загруженных тестовых данных

    @classmethod  # Декоратор для создания метода класса
    def get_api_endpoints(cls) -> Dict[str, List[str]]:  # Метод получения API endpoints
        """Get API endpoints for testing"""  # Документация метода
        test_data = cls.get_test_data()  # Получение тестовых данных
        return test_data.get(
            "api_endpoints", {}
        )  # Возврат API endpoints из тестовых данных

    @classmethod  # Декоратор для создания метода класса
    def get_user_credentials(
        cls, user_type: str = "regular_user"
    ) -> Dict[str, str]:  # Метод получения учетных данных пользователя
        """Get user credentials by type"""  # Документация метода
        test_data = cls.get_test_data()  # Получение тестовых данных
        users = test_data.get("users", {})  # Получение секции пользователей
        return users.get(  # Возврат учетных данных пользователя
            user_type,  # Тип пользователя
            {  # Данные по умолчанию если тип не найден
                "email": cls.TEST_EMAIL,  # Email из настроек
                "password": cls.TEST_PASSWORD,  # Пароль из настроек
                "username": "test",  # Имя пользователя по умолчанию
                "full_name": "Test User",  # Полное имя по умолчанию
            },
        )

    @classmethod  # Декоратор для создания метода класса
    def get_product_data(
        cls, product_id: int = 1
    ) -> Dict[str, Any]:  # Метод получения данных товара по ID
        """Get product data by ID"""  # Документация метода
        test_data = cls.get_test_data()  # Получение тестовых данных
        products = test_data.get("products", {}).get(
            "sample_products", []
        )  # Получение списка товаров
        for product in products:  # Цикл по товарам
            if product.get("id") == product_id:  # Проверка ID товара
                return product  # Возврат найденного товара
        return {}  # Возврат пустого словаря если товар не найден

    @classmethod  # Декоратор для создания метода класса
    def get_environment_info(
        cls,
    ) -> Dict[str, str]:  # Метод получения информации об окружении
        """Get environment information for reporting"""  # Документация метода
        return {  # Возврат словаря с информацией об окружении
            "frontend_url": cls.FRONTEND_URL,  # URL фронтенда
            "backend_url": cls.BACKEND_URL,  # URL бэкенда
            "browser": cls.BROWSER_NAME,  # Название браузера
            "headless": str(cls.HEADLESS),  # Режим headless как строка
            "parallel": str(
                cls.PARALLEL_EXECUTION
            ),  # Параллельное выполнение как строка
            "max_workers": str(
                cls.MAX_WORKERS
            ),  # Максимальное количество воркеров как строка
        }
