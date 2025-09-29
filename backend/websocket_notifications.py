"""
WebSocket Notifications - интеграция WebSocket с API сервисами
"""

import asyncio
from typing import Dict, Any
from websocket_manager import websocket_manager
import logging

logger = logging.getLogger(__name__)


class WebSocketNotifications:
    """Класс для отправки уведомлений через WebSocket"""

    @staticmethod
    async def send_social_update(event_type: str, data: Dict[str, Any]):
        """Отправка обновлений социальной сети"""
        message = {
            "type": "social_update",
            "event": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_subscribers("social", message)
        logger.info(f"Social update sent: {event_type}")

    @staticmethod
    async def send_ecommerce_update(event_type: str, data: Dict[str, Any]):
        """Отправка обновлений e-commerce"""
        message = {
            "type": "ecommerce_update",
            "event": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_subscribers("ecommerce", message)
        logger.info(f"E-commerce update sent: {event_type}")

    @staticmethod
    async def send_tasks_update(event_type: str, data: Dict[str, Any]):
        """Отправка обновлений задач"""
        message = {
            "type": "tasks_update",
            "event": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_subscribers("tasks", message)
        logger.info(f"Tasks update sent: {event_type}")

    @staticmethod
    async def send_analytics_update(event_type: str, data: Dict[str, Any]):
        """Отправка обновлений аналитики"""
        message = {
            "type": "analytics_update",
            "event": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_subscribers("analytics", message)
        logger.info(f"Analytics update sent: {event_type}")

    @staticmethod
    async def send_content_update(event_type: str, data: Dict[str, Any]):
        """Отправка обновлений контента"""
        message = {
            "type": "content_update",
            "event": event_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_subscribers("content", message)
        logger.info(f"Content update sent: {event_type}")

    @staticmethod
    async def send_system_notification(
        notification_type: str, message: str, data: Dict[str, Any] = None
    ):
        """Отправка системных уведомлений"""
        notification = {
            "type": "system_notification",
            "notification_type": notification_type,
            "message": message,
            "data": data or {},
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.broadcast(notification)
        logger.info(f"System notification sent: {notification_type}")

    @staticmethod
    async def send_user_notification(
        user_id: str, notification_type: str, message: str, data: Dict[str, Any] = None
    ):
        """Отправка уведомлений конкретному пользователю"""
        notification = {
            "type": "user_notification",
            "notification_type": notification_type,
            "message": message,
            "data": data or {},
            "timestamp": asyncio.get_event_loop().time(),
        }
        await websocket_manager.send_to_user(notification, user_id)
        logger.info(f"User notification sent to {user_id}: {notification_type}")


# Глобальный экземпляр для использования в API
ws_notifications = WebSocketNotifications()
