"""
Схемы для Social Network модуля
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from .base import BaseSchema, TimestampMixin
from .auth import UserResponse


class PostBase(BaseSchema):
    """Базовая схема поста"""

    content: str = Field(
        ..., min_length=1, max_length=2000, description="Содержимое поста"
    )
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL изображения"
    )
    is_public: bool = Field(True, description="Публичный ли пост")


class PostCreate(PostBase):
    """Схема создания поста"""

    pass


class PostUpdate(BaseSchema):
    """Схема обновления поста"""

    content: Optional[str] = Field(
        None, min_length=1, max_length=2000, description="Содержимое поста"
    )
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL изображения"
    )
    is_public: Optional[bool] = Field(None, description="Публичный ли пост")


class PostResponse(PostBase, TimestampMixin):
    """Схема ответа с данными поста"""

    id: int = Field(..., description="ID поста")
    author: UserResponse = Field(..., description="Автор поста")
    likes_count: int = Field(0, description="Количество лайков")
    comments_count: int = Field(0, description="Количество комментариев")
    is_liked: bool = Field(False, description="Лайкнул ли текущий пользователь")


class PostListResponse(BaseSchema):
    """Схема ответа со списком постов"""

    items: List[PostResponse] = Field(..., description="Список постов")
    total: int = Field(..., description="Общее количество постов")
    skip: int = Field(..., description="Количество пропущенных постов")
    limit: int = Field(..., description="Лимит постов")


class CommentBase(BaseSchema):
    """Базовая схема комментария"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )


class CommentCreate(CommentBase):
    """Схема создания комментария"""

    post_id: int = Field(..., gt=0, description="ID поста")


class CommentUpdate(BaseSchema):
    """Схема обновления комментария"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )


class CommentResponse(CommentBase, TimestampMixin):
    """Схема ответа с данными комментария"""

    id: int = Field(..., description="ID комментария")
    author: UserResponse = Field(..., description="Автор комментария")
    post_id: int = Field(..., description="ID поста")


class CommentListResponse(BaseSchema):
    """Схема ответа со списком комментариев"""

    items: List[CommentResponse] = Field(..., description="Список комментариев")
    total: int = Field(..., description="Общее количество комментариев")
    skip: int = Field(..., description="Количество пропущенных комментариев")
    limit: int = Field(..., description="Лимит комментариев")


class PostLikeResponse(BaseSchema, TimestampMixin):
    """Схема ответа с данными лайка"""

    id: int = Field(..., description="ID лайка")
    user: UserResponse = Field(..., description="Пользователь, поставивший лайк")
    post_id: int = Field(..., description="ID поста")


class FollowCreate(BaseSchema):
    """Схема создания подписки"""

    following_id: int = Field(..., gt=0, description="ID пользователя для подписки")


class FollowResponse(BaseSchema, TimestampMixin):
    """Схема ответа с данными подписки"""

    id: int = Field(..., description="ID подписки")
    follower: UserResponse = Field(..., description="Подписчик")
    following: UserResponse = Field(..., description="На кого подписан")


class FollowListResponse(BaseSchema):
    """Схема ответа со списком подписок"""

    items: List[FollowResponse] = Field(..., description="Список подписок")
    total: int = Field(..., description="Общее количество подписок")
    skip: int = Field(..., description="Количество пропущенных подписок")
    limit: int = Field(..., description="Лимит подписок")


class UserProfileResponse(UserResponse):
    """Расширенная схема профиля пользователя"""

    posts_count: int = Field(0, description="Количество постов")
    followers_count: int = Field(0, description="Количество подписчиков")
    following_count: int = Field(0, description="Количество подписок")
    is_following: bool = Field(False, description="Подписан ли текущий пользователь")


class PostFilters(BaseSchema):
    """Схема фильтров для постов"""

    author_id: Optional[int] = Field(None, gt=0, description="Фильтр по автору")
    is_public: Optional[bool] = Field(None, description="Фильтр по публичности")
    search: Optional[str] = Field(None, min_length=1, description="Поисковый запрос")
    date_from: Optional[datetime] = Field(None, description="Посты с даты")
    date_to: Optional[datetime] = Field(None, description="Посты до даты")
