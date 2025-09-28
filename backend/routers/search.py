"""
API для поиска и фильтрации
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from services.search_service import search_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/search", tags=["search"])


class SearchFilters(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    author_id: Optional[int] = None
    is_published: Optional[bool] = None
    is_verified: Optional[bool] = None
    location: Optional[str] = None
    min_followers: Optional[int] = None


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    query: str
    filters: Optional[Dict[str, Any]] = None


@router.get("/posts", response_model=SearchResponse)
async def search_posts(
    q: str = Query(..., description="Поисковый запрос"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(
        20, ge=1, le=100, description="Количество результатов на странице"
    ),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    tags: Optional[str] = Query(None, description="Фильтр по тегам (через запятую)"),
    date_from: Optional[str] = Query(None, description="Дата от (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Дата до (YYYY-MM-DD)"),
    author_id: Optional[int] = Query(None, description="ID автора"),
    is_published: Optional[bool] = Query(None, description="Статус публикации"),
    current_user: User = Depends(get_current_user),
):
    """Поиск постов"""
    try:
        # Подготавливаем фильтры
        filters = {}
        if category:
            filters["category"] = category
        if tags:
            filters["tags"] = [tag.strip() for tag in tags.split(",")]
        if date_from:
            filters["date_from"] = date_from
        if date_to:
            filters["date_to"] = date_to
        if author_id:
            filters["author_id"] = author_id
        if is_published is not None:
            filters["is_published"] = is_published

        # Выполняем поиск
        result = search_service.search_posts(
            query=q,
            user_id=current_user.id,
            filters=filters,
            page=page,
            per_page=per_page,
        )

        return SearchResponse(
            results=result["posts"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
            query=result["query"],
            filters=result["filters"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска постов: {str(e)}")


@router.get("/users", response_model=SearchResponse)
async def search_users(
    q: str = Query(..., description="Поисковый запрос"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(
        20, ge=1, le=100, description="Количество результатов на странице"
    ),
    is_verified: Optional[bool] = Query(None, description="Статус верификации"),
    location: Optional[str] = Query(None, description="Фильтр по локации"),
    min_followers: Optional[int] = Query(
        None, ge=0, description="Минимальное количество подписчиков"
    ),
    current_user: User = Depends(get_current_user),
):
    """Поиск пользователей"""
    try:
        # Подготавливаем фильтры
        filters = {}
        if is_verified is not None:
            filters["is_verified"] = is_verified
        if location:
            filters["location"] = location
        if min_followers is not None:
            filters["min_followers"] = min_followers

        # Выполняем поиск
        result = search_service.search_users(
            query=q,
            user_id=current_user.id,
            filters=filters,
            page=page,
            per_page=per_page,
        )

        return SearchResponse(
            results=result["users"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
            query=result["query"],
            filters=result["filters"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка поиска пользователей: {str(e)}"
        )


@router.get("/tags", response_model=SearchResponse)
async def search_tags(
    q: Optional[str] = Query(None, description="Поисковый запрос"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(
        20, ge=1, le=100, description="Количество результатов на странице"
    ),
    current_user: User = Depends(get_current_user),
):
    """Поиск тегов"""
    try:
        # Выполняем поиск
        result = search_service.search_tags(
            query=q or "",
            user_id=current_user.id,
            page=page,
            per_page=per_page,
        )

        return SearchResponse(
            results=result["tags"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
            query=result["query"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска тегов: {str(e)}")


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Поисковый запрос"),
    limit: int = Query(10, ge=1, le=20, description="Количество предложений"),
    current_user: User = Depends(get_current_user),
):
    """Получение предложений для автодополнения"""
    try:
        suggestions = search_service.get_search_suggestions(
            query=q,
            user_id=current_user.id,
            limit=limit,
        )

        return {"suggestions": suggestions}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения предложений: {str(e)}"
        )


@router.get("/popular")
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=50, description="Количество популярных запросов"),
    current_user: User = Depends(get_current_user),
):
    """Получение популярных поисковых запросов"""
    try:
        popular = search_service.get_popular_searches(limit=limit)
        return {"popular_searches": popular}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения популярных запросов: {str(e)}"
        )


@router.get("/history")
async def get_search_history(
    limit: int = Query(20, ge=1, le=50, description="Количество записей истории"),
    current_user: User = Depends(get_current_user),
):
    """Получение истории поиска пользователя"""
    try:
        history = search_service.get_user_search_history(
            user_id=current_user.id,
            limit=limit,
        )
        return {"search_history": history}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения истории поиска: {str(e)}"
        )


@router.delete("/history")
async def clear_search_history(
    current_user: User = Depends(get_current_user),
):
    """Очистка истории поиска пользователя"""
    try:
        success = search_service.clear_search_history(user_id=current_user.id)
        if success:
            return {"message": "История поиска очищена"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка очистки истории поиска")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка очистки истории поиска: {str(e)}"
        )


@router.get("/global")
async def global_search(
    q: str = Query(..., description="Поисковый запрос"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(
        20, ge=1, le=100, description="Количество результатов на странице"
    ),
    current_user: User = Depends(get_current_user),
):
    """Глобальный поиск по всем типам контента"""
    try:
        # Выполняем поиск по всем типам
        posts_result = search_service.search_posts(
            query=q,
            user_id=current_user.id,
            page=1,
            per_page=5,  # Ограничиваем для глобального поиска
        )

        users_result = search_service.search_users(
            query=q,
            user_id=current_user.id,
            page=1,
            per_page=5,  # Ограничиваем для глобального поиска
        )

        tags_result = search_service.search_tags(
            query=q,
            user_id=current_user.id,
            page=1,
            per_page=5,  # Ограничиваем для глобального поиска
        )

        return {
            "query": q,
            "results": {
                "posts": {
                    "items": posts_result["posts"],
                    "total": posts_result["total"],
                },
                "users": {
                    "items": users_result["users"],
                    "total": users_result["total"],
                },
                "tags": {
                    "items": tags_result["tags"],
                    "total": tags_result["total"],
                },
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка глобального поиска: {str(e)}"
        )
