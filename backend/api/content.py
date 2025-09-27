from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.content as content_models
import models
from typing import List, Optional

from schemas.content import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse,
    MediaFileCreate,
    MediaFileUpdate,
    MediaFileResponse,
    MediaFileListResponse,
    ArticleFilters,
    CategoryFilters,
    MediaFileFilters,
)
from services.content_service import ContentService
from utils.exceptions import (
    ArticleNotFoundError,
    CategoryNotFoundError,
    NotFoundError,
)

router = APIRouter()


# Articles endpoints
@router.get("/api/content/articles", response_model=ArticleListResponse)
def get_articles(
    skip: int = Query(0, ge=0, description="Количество пропущенных статей"),
    limit: int = Query(20, ge=1, le=100, description="Количество статей на странице"),
    author_id: Optional[int] = Query(None, description="Фильтр по автору"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    tags: Optional[str] = Query(None, description="Фильтр по тегам (через запятую)"),
    published_from: Optional[str] = Query(None, description="Статьи с даты публикации"),
    published_to: Optional[str] = Query(None, description="Статьи до даты публикации"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить список статей с фильтрацией"""
    # Парсим теги
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]

    filters = ArticleFilters(
        author_id=author_id,
        category_id=category_id,
        status=status,
        tags=tags_list,
        published_from=published_from,
        published_to=published_to,
        search=search,
    )

    service = ContentService(db)
    result = service.get_articles(
        skip=skip, limit=limit, filters=filters, user=current_user
    )

    articles = []
    for item in result["items"]:
        articles.append(
            ArticleResponse(
                id=item["article"].id,
                title=item["article"].title,
                excerpt=item["article"].excerpt,
                content=item["article"].content,
                slug=item["article"].slug,
                status=item["article"].status,
                created_at=item["article"].created_at,
                updated_at=item["article"].updated_at,
                published_at=item["article"].published_at,
                author=item["article"].author,
                category=item["article"].category,
                tags=item["article"].tags or [],
                featured_image_url=item["article"].featured_image_url,
                meta_title=item["article"].meta_title,
                meta_description=item["article"].meta_description,
                views_count=item["views_count"],
                is_popular=item["is_popular"],
            )
        )

    return ArticleListResponse(
        items=articles,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/content/articles/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить статью по ID"""
    service = ContentService(db)
    result = service.get_article(article_id, current_user)

    return ArticleResponse(
        id=result["article"].id,
        title=result["article"].title,
        excerpt=result["article"].excerpt,
        content=result["article"].content,
        slug=result["article"].slug,
        status=result["article"].status,
        created_at=result["article"].created_at,
        updated_at=result["article"].updated_at,
        published_at=result["article"].published_at,
        author=result["article"].author,
        category=result["article"].category,
        tags=result["article"].tags or [],
        featured_image_url=result["article"].featured_image_url,
        meta_title=result["article"].meta_title,
        meta_description=result["article"].meta_description,
        views_count=result["views_count"],
        is_popular=result["is_popular"],
    )


@router.post("/api/content/articles", response_model=ArticleResponse)
def create_article(
    article_data: ArticleCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую статью"""
    service = ContentService(db)
    article = service.create_article(article_data, current_user)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        excerpt=article.excerpt,
        content=article.content,
        slug=article.slug,
        status=article.status,
        created_at=article.created_at,
        updated_at=article.updated_at,
        published_at=article.published_at,
        author=article.author,
        category=article.category,
        tags=article.tags or [],
        featured_image_url=article.featured_image_url,
        meta_title=article.meta_title,
        meta_description=article.meta_description,
        views_count=0,
        is_popular=False,
    )


@router.put("/api/content/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить статью"""
    service = ContentService(db)
    article = service.update_article(article_id, article_data, current_user)

    # Получаем обновленную информацию
    result = service.get_article(article_id, current_user)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        excerpt=article.excerpt,
        content=article.content,
        slug=article.slug,
        status=article.status,
        created_at=article.created_at,
        updated_at=article.updated_at,
        published_at=article.published_at,
        author=article.author,
        category=article.category,
        tags=article.tags or [],
        featured_image_url=article.featured_image_url,
        meta_title=article.meta_title,
        meta_description=article.meta_description,
        views_count=result["views_count"],
        is_popular=result["is_popular"],
    )


@router.delete("/api/content/articles/{article_id}")
def delete_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить статью"""
    service = ContentService(db)
    service.delete_article(article_id, current_user)
    return {"message": "Article deleted successfully"}


@router.post(
    "/api/content/articles/{article_id}/publish", response_model=ArticleResponse
)
def publish_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Опубликовать статью"""
    service = ContentService(db)
    article = service.publish_article(article_id, current_user)

    # Получаем обновленную информацию
    result = service.get_article(article_id, current_user)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        excerpt=article.excerpt,
        content=article.content,
        slug=article.slug,
        status=article.status,
        created_at=article.created_at,
        updated_at=article.updated_at,
        published_at=article.published_at,
        author=article.author,
        category=article.category,
        tags=article.tags or [],
        featured_image_url=article.featured_image_url,
        meta_title=article.meta_title,
        meta_description=article.meta_description,
        views_count=result["views_count"],
        is_popular=result["is_popular"],
    )


@router.post(
    "/api/content/articles/{article_id}/unpublish", response_model=ArticleResponse
)
def unpublish_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Снять статью с публикации"""
    service = ContentService(db)
    article = service.unpublish_article(article_id, current_user)

    # Получаем обновленную информацию
    result = service.get_article(article_id, current_user)

    return ArticleResponse(
        id=article.id,
        title=article.title,
        excerpt=article.excerpt,
        content=article.content,
        slug=article.slug,
        status=article.status,
        created_at=article.created_at,
        updated_at=article.updated_at,
        published_at=article.published_at,
        author=article.author,
        category=article.category,
        tags=article.tags or [],
        featured_image_url=article.featured_image_url,
        meta_title=article.meta_title,
        meta_description=article.meta_description,
        views_count=result["views_count"],
        is_popular=result["is_popular"],
    )


# Categories endpoints
@router.get("/api/content/categories", response_model=CategoryListResponse)
def get_categories(
    skip: int = Query(0, ge=0, description="Количество пропущенных категорий"),
    limit: int = Query(
        20, ge=1, le=100, description="Количество категорий на странице"
    ),
    parent_id: Optional[int] = Query(
        None, description="Фильтр по родительской категории"
    ),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    db: Session = Depends(get_db),
):
    """Получить список категорий с фильтрацией"""
    filters = CategoryFilters(
        parent_id=parent_id,
        search=search,
    )

    service = ContentService(db)
    result = service.get_categories(skip=skip, limit=limit, filters=filters)

    categories = []
    for item in result["items"]:
        categories.append(
            CategoryResponse(
                id=item["category"].id,
                name=item["category"].name,
                description=item["category"].description,
                slug=item["category"].slug,
                parent_id=item["category"].parent_id,
                is_active=item["category"].is_active,
                created_at=item["category"].created_at,
                updated_at=item["category"].updated_at,
                articles_count=item["articles_count"],
                subcategories_count=item["subcategories_count"],
            )
        )

    return CategoryListResponse(
        items=categories,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/content/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """Получить категорию по ID"""
    service = ContentService(db)
    result = service.get_category(category_id)

    return CategoryResponse(
        id=result["category"].id,
        name=result["category"].name,
        description=result["category"].description,
        slug=result["category"].slug,
        parent_id=result["category"].parent_id,
        is_active=result["category"].is_active,
        created_at=result["category"].created_at,
        updated_at=result["category"].updated_at,
        articles_count=result["articles_count"],
        subcategories_count=result["subcategories_count"],
    )


@router.post("/api/content/categories", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую категорию"""
    service = ContentService(db)
    category = service.create_category(category_data, current_user)

    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        slug=category.slug,
        parent_id=category.parent_id,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
        articles_count=0,
        subcategories_count=0,
    )


@router.put("/api/content/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить категорию"""
    service = ContentService(db)
    category = service.update_category(category_id, category_data, current_user)

    # Получаем обновленную статистику
    result = service.get_category(category_id)

    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        slug=category.slug,
        parent_id=category.parent_id,
        is_active=category.is_active,
        created_at=category.created_at,
        updated_at=category.updated_at,
        articles_count=result["articles_count"],
        subcategories_count=result["subcategories_count"],
    )


@router.delete("/api/content/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить категорию"""
    service = ContentService(db)
    service.delete_category(category_id, current_user)
    return {"message": "Category deleted successfully"}


@router.get(
    "/api/content/categories/{category_id}/articles", response_model=ArticleListResponse
)
def get_category_articles(
    category_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных статей"),
    limit: int = Query(20, ge=1, le=100, description="Количество статей на странице"),
    db: Session = Depends(get_db),
):
    """Получить статьи категории"""
    service = ContentService(db)
    result = service.get_category_articles(category_id, skip=skip, limit=limit)

    articles = []
    for article in result["items"]:
        articles.append(
            ArticleResponse(
                id=article.id,
                title=article.title,
                excerpt=article.excerpt,
                content=article.content,
                slug=article.slug,
                status=article.status,
                created_at=article.created_at,
                updated_at=article.updated_at,
                published_at=article.published_at,
                author=article.author,
                category=article.category,
                tags=article.tags or [],
                featured_image_url=article.featured_image_url,
                meta_title=article.meta_title,
                meta_description=article.meta_description,
                views_count=getattr(article, "views_count", 0),
                is_popular=getattr(article, "views_count", 0) > 100,
            )
        )

    return ArticleListResponse(
        items=articles,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


# Media files endpoints
@router.get("/api/content/media", response_model=MediaFileListResponse)
def get_media_files(
    skip: int = Query(0, ge=0, description="Количество пропущенных файлов"),
    limit: int = Query(20, ge=1, le=100, description="Количество файлов на странице"),
    file_type: Optional[str] = Query(None, description="Фильтр по типу файла"),
    min_size: Optional[int] = Query(None, ge=0, description="Минимальный размер файла"),
    max_size: Optional[int] = Query(
        None, ge=0, description="Максимальный размер файла"
    ),
    uploaded_from: Optional[str] = Query(None, description="Файлы с даты загрузки"),
    uploaded_to: Optional[str] = Query(None, description="Файлы до даты загрузки"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить список медиафайлов с фильтрацией"""
    filters = MediaFileFilters(
        file_type=file_type,
        min_size=min_size,
        max_size=max_size,
        uploaded_from=uploaded_from,
        uploaded_to=uploaded_to,
        search=search,
    )

    service = ContentService(db)
    result = service.get_media_files(
        skip=skip, limit=limit, filters=filters, user=current_user
    )

    media_files = []
    for media_file in result["items"]:
        media_files.append(
            MediaFileResponse(
                id=media_file.id,
                filename=media_file.filename,
                original_filename=media_file.original_filename,
                file_path=media_file.file_path,
                file_size=media_file.file_size,
                file_type=media_file.file_type,
                mime_type=media_file.mime_type,
                uploaded_at=media_file.uploaded_at,
                uploaded_by=media_file.uploaded_by,
                alt_text=media_file.alt_text,
                caption=media_file.caption,
            )
        )

    return MediaFileListResponse(
        items=media_files,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/content/media/{file_id}", response_model=MediaFileResponse)
def get_media_file(
    file_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить медиафайл по ID"""
    service = ContentService(db)
    media_file = service.get_media_file(file_id, current_user)

    return MediaFileResponse(
        id=media_file.id,
        filename=media_file.filename,
        original_filename=media_file.original_filename,
        file_path=media_file.file_path,
        file_size=media_file.file_size,
        file_type=media_file.file_type,
        mime_type=media_file.mime_type,
        uploaded_at=media_file.uploaded_at,
        uploaded_by=media_file.uploaded_by,
        alt_text=media_file.alt_text,
        caption=media_file.caption,
    )


@router.post("/api/content/media", response_model=MediaFileResponse)
def create_media_file(
    media_file_data: MediaFileCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать запись о медиафайле"""
    service = ContentService(db)
    media_file = service.create_media_file(media_file_data, current_user)

    return MediaFileResponse(
        id=media_file.id,
        filename=media_file.filename,
        original_filename=media_file.original_filename,
        file_path=media_file.file_path,
        file_size=media_file.file_size,
        file_type=media_file.file_type,
        mime_type=media_file.mime_type,
        uploaded_at=media_file.uploaded_at,
        uploaded_by=media_file.uploaded_by,
        alt_text=media_file.alt_text,
        caption=media_file.caption,
    )


@router.put("/api/content/media/{file_id}", response_model=MediaFileResponse)
def update_media_file(
    file_id: int,
    media_file_data: MediaFileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить медиафайл"""
    service = ContentService(db)
    media_file = service.update_media_file(file_id, media_file_data, current_user)

    return MediaFileResponse(
        id=media_file.id,
        filename=media_file.filename,
        original_filename=media_file.original_filename,
        file_path=media_file.file_path,
        file_size=media_file.file_size,
        file_type=media_file.file_type,
        mime_type=media_file.mime_type,
        uploaded_at=media_file.uploaded_at,
        uploaded_by=media_file.uploaded_by,
        alt_text=media_file.alt_text,
        caption=media_file.caption,
    )


@router.delete("/api/content/media/{file_id}")
def delete_media_file(
    file_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить медиафайл"""
    service = ContentService(db)
    service.delete_media_file(file_id, current_user)
    return {"message": "Media file deleted successfully"}


# Upload endpoint
@router.post("/api/content/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Загрузка файлов"""
    # В реальном приложении здесь была бы логика загрузки файлов
    # Пока что возвращаем заглушку
    return {
        "message": "File upload endpoint",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size if hasattr(file, "size") else 0,
        "url": f"/uploads/{file.filename}",
    }


# Analytics endpoints
@router.get("/api/content/analytics")
def get_content_analytics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить аналитику контента"""
    service = ContentService(db)
    analytics = service.get_content_analytics(current_user)
    return analytics
