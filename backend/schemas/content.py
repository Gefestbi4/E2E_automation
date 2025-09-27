"""
Схемы для Content Management модуля
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from .base import BaseSchema, TimestampMixin
from .auth import UserResponse
from enum import Enum


class ArticleStatus(str, Enum):
    """Статусы статьи"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class CategoryBase(BaseSchema):
    """Базовая схема категории"""

    name: str = Field(
        ..., min_length=1, max_length=100, description="Название категории"
    )
    description: Optional[str] = Field(None, description="Описание категории")
    slug: str = Field(
        ..., min_length=1, max_length=100, description="URL slug категории"
    )


class CategoryCreate(CategoryBase):
    """Схема создания категории"""

    pass


class CategoryUpdate(BaseSchema):
    """Схема обновления категории"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Название категории"
    )
    description: Optional[str] = Field(None, description="Описание категории")
    slug: Optional[str] = Field(
        None, min_length=1, max_length=100, description="URL slug категории"
    )


class CategoryFilters(BaseSchema):
    """Фильтры для поиска категорий"""

    search: Optional[str] = Field(None, description="Поиск по названию и описанию")


class CategoryResponse(CategoryBase, TimestampMixin):
    """Схема ответа с данными категории"""

    id: int = Field(..., description="ID категории")
    articles_count: int = Field(0, description="Количество статей в категории")


class CategoryListResponse(BaseSchema):
    """Схема ответа со списком категорий"""

    items: List[CategoryResponse] = Field(..., description="Список категорий")
    total: int = Field(..., description="Общее количество категорий")


class ArticleBase(BaseSchema):
    """Базовая схема статьи"""

    title: str = Field(
        ..., min_length=1, max_length=255, description="Заголовок статьи"
    )
    excerpt: Optional[str] = Field(None, max_length=500, description="Краткое описание")
    content: str = Field(..., min_length=1, description="Содержимое статьи")
    featured_image: Optional[str] = Field(
        None, max_length=500, description="URL главного изображения"
    )
    slug: str = Field(..., min_length=1, max_length=255, description="URL slug статьи")
    status: ArticleStatus = Field(ArticleStatus.DRAFT, description="Статус статьи")
    category_id: Optional[int] = Field(None, gt=0, description="ID категории")
    tags: List[str] = Field(default_factory=list, description="Теги статьи")


class ArticleCreate(ArticleBase):
    """Схема создания статьи"""

    pass


class ArticleUpdate(BaseSchema):
    """Схема обновления статьи"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Заголовок статьи"
    )
    excerpt: Optional[str] = Field(None, max_length=500, description="Краткое описание")
    content: Optional[str] = Field(None, min_length=1, description="Содержимое статьи")
    featured_image: Optional[str] = Field(
        None, max_length=500, description="URL главного изображения"
    )
    slug: Optional[str] = Field(
        None, min_length=1, max_length=255, description="URL slug статьи"
    )
    status: Optional[str] = Field(None, description="Статус статьи")
    category_id: Optional[int] = Field(None, gt=0, description="ID категории")
    tags: Optional[List[str]] = Field(None, description="Теги статьи")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v:
            allowed_statuses = ["draft", "published", "archived"]
            if v not in allowed_statuses:
                raise ValueError(
                    f"Статус должен быть одним из: {', '.join(allowed_statuses)}"
                )
        return v


class ArticleResponse(ArticleBase, TimestampMixin):
    """Схема ответа с данными статьи"""

    id: int = Field(..., description="ID статьи")
    author: UserResponse = Field(..., description="Автор статьи")
    category: Optional[CategoryResponse] = Field(None, description="Категория статьи")
    views_count: int = Field(0, description="Количество просмотров")
    comments_count: int = Field(0, description="Количество комментариев")
    is_published: bool = Field(False, description="Опубликована ли статья")


class ArticleListResponse(BaseSchema):
    """Схема ответа со списком статей"""

    items: List[ArticleResponse] = Field(..., description="Список статей")
    total: int = Field(..., description="Общее количество статей")
    skip: int = Field(..., description="Количество пропущенных статей")
    limit: int = Field(..., description="Лимит статей")


