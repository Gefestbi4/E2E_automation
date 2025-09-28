"""
Сервис для управления ролями и разрешениями
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import logging
import random

logger = logging.getLogger(__name__)


class RolesService:
    """Сервис для управления ролями и разрешениями"""

    def __init__(self):
        # В реальном приложении здесь будет взаимодействие с БД
        self.roles_db = {}  # Моковая БД для ролей
        self.permissions_db = {}  # Моковая БД для разрешений
        self.user_roles_db = {}  # Моковая БД для ролей пользователей

        # Инициализируем базовые роли и разрешения
        self._initialize_default_data()

    def _initialize_default_data(self):
        """Инициализация базовых ролей и разрешений"""

        # Базовые разрешения
        default_permissions = [
            # Пользователи
            {
                "id": 1,
                "name": "users.create",
                "display_name": "Создание пользователей",
                "resource": "users",
                "action": "create",
            },
            {
                "id": 2,
                "name": "users.read",
                "display_name": "Просмотр пользователей",
                "resource": "users",
                "action": "read",
            },
            {
                "id": 3,
                "name": "users.update",
                "display_name": "Редактирование пользователей",
                "resource": "users",
                "action": "update",
            },
            {
                "id": 4,
                "name": "users.delete",
                "display_name": "Удаление пользователей",
                "resource": "users",
                "action": "delete",
            },
            # Посты
            {
                "id": 5,
                "name": "posts.create",
                "display_name": "Создание постов",
                "resource": "posts",
                "action": "create",
            },
            {
                "id": 6,
                "name": "posts.read",
                "display_name": "Просмотр постов",
                "resource": "posts",
                "action": "read",
            },
            {
                "id": 7,
                "name": "posts.update",
                "display_name": "Редактирование постов",
                "resource": "posts",
                "action": "update",
            },
            {
                "id": 8,
                "name": "posts.delete",
                "display_name": "Удаление постов",
                "resource": "posts",
                "action": "delete",
            },
            # Товары
            {
                "id": 9,
                "name": "products.create",
                "display_name": "Создание товаров",
                "resource": "products",
                "action": "create",
            },
            {
                "id": 10,
                "name": "products.read",
                "display_name": "Просмотр товаров",
                "resource": "products",
                "action": "read",
            },
            {
                "id": 11,
                "name": "products.update",
                "display_name": "Редактирование товаров",
                "resource": "products",
                "action": "update",
            },
            {
                "id": 12,
                "name": "products.delete",
                "display_name": "Удаление товаров",
                "resource": "products",
                "action": "delete",
            },
            # Задачи
            {
                "id": 13,
                "name": "tasks.create",
                "display_name": "Создание задач",
                "resource": "tasks",
                "action": "create",
            },
            {
                "id": 14,
                "name": "tasks.read",
                "display_name": "Просмотр задач",
                "resource": "tasks",
                "action": "read",
            },
            {
                "id": 15,
                "name": "tasks.update",
                "display_name": "Редактирование задач",
                "resource": "tasks",
                "action": "update",
            },
            {
                "id": 16,
                "name": "tasks.delete",
                "display_name": "Удаление задач",
                "resource": "tasks",
                "action": "delete",
            },
            # Контент
            {
                "id": 17,
                "name": "content.create",
                "display_name": "Создание контента",
                "resource": "content",
                "action": "create",
            },
            {
                "id": 18,
                "name": "content.read",
                "display_name": "Просмотр контента",
                "resource": "content",
                "action": "read",
            },
            {
                "id": 19,
                "name": "content.update",
                "display_name": "Редактирование контента",
                "resource": "content",
                "action": "update",
            },
            {
                "id": 20,
                "name": "content.delete",
                "display_name": "Удаление контента",
                "resource": "content",
                "action": "delete",
            },
            # Аналитика
            {
                "id": 21,
                "name": "analytics.read",
                "display_name": "Просмотр аналитики",
                "resource": "analytics",
                "action": "read",
            },
            {
                "id": 22,
                "name": "analytics.create",
                "display_name": "Создание отчетов",
                "resource": "analytics",
                "action": "create",
            },
            {
                "id": 23,
                "name": "analytics.update",
                "display_name": "Редактирование отчетов",
                "resource": "analytics",
                "action": "update",
            },
            {
                "id": 24,
                "name": "analytics.delete",
                "display_name": "Удаление отчетов",
                "resource": "analytics",
                "action": "delete",
            },
            # Роли и разрешения
            {
                "id": 25,
                "name": "roles.create",
                "display_name": "Создание ролей",
                "resource": "roles",
                "action": "create",
            },
            {
                "id": 26,
                "name": "roles.read",
                "display_name": "Просмотр ролей",
                "resource": "roles",
                "action": "read",
            },
            {
                "id": 27,
                "name": "roles.update",
                "display_name": "Редактирование ролей",
                "resource": "roles",
                "action": "update",
            },
            {
                "id": 28,
                "name": "roles.delete",
                "display_name": "Удаление ролей",
                "resource": "roles",
                "action": "delete",
            },
            {
                "id": 29,
                "name": "roles.assign",
                "display_name": "Назначение ролей",
                "resource": "roles",
                "action": "assign",
            },
            # Система
            {
                "id": 30,
                "name": "system.admin",
                "display_name": "Администрирование системы",
                "resource": "system",
                "action": "admin",
            },
            {
                "id": 31,
                "name": "system.settings",
                "display_name": "Настройки системы",
                "resource": "system",
                "action": "settings",
            },
        ]

        for perm in default_permissions:
            self.permissions_db[perm["id"]] = perm

        # Базовые роли
        default_roles = [
            {
                "id": 1,
                "name": "super_admin",
                "display_name": "Супер администратор",
                "description": "Полный доступ ко всем функциям системы",
                "is_system": True,
                "permissions": list(range(1, 32)),  # Все разрешения
            },
            {
                "id": 2,
                "name": "admin",
                "display_name": "Администратор",
                "description": "Административный доступ к большинству функций",
                "is_system": False,
                "permissions": list(range(1, 30)),  # Все кроме системных
            },
            {
                "id": 3,
                "name": "moderator",
                "display_name": "Модератор",
                "description": "Модерация контента и пользователей",
                "is_system": False,
                "permissions": [
                    2,
                    3,
                    6,
                    7,
                    8,
                    10,
                    11,
                    14,
                    15,
                    18,
                    19,
                    21,
                    26,
                    27,
                ],  # Чтение и редактирование
            },
            {
                "id": 4,
                "name": "user",
                "display_name": "Пользователь",
                "description": "Обычный пользователь",
                "is_system": True,
                "permissions": [
                    2,
                    5,
                    6,
                    7,
                    9,
                    10,
                    13,
                    14,
                    15,
                    17,
                    18,
                    21,
                ],  # Базовые разрешения
            },
            {
                "id": 5,
                "name": "guest",
                "display_name": "Гость",
                "description": "Ограниченный доступ",
                "is_system": True,
                "permissions": [2, 6, 10, 14, 18, 21],  # Только чтение
            },
        ]

        for role in default_roles:
            self.roles_db[role["id"]] = role

    async def get_all_roles(self) -> List[Dict[str, Any]]:
        """Получить все роли"""
        logger.info("Fetching all roles")
        return list(self.roles_db.values())

    async def get_role_by_id(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Получить роль по ID"""
        logger.info(f"Fetching role by ID: {role_id}")
        return self.roles_db.get(role_id)

    async def get_role_by_name(self, role_name: str) -> Optional[Dict[str, Any]]:
        """Получить роль по имени"""
        logger.info(f"Fetching role by name: {role_name}")
        for role in self.roles_db.values():
            if role["name"] == role_name:
                return role
        return None

    async def create_role(self, role_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создать новую роль"""
        logger.info(f"Creating new role: {role_data['name']}")

        new_role_id = max(self.roles_db.keys()) + 1 if self.roles_db else 1

        role = {
            "id": new_role_id,
            "name": role_data["name"],
            "display_name": role_data["display_name"],
            "description": role_data.get("description", ""),
            "is_active": role_data.get("is_active", True),
            "is_system": False,
            "permissions": role_data.get("permissions", []),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        self.roles_db[new_role_id] = role
        return role

    async def update_role(
        self, role_id: int, role_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Обновить роль"""
        logger.info(f"Updating role: {role_id}")

        if role_id not in self.roles_db:
            return None

        role = self.roles_db[role_id]

        # Нельзя изменять системные роли
        if role.get("is_system", False):
            raise ValueError("Cannot modify system role")

        # Обновляем поля
        for key, value in role_data.items():
            if key in [
                "name",
                "display_name",
                "description",
                "is_active",
                "permissions",
            ]:
                role[key] = value

        role["updated_at"] = datetime.now(timezone.utc).isoformat()

        return role

    async def delete_role(self, role_id: int) -> bool:
        """Удалить роль"""
        logger.info(f"Deleting role: {role_id}")

        if role_id not in self.roles_db:
            return False

        role = self.roles_db[role_id]

        # Нельзя удалять системные роли
        if role.get("is_system", False):
            raise ValueError("Cannot delete system role")

        # Удаляем роль из всех пользователей
        for user_id, user_roles in self.user_roles_db.items():
            self.user_roles_db[user_id] = [
                r for r in user_roles if r["role_id"] != role_id
            ]

        del self.roles_db[role_id]
        return True

    async def get_all_permissions(self) -> List[Dict[str, Any]]:
        """Получить все разрешения"""
        logger.info("Fetching all permissions")
        return list(self.permissions_db.values())

    async def get_permission_by_id(
        self, permission_id: int
    ) -> Optional[Dict[str, Any]]:
        """Получить разрешение по ID"""
        logger.info(f"Fetching permission by ID: {permission_id}")
        return self.permissions_db.get(permission_id)

    async def get_user_roles(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить роли пользователя"""
        logger.info(f"Fetching roles for user: {user_id}")

        user_roles = self.user_roles_db.get(user_id, [])
        roles = []

        for user_role in user_roles:
            role = self.roles_db.get(user_role["role_id"])
            if role and role.get("is_active", True):
                roles.append(
                    {
                        **role,
                        "assigned_at": user_role.get("assigned_at"),
                        "expires_at": user_role.get("expires_at"),
                        "is_active": user_role.get("is_active", True),
                    }
                )

        return roles

    async def assign_role_to_user(
        self,
        user_id: int,
        role_id: int,
        assigned_by: int = None,
        expires_at: str = None,
    ) -> bool:
        """Назначить роль пользователю"""
        logger.info(f"Assigning role {role_id} to user {user_id}")

        if role_id not in self.roles_db:
            return False

        if user_id not in self.user_roles_db:
            self.user_roles_db[user_id] = []

        # Проверяем, не назначена ли уже эта роль
        for user_role in self.user_roles_db[user_id]:
            if user_role["role_id"] == role_id and user_role.get("is_active", True):
                return False  # Роль уже назначена

        user_role = {
            "role_id": role_id,
            "assigned_by": assigned_by,
            "assigned_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at,
            "is_active": True,
        }

        self.user_roles_db[user_id].append(user_role)
        return True

    async def remove_role_from_user(self, user_id: int, role_id: int) -> bool:
        """Удалить роль у пользователя"""
        logger.info(f"Removing role {role_id} from user {user_id}")

        if user_id not in self.user_roles_db:
            return False

        original_length = len(self.user_roles_db[user_id])
        self.user_roles_db[user_id] = [
            r
            for r in self.user_roles_db[user_id]
            if not (r["role_id"] == role_id and r.get("is_active", True))
        ]

        return len(self.user_roles_db[user_id]) < original_length

    async def check_permission(self, user_id: int, permission_name: str) -> bool:
        """Проверить, есть ли у пользователя разрешение"""
        logger.info(f"Checking permission {permission_name} for user {user_id}")

        # Находим разрешение
        permission = None
        for perm in self.permissions_db.values():
            if perm["name"] == permission_name:
                permission = perm
                break

        if not permission:
            return False

        # Получаем роли пользователя
        user_roles = await self.get_user_roles(user_id)

        # Проверяем, есть ли разрешение в любой из ролей
        for role in user_roles:
            if permission["id"] in role.get("permissions", []):
                return True

        return False

    async def get_user_permissions(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить все разрешения пользователя"""
        logger.info(f"Fetching permissions for user {user_id}")

        user_roles = await self.get_user_roles(user_id)
        permission_ids = set()

        for role in user_roles:
            permission_ids.update(role.get("permissions", []))

        permissions = []
        for perm_id in permission_ids:
            if perm_id in self.permissions_db:
                permissions.append(self.permissions_db[perm_id])

        return permissions

    async def get_role_permissions(self, role_id: int) -> List[Dict[str, Any]]:
        """Получить разрешения роли"""
        logger.info(f"Fetching permissions for role {role_id}")

        role = self.roles_db.get(role_id)
        if not role:
            return []

        permissions = []
        for perm_id in role.get("permissions", []):
            if perm_id in self.permissions_db:
                permissions.append(self.permissions_db[perm_id])

        return permissions

    async def update_role_permissions(
        self, role_id: int, permission_ids: List[int]
    ) -> bool:
        """Обновить разрешения роли"""
        logger.info(f"Updating permissions for role {role_id}")

        if role_id not in self.roles_db:
            return False

        role = self.roles_db[role_id]

        # Нельзя изменять системные роли
        if role.get("is_system", False):
            raise ValueError("Cannot modify system role permissions")

        role["permissions"] = permission_ids
        role["updated_at"] = datetime.now(timezone.utc).isoformat()

        return True

    async def get_users_with_role(self, role_id: int) -> List[Dict[str, Any]]:
        """Получить пользователей с определенной ролью"""
        logger.info(f"Fetching users with role {role_id}")

        users = []
        for user_id, user_roles in self.user_roles_db.items():
            for user_role in user_roles:
                if user_role["role_id"] == role_id and user_role.get("is_active", True):
                    users.append(
                        {
                            "user_id": user_id,
                            "assigned_at": user_role.get("assigned_at"),
                            "expires_at": user_role.get("expires_at"),
                        }
                    )
                    break

        return users

    async def get_role_statistics(self) -> Dict[str, Any]:
        """Получить статистику по ролям"""
        logger.info("Fetching role statistics")

        total_roles = len(self.roles_db)
        active_roles = len(
            [r for r in self.roles_db.values() if r.get("is_active", True)]
        )
        system_roles = len(
            [r for r in self.roles_db.values() if r.get("is_system", False)]
        )

        total_permissions = len(self.permissions_db)

        # Статистика по назначениям ролей
        role_assignments = {}
        for user_roles in self.user_roles_db.values():
            for user_role in user_roles:
                if user_role.get("is_active", True):
                    role_id = user_role["role_id"]
                    role_assignments[role_id] = role_assignments.get(role_id, 0) + 1

        return {
            "total_roles": total_roles,
            "active_roles": active_roles,
            "system_roles": system_roles,
            "total_permissions": total_permissions,
            "role_assignments": role_assignments,
        }


# Создаем экземпляр сервиса
roles_service = RolesService()
