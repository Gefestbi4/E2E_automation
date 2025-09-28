"""
API для расширенных уведомлений
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.advanced_notification_service import advanced_notification_service
from auth import get_current_user
from models import User

router = APIRouter(
    prefix="/api/advanced-notifications", tags=["advanced-notifications"]
)


class SmartNotificationRequest(BaseModel):
    notification_type: str
    title: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    smart_features: bool = True


class NotificationPreferences(BaseModel):
    enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    in_app_notifications: Optional[bool] = None
    quiet_hours: Optional[Dict[str, Any]] = None
    categories: Optional[Dict[str, bool]] = None
    priorities: Optional[Dict[str, bool]] = None
    batch_similar: Optional[bool] = None
    max_daily: Optional[int] = None
    digest_frequency: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    data: Dict[str, Any]
    is_read: bool
    created_at: str
    priority: str
    category: str
    smart_features: Dict[str, Any]


class SmartNotificationsResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    categories: List[str]
    priority_distribution: Dict[str, int]


class NotificationAnalytics(BaseModel):
    period_days: int
    total_notifications: int
    read_notifications: int
    unread_notifications: int
    type_distribution: Dict[str, Dict[str, int]]
    priority_distribution: Dict[str, int]
    category_distribution: Dict[str, int]
    average_daily: float
    read_rate: float


@router.post("/create", response_model=NotificationResponse)
async def create_smart_notification(
    request: SmartNotificationRequest, current_user: User = Depends(get_current_user)
):
    """Создать умное уведомление."""
    try:
        notification = await advanced_notification_service.create_smart_notification(
            user_id=current_user.id,
            notification_type=request.notification_type,
            title=request.title,
            message=request.message,
            data=request.data,
            smart_features=request.smart_features,
        )

        if notification is None:
            raise HTTPException(
                status_code=400,
                detail="Уведомление не было создано из-за настроек пользователя",
            )

        return notification
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка создания уведомления: {str(e)}"
        )


@router.get("/", response_model=SmartNotificationsResponse)
async def get_smart_notifications(
    limit: int = Query(20, description="Количество уведомлений"),
    offset: int = Query(0, description="Смещение"),
    unread_only: bool = Query(False, description="Только непрочитанные"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    priority: Optional[str] = Query(None, description="Фильтр по приоритету"),
    current_user: User = Depends(get_current_user),
):
    """Получить умные уведомления с фильтрацией."""
    try:
        result = await advanced_notification_service.get_smart_notifications(
            user_id=current_user.id,
            limit=limit,
            offset=offset,
            unread_only=unread_only,
            category=category,
            priority=priority,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения уведомлений: {str(e)}"
        )


@router.get("/analytics", response_model=NotificationAnalytics)
async def get_notification_analytics(
    period_days: int = Query(30, description="Период в днях"),
    current_user: User = Depends(get_current_user),
):
    """Получить аналитику уведомлений."""
    try:
        analytics = await advanced_notification_service.get_notification_analytics(
            user_id=current_user.id, period_days=period_days
        )
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения аналитики: {str(e)}"
        )


@router.get("/preferences", response_model=NotificationPreferences)
async def get_notification_preferences(current_user: User = Depends(get_current_user)):
    """Получить настройки уведомлений пользователя."""
    try:
        preferences = await advanced_notification_service.get_notification_preferences(
            user_id=current_user.id
        )
        return preferences
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения настроек: {str(e)}"
        )


@router.put("/preferences", response_model=NotificationPreferences)
async def update_notification_preferences(
    preferences: NotificationPreferences, current_user: User = Depends(get_current_user)
):
    """Обновить настройки уведомлений пользователя."""
    try:
        updated_preferences = (
            await advanced_notification_service.update_notification_preferences(
                user_id=current_user.id,
                preferences=preferences.model_dump(exclude_unset=True),
            )
        )
        return updated_preferences
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка обновления настроек: {str(e)}"
        )


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int, current_user: User = Depends(get_current_user)
):
    """Отметить уведомление как прочитанное."""
    try:
        success = await advanced_notification_service.mark_as_read(
            user_id=current_user.id, notification_id=notification_id
        )
        if not success:
            raise HTTPException(status_code=404, detail="Уведомление не найдено")
        return {"message": "Уведомление отмечено как прочитанное"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка обновления уведомления: {str(e)}"
        )


@router.put("/mark-all-read")
async def mark_all_notifications_read(current_user: User = Depends(get_current_user)):
    """Отметить все уведомления как прочитанные."""
    try:
        count = await advanced_notification_service.mark_all_as_read(
            user_id=current_user.id
        )
        return {"message": f"Отмечено как прочитанные {count} уведомлений"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка обновления уведомлений: {str(e)}"
        )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int, current_user: User = Depends(get_current_user)
):
    """Удалить уведомление."""
    try:
        success = await advanced_notification_service.delete_notification(
            user_id=current_user.id, notification_id=notification_id
        )
        if not success:
            raise HTTPException(status_code=404, detail="Уведомление не найдено")
        return {"message": "Уведомление удалено"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка удаления уведомления: {str(e)}"
        )


@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_user)):
    """Получить количество непрочитанных уведомлений."""
    try:
        count = await advanced_notification_service.get_unread_count(
            user_id=current_user.id
        )
        return {"unread_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения количества уведомлений: {str(e)}"
        )


@router.post("/test")
async def send_test_notification(
    notification_type: str = Query(
        "system_alert", description="Тип тестового уведомления"
    ),
    current_user: User = Depends(get_current_user),
):
    """Отправить тестовое уведомление."""
    try:
        notification = await advanced_notification_service.send_test_notification(
            user_id=current_user.id, notification_type=notification_type
        )
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка отправки тестового уведомления: {str(e)}"
        )
