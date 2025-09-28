"""
API для управления ролями и разрешениями
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.roles_service import roles_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/roles", tags=["roles"])


# Pydantic модели для валидации
class RoleCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    is_active: bool = True
    permissions: List[int] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permissions: Optional[List[int]] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: str
    is_active: bool
    is_system: bool
    permissions: List[int]
    created_at: str
    updated_at: str


class PermissionResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: str
    resource: str
    action: str
    is_active: bool


class UserRoleAssign(BaseModel):
    role_id: int
    expires_at: Optional[str] = None


class RoleStatistics(BaseModel):
    total_roles: int
    active_roles: int
    system_roles: int
    total_permissions: int
    role_assignments: Dict[str, int]


@router.get("/", response_model=List[RoleResponse])
async def get_all_roles(current_user: User = Depends(get_current_user)):
    """Получить все роли"""
    try:
        # Проверяем разрешение
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        roles = await roles_service.get_all_roles()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching roles: {str(e)}")


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(role_id: int, current_user: User = Depends(get_current_user)):
    """Получить роль по ID"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        role = await roles_service.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching role: {str(e)}")


@router.post("/", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate, current_user: User = Depends(get_current_user)
):
    """Создать новую роль"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.create"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        role = await roles_service.create_role(role_data.model_dump())
        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating role: {str(e)}")


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int, role_data: RoleUpdate, current_user: User = Depends(get_current_user)
):
    """Обновить роль"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.update"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        role = await roles_service.update_role(
            role_id, role_data.model_dump(exclude_unset=True)
        )
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating role: {str(e)}")


@router.delete("/{role_id}")
async def delete_role(role_id: int, current_user: User = Depends(get_current_user)):
    """Удалить роль"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.delete"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        success = await roles_service.delete_role(role_id)
        if not success:
            raise HTTPException(status_code=404, detail="Role not found")

        return {"message": "Role deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting role: {str(e)}")


@router.get("/permissions/", response_model=List[PermissionResponse])
async def get_all_permissions(current_user: User = Depends(get_current_user)):
    """Получить все разрешения"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        permissions = await roles_service.get_all_permissions()
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching permissions: {str(e)}"
        )


@router.get("/{role_id}/permissions", response_model=List[PermissionResponse])
async def get_role_permissions(
    role_id: int, current_user: User = Depends(get_current_user)
):
    """Получить разрешения роли"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        permissions = await roles_service.get_role_permissions(role_id)
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching role permissions: {str(e)}"
        )


@router.put("/{role_id}/permissions")
async def update_role_permissions(
    role_id: int,
    permission_ids: List[int],
    current_user: User = Depends(get_current_user),
):
    """Обновить разрешения роли"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.update"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        success = await roles_service.update_role_permissions(role_id, permission_ids)
        if not success:
            raise HTTPException(status_code=404, detail="Role not found")

        return {"message": "Role permissions updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating role permissions: {str(e)}"
        )


@router.get("/user/{user_id}/roles", response_model=List[RoleResponse])
async def get_user_roles(user_id: int, current_user: User = Depends(get_current_user)):
    """Получить роли пользователя"""
    try:
        # Пользователь может видеть свои роли или нужны права на просмотр пользователей
        if user_id != current_user.id:
            has_permission = await roles_service.check_permission(
                current_user.id, "users.read"
            )
            if not has_permission:
                raise HTTPException(status_code=403, detail="Insufficient permissions")

        roles = await roles_service.get_user_roles(user_id)
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching user roles: {str(e)}"
        )


@router.get("/user/{user_id}/permissions", response_model=List[PermissionResponse])
async def get_user_permissions(
    user_id: int, current_user: User = Depends(get_current_user)
):
    """Получить разрешения пользователя"""
    try:
        # Пользователь может видеть свои разрешения или нужны права на просмотр пользователей
        if user_id != current_user.id:
            has_permission = await roles_service.check_permission(
                current_user.id, "users.read"
            )
            if not has_permission:
                raise HTTPException(status_code=403, detail="Insufficient permissions")

        permissions = await roles_service.get_user_permissions(user_id)
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching user permissions: {str(e)}"
        )


@router.post("/user/{user_id}/assign")
async def assign_role_to_user(
    user_id: int,
    role_data: UserRoleAssign,
    current_user: User = Depends(get_current_user),
):
    """Назначить роль пользователю"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.assign"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        success = await roles_service.assign_role_to_user(
            user_id, role_data.role_id, current_user.id, role_data.expires_at
        )

        if not success:
            raise HTTPException(status_code=400, detail="Failed to assign role")

        return {"message": "Role assigned successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning role: {str(e)}")


@router.delete("/user/{user_id}/role/{role_id}")
async def remove_role_from_user(
    user_id: int, role_id: int, current_user: User = Depends(get_current_user)
):
    """Удалить роль у пользователя"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.assign"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        success = await roles_service.remove_role_from_user(user_id, role_id)
        if not success:
            raise HTTPException(status_code=404, detail="Role assignment not found")

        return {"message": "Role removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing role: {str(e)}")


@router.get("/check/{permission_name}")
async def check_permission(
    permission_name: str, current_user: User = Depends(get_current_user)
):
    """Проверить разрешение пользователя"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, permission_name
        )
        return {"permission": permission_name, "has_permission": has_permission}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error checking permission: {str(e)}"
        )


@router.get("/role/{role_id}/users")
async def get_users_with_role(
    role_id: int, current_user: User = Depends(get_current_user)
):
    """Получить пользователей с определенной ролью"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        users = await roles_service.get_users_with_role(role_id)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching users with role: {str(e)}"
        )


@router.get("/statistics", response_model=RoleStatistics)
async def get_role_statistics(current_user: User = Depends(get_current_user)):
    """Получить статистику по ролям"""
    try:
        has_permission = await roles_service.check_permission(
            current_user.id, "roles.read"
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        statistics = await roles_service.get_role_statistics()
        return statistics
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching role statistics: {str(e)}"
        )
