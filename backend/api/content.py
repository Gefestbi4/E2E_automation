from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.content as content_models
import models
from typing import List

router = APIRouter()


# Articles endpoints
@router.get("/api/content/articles")
def get_articles(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Получить список статей"""
    articles = (
        db.query(content_models.Article)
        .filter(content_models.Article.status == "published")
        .order_by(content_models.Article.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return articles


@router.post("/api/content/articles")
def create_article(
    article_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую статью"""
    article = content_models.Article(
        title=article_data.get("title"),
        content=article_data.get("content"),
        excerpt=article_data.get("excerpt"),
        author_id=current_user.id,
        category_id=article_data.get("category_id"),
        status=article_data.get("status", "draft"),
        featured_image=article_data.get("featured_image"),
        slug=article_data.get(
            "slug", article_data.get("title", "").lower().replace(" ", "-")
        ),
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.get("/api/content/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Получить статью по ID"""
    article = (
        db.query(content_models.Article)
        .filter(content_models.Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Увеличиваем счетчик просмотров
    article.views_count += 1
    db.commit()
    db.refresh(article)

    return article


@router.put("/api/content/articles/{article_id}")
def update_article(
    article_id: int,
    article_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить статью"""
    article = (
        db.query(content_models.Article)
        .filter(
            content_models.Article.id == article_id,
            content_models.Article.author_id == current_user.id,
        )
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Обновляем поля
    for field, value in article_data.items():
        if hasattr(article, field):
            setattr(article, field, value)

    db.commit()
    db.refresh(article)
    return article


@router.post("/api/content/articles/{article_id}/publish")
def publish_article(
    article_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Опубликовать статью"""
    article = (
        db.query(content_models.Article)
        .filter(
            content_models.Article.id == article_id,
            content_models.Article.author_id == current_user.id,
        )
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.status = "published"
    db.commit()
    db.refresh(article)
    return article


# Categories endpoints
@router.get("/api/content/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получить список категорий"""
    categories = db.query(content_models.Category).all()
    return categories


@router.post("/api/content/categories")
def create_category(
    category_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую категорию"""
    category = content_models.Category(
        name=category_data.get("name"),
        description=category_data.get("description"),
        slug=category_data.get(
            "slug", category_data.get("name", "").lower().replace(" ", "-")
        ),
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# Upload endpoint
@router.post("/api/content/upload")
def upload_file(current_user: models.User = Depends(get_current_user)):
    """Загрузка файлов (заглушка)"""
    # В реальном приложении здесь была бы логика загрузки файлов
    return {"message": "File upload endpoint", "url": "/uploads/placeholder.jpg"}
