"""
Структурированное логирование
"""

import json
import logging
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import Request
import traceback


class StructuredLogger:
    """Структурированный логгер для приложения"""

    def __init__(self, name: str = "app"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Настройка форматтера для JSON
        self.formatter = JSONFormatter()

        # Настройка обработчика
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def info(self, message: str, **kwargs):
        """Информационное сообщение"""
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Предупреждение"""
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs):
        """Ошибка"""
        self._log("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Критическая ошибка"""
        self._log("CRITICAL", message, **kwargs)

    def debug(self, message: str, **kwargs):
        """Отладочное сообщение"""
        self._log("DEBUG", message, **kwargs)

    def _log(self, level: str, message: str, **kwargs):
        """Внутренний метод логирования"""
        extra = {"level": level, "timestamp": datetime.utcnow().isoformat(), **kwargs}

        if level == "DEBUG":
            self.logger.debug(message, extra=extra)
        elif level == "INFO":
            self.logger.info(message, extra=extra)
        elif level == "WARNING":
            self.logger.warning(message, extra=extra)
        elif level == "ERROR":
            self.logger.error(message, extra=extra)
        elif level == "CRITICAL":
            self.logger.critical(message, extra=extra)


class JSONFormatter(logging.Formatter):
    """Форматтер для JSON логов"""

    def format(self, record):
        log_entry = {
            "timestamp": record.timestamp,
            "level": record.level,
            "message": record.message,
            "logger": record.name,
        }

        # Добавляем дополнительные поля
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "getMessage",
                "timestamp",
                "level",
                "message",
                "logger",
            ]:
                log_entry[key] = value

        # Добавляем информацию об исключении
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        return json.dumps(log_entry, ensure_ascii=False, default=str)


class RequestLogger:
    """Логгер для HTTP запросов"""

    def __init__(self, logger: StructuredLogger):
        self.logger = logger

    def log_request(
        self,
        request: Request,
        response_status: int,
        duration: float,
        user_id: Optional[int] = None,
    ):
        """Логирование HTTP запроса"""
        self.logger.info(
            "HTTP request",
            method=request.method,
            url=str(request.url),
            status_code=response_status,
            duration_ms=duration * 1000,
            user_id=user_id,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

    def log_error(
        self, request: Request, error: Exception, user_id: Optional[int] = None
    ):
        """Логирование ошибки запроса"""
        self.logger.error(
            "HTTP request error",
            method=request.method,
            url=str(request.url),
            error_type=type(error).__name__,
            error_message=str(error),
            user_id=user_id,
            client_ip=request.client.host if request.client else None,
        )


class BusinessLogger:
    """Логгер для бизнес-событий"""

    def __init__(self, logger: StructuredLogger):
        self.logger = logger

    def log_user_action(self, action: str, user_id: int, **kwargs):
        """Логирование действий пользователя"""
        self.logger.info("User action", action=action, user_id=user_id, **kwargs)

    def log_business_event(self, event: str, **kwargs):
        """Логирование бизнес-событий"""
        self.logger.info("Business event", event=event, **kwargs)

    def log_security_event(self, event: str, severity: str = "medium", **kwargs):
        """Логирование событий безопасности"""
        self.logger.warning("Security event", event=event, severity=severity, **kwargs)


class DatabaseLogger:
    """Логгер для операций с базой данных"""

    def __init__(self, logger: StructuredLogger):
        self.logger = logger

    def log_query(self, query: str, duration: float, **kwargs):
        """Логирование SQL запроса"""
        self.logger.debug(
            "Database query",
            query=query[:200] + "..." if len(query) > 200 else query,
            duration_ms=duration * 1000,
            **kwargs
        )

    def log_transaction(self, operation: str, table: str, **kwargs):
        """Логирование транзакции"""
        self.logger.info(
            "Database transaction", operation=operation, table=table, **kwargs
        )

    def log_error(self, error: Exception, query: str = None):
        """Логирование ошибки БД"""
        self.logger.error(
            "Database error",
            error_type=type(error).__name__,
            error_message=str(error),
            query=query[:200] + "..." if query and len(query) > 200 else query,
        )


# Глобальные экземпляры логгеров
app_logger = StructuredLogger("app")
request_logger = RequestLogger(app_logger)
business_logger = BusinessLogger(app_logger)
database_logger = DatabaseLogger(app_logger)
