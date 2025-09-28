"""
Сервис мониторинга и логирования
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, timezone
import logging
import json
import asyncio
import psutil
import time
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    module: str
    function: str
    line_number: int
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


@dataclass
class SystemMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_used_gb: float
    disk_free_gb: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_connections: int
    load_average: List[float]


@dataclass
class ApplicationMetrics:
    timestamp: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    active_users: int
    database_connections: int
    cache_hit_rate: float
    error_rate: float


class MonitoringService:
    """Сервис мониторинга и логирования"""

    def __init__(self):
        self.logs = []  # В реальном приложении здесь будет база данных
        self.system_metrics = []
        self.application_metrics = []
        self.alerts = []

        # Настройки мониторинга
        self.config = {
            "max_logs": 10000,
            "max_metrics": 1000,
            "metrics_interval": 60,  # секунды
            "alert_thresholds": {
                "cpu_percent": 80,
                "memory_percent": 85,
                "disk_usage_percent": 90,
                "error_rate": 5,
                "response_time": 2.0,
            },
            "log_retention_days": 30,
        }

        # Запускаем сбор метрик только если есть event loop
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._collect_metrics_loop())
            asyncio.create_task(self._cleanup_old_data())
        except RuntimeError:
            # Нет запущенного event loop, пропускаем
            pass

    async def log(
        self,
        level: LogLevel,
        message: str,
        module: str = "",
        function: str = "",
        line_number: int = 0,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None,
    ):
        """Логирование события"""
        try:
            log_entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=level.value,
                message=message,
                module=module,
                function=function,
                line_number=line_number,
                user_id=user_id,
                request_id=request_id,
                extra_data=extra_data,
            )

            # Добавляем в список логов
            self.logs.append(log_entry)

            # Ограничиваем количество логов
            if len(self.logs) > self.config["max_logs"]:
                self.logs = self.logs[-self.config["max_logs"] :]

            # Логируем в стандартный логгер
            logger_method = getattr(logger, level.value.lower())
            logger_method(f"{module}:{function}:{line_number} - {message}")

            # Проверяем на критические события
            if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
                await self._check_for_alerts(log_entry)

        except Exception as e:
            logger.error(f"Error logging event: {e}")

    async def get_logs(
        self,
        level: Optional[str] = None,
        module: Optional[str] = None,
        user_id: Optional[int] = None,
        limit: int = 100,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Получение логов с фильтрацией"""
        try:
            filtered_logs = self.logs.copy()

            # Фильтрация по уровню
            if level:
                filtered_logs = [
                    log for log in filtered_logs if log.level == level.upper()
                ]

            # Фильтрация по модулю
            if module:
                filtered_logs = [log for log in filtered_logs if module in log.module]

            # Фильтрация по пользователю
            if user_id:
                filtered_logs = [log for log in filtered_logs if log.user_id == user_id]

            # Фильтрация по времени
            if start_time:
                start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                filtered_logs = [
                    log
                    for log in filtered_logs
                    if datetime.fromisoformat(log.timestamp.replace("Z", "+00:00"))
                    >= start_dt
                ]

            if end_time:
                end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                filtered_logs = [
                    log
                    for log in filtered_logs
                    if datetime.fromisoformat(log.timestamp.replace("Z", "+00:00"))
                    <= end_dt
                ]

            # Сортировка по времени (новые сначала)
            filtered_logs.sort(key=lambda x: x.timestamp, reverse=True)

            # Ограничение количества
            filtered_logs = filtered_logs[:limit]

            # Конвертируем в словари
            return [asdict(log) for log in filtered_logs]

        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return []

    async def get_system_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Получение системных метрик"""
        try:
            metrics = self.system_metrics[-limit:] if self.system_metrics else []
            return [asdict(metric) for metric in metrics]
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return []

    async def get_application_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Получение метрик приложения"""
        try:
            metrics = (
                self.application_metrics[-limit:] if self.application_metrics else []
            )
            return [asdict(metric) for metric in metrics]
        except Exception as e:
            logger.error(f"Error getting application metrics: {e}")
            return []

    async def _collect_system_metrics(self) -> SystemMetrics:
        """Сбор системных метрик"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # Память
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / 1024 / 1024
            memory_available_mb = memory.available / 1024 / 1024

            # Диск
            disk = psutil.disk_usage("/")
            disk_usage_percent = disk.percent
            disk_used_gb = disk.used / 1024 / 1024 / 1024
            disk_free_gb = disk.free / 1024 / 1024 / 1024

            # Сеть
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv

            # Соединения
            active_connections = len(psutil.net_connections())

            # Нагрузка системы
            load_average = (
                list(psutil.getloadavg())
                if hasattr(psutil, "getloadavg")
                else [0.0, 0.0, 0.0]
            )

            return SystemMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_usage_percent,
                disk_used_gb=disk_used_gb,
                disk_free_gb=disk_free_gb,
                network_bytes_sent=network_bytes_sent,
                network_bytes_recv=network_bytes_recv,
                active_connections=active_connections,
                load_average=load_average,
            )

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                memory_available_mb=0.0,
                disk_usage_percent=0.0,
                disk_used_gb=0.0,
                disk_free_gb=0.0,
                network_bytes_sent=0,
                network_bytes_recv=0,
                active_connections=0,
                load_average=[0.0, 0.0, 0.0],
            )

    async def _collect_application_metrics(self) -> ApplicationMetrics:
        """Сбор метрик приложения"""
        try:
            # В реальном приложении эти метрики будут собираться из различных источников
            # Пока используем моковые данные

            total_requests = len(self.logs)
            successful_requests = len(
                [log for log in self.logs if log.level in ["INFO", "DEBUG"]]
            )
            failed_requests = len(
                [log for log in self.logs if log.level in ["ERROR", "CRITICAL"]]
            )

            average_response_time = 0.5  # Моковое значение
            active_users = 1  # Моковое значение
            database_connections = 5  # Моковое значение
            cache_hit_rate = 0.85  # Моковое значение

            error_rate = (
                (failed_requests / total_requests * 100) if total_requests > 0 else 0
            )

            return ApplicationMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                total_requests=total_requests,
                successful_requests=successful_requests,
                failed_requests=failed_requests,
                average_response_time=average_response_time,
                active_users=active_users,
                database_connections=database_connections,
                cache_hit_rate=cache_hit_rate,
                error_rate=error_rate,
            )

        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
            return ApplicationMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_response_time=0.0,
                active_users=0,
                database_connections=0,
                cache_hit_rate=0.0,
                error_rate=0.0,
            )

    async def _collect_metrics_loop(self):
        """Цикл сбора метрик"""
        while True:
            try:
                # Собираем системные метрики
                system_metrics = await self._collect_system_metrics()
                self.system_metrics.append(system_metrics)

                # Собираем метрики приложения
                app_metrics = await self._collect_application_metrics()
                self.application_metrics.append(app_metrics)

                # Ограничиваем количество метрик
                if len(self.system_metrics) > self.config["max_metrics"]:
                    self.system_metrics = self.system_metrics[
                        -self.config["max_metrics"] :
                    ]

                if len(self.application_metrics) > self.config["max_metrics"]:
                    self.application_metrics = self.application_metrics[
                        -self.config["max_metrics"] :
                    ]

                # Проверяем на алерты
                await self._check_metric_alerts(system_metrics, app_metrics)

                # Ждем до следующего сбора
                await asyncio.sleep(self.config["metrics_interval"])

            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                await asyncio.sleep(60)  # Ждем минуту при ошибке

    async def _check_metric_alerts(
        self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics
    ):
        """Проверка метрик на алерты"""
        try:
            thresholds = self.config["alert_thresholds"]

            # Проверка CPU
            if system_metrics.cpu_percent > thresholds["cpu_percent"]:
                await self._create_alert(
                    "high_cpu_usage",
                    f"High CPU usage: {system_metrics.cpu_percent}%",
                    "warning",
                    {"cpu_percent": system_metrics.cpu_percent},
                )

            # Проверка памяти
            if system_metrics.memory_percent > thresholds["memory_percent"]:
                await self._create_alert(
                    "high_memory_usage",
                    f"High memory usage: {system_metrics.memory_percent}%",
                    "warning",
                    {"memory_percent": system_metrics.memory_percent},
                )

            # Проверка диска
            if system_metrics.disk_usage_percent > thresholds["disk_usage_percent"]:
                await self._create_alert(
                    "high_disk_usage",
                    f"High disk usage: {system_metrics.disk_usage_percent}%",
                    "warning",
                    {"disk_usage_percent": system_metrics.disk_usage_percent},
                )

            # Проверка ошибок
            if app_metrics.error_rate > thresholds["error_rate"]:
                await self._create_alert(
                    "high_error_rate",
                    f"High error rate: {app_metrics.error_rate}%",
                    "error",
                    {"error_rate": app_metrics.error_rate},
                )

            # Проверка времени ответа
            if app_metrics.average_response_time > thresholds["response_time"]:
                await self._create_alert(
                    "slow_response_time",
                    f"Slow response time: {app_metrics.average_response_time}s",
                    "warning",
                    {"response_time": app_metrics.average_response_time},
                )

        except Exception as e:
            logger.error(f"Error checking metric alerts: {e}")

    async def _check_for_alerts(self, log_entry: LogEntry):
        """Проверка логов на алерты"""
        try:
            # Критические ошибки
            if log_entry.level == "CRITICAL":
                await self._create_alert(
                    "critical_error",
                    f"Critical error: {log_entry.message}",
                    "critical",
                    {"log_entry": asdict(log_entry)},
                )

            # Множественные ошибки
            recent_errors = [log for log in self.logs[-10:] if log.level == "ERROR"]
            if len(recent_errors) >= 5:
                await self._create_alert(
                    "multiple_errors",
                    f"Multiple errors detected: {len(recent_errors)} in last 10 logs",
                    "warning",
                    {"error_count": len(recent_errors)},
                )

        except Exception as e:
            logger.error(f"Error checking log alerts: {e}")

    async def _create_alert(
        self, alert_type: str, message: str, severity: str, data: Dict[str, Any]
    ):
        """Создание алерта"""
        try:
            alert = {
                "id": len(self.alerts) + 1,
                "type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": data,
                "resolved": False,
            }

            self.alerts.append(alert)

            # Логируем алерт
            await self.log(
                LogLevel.WARNING,
                f"Alert created: {message}",
                "monitoring",
                "_create_alert",
                0,
                extra_data=alert,
            )

        except Exception as e:
            logger.error(f"Error creating alert: {e}")

    async def get_alerts(
        self, resolved: Optional[bool] = None, severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Получение алертов"""
        try:
            filtered_alerts = self.alerts.copy()

            if resolved is not None:
                filtered_alerts = [
                    alert for alert in filtered_alerts if alert["resolved"] == resolved
                ]

            if severity:
                filtered_alerts = [
                    alert for alert in filtered_alerts if alert["severity"] == severity
                ]

            # Сортировка по времени (новые сначала)
            filtered_alerts.sort(key=lambda x: x["timestamp"], reverse=True)

            return filtered_alerts

        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            return []

    async def resolve_alert(self, alert_id: int) -> bool:
        """Разрешение алерта"""
        try:
            for alert in self.alerts:
                if alert["id"] == alert_id:
                    alert["resolved"] = True
                    alert["resolved_at"] = datetime.now(timezone.utc).isoformat()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False

    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Получение данных для дашборда"""
        try:
            # Последние метрики
            latest_system = self.system_metrics[-1] if self.system_metrics else None
            latest_app = (
                self.application_metrics[-1] if self.application_metrics else None
            )

            # Статистика логов
            log_stats = {
                "total": len(self.logs),
                "by_level": {},
                "recent_errors": len(
                    [log for log in self.logs[-100:] if log.level == "ERROR"]
                ),
            }

            for log in self.logs:
                level = log.level
                log_stats["by_level"][level] = log_stats["by_level"].get(level, 0) + 1

            # Активные алерты
            active_alerts = [alert for alert in self.alerts if not alert["resolved"]]

            return {
                "system_metrics": asdict(latest_system) if latest_system else None,
                "application_metrics": asdict(latest_app) if latest_app else None,
                "log_stats": log_stats,
                "active_alerts": len(active_alerts),
                "alerts_by_severity": {
                    "critical": len(
                        [a for a in active_alerts if a["severity"] == "critical"]
                    ),
                    "error": len(
                        [a for a in active_alerts if a["severity"] == "error"]
                    ),
                    "warning": len(
                        [a for a in active_alerts if a["severity"] == "warning"]
                    ),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {}

    async def _cleanup_old_data(self):
        """Очистка старых данных"""
        while True:
            try:
                await asyncio.sleep(3600)  # Каждый час

                cutoff_time = datetime.now(timezone.utc) - timedelta(
                    days=self.config["log_retention_days"]
                )

                # Очищаем старые логи
                self.logs = [
                    log
                    for log in self.logs
                    if datetime.fromisoformat(log.timestamp.replace("Z", "+00:00"))
                    > cutoff_time
                ]

                # Очищаем старые метрики
                self.system_metrics = [
                    metric
                    for metric in self.system_metrics
                    if datetime.fromisoformat(metric.timestamp.replace("Z", "+00:00"))
                    > cutoff_time
                ]

                self.application_metrics = [
                    metric
                    for metric in self.application_metrics
                    if datetime.fromisoformat(metric.timestamp.replace("Z", "+00:00"))
                    > cutoff_time
                ]

                logger.info("Cleaned up old monitoring data")

            except Exception as e:
                logger.error(f"Error in cleanup: {e}")


# Создаем глобальный экземпляр сервиса
monitoring_service = MonitoringService()
