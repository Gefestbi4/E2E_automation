from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.analytics as analytics_models
import models
from typing import List, Optional

from schemas.analytics import (
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    DashboardListResponse,
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    ReportListResponse,
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertListResponse,
    MetricCreate,
    MetricUpdate,
    MetricResponse,
    MetricListResponse,
    EventCreate,
    EventResponse,
)
from services.analytics_service import AnalyticsService
from utils.exceptions import (
    DashboardNotFoundError,
    ReportNotFoundError,
    AlertNotFoundError,
    MetricNotFoundError,
)

router = APIRouter()


# Dashboard endpoints
@router.get("/api/analytics/dashboard")
def get_dashboard_data(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить данные для главного дашборда"""
    service = AnalyticsService(db)
    dashboard_data = service.get_dashboard_data(current_user)
    return dashboard_data


@router.get("/api/analytics/dashboards", response_model=DashboardListResponse)
def get_dashboards(
    skip: int = Query(0, ge=0, description="Количество пропущенных дашбордов"),
    limit: int = Query(
        20, ge=1, le=100, description="Количество дашбордов на странице"
    ),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить дашборды пользователя"""
    service = AnalyticsService(db)
    result = service.get_dashboards(current_user, skip=skip, limit=limit)

    dashboards = []
    for dashboard in result["items"]:
        dashboards.append(DashboardResponse.from_orm(dashboard))

    return DashboardListResponse(
        items=dashboards,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get(
    "/api/analytics/dashboards/{dashboard_id}", response_model=DashboardResponse
)
def get_dashboard(
    dashboard_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить дашборд по ID"""
    service = AnalyticsService(db)
    dashboard = service.get_dashboard(dashboard_id, current_user)
    return DashboardResponse.from_orm(dashboard)


@router.post("/api/analytics/dashboards", response_model=DashboardResponse)
def create_dashboard(
    dashboard_data: DashboardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый дашборд"""
    service = AnalyticsService(db)
    dashboard = service.create_dashboard(dashboard_data, current_user)
    return DashboardResponse.from_orm(dashboard)


@router.put(
    "/api/analytics/dashboards/{dashboard_id}", response_model=DashboardResponse
)
def update_dashboard(
    dashboard_id: int,
    dashboard_data: DashboardUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить дашборд"""
    service = AnalyticsService(db)
    dashboard = service.update_dashboard(dashboard_id, dashboard_data, current_user)
    return DashboardResponse.from_orm(dashboard)


@router.delete("/api/analytics/dashboards/{dashboard_id}")
def delete_dashboard(
    dashboard_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить дашборд"""
    service = AnalyticsService(db)
    service.delete_dashboard(dashboard_id, current_user)
    return {"message": "Dashboard deleted successfully"}


# Metrics endpoints
@router.get("/api/analytics/metrics", response_model=MetricListResponse)
def get_metrics(
    skip: int = Query(0, ge=0, description="Количество пропущенных метрик"),
    limit: int = Query(20, ge=1, le=100, description="Количество метрик на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить метрики пользователя"""
    service = AnalyticsService(db)
    result = service.get_metrics(current_user, skip=skip, limit=limit)

    metrics = []
    for metric in result["items"]:
        metrics.append(MetricResponse.from_orm(metric))

    return MetricListResponse(
        items=metrics,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/analytics/metrics/{metric_id}", response_model=MetricResponse)
def get_metric(
    metric_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить метрику по ID"""
    service = AnalyticsService(db)
    metric = service.get_metric(metric_id, current_user)
    return MetricResponse.from_orm(metric)


@router.post("/api/analytics/metrics", response_model=MetricResponse)
def create_metric(
    metric_data: MetricCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую метрику"""
    service = AnalyticsService(db)
    metric = service.create_metric(metric_data, current_user)
    return MetricResponse.from_orm(metric)


@router.put("/api/analytics/metrics/{metric_id}", response_model=MetricResponse)
def update_metric(
    metric_id: int,
    metric_data: MetricUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить метрику"""
    service = AnalyticsService(db)
    metric = service.update_metric(metric_id, metric_data, current_user)
    return MetricResponse.from_orm(metric)


@router.delete("/api/analytics/metrics/{metric_id}")
def delete_metric(
    metric_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить метрику"""
    service = AnalyticsService(db)
    service.delete_metric(metric_id, current_user)
    return {"message": "Metric deleted successfully"}


@router.get("/api/analytics/metrics/{metric_id}/data")
def get_metric_data(
    metric_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить данные метрики"""
    service = AnalyticsService(db)
    data = service.get_metric_data(metric_id, current_user)
    return data


# Reports endpoints
@router.get("/api/analytics/reports", response_model=ReportListResponse)
def get_reports(
    skip: int = Query(0, ge=0, description="Количество пропущенных отчетов"),
    limit: int = Query(20, ge=1, le=100, description="Количество отчетов на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить отчеты пользователя"""
    service = AnalyticsService(db)
    result = service.get_reports(current_user, skip=skip, limit=limit)

    reports = []
    for report in result["items"]:
        reports.append(ReportResponse.from_orm(report))

    return ReportListResponse(
        items=reports,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/analytics/reports/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить отчет по ID"""
    service = AnalyticsService(db)
    report = service.get_report(report_id, current_user)
    return ReportResponse.from_orm(report)


@router.post("/api/analytics/reports", response_model=ReportResponse)
def create_report(
    report_data: ReportCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый отчет"""
    service = AnalyticsService(db)
    report = service.create_report(report_data, current_user)
    return ReportResponse.from_orm(report)


@router.put("/api/analytics/reports/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_data: ReportUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить отчет"""
    service = AnalyticsService(db)
    report = service.update_report(report_id, report_data, current_user)
    return ReportResponse.from_orm(report)


@router.delete("/api/analytics/reports/{report_id}")
def delete_report(
    report_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить отчет"""
    service = AnalyticsService(db)
    service.delete_report(report_id, current_user)
    return {"message": "Report deleted successfully"}


# Alerts endpoints
@router.get("/api/analytics/alerts", response_model=AlertListResponse)
def get_alerts(
    skip: int = Query(0, ge=0, description="Количество пропущенных алертов"),
    limit: int = Query(20, ge=1, le=100, description="Количество алертов на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить алерты пользователя"""
    service = AnalyticsService(db)
    result = service.get_alerts(current_user, skip=skip, limit=limit)

    alerts = []
    for alert in result["items"]:
        alerts.append(AlertResponse.from_orm(alert))

    return AlertListResponse(
        items=alerts,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/analytics/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить алерт по ID"""
    service = AnalyticsService(db)
    alert = service.get_alert(alert_id, current_user)
    return AlertResponse.from_orm(alert)


@router.post("/api/analytics/alerts", response_model=AlertResponse)
def create_alert(
    alert_data: AlertCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый алерт"""
    service = AnalyticsService(db)
    alert = service.create_alert(alert_data, current_user)
    return AlertResponse.from_orm(alert)


@router.put("/api/analytics/alerts/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить алерт"""
    service = AnalyticsService(db)
    alert = service.update_alert(alert_id, alert_data, current_user)
    return AlertResponse.from_orm(alert)


@router.delete("/api/analytics/alerts/{alert_id}")
def delete_alert(
    alert_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить алерт"""
    service = AnalyticsService(db)
    service.delete_alert(alert_id, current_user)
    return {"message": "Alert deleted successfully"}


# Events tracking
@router.post("/api/analytics/events", response_model=EventResponse)
def track_event(
    event_data: EventCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Отслеживание событий"""
    service = AnalyticsService(db)
    event = service.track_event(event_data, current_user)
    return EventResponse.from_orm(event)


@router.get("/api/analytics/events")
def get_events(
    skip: int = Query(0, ge=0, description="Количество пропущенных событий"),
    limit: int = Query(50, ge=1, le=200, description="Количество событий на странице"),
    event_type: Optional[str] = Query(None, description="Фильтр по типу события"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить события пользователя"""
    service = AnalyticsService(db)
    result = service.get_events(
        current_user, skip=skip, limit=limit, event_type=event_type
    )
    return result
