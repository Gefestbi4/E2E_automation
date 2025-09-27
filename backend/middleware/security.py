"""
Middleware для безопасности
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from security import check_rate_limit, get_remaining_requests, get_client_ip

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Middleware для обеспечения безопасности"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        # Проверка rate limit
        if not check_rate_limit(request):
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Превышен лимит запросов", "retry_after": 3600},
            )
            await response(scope, receive, send)
            return

        # Добавление заголовков безопасности
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                headers.update(self._get_security_headers())
                message["headers"] = list(headers.items())
            await send(message)

        await self.app(scope, receive, send_wrapper)

    def _get_security_headers(self) -> dict:
        """Получение заголовков безопасности"""
        return {
            b"X-Content-Type-Options": b"nosniff",
            b"X-Frame-Options": b"DENY",
            b"X-XSS-Protection": b"1; mode=block",
            b"Strict-Transport-Security": b"max-age=31536000; includeSubDomains",
            b"Referrer-Policy": b"strict-origin-when-cross-origin",
            b"Content-Security-Policy": b"default-src 'self'",
        }


class RequestLoggingMiddleware:
    """Middleware для логирования запросов"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()

        # Логирование входящего запроса
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": get_client_ip(request),
                "user_agent": request.headers.get("user-agent", ""),
            },
        )

        # Обработка ответа
        response_sent = False

        async def send_wrapper(message):
            nonlocal response_sent
            if message["type"] == "http.response.start" and not response_sent:
                response_sent = True
                process_time = time.time() - start_time

                logger.info(
                    f"Response: {message.get('status', 200)} in {process_time:.3f}s",
                    extra={
                        "status_code": message.get("status", 200),
                        "process_time": process_time,
                        "client_ip": get_client_ip(request),
                    },
                )

            await send(message)

        await self.app(scope, receive, send_wrapper)
