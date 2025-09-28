"""
API для настроек и приватности пользователей
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
from services.settings_service import settings_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsUpdateRequest(BaseModel):
    settings: Dict[str, Any]


class PrivacySettingsUpdate(BaseModel):
    profile_visibility: Optional[str] = None
    show_email: Optional[bool] = None
    show_phone: Optional[bool] = None
    show_location: Optional[bool] = None
    show_birth_date: Optional[bool] = None
    show_online_status: Optional[bool] = None
    allow_search_engines: Optional[bool] = None
    allow_direct_messages: Optional[str] = None
    show_activity_status: Optional[bool] = None


class NotificationSettingsUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    in_app_notifications: Optional[bool] = None
    new_follower: Optional[bool] = None
    new_like: Optional[bool] = None
    new_comment: Optional[bool] = None
    new_message: Optional[bool] = None
    new_post_like: Optional[bool] = None
    new_post_comment: Optional[bool] = None
    marketing_emails: Optional[bool] = None
    security_alerts: Optional[bool] = None
    weekly_digest: Optional[bool] = None


class SecuritySettingsUpdate(BaseModel):
    two_factor_enabled: Optional[bool] = None
    login_notifications: Optional[bool] = None
    password_change_notifications: Optional[bool] = None
    suspicious_activity_alerts: Optional[bool] = None
    session_timeout: Optional[int] = None
    max_login_attempts: Optional[int] = None
    require_password_for_sensitive_actions: Optional[bool] = None


class AppearanceSettingsUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    compact_mode: Optional[bool] = None
    show_animations: Optional[bool] = None
    font_size: Optional[str] = None


class ContentSettingsUpdate(BaseModel):
    auto_play_videos: Optional[bool] = None
    auto_play_sounds: Optional[bool] = None
    show_nsfw_content: Optional[bool] = None
    content_filtering: Optional[str] = None
    auto_save_drafts: Optional[bool] = None
    draft_retention_days: Optional[int] = None


class SocialSettingsUpdate(BaseModel):
    auto_follow_back: Optional[bool] = None
    show_follow_suggestions: Optional[bool] = None
    allow_tagging: Optional[bool] = None
    allow_mentions: Optional[bool] = None
    show_online_friends: Optional[bool] = None
    show_mutual_friends: Optional[bool] = None


@router.get("/")
async def get_all_settings(current_user: User = Depends(get_current_user)):
    """Получение всех настроек пользователя"""
    try:
        settings = settings_service.get_user_settings(current_user.id)
        return {"settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/")
async def update_settings(
    request: SettingsUpdateRequest,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек пользователя"""
    try:
        success = settings_service.update_user_settings(
            current_user.id, "general", request.settings
        )
        if success:
            return {"message": "Настройки обновлены успешно"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка обновления настроек")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/privacy")
async def get_privacy_settings(current_user: User = Depends(get_current_user)):
    """Получение настроек приватности"""
    try:
        settings = settings_service.get_privacy_settings(current_user.id)
        return {"privacy_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/privacy")
async def update_privacy_settings(
    request: PrivacySettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек приватности"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_privacy_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Настройки приватности обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления настроек приватности"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications")
async def get_notification_settings(current_user: User = Depends(get_current_user)):
    """Получение настроек уведомлений"""
    try:
        settings = settings_service.get_notification_settings(current_user.id)
        return {"notification_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/notifications")
async def update_notification_settings(
    request: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек уведомлений"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_notification_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Настройки уведомлений обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления настроек уведомлений"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/security")
async def get_security_settings(current_user: User = Depends(get_current_user)):
    """Получение настроек безопасности"""
    try:
        settings = settings_service.get_security_settings(current_user.id)
        return {"security_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/security")
async def update_security_settings(
    request: SecuritySettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек безопасности"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_security_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Настройки безопасности обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления настроек безопасности"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/appearance")
async def get_appearance_settings(current_user: User = Depends(get_current_user)):
    """Получение настроек внешнего вида"""
    try:
        settings = settings_service.get_appearance_settings(current_user.id)
        return {"appearance_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/appearance")
async def update_appearance_settings(
    request: AppearanceSettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек внешнего вида"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_appearance_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Настройки внешнего вида обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления настроек внешнего вида"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/content")
async def get_content_settings(current_user: User = Depends(get_current_user)):
    """Получение настроек контента"""
    try:
        settings = settings_service.get_content_settings(current_user.id)
        return {"content_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/content")
async def update_content_settings(
    request: ContentSettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление настроек контента"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_content_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Настройки контента обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления настроек контента"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/social")
async def get_social_settings(current_user: User = Depends(get_current_user)):
    """Получение социальных настроек"""
    try:
        settings = settings_service.get_social_settings(current_user.id)
        return {"social_settings": settings}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/social")
async def update_social_settings(
    request: SocialSettingsUpdate,
    current_user: User = Depends(get_current_user),
):
    """Обновление социальных настроек"""
    try:
        # Фильтруем только переданные поля
        settings_dict = {k: v for k, v in request.dict().items() if v is not None}

        success = settings_service.update_social_settings(
            current_user.id, settings_dict
        )
        if success:
            return {"message": "Социальные настройки обновлены успешно"}
        else:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления социальных настроек"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_settings_to_default(current_user: User = Depends(get_current_user)):
    """Сброс настроек к значениям по умолчанию"""
    try:
        success = settings_service.reset_settings_to_default(current_user.id)
        if success:
            return {"message": "Настройки сброшены к значениям по умолчанию"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка сброса настроек")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_user_data(current_user: User = Depends(get_current_user)):
    """Экспорт данных пользователя"""
    try:
        data = settings_service.export_user_data(current_user.id)
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/data")
async def delete_user_data(current_user: User = Depends(get_current_user)):
    """Удаление всех данных пользователя (GDPR)"""
    try:
        success = settings_service.delete_user_data(current_user.id)
        if success:
            return {"message": "Все данные пользователя удалены"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка удаления данных")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
