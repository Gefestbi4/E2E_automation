"""
API для мониторинга и логирования
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.monitoring_service import monitoring_service, LogLevel
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


class LogRequest(BaseModel):
    level: str
    message: str
    module: Optional[str] = ""
    function: Optional[str] = ""
    line_number: Optional[int] = 0
    extra_data: Optional[Dict[str, Any]] = None


class LogResponse(BaseModel):
    timestamp: str
    level: str
    message: str
    module: str
    function: str
    line_number: int
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None


class SystemMetricsResponse(BaseModel):
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


class ApplicationMetricsResponse(BaseModel):
    timestamp: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    active_users: int
    database_connections: int
    cache_hit_rate: float
    error_rate: float


class AlertResponse(BaseModel):
    id: int
    type: str
    message: str
    severity: str
    timestamp: str
    data: Dict[str, Any]
    resolved: bool
    resolved_at: Optional[str] = None


@router.post("/logs")
async def create_log(
    log_request: LogRequest, current_user: User = Depends(get_current_user)
):
    """Создать лог запись"""
    try:
        # Валидируем уровень лога
        try:
            log_level = LogLevel(log_request.level.upper())
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid log level: {log_request.level}"
            )

        await monitoring_service.log(
            level=log_level,
            message=log_request.message,
            module=log_request.module,
            function=log_request.function,
            line_number=log_request.line_number,
            user_id=current_user.id,
            extra_data=log_request.extra_data,
        )

        return {"message": "Log created successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating log: {str(e)}")


@router.get("/logs", response_model=List[LogResponse])
async def get_logs(
    level: Optional[str] = Query(None, description="Фильтр по уровню лога"),
    module: Optional[str] = Query(None, description="Фильтр по модулю"),
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю"),
    limit: int = Query(100, description="Количество записей"),
    start_time: Optional[str] = Query(None, description="Начальное время (ISO format)"),
    end_time: Optional[str] = Query(None, description="Конечное время (ISO format)"),
    current_user: User = Depends(get_current_user),
):
    """Получить логи с фильтрацией"""
    try:
        logs = await monitoring_service.get_logs(
            level=level,
            module=module,
            user_id=user_id,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
        )
        return logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting logs: {str(e)}")


@router.get("/system-metrics", response_model=List[SystemMetricsResponse])
async def get_system_metrics(
    limit: int = Query(100, description="Количество записей"),
    current_user: User = Depends(get_current_user),
):
    """Получить системные метрики"""
    try:
        metrics = await monitoring_service.get_system_metrics(limit=limit)
        return metrics

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting system metrics: {str(e)}"
        )


@router.get("/application-metrics", response_model=List[ApplicationMetricsResponse])
async def get_application_metrics(
    limit: int = Query(100, description="Количество записей"),
    current_user: User = Depends(get_current_user),
):
    """Получить метрики приложения"""
    try:
        metrics = await monitoring_service.get_application_metrics(limit=limit)
        return metrics

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting application metrics: {str(e)}"
        )


@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    resolved: Optional[bool] = Query(None, description="Фильтр по статусу разрешения"),
    severity: Optional[str] = Query(None, description="Фильтр по серьезности"),
    current_user: User = Depends(get_current_user),
):
    """Получить алерты"""
    try:
        alerts = await monitoring_service.get_alerts(
            resolved=resolved, severity=severity
        )
        return alerts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting alerts: {str(e)}")


@router.put("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: int, current_user: User = Depends(get_current_user)):
    """Разрешить алерт"""
    try:
        success = await monitoring_service.resolve_alert(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")

        return {"message": "Alert resolved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resolving alert: {str(e)}")


@router.get("/dashboard")
async def get_dashboard_data(current_user: User = Depends(get_current_user)):
    """Получить данные для дашборда мониторинга"""
    try:
        dashboard_data = await monitoring_service.get_dashboard_data()
        return dashboard_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting dashboard data: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Проверка здоровья системы"""
    try:
        # Получаем последние метрики
        system_metrics = await monitoring_service.get_system_metrics(limit=1)
        app_metrics = await monitoring_service.get_application_metrics(limit=1)

        # Определяем статус здоровья
        health_status = "healthy"
        issues = []

        if system_metrics:
            latest_system = system_metrics[0]
            if latest_system["cpu_percent"] > 90:
                health_status = "unhealthy"
                issues.append("High CPU usage")

            if latest_system["memory_percent"] > 90:
                health_status = "unhealthy"
                issues.append("High memory usage")

            if latest_system["disk_usage_percent"] > 95:
                health_status = "unhealthy"
                issues.append("High disk usage")

        if app_metrics:
            latest_app = app_metrics[0]
            if latest_app["error_rate"] > 10:
                health_status = "unhealthy"
                issues.append("High error rate")

        return {
            "status": health_status,
            "timestamp": (
                monitoring_service.system_metrics[-1].timestamp
                if monitoring_service.system_metrics
                else None
            ),
            "issues": issues,
            "system_metrics": system_metrics[0] if system_metrics else None,
            "application_metrics": app_metrics[0] if app_metrics else None,
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": None,
            "issues": [f"Health check failed: {str(e)}"],
            "system_metrics": None,
            "application_metrics": None,
        }
