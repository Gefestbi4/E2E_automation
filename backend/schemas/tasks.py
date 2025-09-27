"""
Схемы для Task Management модуля
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from .base import BaseSchema, TimestampMixin
from .auth import UserResponse


class BoardBase(BaseSchema):
    """Базовая схема доски"""

    name: str = Field(..., min_length=1, max_length=255, description="Название доски")
    description: Optional[str] = Field(None, description="Описание доски")
    is_public: bool = Field(False, description="Публичная ли доска")


class BoardCreate(BoardBase):
    """Схема создания доски"""

    pass


class BoardUpdate(BaseSchema):
    """Схема обновления доски"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Название доски"
    )
    description: Optional[str] = Field(None, description="Описание доски")
    is_public: Optional[bool] = Field(None, description="Публичная ли доска")


class BoardResponse(BoardBase, TimestampMixin):
    """Схема ответа с данными доски"""

    id: int = Field(..., description="ID доски")
    user: UserResponse = Field(..., description="Владелец доски")
    cards_count: int = Field(0, description="Количество карточек")
    completed_cards: int = Field(0, description="Количество завершенных карточек")


class BoardFilters(BaseSchema):
    """Фильтры для поиска досок"""

    is_public: Optional[bool] = Field(None, description="Публичные доски")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


class BoardListResponse(BaseSchema):
    """Схема ответа со списком досок"""

    items: List[BoardResponse] = Field(..., description="Список досок")
    total: int = Field(..., description="Общее количество досок")
    skip: int = Field(..., description="Количество пропущенных досок")
    limit: int = Field(..., description="Лимит досок")


class CardBase(BaseSchema):
    """Базовая схема карточки"""

    title: str = Field(
        ..., min_length=1, max_length=255, description="Название карточки"
    )
    description: Optional[str] = Field(None, description="Описание карточки")
    priority: str = Field("medium", description="Приоритет карточки")
    status: str = Field("todo", description="Статус карточки")
    deadline: Optional[datetime] = Field(None, description="Дедлайн")


class CardCreate(CardBase):
    """Схема создания карточки"""

    board_id: int = Field(..., gt=0, description="ID доски")
    assigned_to_id: Optional[int] = Field(None, gt=0, description="ID исполнителя")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        allowed_priorities = ["low", "medium", "high", "urgent"]
        if v not in allowed_priorities:
            raise ValueError(
                f"Приоритет должен быть одним из: {', '.join(allowed_priorities)}"
            )
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed_statuses = ["todo", "in_progress", "review", "done"]
        if v not in allowed_statuses:
            raise ValueError(
                f"Статус должен быть одним из: {', '.join(allowed_statuses)}"
            )
        return v


class CardUpdate(BaseSchema):
    """Схема обновления карточки"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Название карточки"
    )
    description: Optional[str] = Field(None, description="Описание карточки")
    priority: Optional[str] = Field(None, description="Приоритет карточки")
    status: Optional[str] = Field(None, description="Статус карточки")
    deadline: Optional[datetime] = Field(None, description="Дедлайн")
    assigned_to_id: Optional[int] = Field(None, gt=0, description="ID исполнителя")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        if v:
            allowed_priorities = ["low", "medium", "high", "urgent"]
            if v not in allowed_priorities:
                raise ValueError(
                    f"Приоритет должен быть одним из: {', '.join(allowed_priorities)}"
                )
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v:
            allowed_statuses = ["todo", "in_progress", "review", "done"]
            if v not in allowed_statuses:
                raise ValueError(
                    f"Статус должен быть одним из: {', '.join(allowed_statuses)}"
                )
        return v


class CardResponse(CardBase, TimestampMixin):
    """Схема ответа с данными карточки"""

    id: int = Field(..., description="ID карточки")
    board_id: int = Field(..., description="ID доски")
    assigned_to: Optional[UserResponse] = Field(None, description="Исполнитель")
    comments_count: int = Field(0, description="Количество комментариев")
    is_overdue: bool = Field(False, description="Просрочена ли карточка")


class CardListResponse(BaseSchema):
    """Схема ответа со списком карточек"""

    items: List[CardResponse] = Field(..., description="Список карточек")
    total: int = Field(..., description="Общее количество карточек")
    skip: int = Field(..., description="Количество пропущенных карточек")
    limit: int = Field(..., description="Лимит карточек")


class CardCommentBase(BaseSchema):
    """Базовая схема комментария к карточке"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )


class CardCommentCreate(CardCommentBase):
    """Схема создания комментария к карточке"""

    card_id: int = Field(..., gt=0, description="ID карточки")


class CardCommentUpdate(BaseSchema):
    """Схема обновления комментария к карточке"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )


class CardCommentResponse(CardCommentBase, TimestampMixin):
    """Схема ответа с данными комментария к карточке"""

    id: int = Field(..., description="ID комментария")
    card_id: int = Field(..., description="ID карточки")
    author: UserResponse = Field(..., description="Автор комментария")


class CardCommentListResponse(BaseSchema):
    """Схема ответа со списком комментариев к карточке"""

    items: List[CardCommentResponse] = Field(..., description="Список комментариев")
    total: int = Field(..., description="Общее количество комментариев")
    skip: int = Field(..., description="Количество пропущенных комментариев")
    limit: int = Field(..., description="Лимит комментариев")


class BoardStatsResponse(BaseSchema):
    """Схема ответа со статистикой доски"""

    board_id: int = Field(..., description="ID доски")
    total_cards: int = Field(..., description="Общее количество карточек")
    todo_cards: int = Field(..., description="Количество карточек в статусе 'todo'")
    in_progress_cards: int = Field(
        ..., description="Количество карточек в статусе 'in_progress'"
    )
    review_cards: int = Field(..., description="Количество карточек в статусе 'review'")
    done_cards: int = Field(..., description="Количество карточек в статусе 'done'")
    overdue_cards: int = Field(..., description="Количество просроченных карточек")
    completion_rate: float = Field(..., description="Процент завершения")


class CardFilters(BaseSchema):
    """Схема фильтров для карточек"""

    board_id: Optional[int] = Field(None, gt=0, description="Фильтр по доске")
    status: Optional[str] = Field(None, description="Фильтр по статусу")
    priority: Optional[str] = Field(None, description="Фильтр по приоритету")
    assigned_to_id: Optional[int] = Field(
        None, gt=0, description="Фильтр по исполнителю"
    )
    search: Optional[str] = Field(None, min_length=1, description="Поисковый запрос")
    overdue: Optional[bool] = Field(None, description="Только просроченные")
    deadline_from: Optional[datetime] = Field(None, description="Дедлайн с даты")
    deadline_to: Optional[datetime] = Field(None, description="Дедлайн до даты")
