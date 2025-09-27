"""
Система сбора метрик
"""

import time
import psutil
from typing import Dict, Any, Optional
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from fastapi import Request, Response
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Сборщик метрик приложения"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsCollector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.request_count = Counter(
            "http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status_code"],
        )

        self.request_duration = Histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"],
        )

        self.active_connections = Gauge(
            "http_active_connections", "Number of active HTTP connections"
        )

        self.database_connections = Gauge(
            "database_connections_active", "Number of active database connections"
        )

        self.memory_usage = Gauge("memory_usage_bytes", "Memory usage in bytes")

        self.cpu_usage = Gauge("cpu_usage_percent", "CPU usage percentage")

        self.error_count = Counter(
            "http_errors_total",
            "Total HTTP errors",
            ["method", "endpoint", "error_type"],
        )

        self.business_metrics = {
            "users_registered": Counter(
                "users_registered_total", "Total registered users"
            ),
            "products_created": Counter(
                "products_created_total", "Total products created"
            ),
            "orders_placed": Counter("orders_placed_total", "Total orders placed"),
            "posts_created": Counter("posts_created_total", "Total posts created"),
            "articles_published": Counter(
                "articles_published_total", "Total articles published"
            ),
        }

    def record_request(
        self, method: str, endpoint: str, status_code: int, duration: float
    ):
        """Записать метрику запроса"""
        self.request_count.labels(
            method=method, endpoint=endpoint, status_code=str(status_code)
        ).inc()

        self.request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def record_error(self, method: str, endpoint: str, error_type: str):
        """Записать метрику ошибки"""
        self.error_count.labels(
            method=method, endpoint=endpoint, error_type=error_type
        ).inc()

    def record_business_metric(self, metric_name: str, value: float = 1.0):
        """Записать бизнес-метрику"""
        if metric_name in self.business_metrics:
            self.business_metrics[metric_name].inc(value)

    def update_system_metrics(self):
        """Обновить системные метрики"""
        # Память
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_usage.set(cpu_percent)

    def get_metrics(self) -> str:
        """Получить метрики в формате Prometheus"""
        self.update_system_metrics()
        return generate_latest()


class PrometheusMetrics:
    """Middleware для сбора метрик Prometheus"""

    def __init__(self, app, metrics_collector: MetricsCollector):
        self.app = app
        self.metrics = metrics_collector

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()

        # Обработка запроса
        response_sent = False
        status_code = 500

        async def send_wrapper(message):
            nonlocal response_sent, status_code
            if message["type"] == "http.response.start" and not response_sent:
                response_sent = True
                status_code = message.get("status", 500)

                # Записать метрики
                duration = time.time() - start_time
                method = request.method
                endpoint = self._get_endpoint_name(request.url.path)

                self.metrics.record_request(method, endpoint, status_code, duration)

                # Записать ошибку если статус >= 400
                if status_code >= 400:
                    error_type = self._get_error_type(status_code)
                    self.metrics.record_error(method, endpoint, error_type)

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # Записать метрику исключения
            duration = time.time() - start_time
            method = request.method
            endpoint = self._get_endpoint_name(request.url.path)

            self.metrics.record_request(method, endpoint, 500, duration)
            self.metrics.record_error(method, endpoint, "exception")

            raise

    def _get_endpoint_name(self, path: str) -> str:
        """Получить имя endpoint для метрик"""
        # Упрощаем путь для группировки метрик
        if path.startswith("/api/"):
            parts = path.split("/")
            if len(parts) >= 3:
                return f"/api/{parts[2]}"  # /api/auth, /api/ecommerce, etc.
        return path

    def _get_error_type(self, status_code: int) -> str:
        """Получить тип ошибки по статус коду"""
        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "unknown"


class MetricsEndpoint:
    """Endpoint для получения метрик"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector

    async def get_metrics(self) -> Response:
        """Получить метрики в формате Prometheus"""
        metrics_data = self.metrics.get_metrics()
        return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)

    async def get_health(self) -> Dict[str, Any]:
        """Получить статус здоровья системы"""
        self.metrics.update_system_metrics()

        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "system": {
                "memory_usage_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "cpu_usage_percent": cpu_percent,
                "disk_usage_percent": psutil.disk_usage("/").percent,
            },
            "metrics": {
                "total_requests": sum(
                    sample.value
                    for sample in self.metrics.request_count.collect()[0].samples
                ),
                "total_errors": sum(
                    sample.value
                    for sample in self.metrics.error_count.collect()[0].samples
                ),
            },
        }