class ArticleCommentBase(BaseSchema):
    """Базовая схема комментария к статье"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )
    parent_id: Optional[int] = Field(
        None, gt=0, description="ID родительского комментария"
    )


class ArticleCommentCreate(ArticleCommentBase):
    """Схема создания комментария к статье"""

    article_id: int = Field(..., gt=0, description="ID статьи")


class ArticleCommentUpdate(BaseSchema):
    """Схема обновления комментария к статье"""

    content: str = Field(
        ..., min_length=1, max_length=1000, description="Содержимое комментария"
    )


class ArticleCommentResponse(ArticleCommentBase, TimestampMixin):
    """Схема ответа с данными комментария к статье"""

    id: int = Field(..., description="ID комментария")
    article_id: int = Field(..., description="ID статьи")
    author: UserResponse = Field(..., description="Автор комментария")
    replies: List["ArticleCommentResponse"] = Field(
        default_factory=list, description="Ответы на комментарий"
    )


class ArticleCommentListResponse(BaseSchema):
    """Схема ответа со списком комментариев к статье"""

    items: List[ArticleCommentResponse] = Field(..., description="Список комментариев")
    total: int = Field(..., description="Общее количество комментариев")
    skip: int = Field(..., description="Количество пропущенных комментариев")
    limit: int = Field(..., description="Лимит комментариев")


class MediaFileBase(BaseSchema):
    """Базовая схема медиа файла"""

    filename: str = Field(..., min_length=1, max_length=255, description="Имя файла")
    original_filename: str = Field(
        ..., min_length=1, max_length=255, description="Оригинальное имя файла"
    )
    file_path: str = Field(
        ..., min_length=1, max_length=500, description="Путь к файлу"
    )
    file_size: int = Field(..., gt=0, description="Размер файла в байтах")
    mime_type: str = Field(
        ..., min_length=1, max_length=100, description="MIME тип файла"
    )
    alt_text: Optional[str] = Field(
        None, max_length=255, description="Альтернативный текст"
    )


class MediaFileCreate(MediaFileBase):
    """Схема создания медиа файла"""

    pass


class MediaFileUpdate(BaseSchema):
    """Схема обновления медиа файла"""

    filename: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Имя файла"
    )
    alt_text: Optional[str] = Field(
        None, max_length=255, description="Альтернативный текст"
    )


class MediaFileResponse(MediaFileBase, TimestampMixin):
    """Схема ответа с данными медиа файла"""

    id: int = Field(..., description="ID файла")
    uploader: UserResponse = Field(..., description="Загрузивший файл")
    url: str = Field(..., description="URL файла")


class MediaFileListResponse(BaseSchema):
    """Схема ответа со списком медиа файлов"""

    items: List[MediaFileResponse] = Field(..., description="Список файлов")
    total: int = Field(..., description="Общее количество файлов")
    skip: int = Field(..., description="Количество пропущенных файлов")
    limit: int = Field(..., description="Лимит файлов")


class ArticleFilters(BaseSchema):
    """Схема фильтров для статей"""

    category_id: Optional[int] = Field(None, gt=0, description="Фильтр по категории")
    author_id: Optional[int] = Field(None, gt=0, description="Фильтр по автору")
    status: Optional[str] = Field(None, description="Фильтр по статусу")
    tags: Optional[List[str]] = Field(None, description="Фильтр по тегам")
    search: Optional[str] = Field(None, min_length=1, description="Поисковый запрос")
    date_from: Optional[datetime] = Field(None, description="Статьи с даты")
    date_to: Optional[datetime] = Field(None, description="Статьи до даты")
    published_only: Optional[bool] = Field(None, description="Только опубликованные")


class MediaFileFilters(BaseSchema):
    """Схема фильтров для медиа файлов"""

    mime_type: Optional[str] = Field(None, description="Фильтр по MIME типу")
    uploader_id: Optional[int] = Field(None, gt=0, description="Фильтр по загрузившему")
    search: Optional[str] = Field(None, min_length=1, description="Поисковый запрос")
    date_from: Optional[datetime] = Field(None, description="Файлы с даты")
    date_to: Optional[datetime] = Field(None, description="Файлы до даты")
