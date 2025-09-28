"""
Сервис уведомлений
"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
import json
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Сервис для отправки уведомлений"""

    def __init__(self):
        self.mail_config = ConnectionConfig(
            MAIL_USERNAME="noreply@example.com",
            MAIL_PASSWORD="password",
            MAIL_FROM="noreply@example.com",
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        self.fastmail = FastMail(self.mail_config)

        # In-memory хранилище уведомлений (в продакшене использовать Redis)
        self.notifications: Dict[int, List[Dict]] = {}

    async def send_email_notification(
        self, to_email: str, subject: str, template: str, context: Dict[str, Any]
    ) -> bool:
        """Отправка email уведомления"""
        try:
            # В реальном приложении здесь будет отправка email
            logger.info(f"Email notification sent to {to_email}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def send_push_notification(
        self, user_id: int, title: str, body: str, data: Optional[Dict] = None
    ) -> bool:
        """Отправка push уведомления"""
        try:
            # В реальном приложении здесь будет отправка через FCM/APNS
            logger.info(f"Push notification sent to user {user_id}: {title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send push to user {user_id}: {e}")
            return False

    async def create_in_app_notification(
        self,
        user_id: int,
        type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None,
    ) -> Dict:
        """Создание in-app уведомления"""
        notification = {
            "id": len(self.notifications.get(user_id, [])) + 1,
            "type": type,
            "title": title,
            "message": message,
            "data": data or {},
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        if user_id not in self.notifications:
            self.notifications[user_id] = []

        self.notifications[user_id].append(notification)

        # Ограничиваем количество уведомлений на пользователя
        if len(self.notifications[user_id]) > 100:
            self.notifications[user_id] = self.notifications[user_id][-100:]

        logger.info(f"In-app notification created for user {user_id}: {title}")
        return notification

    async def get_user_notifications(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> List[Dict]:
        """Получение уведомлений пользователя"""
        user_notifications = self.notifications.get(user_id, [])
        return user_notifications[offset : offset + limit]

    async def mark_notification_read(self, user_id: int, notification_id: int) -> bool:
        """Отметить уведомление как прочитанное"""
        user_notifications = self.notifications.get(user_id, [])
        for notification in user_notifications:
            if notification["id"] == notification_id:
                notification["is_read"] = True
                return True
        return False

    async def mark_all_notifications_read(self, user_id: int) -> int:
        """Отметить все уведомления как прочитанные"""
        user_notifications = self.notifications.get(user_id, [])
        count = 0
        for notification in user_notifications:
            if not notification["is_read"]:
                notification["is_read"] = True
                count += 1
        return count

    async def get_unread_count(self, user_id: int) -> int:
        """Получить количество непрочитанных уведомлений"""
        user_notifications = self.notifications.get(user_id, [])
        return sum(1 for n in user_notifications if not n["is_read"])

    async def send_notification(
        self,
        user_id: int,
        type: str,
        title: str,
        message: str,
        channels: List[str] = ["in_app"],
        data: Optional[Dict] = None,
    ) -> Dict:
        """Универсальная отправка уведомления"""
        results = {}

        # In-app уведомление
        if "in_app" in channels:
            notification = await self.create_in_app_notification(
                user_id, type, title, message, data
            )
            results["in_app"] = notification

        # Email уведомление
        if "email" in channels:
            # Здесь нужно получить email пользователя из БД
            email_result = await self.send_email_notification(
                f"user{user_id}@example.com",  # Временный email
                title,
                "notification.html",
                {"message": message, "data": data},
            )
            results["email"] = email_result

        # Push уведомление
        if "push" in channels:
            push_result = await self.send_push_notification(
                user_id, title, message, data
            )
            results["push"] = push_result

        return results


# Глобальный экземпляр сервиса
notification_service = NotificationService()
