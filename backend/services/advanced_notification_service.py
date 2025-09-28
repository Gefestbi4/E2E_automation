"""
Расширенный сервис для управления умными уведомлениями
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import logging
import random
import json

logger = logging.getLogger(__name__)


class AdvancedNotificationService:
    """Расширенный сервис для управления умными уведомлениями"""

    def __init__(self):
        # В реальном приложении здесь будет взаимодействие с БД
        self.notifications_db = {}  # Моковая БД для хранения уведомлений
        self.user_preferences = {}  # Настройки уведомлений пользователей
        self.notification_templates = {
            "welcome": {
                "title": "Добро пожаловать!",
                "message": "Спасибо за регистрацию в нашей системе",
                "priority": "high",
                "category": "system",
            },
            "new_follower": {
                "title": "Новый подписчик",
                "message": "{follower_name} подписался на вас",
                "priority": "medium",
                "category": "social",
            },
            "post_like": {
                "title": "Лайк поста",
                "message": "{user_name} поставил лайк вашему посту",
                "priority": "low",
                "category": "social",
            },
            "comment_on_post": {
                "title": "Новый комментарий",
                "message": "{user_name} прокомментировал ваш пост",
                "priority": "medium",
                "category": "social",
            },
            "task_assigned": {
                "title": "Новая задача",
                "message": "Вам назначена новая задача: {task_title}",
                "priority": "high",
                "category": "work",
            },
            "product_update": {
                "title": "Обновление продукта",
                "message": "Доступно обновление для {product_name}",
                "priority": "medium",
                "category": "product",
            },
            "system_maintenance": {
                "title": "Техническое обслуживание",
                "message": "Запланировано техническое обслуживание с {start_time} до {end_time}",
                "priority": "high",
                "category": "system",
            },
            "security_alert": {
                "title": "Предупреждение безопасности",
                "message": "Обнаружена подозрительная активность в вашем аккаунте",
                "priority": "critical",
                "category": "security",
            },
        }

        # Умные правила для уведомлений
        self.smart_rules = {
            "batch_similar": True,  # Группировать похожие уведомления
            "quiet_hours": {"start": "22:00", "end": "08:00"},  # Тихие часы
            "max_daily": 50,  # Максимум уведомлений в день
            "priority_escalation": True,  # Повышение приоритета старых уведомлений
        }

    async def create_smart_notification(
        self,
        user_id: int,
        notification_type: str,
        title: Optional[str] = None,
        message: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        smart_features: bool = True,
    ) -> Dict[str, Any]:
        """Создает умное уведомление с автоматическими функциями."""
        logger.info(
            f"Creating smart notification for user {user_id}: {notification_type}"
        )

        # Проверяем, нужно ли отправлять уведомление
        if smart_features and not await self._should_send_notification(
            user_id, notification_type
        ):
            logger.info(
                f"Notification suppressed for user {user_id} due to smart rules"
            )
            return None

        # Получаем шаблон уведомления
        template = self.notification_templates.get(notification_type, {})

        # Формируем заголовок и сообщение
        final_title = title or template.get("title", "Уведомление")
        final_message = message or template.get("message", "У вас новое уведомление")

        # Применяем шаблонные переменные
        if data:
            final_title = self._apply_template_variables(final_title, data)
            final_message = self._apply_template_variables(final_message, data)

        # Определяем приоритет
        priority = template.get("priority", "low")
        if smart_features and await self._should_escalate_priority(
            user_id, notification_type
        ):
            priority = self._escalate_priority(priority)

        # Создаем уведомление
        notification_id = len(self.notifications_db) + 1
        notification = {
            "id": notification_id,
            "user_id": user_id,
            "type": notification_type,
            "title": final_title,
            "message": final_message,
            "data": data or {},
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "priority": priority,
            "category": template.get("category", "general"),
            "smart_features": {
                "batch_id": await self._get_batch_id(user_id, notification_type),
                "escalated": priority != template.get("priority", "low"),
                "quiet_hours_override": await self._is_quiet_hours_override(
                    notification_type
                ),
            },
        }

        if user_id not in self.notifications_db:
            self.notifications_db[user_id] = []

        self.notifications_db[user_id].append(notification)

        # Применяем умные функции
        if smart_features:
            await self._apply_smart_features(user_id, notification)

        return notification

    async def get_smart_notifications(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False,
        category: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Получает уведомления с умной группировкой и фильтрацией."""
        logger.info(f"Fetching smart notifications for user {user_id}")

        user_notifications = self.notifications_db.get(user_id, [])

        # Применяем фильтры
        if unread_only:
            user_notifications = [n for n in user_notifications if not n["is_read"]]

        if category:
            user_notifications = [
                n for n in user_notifications if n.get("category") == category
            ]

        if priority:
            user_notifications = [
                n for n in user_notifications if n.get("priority") == priority
            ]

        # Сортируем по приоритету и дате
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        user_notifications.sort(
            key=lambda x: (
                priority_order.get(x.get("priority", "low"), 3),
                -datetime.fromisoformat(
                    x["created_at"].replace("Z", "+00:00")
                ).timestamp(),
            )
        )

        # Группируем похожие уведомления
        grouped_notifications = await self._group_similar_notifications(
            user_notifications
        )

        # Применяем лимит и офсет
        paginated_notifications = grouped_notifications[offset : offset + limit]

        return {
            "notifications": paginated_notifications,
            "total": len(grouped_notifications),
            "unread_count": await self.get_unread_count(user_id),
            "categories": await self._get_notification_categories(user_id),
            "priority_distribution": await self._get_priority_distribution(user_id),
        }

    async def get_notification_analytics(
        self, user_id: int, period_days: int = 30
    ) -> Dict[str, Any]:
        """Получает аналитику уведомлений пользователя."""
        logger.info(
            f"Getting notification analytics for user {user_id}, period: {period_days} days"
        )

        user_notifications = self.notifications_db.get(user_id, [])
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=period_days)

        recent_notifications = [
            n
            for n in user_notifications
            if datetime.fromisoformat(n["created_at"].replace("Z", "+00:00"))
            >= cutoff_date
        ]

        # Статистика по типам
        type_stats = {}
        for notification in recent_notifications:
            n_type = notification["type"]
            if n_type not in type_stats:
                type_stats[n_type] = {"total": 0, "read": 0, "unread": 0}
            type_stats[n_type]["total"] += 1
            if notification["is_read"]:
                type_stats[n_type]["read"] += 1
            else:
                type_stats[n_type]["unread"] += 1

        # Статистика по приоритетам
        priority_stats = {}
        for notification in recent_notifications:
            priority = notification.get("priority", "low")
            if priority not in priority_stats:
                priority_stats[priority] = 0
            priority_stats[priority] += 1

        # Статистика по категориям
        category_stats = {}
        for notification in recent_notifications:
            category = notification.get("category", "general")
            if category not in category_stats:
                category_stats[category] = 0
            category_stats[category] += 1

        return {
            "period_days": period_days,
            "total_notifications": len(recent_notifications),
            "read_notifications": len(
                [n for n in recent_notifications if n["is_read"]]
            ),
            "unread_notifications": len(
                [n for n in recent_notifications if not n["is_read"]]
            ),
            "type_distribution": type_stats,
            "priority_distribution": priority_stats,
            "category_distribution": category_stats,
            "average_daily": len(recent_notifications) / period_days,
            "read_rate": len([n for n in recent_notifications if n["is_read"]])
            / max(len(recent_notifications), 1),
        }

    async def update_notification_preferences(
        self, user_id: int, preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Обновляет настройки уведомлений пользователя."""
        logger.info(f"Updating notification preferences for user {user_id}")

        default_preferences = {
            "enabled": True,
            "email_notifications": True,
            "push_notifications": True,
            "in_app_notifications": True,
            "quiet_hours": {"enabled": True, "start": "22:00", "end": "08:00"},
            "categories": {
                "system": True,
                "social": True,
                "work": True,
                "product": True,
                "security": True,
            },
            "priorities": {
                "critical": True,
                "high": True,
                "medium": True,
                "low": False,
            },
            "batch_similar": True,
            "max_daily": 50,
            "digest_frequency": "daily",  # daily, weekly, never
        }

        current_preferences = self.user_preferences.get(user_id, default_preferences)
        current_preferences.update(preferences)
        self.user_preferences[user_id] = current_preferences

        return current_preferences

    async def get_notification_preferences(self, user_id: int) -> Dict[str, Any]:
        """Получает настройки уведомлений пользователя."""
        default_preferences = {
            "enabled": True,
            "email_notifications": True,
            "push_notifications": True,
            "in_app_notifications": True,
            "quiet_hours": {"enabled": True, "start": "22:00", "end": "08:00"},
            "categories": {
                "system": True,
                "social": True,
                "work": True,
                "product": True,
                "security": True,
            },
            "priorities": {
                "critical": True,
                "high": True,
                "medium": True,
                "low": False,
            },
            "batch_similar": True,
            "max_daily": 50,
            "digest_frequency": "daily",
        }

        return self.user_preferences.get(user_id, default_preferences)

    async def mark_as_read(self, user_id: int, notification_id: int) -> bool:
        """Отмечает уведомление как прочитанное."""
        logger.info(
            f"Marking notification {notification_id} as read for user {user_id}"
        )

        user_notifications = self.notifications_db.get(user_id, [])
        for notification in user_notifications:
            if notification["id"] == notification_id:
                notification["is_read"] = True
                notification["read_at"] = datetime.now(timezone.utc).isoformat()
                return True
        return False

    async def mark_all_as_read(self, user_id: int) -> int:
        """Отмечает все уведомления пользователя как прочитанные."""
        logger.info(f"Marking all notifications as read for user {user_id}")

        user_notifications = self.notifications_db.get(user_id, [])
        count = 0
        for notification in user_notifications:
            if not notification["is_read"]:
                notification["is_read"] = True
                notification["read_at"] = datetime.now(timezone.utc).isoformat()
                count += 1
        return count

    async def get_unread_count(self, user_id: int) -> int:
        """Получает количество непрочитанных уведомлений."""
        user_notifications = self.notifications_db.get(user_id, [])
        return len([n for n in user_notifications if not n["is_read"]])

    async def delete_notification(self, user_id: int, notification_id: int) -> bool:
        """Удаляет уведомление."""
        logger.info(f"Deleting notification {notification_id} for user {user_id}")

        user_notifications = self.notifications_db.get(user_id, [])
        for i, notification in enumerate(user_notifications):
            if notification["id"] == notification_id:
                del user_notifications[i]
                return True
        return False

    async def send_test_notification(
        self, user_id: int, notification_type: str = "system_alert"
    ) -> Dict[str, Any]:
        """Отправляет тестовое уведомление."""
        logger.info(
            f"Sending test notification to user {user_id}, type: {notification_type}"
        )

        test_data = {
            "test": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_name": f"Test User {user_id}",
            "follower_name": "Test Follower",
            "task_title": "Test Task",
            "product_name": "Test Product",
        }

        return await self.create_smart_notification(
            user_id=user_id, notification_type=notification_type, data=test_data
        )

    # Приватные методы для умных функций

    async def _should_send_notification(
        self, user_id: int, notification_type: str
    ) -> bool:
        """Определяет, нужно ли отправлять уведомление на основе умных правил."""
        preferences = await self.get_notification_preferences(user_id)

        # Проверяем, включены ли уведомления
        if not preferences.get("enabled", True):
            return False

        # Проверяем тихие часы
        if preferences.get("quiet_hours", {}).get("enabled", False):
            current_time = datetime.now(timezone.utc).time()
            start_time = datetime.strptime(
                preferences["quiet_hours"]["start"], "%H:%M"
            ).time()
            end_time = datetime.strptime(
                preferences["quiet_hours"]["end"], "%H:%M"
            ).time()

            if start_time <= end_time:  # Обычный случай (например, 22:00 - 08:00)
                if start_time <= current_time <= end_time:
                    return False
            else:  # Переход через полночь (например, 22:00 - 08:00)
                if current_time >= start_time or current_time <= end_time:
                    return False

        # Проверяем лимит уведомлений в день
        today = datetime.now(timezone.utc).date()
        today_notifications = [
            n
            for n in self.notifications_db.get(user_id, [])
            if datetime.fromisoformat(n["created_at"].replace("Z", "+00:00")).date()
            == today
        ]

        max_daily = preferences.get("max_daily", 50)
        if len(today_notifications) >= max_daily:
            return False

        return True

    async def _should_escalate_priority(
        self, user_id: int, notification_type: str
    ) -> bool:
        """Определяет, нужно ли повысить приоритет уведомления."""
        if not self.smart_rules.get("priority_escalation", True):
            return False

        # Повышаем приоритет, если есть много непрочитанных уведомлений
        unread_count = await self.get_unread_count(user_id)
        return unread_count > 10

    def _escalate_priority(self, current_priority: str) -> str:
        """Повышает приоритет уведомления."""
        priority_levels = ["low", "medium", "high", "critical"]
        current_index = priority_levels.index(current_priority)
        if current_index < len(priority_levels) - 1:
            return priority_levels[current_index + 1]
        return current_priority

    async def _get_batch_id(self, user_id: int, notification_type: str) -> str:
        """Генерирует ID для группировки похожих уведомлений."""
        if not self.smart_rules.get("batch_similar", True):
            return f"{user_id}_{notification_type}_{datetime.now(timezone.utc).timestamp()}"

        # Группируем уведомления по типу и времени (в пределах часа)
        current_hour = datetime.now(timezone.utc).replace(
            minute=0, second=0, microsecond=0
        )
        return f"{user_id}_{notification_type}_{current_hour.timestamp()}"

    async def _is_quiet_hours_override(self, notification_type: str) -> bool:
        """Определяет, может ли уведомление переопределить тихие часы."""
        critical_types = ["security_alert", "system_maintenance"]
        return notification_type in critical_types

    async def _apply_smart_features(self, user_id: int, notification: Dict[str, Any]):
        """Применяет умные функции к уведомлению."""
        # Здесь можно добавить логику для:
        # - Автоматической группировки
        # - Умного планирования отправки
        # - Персонализации контента
        pass

    async def _group_similar_notifications(
        self, notifications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Группирует похожие уведомления."""
        if not self.smart_rules.get("batch_similar", True):
            return notifications

        grouped = {}
        for notification in notifications:
            batch_id = notification.get("smart_features", {}).get("batch_id", "")
            if batch_id not in grouped:
                grouped[batch_id] = {
                    "id": f"batch_{batch_id}",
                    "type": notification["type"],
                    "title": notification["title"],
                    "message": notification["message"],
                    "count": 1,
                    "notifications": [notification],
                    "created_at": notification["created_at"],
                    "priority": notification["priority"],
                    "category": notification["category"],
                    "is_read": notification["is_read"],
                }
            else:
                grouped[batch_id]["count"] += 1
                grouped[batch_id]["notifications"].append(notification)
                # Обновляем время на самое новое
                if notification["created_at"] > grouped[batch_id]["created_at"]:
                    grouped[batch_id]["created_at"] = notification["created_at"]

        return list(grouped.values())

    async def _get_notification_categories(self, user_id: int) -> List[str]:
        """Получает список категорий уведомлений пользователя."""
        user_notifications = self.notifications_db.get(user_id, [])
        categories = set()
        for notification in user_notifications:
            if "category" in notification:
                categories.add(notification["category"])
        return list(categories)

    async def _get_priority_distribution(self, user_id: int) -> Dict[str, int]:
        """Получает распределение приоритетов уведомлений пользователя."""
        user_notifications = self.notifications_db.get(user_id, [])
        distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for notification in user_notifications:
            priority = notification.get("priority", "low")
            if priority in distribution:
                distribution[priority] += 1

        return distribution

    def _apply_template_variables(self, text: str, data: Dict[str, Any]) -> str:
        """Применяет переменные шаблона к тексту."""
        for key, value in data.items():
            placeholder = f"{{{key}}}"
            if placeholder in text:
                text = text.replace(placeholder, str(value))
        return text


# Создаем экземпляр сервиса
advanced_notification_service = AdvancedNotificationService()
