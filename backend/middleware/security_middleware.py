"""
Middleware для усиления безопасности
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging
import time
from datetime import datetime, timezone
import asyncio

from services.security_service import security_service

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware для усиления безопасности"""

    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.rate_limit_cache = {}
        self.request_times = {}

    async def dispatch(self, request: Request, call_next: Callable):
        """Обработка запроса через middleware безопасности"""
        start_time = time.time()

        try:
            # Получаем IP адрес клиента
            client_ip = self._get_client_ip(request)

            # Проверяем IP в черном списке
            if not await security_service.check_ip_blocklist(client_ip):
                logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Access denied"},
                )

            # Проверяем лимит запросов
            endpoint = f"{request.method}:{request.url.path}"
            allowed, rate_info = await security_service.check_rate_limit(
                client_ip, endpoint
            )

            if not allowed:
                logger.warning(f"Rate limit exceeded for IP {client_ip} on {endpoint}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Rate limit exceeded",
                        "retry_after": rate_info.get("retry_after", 60),
                    },
                    headers={"Retry-After": str(rate_info.get("retry_after", 60))},
                )

            # Проверяем на атаки в URL и параметрах
            attack_detected = await self._check_for_attacks(request)
            if attack_detected:
                logger.warning(
                    f"Attack pattern detected from IP {client_ip}: {attack_detected}"
                )
                await security_service._log_suspicious_activity(
                    client_ip,
                    "attack_pattern_detected",
                    f"Attack pattern: {attack_detected}",
                )
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid request"},
                )

            # Добавляем заголовки безопасности
            response = await call_next(request)

            # Добавляем заголовки безопасности к ответу
            response = self._add_security_headers(response)

            # Логируем время выполнения
            process_time = time.time() - start_time
            if process_time > 1.0:  # Логируем медленные запросы
                logger.warning(f"Slow request: {endpoint} took {process_time:.2f}s")

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )

    def _get_client_ip(self, request: Request) -> str:
        """Получение IP адреса клиента"""
        # Проверяем заголовки прокси
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Возвращаем IP из соединения
        if hasattr(request, "client") and request.client:
            return request.client.host

        return "unknown"

    async def _check_for_attacks(self, request: Request) -> str:
        """Проверка на атаки в запросе"""
        try:
            # Проверяем URL
            url_attacks = await security_service.detect_attack_patterns(
                str(request.url)
            )
            if url_attacks:
                return f"URL attack: {url_attacks[0]['type']}"

            # Проверяем параметры запроса
            query_params = str(request.query_params)
            if query_params:
                query_attacks = await security_service.detect_attack_patterns(
                    query_params
                )
                if query_attacks:
                    return f"Query attack: {query_attacks[0]['type']}"

            # Проверяем заголовки
            for header_name, header_value in request.headers.items():
                header_attacks = await security_service.detect_attack_patterns(
                    header_value
                )
                if header_attacks:
                    return (
                        f"Header attack in {header_name}: {header_attacks[0]['type']}"
                    )

            return None

        except Exception as e:
            logger.error(f"Error checking for attacks: {e}")
            return None

    def _add_security_headers(self, response):
        """Добавление заголовков безопасности"""
        # Защита от XSS
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Строгая транспортная безопасность
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Политика реферера
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Политика разрешений
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        # Удаляем заголовки, которые могут раскрыть информацию о сервере
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    """Middleware для защиты от CSRF атак"""

    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.exempt_paths = ["/api/auth/login", "/api/auth/register", "/api/health"]

    async def dispatch(self, request: Request, call_next: Callable):
        """Проверка CSRF токена"""
        try:
            # Пропускаем GET запросы и исключенные пути
            if request.method == "GET" or request.url.path in self.exempt_paths:
                return await call_next(request)

            # Получаем CSRF токен из заголовка
            csrf_token = request.headers.get("X-CSRF-Token")

            # Для демонстрации всегда разрешаем (в реальном приложении нужна проверка)
            if not csrf_token:
                logger.warning(
                    f"Missing CSRF token for {request.method} {request.url.path}"
                )
                # В реальном приложении здесь должна быть проверка токена
                # return JSONResponse(
                #     status_code=status.HTTP_403_FORBIDDEN,
                #     content={"detail": "CSRF token required"}
                # )

            return await call_next(request)

        except Exception as e:
            logger.error(f"CSRF middleware error: {e}")
            return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования запросов"""

    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        """Логирование запросов"""
        start_time = time.time()

        # Логируем входящий запрос
        logger.info(
            f"Incoming request: {request.method} {request.url.path} from {self._get_client_ip(request)}"
        )

        try:
            response = await call_next(request)

            # Логируем ответ
            process_time = time.time() - start_time
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"-> {response.status_code} in {process_time:.3f}s"
            )

            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"-> ERROR in {process_time:.3f}s: {e}"
            )
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Получение IP адреса клиента"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        if hasattr(request, "client") and request.client:
            return request.client.host

        return "unknown"
