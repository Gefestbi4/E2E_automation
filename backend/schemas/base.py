"""
Базовые Pydantic схемы для всех модулей
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    """Базовая схема с общими настройками"""

    model_config = ConfigDict(
        from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True
    )


class TimestampMixin(BaseModel):
    """Миксин для временных меток"""

    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")


class PaginationParams(BaseModel):
    """Параметры пагинации"""

    skip: int = Field(0, ge=0, description="Количество записей для пропуска")
    limit: int = Field(20, ge=1, le=100, description="Количество записей для возврата")


class SearchParams(BaseModel):
    """Параметры поиска"""

    search: Optional[str] = Field(None, description="Поисковый запрос")
    sort_by: Optional[str] = Field(None, description="Поле для сортировки")
    sort_order: Optional[str] = Field(
        "asc", pattern="^(asc|desc)$", description="Порядок сортировки"
    )


class ErrorResponse(BaseModel):
    """Схема для ошибок API"""

    detail: str = Field(..., description="Описание ошибки")
    error_code: Optional[str] = Field(None, description="Код ошибки")
    field: Optional[str] = Field(None, description="Поле с ошибкой")


class SuccessResponse(BaseModel):
    """Схема для успешных ответов"""

    message: str = Field(..., description="Сообщение об успехе")
    data: Optional[dict] = Field(None, description="Дополнительные данные")
