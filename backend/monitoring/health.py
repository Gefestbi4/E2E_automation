"""
Проверка здоровья системы
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from models import SessionLocal
import psutil
import logging

logger = logging.getLogger(__name__)


class HealthChecker:
    """Проверка здоровья различных компонентов системы"""

    def __init__(self):
        self.checks = {
            "database": self._check_database,
            "memory": self._check_memory,
            "disk": self._check_disk,
            "cpu": self._check_cpu,
        }

    async def check_all(self) -> Dict[str, Any]:
        """Проверить все компоненты системы"""
        results = {}
        overall_status = "healthy"

        for check_name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[check_name] = result

                if result["status"] != "healthy":
                    overall_status = "unhealthy"

            except Exception as e:
                logger.error(f"Health check failed for {check_name}: {e}")
                results[check_name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": time.time(),
                }
                overall_status = "unhealthy"

        return {"status": overall_status, "timestamp": time.time(), "checks": results}

    async def _check_database(self) -> Dict[str, Any]:
        """Проверка подключения к базе данных"""
        try:
            db = SessionLocal()
            # Простой запрос для проверки подключения
            from sqlalchemy import text

            db.execute(text("SELECT 1"))
            db.close()

            return {
                "status": "healthy",
                "message": "Database connection successful",
                "timestamp": time.time(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "timestamp": time.time(),
            }

    async def _check_memory(self) -> Dict[str, Any]:
        """Проверка использования памяти"""
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        status = "healthy"
        if memory_percent > 90:
            status = "critical"
        elif memory_percent > 80:
            status = "warning"

        return {
            "status": status,
            "memory_percent": memory_percent,
            "memory_available_gb": memory.available / (1024**3),
            "memory_total_gb": memory.total / (1024**3),
            "timestamp": time.time(),
        }

    async def _check_disk(self) -> Dict[str, Any]:
        """Проверка использования диска"""
        disk = psutil.disk_usage("/")
        disk_percent = (disk.used / disk.total) * 100

        status = "healthy"
        if disk_percent > 95:
            status = "critical"
        elif disk_percent > 85:
            status = "warning"

        return {
            "status": status,
            "disk_percent": disk_percent,
            "disk_free_gb": disk.free / (1024**3),
            "disk_total_gb": disk.total / (1024**3),
            "timestamp": time.time(),
        }

    async def _check_cpu(self) -> Dict[str, Any]:
        """Проверка использования CPU"""
        cpu_percent = psutil.cpu_percent(interval=1)

        status = "healthy"
        if cpu_percent > 90:
            status = "critical"
        elif cpu_percent > 80:
            status = "warning"

        return {
            "status": status,
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count(),
            "timestamp": time.time(),
        }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Проверка внешних зависимостей"""
        dependencies = {
            "database": await self._check_database(),
            "redis": await self._check_redis(),
            "external_api": await self._check_external_api(),
        }

        overall_status = "healthy"
        for dep_name, dep_result in dependencies.items():
            if dep_result["status"] != "healthy":
                overall_status = "degraded"

        return {
            "status": overall_status,
            "dependencies": dependencies,
            "timestamp": time.time(),
        }

    async def _check_redis(self) -> Dict[str, Any]:
        """Проверка Redis (если используется)"""
        # Заглушка для Redis - в реальном приложении здесь будет проверка Redis
        return {
            "status": "healthy",
            "message": "Redis not configured",
            "timestamp": time.time(),
        }

    async def _check_external_api(self) -> Dict[str, Any]:
        """Проверка внешних API"""
        # Заглушка для внешних API
        return {
            "status": "healthy",
            "message": "No external APIs configured",
            "timestamp": time.time(),
        }


class HealthEndpoint:
    """Endpoint для проверки здоровья системы"""

    def __init__(self, health_checker: HealthChecker):
        self.health_checker = health_checker

    async def get_health(self) -> Dict[str, Any]:
        """Получить статус здоровья системы"""
        return await self.health_checker.check_all()

    async def get_health_detailed(self) -> Dict[str, Any]:
        """Получить детальный статус здоровья"""
        health_status = await self.health_checker.check_all()
        dependencies_status = await self.health_checker.check_dependencies()

        return {
            "overall": health_status,
            "dependencies": dependencies_status,
            "timestamp": time.time(),
        }

    async def get_ready(self) -> Dict[str, Any]:
        """Проверка готовности к работе"""
        health_status = await self.health_checker.check_all()

        if health_status["status"] == "healthy":
            return {
                "status": "ready",
                "message": "Service is ready to accept requests",
                "timestamp": time.time(),
            }
        else:
            return {
                "status": "not_ready",
                "message": "Service is not ready",
                "issues": [
                    check
                    for check, result in health_status["checks"].items()
                    if result["status"] != "healthy"
                ],
                "timestamp": time.time(),
            }

    async def get_live(self) -> Dict[str, Any]:
        """Проверка жизнеспособности"""
        return {
            "status": "alive",
            "message": "Service is alive",
            "timestamp": time.time(),
        }
