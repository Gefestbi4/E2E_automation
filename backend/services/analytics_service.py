"""
Сервис для Analytics модуля
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from datetime import datetime, timedelta

import models_package.analytics as analytics_models
from models import User
from schemas.analytics import (
    DashboardCreate,
    DashboardUpdate,
    DashboardFilters,
    ReportCreate,
    ReportUpdate,
    ReportFilters,
    AlertCreate,
    AlertUpdate,
    AlertFilters,
)
from utils.database import QueryBuilder, PaginationHelper, SearchHelper
from utils.exceptions import (
    DashboardNotFoundError,
    ReportNotFoundError,
    AlertNotFoundError,
    NotFoundError,
    BusinessLogicError,
)


class AnalyticsService:
    """Сервис для работы с аналитикой"""

    def __init__(self, db: Session):
        self.db = db

    # Dashboards methods
    def get_dashboards(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[DashboardFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список дашбордов с фильтрацией"""
        query = self.db.query(analytics_models.Dashboard)

        if filters:
            # Фильтр по создателю
            if filters.created_by_id:
                query = query.filter(
                    analytics_models.Dashboard.created_by_id == filters.created_by_id
                )

            # Фильтр по публичности
            if filters.is_public is not None:
                query = query.filter(
                    analytics_models.Dashboard.is_public == filters.is_public
                )

            # Фильтр по умолчанию
            if filters.is_default is not None:
                query = query.filter(
                    analytics_models.Dashboard.is_default == filters.is_default
                )

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    analytics_models.Dashboard,
                    filters.search,
                    ["name", "description"],
                )

        # Если пользователь не указан, показываем только публичные дашборды
        if not user:
            query = query.filter(analytics_models.Dashboard.is_public == True)
        else:
            # Показываем дашборды пользователя и публичные дашборды
            query = query.filter(
                or_(
                    analytics_models.Dashboard.created_by_id == user.id,
                    analytics_models.Dashboard.is_public == True,
                )
            )

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(analytics_models.Dashboard.created_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем статистику для каждого дашборда
        dashboards_with_stats = []
        for dashboard in result["items"]:
            # Подсчитываем количество отчетов в дашборде
            reports_count = (
                self.db.query(analytics_models.Report)
                .filter(analytics_models.Report.dashboard_id == dashboard.id)
                .count()
            )

            # Подсчитываем количество алертов
            alerts_count = (
                self.db.query(analytics_models.Alert)
                .filter(analytics_models.Alert.dashboard_id == dashboard.id)
                .count()
            )

            dashboards_with_stats.append(
                {
                    "dashboard": dashboard,
                    "reports_count": reports_count,
                    "alerts_count": alerts_count,
                }
            )

        result["items"] = dashboards_with_stats
        return result

    def get_dashboard(
        self, dashboard_id: int, user: Optional[User] = None
    ) -> Dict[str, Any]:
        """Получить дашборд по ID"""
        query = self.db.query(analytics_models.Dashboard).filter(
            analytics_models.Dashboard.id == dashboard_id
        )

        # Проверяем права доступа
        if user:
            query = query.filter(
                or_(
                    analytics_models.Dashboard.created_by_id == user.id,
                    analytics_models.Dashboard.is_public == True,
                )
            )
        else:
            query = query.filter(analytics_models.Dashboard.is_public == True)

        dashboard = query.first()

        if not dashboard:
            raise DashboardNotFoundError(str(dashboard_id))

        # Получаем отчеты пользователя (модель Report не связана с Dashboard)
        reports = (
            self.db.query(analytics_models.Report)
            .filter(analytics_models.Report.created_by_id == user.id)
            .order_by(analytics_models.Report.created_at.desc())
            .limit(5)  # Ограничиваем количество отчетов
            .all()
        )

        # Получаем алерты пользователя (модель Alert не связана с Dashboard)
        alerts = (
            self.db.query(analytics_models.Alert)
            .filter(analytics_models.Alert.created_by_id == user.id)
            .order_by(analytics_models.Alert.created_at.desc())
            .limit(5)  # Ограничиваем количество алертов
            .all()
        )

        # Подсчитываем статистику
        reports_count = len(reports)
        alerts_count = len(alerts)

        return {
            "dashboard": dashboard,
            "reports": reports,
            "alerts": alerts,
            "reports_count": reports_count,
            "alerts_count": alerts_count,
        }

    def create_dashboard(
        self, dashboard_data: DashboardCreate, user: User
    ) -> analytics_models.Dashboard:
        """Создать новый дашборд"""
        dashboard = analytics_models.Dashboard(
            name=dashboard_data.name,
            description=dashboard_data.description,
            is_public=dashboard_data.is_public,
            created_by_id=user.id,
            layout_config={},
        )
        self.db.add(dashboard)
        self.db.commit()
        self.db.refresh(dashboard)
        return dashboard

    def update_dashboard(
        self, dashboard_id: int, dashboard_data: DashboardUpdate, user: User
    ) -> analytics_models.Dashboard:
        """Обновить дашборд"""
        dashboard_info = self.get_dashboard(dashboard_id, user)
        dashboard = dashboard_info["dashboard"]

        # Проверяем, что пользователь является создателем дашборда
        if dashboard.created_by_id != user.id:
            raise NotFoundError("Dashboard", str(dashboard_id))

        update_data = dashboard_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(dashboard, field, value)

        self.db.commit()
        self.db.refresh(dashboard)
        return dashboard

    def delete_dashboard(self, dashboard_id: int, user: User) -> bool:
        """Удалить дашборд"""
        dashboard_info = self.get_dashboard(dashboard_id, user)
        dashboard = dashboard_info["dashboard"]

        # Проверяем, что пользователь является создателем дашборда
        if dashboard.created_by_id != user.id:
            raise NotFoundError("Dashboard", str(dashboard_id))

        # Удаляем все отчеты и алерты дашборда
        self.db.query(analytics_models.Report).filter(
            analytics_models.Report.dashboard_id == dashboard_id
        ).delete()

        self.db.query(analytics_models.Alert).filter(
            analytics_models.Alert.dashboard_id == dashboard_id
        ).delete()

        self.db.delete(dashboard)
        self.db.commit()
        return True

    # Reports methods
    def get_reports(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[ReportFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список отчетов с фильтрацией"""
        query = self.db.query(analytics_models.Report)

        if filters:
            # Фильтр по дашборду
            if filters.dashboard_id:
                query = query.filter(
                    analytics_models.Report.dashboard_id == filters.dashboard_id
                )

            # Фильтр по типу отчета
            if filters.type:
                query = query.filter(analytics_models.Report.type == filters.type)

            # Фильтр по статусу
            if filters.status:
                query = query.filter(analytics_models.Report.status == filters.status)

            # Фильтр по расписанию
            if filters.schedule:
                query = query.filter(
                    analytics_models.Report.schedule == filters.schedule
                )

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    analytics_models.Report,
                    filters.search,
                    ["name", "description"],
                )

        # Если пользователь указан, показываем только его отчеты
        if user:
            query = query.filter(analytics_models.Report.created_by_id == user.id)

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(analytics_models.Report.created_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем дополнительную информацию для каждого отчета
        reports_with_stats = []
        for report in result["items"]:
            # Проверяем, активен ли отчет
            is_active = report.status == "active"

            # Проверяем, нужно ли обновить отчет
            needs_update = False
            if report.schedule and report.last_run:
                # Простая логика проверки необходимости обновления
                if report.schedule == "daily":
                    needs_update = (datetime.now() - report.last_run).days >= 1
                elif report.schedule == "weekly":
                    needs_update = (datetime.now() - report.last_run).days >= 7
                elif report.schedule == "monthly":
                    needs_update = (datetime.now() - report.last_run).days >= 30

            reports_with_stats.append(
                {
                    "report": report,
                    "is_active": is_active,
                    "needs_update": needs_update,
                }
            )

        result["items"] = reports_with_stats
        return result

    def get_report(self, report_id: int, user: Optional[User] = None) -> Dict[str, Any]:
        """Получить отчет по ID"""
        query = self.db.query(analytics_models.Report).filter(
            analytics_models.Report.id == report_id
        )

        # Если пользователь указан, проверяем права доступа
        if user:
            query = query.filter(analytics_models.Report.created_by_id == user.id)

        report = query.first()

        if not report:
            raise ReportNotFoundError(str(report_id))

        # Проверяем, активен ли отчет
        is_active = report.status == "active"

        # Проверяем, нужно ли обновить отчет
        needs_update = False
        if report.schedule and report.last_run:
            if report.schedule == "daily":
                needs_update = (datetime.now() - report.last_run).days >= 1
            elif report.schedule == "weekly":
                needs_update = (datetime.now() - report.last_run).days >= 7
            elif report.schedule == "monthly":
                needs_update = (datetime.now() - report.last_run).days >= 30

        return {
            "report": report,
            "is_active": is_active,
            "needs_update": needs_update,
        }

    def create_report(
        self, report_data: ReportCreate, user: User
    ) -> analytics_models.Report:
        """Создать новый отчет"""
        report = analytics_models.Report(
            name=report_data.name,
            description=report_data.description,
            type=report_data.type,
            parameters=report_data.parameters or {},
            dashboard_id=report_data.dashboard_id,
            created_by_id=user.id,
            status=report_data.status or "active",
            schedule=report_data.schedule,
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def update_report(
        self, report_id: int, report_data: ReportUpdate, user: User
    ) -> analytics_models.Report:
        """Обновить отчет"""
        report_info = self.get_report(report_id, user)
        report = report_info["report"]

        update_data = report_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(report, field, value)

        self.db.commit()
        self.db.refresh(report)
        return report

    def delete_report(self, report_id: int, user: User) -> bool:
        """Удалить отчет"""
        report_info = self.get_report(report_id, user)
        report = report_info["report"]

        self.db.delete(report)
        self.db.commit()
        return True

    def run_report(self, report_id: int, user: User) -> Dict[str, Any]:
        """Запустить отчет"""
        report_info = self.get_report(report_id, user)
        report = report_info["report"]

        # Обновляем время последнего запуска
        report.last_run = datetime.now()
        self.db.commit()

        # Здесь была бы логика генерации отчета
        # Пока что возвращаем заглушку
        return {
            "report_id": report_id,
            "status": "completed",
            "data": {
                "message": "Report generated successfully",
                "generated_at": datetime.now().isoformat(),
            },
        }

    # Alerts methods
    def get_alerts(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[AlertFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список алертов с фильтрацией"""
        query = self.db.query(analytics_models.Alert)

        if filters:
            # Фильтр по дашборду
            if filters.dashboard_id:
                query = query.filter(
                    analytics_models.Alert.dashboard_id == filters.dashboard_id
                )

            # Фильтр по типу алерта
            if filters.type:
                query = query.filter(analytics_models.Alert.type == filters.type)

            # Фильтр по статусу
            if filters.status:
                query = query.filter(analytics_models.Alert.status == filters.status)

            # Фильтр по приоритету
            if filters.priority:
                query = query.filter(
                    analytics_models.Alert.priority == filters.priority
                )

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    analytics_models.Alert,
                    filters.search,
                    ["name", "message"],
                )

        # Если пользователь указан, показываем только его алерты
        if user:
            query = query.filter(analytics_models.Alert.created_by_id == user.id)

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(analytics_models.Alert.created_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем дополнительную информацию для каждого алерта
        alerts_with_stats = []
        for alert in result["items"]:
            # Проверяем, активен ли алерт
            is_active = alert.status == "active"

            # Проверяем, просрочен ли алерт
            is_overdue = False
            if alert.due_date and alert.status != "resolved":
                is_overdue = alert.due_date < datetime.now()

            alerts_with_stats.append(
                {
                    "alert": alert,
                    "is_active": is_active,
                    "is_overdue": is_overdue,
                }
            )

        result["items"] = alerts_with_stats
        return result

    def get_alert(self, alert_id: int, user: Optional[User] = None) -> Dict[str, Any]:
        """Получить алерт по ID"""
        query = self.db.query(analytics_models.Alert).filter(
            analytics_models.Alert.id == alert_id
        )

        # Если пользователь указан, проверяем права доступа
        if user:
            query = query.filter(analytics_models.Alert.created_by_id == user.id)

        alert = query.first()

        if not alert:
            raise AlertNotFoundError(str(alert_id))

        # Проверяем, активен ли алерт
        is_active = alert.status == "active"

        # Проверяем, просрочен ли алерт
        is_overdue = False
        if alert.due_date and alert.status != "resolved":
            is_overdue = alert.due_date < datetime.now()

        return {
            "alert": alert,
            "is_active": is_active,
            "is_overdue": is_overdue,
        }

    def create_alert(
        self, alert_data: AlertCreate, user: User
    ) -> analytics_models.Alert:
        """Создать новый алерт"""
        alert = analytics_models.Alert(
            name=alert_data.name,
            message=alert_data.message,
            type=alert_data.type,
            priority=alert_data.priority,
            dashboard_id=alert_data.dashboard_id,
            created_by_id=user.id,
            status=alert_data.status or "active",
            due_date=alert_data.due_date,
            conditions=alert_data.conditions or {},
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def update_alert(
        self, alert_id: int, alert_data: AlertUpdate, user: User
    ) -> analytics_models.Alert:
        """Обновить алерт"""
        alert_info = self.get_alert(alert_id, user)
        alert = alert_info["alert"]

        update_data = alert_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(alert, field, value)

        self.db.commit()
        self.db.refresh(alert)
        return alert

    def delete_alert(self, alert_id: int, user: User) -> bool:
        """Удалить алерт"""
        alert_info = self.get_alert(alert_id, user)
        alert = alert_info["alert"]

        self.db.delete(alert)
        self.db.commit()
        return True

    def resolve_alert(self, alert_id: int, user: User) -> analytics_models.Alert:
        """Решить алерт"""
        alert_info = self.get_alert(alert_id, user)
        alert = alert_info["alert"]

        alert.status = "resolved"
        alert.resolved_at = datetime.now()
        self.db.commit()
        self.db.refresh(alert)
        return alert

    # Analytics methods
    def get_system_analytics(self, user: User) -> Dict[str, Any]:
        """Получить системную аналитику"""
        # Общая статистика пользователей
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()

        # Статистика по модулям (заглушки, так как нет реальных данных)
        ecommerce_stats = {
            "total_products": 0,
            "total_orders": 0,
            "total_revenue": 0,
        }

        social_stats = {
            "total_posts": 0,
            "total_comments": 0,
            "total_follows": 0,
        }

        tasks_stats = {
            "total_boards": 0,
            "total_cards": 0,
            "completed_cards": 0,
        }

        content_stats = {
            "total_articles": 0,
            "published_articles": 0,
            "total_categories": 0,
        }

        # Статистика дашбордов пользователя
        user_dashboards = (
            self.db.query(analytics_models.Dashboard)
            .filter(analytics_models.Dashboard.created_by_id == user.id)
            .count()
        )

        user_reports = (
            self.db.query(analytics_models.Report)
            .filter(analytics_models.Report.created_by_id == user.id)
            .count()
        )

        user_alerts = (
            self.db.query(analytics_models.Alert)
            .filter(analytics_models.Alert.created_by_id == user.id)
            .count()
        )

        return {
            "users": {
                "total": total_users,
                "active": active_users,
            },
            "modules": {
                "ecommerce": ecommerce_stats,
                "social": social_stats,
                "tasks": tasks_stats,
                "content": content_stats,
            },
            "analytics": {
                "dashboards": user_dashboards,
                "reports": user_reports,
                "alerts": user_alerts,
            },
        }

    def get_dashboard_analytics(self, dashboard_id: int, user: User) -> Dict[str, Any]:
        """Получить аналитику дашборда"""
        dashboard_info = self.get_dashboard(dashboard_id, user)
        dashboard = dashboard_info["dashboard"]

        # Статистика отчетов
        total_reports = len(dashboard_info["reports"])
        active_reports = len(
            [r for r in dashboard_info["reports"] if r.status == "active"]
        )

        # Статистика алертов
        total_alerts = len(dashboard_info["alerts"])
        active_alerts = len(
            [a for a in dashboard_info["alerts"] if a.status == "active"]
        )
        overdue_alerts = len(
            [
                a
                for a in dashboard_info["alerts"]
                if a.due_date and a.due_date < datetime.now() and a.status != "resolved"
            ]
        )

        return {
            "dashboard_id": dashboard_id,
            "reports": {
                "total": total_reports,
                "active": active_reports,
            },
            "alerts": {
                "total": total_alerts,
                "active": active_alerts,
                "overdue": overdue_alerts,
            },
        }

    def track_event(self, event_data, user: User) -> dict:
        """Отслеживание события"""
        # Простое логирование события (модель Event не существует)
        event_info = {
            "name": getattr(
                event_data, "name", getattr(event_data, "event_type", "unknown")
            ),
            "properties": getattr(
                event_data, "properties", getattr(event_data, "event_data", {})
            ),
            "user_id": user.id,
            "timestamp": datetime.now().isoformat(),
        }
        # В реальном приложении здесь было бы сохранение в БД
        return event_info
