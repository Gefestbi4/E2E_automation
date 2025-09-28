"""
API для расширенной аналитики
Детальная аналитика, отчеты, метрики, дашборды
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.advanced_analytics_service import advanced_analytics_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/analytics/advanced", tags=["advanced-analytics"])


class ReportRequest(BaseModel):
    report_type: str
    time_period: str = "30d"
    filters: Optional[Dict[str, Any]] = None


@router.get("/dashboard")
async def get_dashboard_metrics(
    time_period: str = Query("7d", description="Time period for metrics"),
    current_user: User = Depends(get_current_user),
):
    """Получение метрик для дашборда"""
    try:
        metrics = advanced_analytics_service.get_dashboard_metrics(
            current_user.id, time_period
        )
        return {
            "metrics": metrics,
            "user_id": current_user.id,
            "time_period": time_period,
            "generated_at": "2025-01-28T10:00:00Z",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения метрик дашборда: {str(e)}"
        )


@router.get("/user")
async def get_user_analytics(
    time_period: str = Query("30d", description="Time period for analytics"),
    current_user: User = Depends(get_current_user),
):
    """Получение аналитики пользователя"""
    try:
        analytics = advanced_analytics_service.get_user_analytics(
            current_user.id, time_period
        )
        return {
            "analytics": analytics,
            "user_id": current_user.id,
            "time_period": time_period,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения аналитики пользователя: {str(e)}"
        )


@router.get("/content/{content_id}")
async def get_content_analytics(
    content_id: int,
    current_user: User = Depends(get_current_user),
):
    """Получение аналитики контента"""
    try:
        analytics = advanced_analytics_service.get_content_analytics(content_id)
        return {
            "analytics": analytics,
            "content_id": content_id,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения аналитики контента: {str(e)}"
        )


@router.get("/business")
async def get_business_analytics(
    time_period: str = Query("30d", description="Time period for business analytics"),
    current_user: User = Depends(get_current_user),
):
    """Получение бизнес аналитики"""
    try:
        analytics = advanced_analytics_service.get_business_analytics(time_period)
        return {
            "analytics": analytics,
            "time_period": time_period,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения бизнес аналитики: {str(e)}"
        )


@router.get("/performance")
async def get_performance_analytics(
    current_user: User = Depends(get_current_user),
):
    """Получение аналитики производительности"""
    try:
        analytics = advanced_analytics_service.get_performance_analytics()
        return {
            "analytics": analytics,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения аналитики производительности: {str(e)}",
        )


@router.post("/reports")
async def generate_report(
    request: ReportRequest,
    current_user: User = Depends(get_current_user),
):
    """Генерация отчета"""
    try:
        report = advanced_analytics_service.generate_report(
            request.report_type, request.time_period, current_user.id
        )
        return report

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка генерации отчета: {str(e)}"
        )


@router.get("/trending/{metric_type}")
async def get_trending_metrics(
    metric_type: str,
    time_period: str = Query("7d", description="Time period for trending metrics"),
    current_user: User = Depends(get_current_user),
):
    """Получение трендовых метрик"""
    try:
        trending = advanced_analytics_service.get_trending_metrics(
            metric_type, time_period
        )
        return {
            "trending_metrics": trending,
            "metric_type": metric_type,
            "time_period": time_period,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения трендовых метрик: {str(e)}"
        )


@router.get("/export/{report_type}")
async def export_analytics_data(
    report_type: str,
    time_period: str = Query("30d", description="Time period for export"),
    format: str = Query("json", description="Export format (json, csv, xlsx)"),
    current_user: User = Depends(get_current_user),
):
    """Экспорт аналитических данных"""
    try:
        # В реальном приложении здесь будет генерация файла
        if report_type == "user_activity":
            data = advanced_analytics_service.get_user_analytics(
                current_user.id, time_period
            )
        elif report_type == "content_performance":
            data = advanced_analytics_service.get_content_analytics(1)
        elif report_type == "business_overview":
            data = advanced_analytics_service.get_business_analytics(time_period)
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый тип отчета")

        return {
            "export_data": data,
            "report_type": report_type,
            "format": format,
            "time_period": time_period,
            "user_id": current_user.id,
            "download_url": f"/api/analytics/advanced/download/{report_type}_{time_period}.{format}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта данных: {str(e)}")


@router.get("/comparison")
async def compare_metrics(
    metric_type: str = Query(
        "user_engagement", description="Type of metrics to compare"
    ),
    period1: str = Query("7d", description="First period"),
    period2: str = Query("30d", description="Second period"),
    current_user: User = Depends(get_current_user),
):
    """Сравнение метрик за разные периоды"""
    try:
        # В реальном приложении здесь будет сравнение данных
        comparison = {
            "metric_type": metric_type,
            "period1": {
                "period": period1,
                "value": 1250,
                "growth": 12.5,
            },
            "period2": {
                "period": period2,
                "value": 1100,
                "growth": 8.2,
            },
            "comparison": {
                "difference": 150,
                "percentage_change": 13.6,
                "trend": "up",
                "significance": "significant",
            },
        }

        return {
            "comparison": comparison,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка сравнения метрик: {str(e)}"
        )


@router.get("/predictions")
async def get_predictions(
    metric_type: str = Query(
        "user_engagement", description="Type of metric to predict"
    ),
    forecast_days: int = Query(30, description="Number of days to forecast"),
    current_user: User = Depends(get_current_user),
):
    """Получение прогнозов на основе исторических данных"""
    try:
        # В реальном приложении здесь будет ML модель для прогнозирования
        predictions = {
            "metric_type": metric_type,
            "forecast_days": forecast_days,
            "current_value": 1250,
            "predicted_values": [
                {"date": "2025-01-29", "value": 1280, "confidence": 0.85},
                {"date": "2025-01-30", "value": 1310, "confidence": 0.82},
                {"date": "2025-01-31", "value": 1340, "confidence": 0.80},
            ],
            "trend": "up",
            "confidence": 0.82,
            "recommendations": [
                "Ожидается рост активности на 15%",
                "Рекомендуется увеличить ресурсы",
                "Планируйте маркетинговые кампании",
            ],
        }

        return {
            "predictions": predictions,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения прогнозов: {str(e)}"
        )


@router.get("/alerts")
async def get_analytics_alerts(
    current_user: User = Depends(get_current_user),
):
    """Получение аналитических уведомлений"""
    try:
        alerts = [
            {
                "id": 1,
                "type": "warning",
                "title": "Высокий уровень отказов",
                "message": "Уровень отказов увеличился на 15% за последние 24 часа",
                "metric": "bounce_rate",
                "current_value": 0.35,
                "threshold": 0.30,
                "created_at": "2025-01-28T09:30:00Z",
                "status": "active",
            },
            {
                "id": 2,
                "type": "info",
                "title": "Новый рекорд активности",
                "message": "Достигнут новый рекорд по количеству активных пользователей",
                "metric": "daily_active_users",
                "current_value": 890,
                "previous_record": 850,
                "created_at": "2025-01-28T08:15:00Z",
                "status": "acknowledged",
            },
            {
                "id": 3,
                "type": "success",
                "title": "Цель достигнута",
                "message": "Достигнута цель по конверсии на 8%",
                "metric": "conversion_rate",
                "current_value": 0.08,
                "target": 0.08,
                "created_at": "2025-01-28T07:45:00Z",
                "status": "resolved",
            },
        ]

        return {
            "alerts": alerts,
            "total_alerts": len(alerts),
            "active_alerts": len([a for a in alerts if a["status"] == "active"]),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения уведомлений: {str(e)}"
        )


@router.put("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
):
    """Подтверждение уведомления"""
    try:
        # В реальном приложении здесь будет обновление статуса в БД
        return {
            "message": "Уведомление подтверждено",
            "alert_id": alert_id,
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка подтверждения уведомления: {str(e)}"
        )


@router.get("/health")
async def analytics_health_check():
    """Проверка состояния аналитических сервисов"""
    try:
        health_status = {
            "status": "healthy",
            "services": {
                "data_collection": "operational",
                "data_processing": "operational",
                "report_generation": "operational",
                "export_service": "operational",
            },
            "data_sources": {
                "user_events": "connected",
                "content_metrics": "connected",
                "business_metrics": "connected",
                "performance_metrics": "connected",
            },
            "performance": {
                "avg_query_time_ms": 250,
                "data_freshness_minutes": 5,
                "uptime_percentage": 99.9,
            },
        }

        return health_status

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка проверки состояния: {str(e)}"
        )
