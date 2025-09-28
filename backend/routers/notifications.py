"""
API для уведомлений
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from services.notification_service import notification_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


class NotificationCreate(BaseModel):
    type: str
    title: str
    message: str
    channels: List[str] = ["in_app"]
    data: Optional[dict] = None


class NotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    message: str
    data: dict
    is_read: bool
    created_at: str


class NotificationStats(BaseModel):
    total: int
    unread: int
    by_type: dict


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
):
    """Получить уведомления пользователя"""
    notifications = await notification_service.get_user_notifications(
        current_user.id, limit, offset
    )
    return notifications


@router.get("/stats", response_model=NotificationStats)
async def get_notification_stats(current_user: User = Depends(get_current_user)):
    """Получить статистику уведомлений"""
    notifications = await notification_service.get_user_notifications(
        current_user.id, limit=1000
    )

    total = len(notifications)
    unread = await notification_service.get_unread_count(current_user.id)

    by_type = {}
    for notification in notifications:
        notification_type = notification["type"]
        if notification_type not in by_type:
            by_type[notification_type] = {"total": 0, "unread": 0}
        by_type[notification_type]["total"] += 1
        if not notification["is_read"]:
            by_type[notification_type]["unread"] += 1

    return NotificationStats(total=total, unread=unread, by_type=by_type)


@router.post("/mark-read/{notification_id}")
async def mark_notification_read(
    notification_id: int, current_user: User = Depends(get_current_user)
):
    """Отметить уведомление как прочитанное"""
    success = await notification_service.mark_notification_read(
        current_user.id, notification_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}


@router.post("/mark-all-read")
async def mark_all_notifications_read(current_user: User = Depends(get_current_user)):
    """Отметить все уведомления как прочитанные"""
    count = await notification_service.mark_all_notifications_read(current_user.id)
    return {"message": f"{count} notifications marked as read"}


@router.post("/send")
async def send_notification(
    notification: NotificationCreate, current_user: User = Depends(get_current_user)
):
    """Отправить уведомление (для тестирования)"""
    results = await notification_service.send_notification(
        current_user.id,
        notification.type,
        notification.title,
        notification.message,
        notification.channels,
        notification.data,
    )
    return {"message": "Notification sent", "results": results}


@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_user)):
    """Получить количество непрочитанных уведомлений"""
    count = await notification_service.get_unread_count(current_user.id)
    return {"unread_count": count}
