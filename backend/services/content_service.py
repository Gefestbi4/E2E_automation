"""
Сервис для Content Management модуля
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

import models_package.content as content_models
from models import User
from schemas.content import (
    ArticleCreate,
    ArticleUpdate,
    ArticleFilters,
    CategoryCreate,
    CategoryUpdate,
    CategoryFilters,
    MediaFileCreate,
    MediaFileUpdate,
    MediaFileFilters,
)
from utils.database import QueryBuilder, PaginationHelper, SearchHelper
from utils.exceptions import (
    ArticleNotFoundError,
    CategoryNotFoundError,
    NotFoundError,
    BusinessLogicError,
)


class ContentService:
    """Сервис для работы с контентом"""

    def __init__(self, db: Session):
        self.db = db

    # Articles methods
    def get_articles(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[ArticleFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список статей с фильтрацией"""
        query = self.db.query(content_models.Article)

        if filters:
            # Фильтр по автору
            if filters.author_id:
                query = query.filter(
                    content_models.Article.author_id == filters.author_id
                )

            # Фильтр по категории
            if filters.category_id:
                query = query.filter(
                    content_models.Article.category_id == filters.category_id
                )

            # Фильтр по статусу
            if filters.status:
                query = query.filter(content_models.Article.status == filters.status)

            # Фильтр по тегам
            if filters.tags:
                for tag in filters.tags:
                    query = query.filter(content_models.Article.tags.contains([tag]))

            # Фильтр по дате публикации
            if filters.date_from:
                query = query.filter(
                    content_models.Article.published_at >= filters.date_from
                )
            if filters.date_to:
                query = query.filter(
                    content_models.Article.published_at <= filters.date_to
                )
            if filters.published_only:
                query = query.filter(content_models.Article.status == "PUBLISHED")

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    content_models.Article,
                    filters.search,
                    ["title", "excerpt", "content"],
                )

        # Если пользователь не указан, показываем только опубликованные статьи
        if not user:
            query = query.filter(content_models.Article.status == "PUBLISHED")
        else:
            # Показываем статьи пользователя и опубликованные статьи
            query = query.filter(
                or_(
                    content_models.Article.author_id == user.id,
                    content_models.Article.status == "PUBLISHED",
                )
            )

        # Сортировка по дате публикации (новые сначала)
        query = query.order_by(content_models.Article.published_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем дополнительную информацию для каждой статьи
        articles_with_stats = []
        for article in result["items"]:
            # Подсчитываем просмотры (если есть поле views)
            views_count = getattr(article, "views_count", 0)

            # Проверяем, является ли статья популярной (более 100 просмотров)
            is_popular = views_count > 100

            articles_with_stats.append(
                {
                    "article": article,
                    "views_count": views_count,
                    "is_popular": is_popular,
                }
            )

        result["items"] = articles_with_stats
        return result

    def get_article(
        self, article_id: int, user: Optional[User] = None
    ) -> Dict[str, Any]:
        """Получить статью по ID"""
        query = self.db.query(content_models.Article).filter(
            content_models.Article.id == article_id
        )

        # Проверяем права доступа
        if user:
            query = query.filter(
                or_(
                    content_models.Article.author_id == user.id,
                    content_models.Article.status == "PUBLISHED",
                )
            )
        else:
            query = query.filter(content_models.Article.status == "PUBLISHED")

        article = query.first()

        if not article:
            raise ArticleNotFoundError(str(article_id))

        # Увеличиваем счетчик просмотров
        if hasattr(article, "views_count"):
            article.views_count = getattr(article, "views_count", 0) + 1
            self.db.commit()

        # Подсчитываем просмотры
        views_count = getattr(article, "views_count", 0)
        is_popular = views_count > 100

        return {
            "article": article,
            "views_count": views_count,
            "is_popular": is_popular,
        }

    def create_article(
        self, article_data: ArticleCreate, user: User
    ) -> content_models.Article:
        """Создать новую статью"""
        article = content_models.Article(
            title=article_data.title,
            excerpt=article_data.excerpt,
            content=article_data.content,
            slug=article_data.slug,
            status=article_data.status.upper(),  # Конвертируем в uppercase для enum
            author_id=user.id,
            category_id=article_data.category_id,
            tags=article_data.tags or [],
            featured_image=article_data.featured_image,
            meta_title=getattr(article_data, "meta_title", None),
            meta_description=getattr(article_data, "meta_description", None),
        )
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def update_article(
        self, article_id: int, article_data: ArticleUpdate, user: User
    ) -> content_models.Article:
        """Обновить статью"""
        article_info = self.get_article(article_id, user)
        article = article_info["article"]

        # Проверяем, что пользователь является автором статьи
        if article.author_id != user.id:
            raise NotFoundError("Article", str(article_id))

        update_data = article_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(article, field, value)

        self.db.commit()
        self.db.refresh(article)
        return article

    def delete_article(self, article_id: int, user: User) -> bool:
        """Удалить статью"""
        article_info = self.get_article(article_id, user)
        article = article_info["article"]

        # Проверяем, что пользователь является автором статьи
        if article.author_id != user.id:
            raise NotFoundError("Article", str(article_id))

        self.db.delete(article)
        self.db.commit()
        return True

    def publish_article(self, article_id: int, user: User) -> content_models.Article:
        """Опубликовать статью"""
        article_info = self.get_article(article_id, user)
        article = article_info["article"]

        # Проверяем, что пользователь является автором статьи
        if article.author_id != user.id:
            raise NotFoundError("Article", str(article_id))

        article.status = "PUBLISHED"
        article.published_at = datetime.now()
        self.db.commit()
        self.db.refresh(article)
        return article

    def unpublish_article(self, article_id: int, user: User) -> content_models.Article:
        """Снять статью с публикации"""
        article_info = self.get_article(article_id, user)
        article = article_info["article"]

        # Проверяем, что пользователь является автором статьи
        if article.author_id != user.id:
            raise NotFoundError("Article", str(article_id))

        article.status = "DRAFT"
        self.db.commit()
        self.db.refresh(article)
        return article

    # Categories methods
    def get_categories(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[CategoryFilters] = None,
    ) -> Dict[str, Any]:
        """Получить список категорий с фильтрацией"""
        query = self.db.query(content_models.Category)

        if filters:
            # Фильтр по родительской категории
            if filters.parent_id is not None:
                query = query.filter(
                    content_models.Category.parent_id == filters.parent_id
                )

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    content_models.Category,
                    filters.search,
                    ["name", "description"],
                )

        # Сортировка по имени
        query = query.order_by(content_models.Category.name.asc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем статистику для каждой категории
        categories_with_stats = []
        for category in result["items"]:
            # Подсчитываем количество статей в категории
            articles_count = (
                self.db.query(content_models.Article)
                .filter(content_models.Article.category_id == category.id)
                .count()
            )

            # Подсчитываем количество подкатегорий
            subcategories_count = (
                self.db.query(content_models.Category)
                .filter(content_models.Category.parent_id == category.id)
                .count()
            )

            categories_with_stats.append(
                {
                    "category": category,
                    "articles_count": articles_count,
                    "subcategories_count": subcategories_count,
                }
            )

        result["items"] = categories_with_stats
        return result

    def get_category(self, category_id: int) -> Dict[str, Any]:
        """Получить категорию по ID"""
        category = (
            self.db.query(content_models.Category)
            .filter(content_models.Category.id == category_id)
            .first()
        )

        if not category:
            raise CategoryNotFoundError(str(category_id))

        # Подсчитываем статистику
        articles_count = (
            self.db.query(content_models.Article)
            .filter(content_models.Article.category_id == category_id)
            .count()
        )

        subcategories_count = (
            self.db.query(content_models.Category)
            .filter(content_models.Category.parent_id == category_id)
            .count()
        )

        return {
            "category": category,
            "articles_count": articles_count,
            "subcategories_count": subcategories_count,
        }

    def create_category(
        self, category_data: CategoryCreate, user: User
    ) -> content_models.Category:
        """Создать новую категорию"""
        category = content_models.Category(
            name=category_data.name,
            description=category_data.description,
            slug=category_data.slug,
            is_active=getattr(category_data, "is_active", True),
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(
        self, category_id: int, category_data: CategoryUpdate, user: User
    ) -> content_models.Category:
        """Обновить категорию"""
        category_info = self.get_category(category_id)
        category = category_info["category"]

        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int, user: User) -> bool:
        """Удалить категорию"""
        category_info = self.get_category(category_id)
        category = category_info["category"]

        # Проверяем, что в категории нет статей
        if category_info["articles_count"] > 0:
            raise BusinessLogicError(
                "Cannot delete category with articles. Move articles to another category first."
            )

        # Проверяем, что в категории нет подкатегорий
        if category_info["subcategories_count"] > 0:
            raise BusinessLogicError(
                "Cannot delete category with subcategories. Delete subcategories first."
            )

        self.db.delete(category)
        self.db.commit()
        return True

    # Media files methods
    def get_media_files(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[MediaFileFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список медиафайлов с фильтрацией"""
        query = self.db.query(content_models.MediaFile)

        if filters:
            # Фильтр по типу файла
            if filters.file_type:
                query = query.filter(
                    content_models.MediaFile.file_type == filters.file_type
                )

            # Фильтр по размеру файла
            if filters.min_size:
                query = query.filter(
                    content_models.MediaFile.file_size >= filters.min_size
                )
            if filters.max_size:
                query = query.filter(
                    content_models.MediaFile.file_size <= filters.max_size
                )

            # Фильтр по дате загрузки
            if filters.uploaded_from:
                query = query.filter(
                    content_models.MediaFile.uploaded_at >= filters.uploaded_from
                )
            if filters.uploaded_to:
                query = query.filter(
                    content_models.MediaFile.uploaded_at <= filters.uploaded_to
                )

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    content_models.MediaFile,
                    filters.search,
                    ["filename", "original_filename"],
                )

        # Если пользователь указан, показываем только его файлы
        if user:
            query = query.filter(content_models.MediaFile.uploaded_by_id == user.id)

        # Сортировка по дате загрузки (новые сначала)
        query = query.order_by(content_models.MediaFile.uploaded_at.desc())

        return PaginationHelper.paginate_query(query, skip, limit)

    def get_media_file(
        self, file_id: int, user: Optional[User] = None
    ) -> content_models.MediaFile:
        """Получить медиафайл по ID"""
        query = self.db.query(content_models.MediaFile).filter(
            content_models.MediaFile.id == file_id
        )

        # Если пользователь указан, проверяем права доступа
        if user:
            query = query.filter(content_models.MediaFile.uploaded_by_id == user.id)

        media_file = query.first()

        if not media_file:
            raise NotFoundError("MediaFile", str(file_id))

        return media_file

    def create_media_file(
        self, media_file_data: MediaFileCreate, user: User
    ) -> content_models.MediaFile:
        """Создать запись о медиафайле"""
        media_file = content_models.MediaFile(
            filename=media_file_data.filename,
            original_filename=media_file_data.original_filename,
            file_path=media_file_data.file_path,
            file_size=media_file_data.file_size,
            file_type=media_file_data.file_type,
            mime_type=media_file_data.mime_type,
            uploaded_by_id=user.id,
            alt_text=media_file_data.alt_text,
            caption=media_file_data.caption,
        )
        self.db.add(media_file)
        self.db.commit()
        self.db.refresh(media_file)
        return media_file

    def update_media_file(
        self, file_id: int, media_file_data: MediaFileUpdate, user: User
    ) -> content_models.MediaFile:
        """Обновить медиафайл"""
        media_file = self.get_media_file(file_id, user)

        update_data = media_file_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(media_file, field, value)

        self.db.commit()
        self.db.refresh(media_file)
        return media_file

    def delete_media_file(self, file_id: int, user: User) -> bool:
        """Удалить медиафайл"""
        media_file = self.get_media_file(file_id, user)

        self.db.delete(media_file)
        self.db.commit()
        return True

    # Analytics methods
    def get_content_analytics(self, user: User) -> Dict[str, Any]:
        """Получить аналитику контента"""
        # Статистика статей
        total_articles = (
            self.db.query(content_models.Article)
            .filter(content_models.Article.author_id == user.id)
            .count()
        )

        published_articles = (
            self.db.query(content_models.Article)
            .filter(
                and_(
                    content_models.Article.author_id == user.id,
                    content_models.Article.status == "PUBLISHED",
                )
            )
            .count()
        )

        draft_articles = (
            self.db.query(content_models.Article)
            .filter(
                and_(
                    content_models.Article.author_id == user.id,
                    content_models.Article.status == "DRAFT",
                )
            )
            .count()
        )

        # Статистика категорий
        total_categories = self.db.query(content_models.Category).count()

        # Статистика медиафайлов
        total_media_files = (
            self.db.query(content_models.MediaFile)
            .filter(content_models.MediaFile.uploaded_by_id == user.id)
            .count()
        )

        total_media_size = (
            self.db.query(func.sum(content_models.MediaFile.file_size))
            .filter(content_models.MediaFile.uploaded_by_id == user.id)
            .scalar()
            or 0
        )

        # Популярные статьи (по просмотрам)
        popular_articles = (
            self.db.query(content_models.Article)
            .filter(
                and_(
                    content_models.Article.author_id == user.id,
                    content_models.Article.status == "PUBLISHED",
                )
            )
            .order_by(content_models.Article.views_count.desc())
            .limit(5)
            .all()
        )

        return {
            "articles": {
                "total": total_articles,
                "published": published_articles,
                "draft": draft_articles,
            },
            "categories": {
                "total": total_categories,
            },
            "media_files": {
                "total": total_media_files,
                "total_size": total_media_size,
            },
            "popular_articles": [
                {
                    "id": article.id,
                    "title": article.title,
                    "views_count": getattr(article, "views_count", 0),
                }
                for article in popular_articles
            ],
        }

    def get_category_articles(
        self, category_id: int, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить статьи категории"""
        # Проверяем, что категория существует
        category = self.get_category(category_id)["category"]

        query = (
            self.db.query(content_models.Article)
            .filter(content_models.Article.category_id == category_id)
            .filter(content_models.Article.status == "PUBLISHED")
            .order_by(content_models.Article.published_at.desc())
        )

        return PaginationHelper.paginate_query(query, skip, limit)
