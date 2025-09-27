"""
API endpoints для мониторинга
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from monitoring import MetricsCollector, HealthChecker, MetricsEndpoint, HealthEndpoint
from monitoring.logging import app_logger

router = APIRouter()

# Глобальные экземпляры
metrics_collector = MetricsCollector()
health_checker = HealthChecker()
metrics_endpoint = MetricsEndpoint(metrics_collector)
health_endpoint = HealthEndpoint(health_checker)


@router.get("/metrics")
async def get_metrics():
    """Получить метрики в формате Prometheus"""
    try:
        return await metrics_endpoint.get_metrics()
    except Exception as e:
        app_logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve metrics",
        )


@router.get("/health")
async def get_health():
    """Получить статус здоровья системы"""
    try:
        return await health_endpoint.get_health()
    except Exception as e:
        app_logger.error("Health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed",
        )


@router.get("/health/detailed")
async def get_health_detailed():
    """Получить детальный статус здоровья"""
    try:
        return await health_endpoint.get_health_detailed()
    except Exception as e:
        app_logger.error("Detailed health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Detailed health check failed",
        )


@router.get("/ready")
async def get_ready():
    """Проверка готовности к работе (для Kubernetes)"""
    try:
        return await health_endpoint.get_ready()
    except Exception as e:
        app_logger.error("Readiness check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Readiness check failed",
        )


@router.get("/live")
async def get_live():
    """Проверка жизнеспособности (для Kubernetes)"""
    try:
        return await health_endpoint.get_live()
    except Exception as e:
        app_logger.error("Liveness check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Liveness check failed",
        )


@router.get("/status")
async def get_status():
    """Получить общий статус системы"""
    try:
        health_status = await health_endpoint.get_health()
        metrics_data = await metrics_endpoint.get_health()

        return {
            "status": "ok" if health_status["status"] == "healthy" else "degraded",
            "health": health_status,
            "metrics": metrics_data,
            "timestamp": health_status["timestamp"],
        }
    except Exception as e:
        app_logger.error("Status check failed", error=str(e))
        return {"status": "error", "error": str(e), "timestamp": None}
