"""
Утилиты для логирования
"""

import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime
import json
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """JSON форматтер для логов"""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Добавляем дополнительные поля если есть
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id

        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        if hasattr(record, "duration"):
            log_entry["duration"] = record.duration

        if hasattr(record, "status_code"):
            log_entry["status_code"] = record.status_code

        if hasattr(record, "method"):
            log_entry["method"] = record.method

        if hasattr(record, "path"):
            log_entry["path"] = record.path

        if hasattr(record, "ip_address"):
            log_entry["ip_address"] = record.ip_address

        # Добавляем исключение если есть
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


class LoggerSetup:
    """Настройка логгера"""

    @staticmethod
    def setup_logging(
        log_level: str = "INFO",
        log_format: str = "json",
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """Настройка системы логирования"""

        # Создаем корневой логгер
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level.upper()))

        # Очищаем существующие обработчики
        logger.handlers.clear()

        # Настраиваем форматтер
        if log_format.lower() == "json":
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Файловый обработчик если указан
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Получить логгер по имени"""
        return logging.getLogger(name)


class RequestLogger:
    """Логгер для HTTP запросов"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration: float,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        """Логирование HTTP запроса"""
        self.logger.info(
            f"{method} {path} - {status_code}",
            extra={
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration": duration,
                "user_id": user_id,
                "ip_address": ip_address,
                "request_id": request_id,
            },
        )

    def log_error(
        self,
        error: Exception,
        method: str,
        path: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        """Логирование ошибки"""
        self.logger.error(
            f"Error in {method} {path}: {str(error)}",
            extra={
                "method": method,
                "path": path,
                "user_id": user_id,
                "ip_address": ip_address,
                "request_id": request_id,
            },
            exc_info=True,
        )


class DatabaseLogger:
    """Логгер для операций с базой данных"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_query(
        self, operation: str, table: str, duration: float, user_id: Optional[int] = None
    ):
        """Логирование запроса к БД"""
        self.logger.debug(
            f"DB {operation} on {table}",
            extra={
                "operation": operation,
                "table": table,
                "duration": duration,
                "user_id": user_id,
            },
        )

    def log_error(
        self,
        error: Exception,
        operation: str,
        table: str,
        user_id: Optional[int] = None,
    ):
        """Логирование ошибки БД"""
        self.logger.error(
            f"DB Error in {operation} on {table}: {str(error)}",
            extra={"operation": operation, "table": table, "user_id": user_id},
            exc_info=True,
        )


class BusinessLogicLogger:
    """Логгер для бизнес-логики"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_user_action(
        self,
        action: str,
        user_id: int,
        resource_type: str,
        resource_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Логирование действий пользователя"""
        self.logger.info(
            f"User {user_id} performed {action} on {resource_type}",
            extra={
                "action": action,
                "user_id": user_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": details or {},
            },
        )

    def log_business_event(
        self,
        event: str,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Логирование бизнес-событий"""
        self.logger.info(
            f"Business event: {event}",
            extra={"event": event, "user_id": user_id, "details": details or {}},
        )


class SecurityLogger:
    """Логгер для событий безопасности"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_auth_attempt(
        self,
        email: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Логирование попытки аутентификации"""
        level = logging.INFO if success else logging.WARNING
        self.logger.log(
            level,
            f"Auth attempt for {email}: {'SUCCESS' if success else 'FAILED'}",
            extra={
                "email": email,
                "success": success,
                "ip_address": ip_address,
                "user_agent": user_agent,
            },
        )

    def log_suspicious_activity(
        self,
        activity: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Логирование подозрительной активности"""
        self.logger.warning(
            f"Suspicious activity: {activity}",
            extra={
                "activity": activity,
                "user_id": user_id,
                "ip_address": ip_address,
                "details": details or {},
            },
        )


# Глобальные логгеры
def get_logger(name: str) -> logging.Logger:
    """Получить логгер"""
    return LoggerSetup.get_logger(name)


def setup_app_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Настройка логирования для приложения"""
    return LoggerSetup.setup_logging(log_level, "json", log_file)
