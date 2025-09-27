from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.analytics as analytics_models
import models
from typing import List, Dict, Any

router = APIRouter()


# Dashboard endpoints
@router.get("/api/analytics/dashboard")
def get_dashboard_data(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить данные для дашборда"""
    # Mock данные для демонстрации
    dashboard_data = {
        "stats": {
            "total_users": db.query(models.User).count(),
            "total_products": 89,  # Mock data
            "total_orders": 456,  # Mock data
            "total_revenue": 125000,  # Mock data
        },
        "recent_activity": [
            {
                "type": "user_registration",
                "message": "New user: John Doe",
                "timestamp": "2 minutes ago",
            },
            {
                "type": "order",
                "message": "Order from Jane Smith: $299.99",
                "timestamp": "5 minutes ago",
            },
        ],
        "charts": {
            "user_growth": {
                "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                "data": [100, 150, 200, 250, 300],
            },
            "revenue": {
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "data": [25000, 30000, 35000, 35000],
            },
        },
    }
    return dashboard_data


@router.get("/api/analytics/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """Получить список метрик"""
    metrics = (
        db.query(analytics_models.Metric)
        .filter(analytics_models.Metric.is_active == True)
        .all()
    )
    return metrics


@router.post("/api/analytics/metrics")
def create_metric(
    metric_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую метрику"""
    metric = analytics_models.Metric(**metric_data)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


@router.get("/api/analytics/metrics/{metric_id}/data")
def get_metric_data(metric_id: int, db: Session = Depends(get_db)):
    """Получить данные метрики"""
    metric = (
        db.query(analytics_models.Metric)
        .filter(analytics_models.Metric.id == metric_id)
        .first()
    )
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    data_points = (
        db.query(analytics_models.MetricData)
        .filter(analytics_models.MetricData.metric_id == metric_id)
        .order_by(analytics_models.MetricData.timestamp.desc())
        .limit(100)
        .all()
    )
    return data_points


# Reports endpoints
@router.get("/api/analytics/reports")
def get_reports(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить отчеты пользователя"""
    reports = (
        db.query(analytics_models.Report)
        .filter(analytics_models.Report.created_by_id == current_user.id)
        .all()
    )
    return reports


@router.post("/api/analytics/reports")
def create_report(
    report_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый отчет"""
    report = analytics_models.Report(
        name=report_data.get("name"),
        description=report_data.get("description"),
        report_type=report_data.get("report_type"),
        parameters=report_data.get("parameters", {}),
        created_by_id=current_user.id,
        is_public=report_data.get("is_public", False),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("/api/analytics/reports/{report_id}")
def get_report(
    report_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить отчет по ID"""
    report = (
        db.query(analytics_models.Report)
        .filter(
            analytics_models.Report.id == report_id,
            analytics_models.Report.created_by_id == current_user.id,
        )
        .first()
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# Dashboards endpoints
@router.get("/api/analytics/dashboards")
def get_dashboards(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить дашборды пользователя"""
    dashboards = (
        db.query(analytics_models.Dashboard)
        .filter(analytics_models.Dashboard.created_by_id == current_user.id)
        .all()
    )
    return dashboards


@router.post("/api/analytics/dashboards")
def create_dashboard(
    dashboard_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый дашборд"""
    dashboard = analytics_models.Dashboard(
        name=dashboard_data.get("name"),
        description=dashboard_data.get("description"),
        created_by_id=current_user.id,
        is_public=dashboard_data.get("is_public", False),
        layout_config=dashboard_data.get("layout_config", {}),
    )
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    return dashboard


# Alerts endpoints
@router.get("/api/analytics/alerts")
def get_alerts(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить алерты пользователя"""
    alerts = (
        db.query(analytics_models.Alert)
        .filter(analytics_models.Alert.created_by_id == current_user.id)
        .all()
    )
    return alerts


@router.post("/api/analytics/alerts")
def create_alert(
    alert_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый алерт"""
    alert = analytics_models.Alert(
        name=alert_data.get("name"),
        description=alert_data.get("description"),
        condition=alert_data.get("condition", {}),
        threshold=alert_data.get("threshold"),
        created_by_id=current_user.id,
        is_active=alert_data.get("is_active", True),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


# Events tracking
@router.post("/api/analytics/events")
def track_event(event_data: dict, db: Session = Depends(get_db)):
    """Отслеживание событий"""
    # В реальном приложении здесь была бы логика сохранения событий
    return {"message": "Event tracked", "event_type": event_data.get("type")}
