"""
Схемы для модуля аутентификации
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from .base import BaseSchema


class UserBase(BaseSchema):
    """Базовая схема пользователя"""

    email: EmailStr = Field(..., description="Email пользователя")
    username: str = Field(
        ..., min_length=3, max_length=20, description="Имя пользователя"
    )


class UserRegistration(BaseSchema):
    """Схема регистрации пользователя"""

    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль")
    confirm_password: str = Field(..., description="Подтверждение пароля")
    full_name: Optional[str] = Field(None, max_length=100, description="Полное имя")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v


class UserCreate(UserBase):
    """Схема создания пользователя"""

    password: str = Field(..., min_length=8, description="Пароль")
    full_name: Optional[str] = Field(None, max_length=100, description="Полное имя")


class UserLogin(BaseSchema):
    """Схема входа в систему"""

    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., description="Пароль")


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""

    id: int = Field(..., description="ID пользователя")
    full_name: Optional[str] = Field(None, description="Полное имя")
    is_active: bool = Field(..., description="Активен ли пользователь")
    is_verified: bool = Field(..., description="Подтвержден ли email")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")


class UserUpdate(BaseSchema):
    """Схема обновления пользователя"""

    full_name: Optional[str] = Field(None, max_length=100, description="Полное имя")
    username: Optional[str] = Field(
        None, min_length=3, max_length=20, description="Имя пользователя"
    )


class ChangePassword(BaseSchema):
    """Схема смены пароля"""

    current_password: str = Field(..., description="Текущий пароль")
    new_password: str = Field(..., min_length=8, description="Новый пароль")
    confirm_password: str = Field(..., description="Подтверждение нового пароля")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Пароли не совпадают")
        return v

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v


class EmailVerification(BaseSchema):
    """Схема подтверждения email"""

    token: str = Field(..., description="Токен подтверждения")


class Token(BaseSchema):
    """Схема токенов"""

    access_token: str = Field(..., description="Access токен")
    refresh_token: str = Field(..., description="Refresh токен")
    token_type: str = Field("bearer", description="Тип токена")
    expires_in: int = Field(..., description="Время жизни токена в секундах")


class RefreshToken(BaseSchema):
    """Схема refresh токена"""

    refresh_token: str = Field(..., description="Refresh токен")


class TokenData(BaseSchema):
    """Схема данных токена"""

    email: Optional[str] = Field(None, description="Email из токена")
