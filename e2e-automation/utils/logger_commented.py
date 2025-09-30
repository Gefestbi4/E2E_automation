"""
Test logger utility for E2E automation  # Документация утилиты логирования для E2E автоматизации
"""

import logging  # Импорт модуля логирования Python
import os  # Импорт модуля для работы с операционной системой
from datetime import datetime  # Импорт класса datetime для работы с датой и временем
from typing import Optional  # Импорт типа Optional для аннотаций типов
from pathlib import Path  # Импорт Path для работы с путями файлов


class TestLogger:  # Определение класса логгера тестов
    """Enhanced logger for E2E tests with file and console output"""  # Документация класса

    def __init__(
        self, name: str = "E2E_Test", log_level: str = "INFO"
    ):  # Конструктор класса TestLogger
        self.name = name  # Инициализация имени логгера
        self.log_level = getattr(
            logging, log_level.upper(), logging.INFO
        )  # Установка уровня логирования
        self.logger = self._setup_logger()  # Настройка логгера
        self.test_start_time = datetime.now()  # Инициализация времени начала теста

    def _setup_logger(self) -> logging.Logger:  # Приватный метод настройки логгера
        """Setup logger with file and console handlers"""  # Документация метода
        logger = logging.getLogger(self.name)  # Получение логгера по имени
        logger.setLevel(self.log_level)  # Установка уровня логирования

        # Clear existing handlers  # Комментарий об очистке существующих обработчиков
        logger.handlers.clear()  # Очистка всех существующих обработчиков

        # Create logs directory if it doesn't exist  # Комментарий о создании папки логов
        log_dir = Path("/app/logs")  # Создание пути к папке логов
        log_dir.mkdir(exist_ok=True)  # Создание папки логов если она не существует

        # File handler  # Комментарий о файловом обработчике
        log_file = (
            log_dir / f"e2e_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )  # Создание имени файла лога с временной меткой
        file_handler = logging.FileHandler(
            log_file, encoding="utf-8"
        )  # Создание файлового обработчика
        file_handler.setLevel(
            self.log_level
        )  # Установка уровня логирования для файлового обработчика

        # Console handler  # Комментарий о консольном обработчике
        console_handler = logging.StreamHandler()  # Создание консольного обработчика
        console_handler.setLevel(
            self.log_level
        )  # Установка уровня логирования для консольного обработчика

        # Formatter  # Комментарий о форматтере
        formatter = logging.Formatter(  # Создание форматтера логов
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщения лога
            datefmt="%Y-%m-%d %H:%M:%S",  # Формат даты и времени
        )
        file_handler.setFormatter(
            formatter
        )  # Установка форматтера для файлового обработчика
        console_handler.setFormatter(
            formatter
        )  # Установка форматтера для консольного обработчика

        # Add handlers  # Комментарий о добавлении обработчиков
        logger.addHandler(file_handler)  # Добавление файлового обработчика к логгеру
        logger.addHandler(
            console_handler
        )  # Добавление консольного обработчика к логгеру

        return logger  # Возврат настроенного логгера

    def info(
        self, message: str, extra: Optional[dict] = None
    ):  # Метод логирования информационных сообщений
        """Log info message"""  # Документация метода
        self.logger.info(message, extra=extra)  # Логирование информационного сообщения

    def debug(
        self, message: str, extra: Optional[dict] = None
    ):  # Метод логирования отладочных сообщений
        """Log debug message"""  # Документация метода
        self.logger.debug(message, extra=extra)  # Логирование отладочного сообщения

    def warning(
        self, message: str, extra: Optional[dict] = None
    ):  # Метод логирования предупреждений
        """Log warning message"""  # Документация метода
        self.logger.warning(message, extra=extra)  # Логирование предупреждения

    def error(
        self, message: str, extra: Optional[dict] = None
    ):  # Метод логирования ошибок
        """Log error message"""  # Документация метода
        self.logger.error(message, extra=extra)  # Логирование ошибки

    def critical(
        self, message: str, extra: Optional[dict] = None
    ):  # Метод логирования критических ошибок
        """Log critical message"""  # Документация метода
        self.logger.critical(message, extra=extra)  # Логирование критической ошибки

    def test_start(self, test_name: str):  # Метод логирования начала теста
        """Log test start"""  # Документация метода
        self.test_start_time = datetime.now()  # Установка времени начала теста
        self.info(f"🚀 Starting test: {test_name}")  # Логирование начала теста с эмодзи

    def test_end(
        self, test_name: str, status: str = "PASSED"
    ):  # Метод логирования окончания теста
        """Log test end with duration"""  # Документация метода
        duration = (
            datetime.now() - self.test_start_time
        )  # Вычисление длительности теста
        status_emoji = (
            "✅" if status == "PASSED" else "❌"
        )  # Выбор эмодзи в зависимости от статуса
        self.info(  # Логирование окончания теста
            f"{status_emoji} Test {status}: {test_name} (Duration: {duration.total_seconds():.2f}s)"
        )

    def step(
        self, step_name: str, step_data: Optional[dict] = None
    ):  # Метод логирования шага теста
        """Log test step"""  # Документация метода
        message = f"📝 Step: {step_name}"  # Создание сообщения о шаге
        if step_data:  # Проверка наличия данных шага
            message += f" | Data: {step_data}"  # Добавление данных к сообщению
        self.info(message)  # Логирование шага

    def assertion(  # Метод логирования результата проверки
        self, assertion_name: str, expected: any, actual: any, passed: bool = True
    ):
        """Log assertion result"""  # Документация метода
        status = "✅ PASS" if passed else "❌ FAIL"  # Определение статуса проверки
        self.info(  # Логирование результата проверки
            f"{status} Assertion: {assertion_name} | Expected: {expected} | Actual: {actual}"
        )

    def api_request(  # Метод логирования API запроса
        self,
        method: str,
        url: str,
        status_code: int = None,
        response_time: float = None,
    ):
        """Log API request"""  # Документация метода
        message = f"🌐 API {method}: {url}"  # Создание сообщения об API запросе
        if status_code:  # Проверка наличия статус кода
            message += f" | Status: {status_code}"  # Добавление статус кода к сообщению
        if response_time:  # Проверка наличия времени ответа
            message += f" | Time: {response_time:.2f}ms"  # Добавление времени ответа к сообщению
        self.info(message)  # Логирование API запроса

    def browser_action(
        self, action: str, element: str = None, value: str = None
    ):  # Метод логирования действия браузера
        """Log browser action"""  # Документация метода
        message = f"🖱️ Browser: {action}"  # Создание сообщения о действии браузера
        if element:  # Проверка наличия элемента
            message += f" | Element: {element}"  # Добавление элемента к сообщению
        if value:  # Проверка наличия значения
            message += f" | Value: {value}"  # Добавление значения к сообщению
        self.info(message)  # Логирование действия браузера

    def screenshot(self, screenshot_path: str):  # Метод логирования создания скриншота
        """Log screenshot taken"""  # Документация метода
        self.info(
            f"📸 Screenshot taken: {screenshot_path}"
        )  # Логирование создания скриншота

    def performance(
        self, metric_name: str, value: float, unit: str = "ms"
    ):  # Метод логирования метрики производительности
        """Log performance metric"""  # Документация метода
        self.info(
            f"⚡ Performance: {metric_name} = {value:.2f}{unit}"
        )  # Логирование метрики производительности

    def error_with_context(
        self, error: Exception, context: str = ""
    ):  # Метод логирования ошибки с контекстом
        """Log error with context"""  # Документация метода
        error_msg = (  # Создание сообщения об ошибке
            f"❌ Error in {context}: {str(error)}"  # Сообщение с контекстом
            if context  # Если контекст указан
            else f"❌ Error: {str(error)}"  # Сообщение без контекста
        )
        self.error(error_msg)  # Логирование ошибки
        self.debug(  # Логирование деталей ошибки
            f"Error details: {error.__class__.__name__}", extra={"exception": error}
        )

    def test_data(
        self, data_name: str, data_value: any
    ):  # Метод логирования тестовых данных
        """Log test data usage"""  # Документация метода
        self.debug(
            f"📊 Test Data: {data_name} = {data_value}"
        )  # Логирование использования тестовых данных

    def environment_info(self, info: dict):  # Метод логирования информации об окружении
        """Log environment information"""  # Документация метода
        self.info(
            "🔧 Environment Info:"
        )  # Логирование заголовка информации об окружении
        for key, value in info.items():  # Цикл по информации об окружении
            self.info(f"  {key}: {value}")  # Логирование каждого параметра окружения

    def test_summary(  # Метод логирования сводки тестов
        self, total_tests: int, passed: int, failed: int, skipped: int = 0
    ):
        """Log test summary"""  # Документация метода
        self.info("📊 Test Summary:")  # Логирование заголовка сводки
        self.info(f"  Total: {total_tests}")  # Логирование общего количества тестов
        self.info(f"  Passed: {passed} ✅")  # Логирование количества пройденных тестов
        self.info(f"  Failed: {failed} ❌")  # Логирование количества проваленных тестов
        self.info(
            f"  Skipped: {skipped} ⏭️"
        )  # Логирование количества пропущенных тестов

        if total_tests > 0:  # Проверка что тесты были запущены
            success_rate = (
                passed / total_tests
            ) * 100  # Вычисление процента успешности
            self.info(
                f"  Success Rate: {success_rate:.1f}%"
            )  # Логирование процента успешности

    def cleanup(self):  # Метод очистки ресурсов логгера
        """Cleanup logger resources"""  # Документация метода
        for handler in self.logger.handlers[:]:  # Цикл по всем обработчикам логгера
            handler.close()  # Закрытие обработчика
            self.logger.removeHandler(handler)  # Удаление обработчика из логгера
