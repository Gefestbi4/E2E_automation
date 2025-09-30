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

    def info(self, message: str, extra: Optional[dict] = None):
        """Log info message"""
        self.logger.info(message, extra=extra)

    def debug(self, message: str, extra: Optional[dict] = None):
        """Log debug message"""
        self.logger.debug(message, extra=extra)

    def warning(self, message: str, extra: Optional[dict] = None):
        """Log warning message"""
        self.logger.warning(message, extra=extra)

    def error(self, message: str, extra: Optional[dict] = None):
        """Log error message"""
        self.logger.error(message, extra=extra)

    def critical(self, message: str, extra: Optional[dict] = None):
        """Log critical message"""
        self.logger.critical(message, extra=extra)

    def test_start(self, test_name: str):
        """Log test start"""
        self.test_start_time = datetime.now()
        self.info(f"🚀 Starting test: {test_name}")

    def test_end(self, test_name: str, status: str = "PASSED"):
        """Log test end with duration"""
        duration = datetime.now() - self.test_start_time
        status_emoji = "✅" if status == "PASSED" else "❌"
        self.info(
            f"{status_emoji} Test {status}: {test_name} (Duration: {duration.total_seconds():.2f}s)"
        )

    def step(self, step_name: str, step_data: Optional[dict] = None):
        """Log test step"""
        message = f"📝 Step: {step_name}"
        if step_data:
            message += f" | Data: {step_data}"
        self.info(message)

    def assertion(
        self, assertion_name: str, expected: any, actual: any, passed: bool = True
    ):
        """Log assertion result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.info(
            f"{status} Assertion: {assertion_name} | Expected: {expected} | Actual: {actual}"
        )

    def api_request(
        self,
        method: str,
        url: str,
        status_code: int = None,
        response_time: float = None,
    ):
        """Log API request"""
        message = f"🌐 API {method}: {url}"
        if status_code:
            message += f" | Status: {status_code}"
        if response_time:
            message += f" | Time: {response_time:.2f}ms"
        self.info(message)

    def browser_action(self, action: str, element: str = None, value: str = None):
        """Log browser action"""
        message = f"🖱️ Browser: {action}"
        if element:
            message += f" | Element: {element}"
        if value:
            message += f" | Value: {value}"
        self.info(message)

    def screenshot(self, screenshot_path: str):
        """Log screenshot taken"""
        self.info(f"📸 Screenshot taken: {screenshot_path}")

    def performance(self, metric_name: str, value: float, unit: str = "ms"):
        """Log performance metric"""
        self.info(f"⚡ Performance: {metric_name} = {value:.2f}{unit}")

    def error_with_context(self, error: Exception, context: str = ""):
        """Log error with context"""
        error_msg = (
            f"❌ Error in {context}: {str(error)}"
            if context
            else f"❌ Error: {str(error)}"
        )
        self.error(error_msg)
        self.debug(
            f"Error details: {error.__class__.__name__}", extra={"exception": error}
        )

    def test_data(self, data_name: str, data_value: any):
        """Log test data usage"""
        self.debug(f"📊 Test Data: {data_name} = {data_value}")

    def environment_info(self, info: dict):
        """Log environment information"""
        self.info("🔧 Environment Info:")
        for key, value in info.items():
            self.info(f"  {key}: {value}")

    def test_summary(
        self, total_tests: int, passed: int, failed: int, skipped: int = 0
    ):
        """Log test summary"""
        self.info("📊 Test Summary:")
        self.info(f"  Total: {total_tests}")
        self.info(f"  Passed: {passed} ✅")
        self.info(f"  Failed: {failed} ❌")
        self.info(f"  Skipped: {skipped} ⏭️")

        if total_tests > 0:
            success_rate = (passed / total_tests) * 100
            self.info(f"  Success Rate: {success_rate:.1f}%")

    def cleanup(self):
        """Cleanup logger resources"""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
