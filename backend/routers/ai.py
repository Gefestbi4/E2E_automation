"""
API для AI и Machine Learning функций
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.ai_service import ai_service
from auth import get_current_user
from models import User

router = APIRouter(prefix="/api/ai", tags=["ai"])


class ContentAnalysisRequest(BaseModel):
    content: str


class ContentRecommendationRequest(BaseModel):
    content_type: str = "posts"
    limit: int = 10


class UserRecommendationRequest(BaseModel):
    limit: int = 10


class FeedPersonalizationRequest(BaseModel):
    posts: List[Dict[str, Any]]
    limit: int = 20


@router.get("/recommendations/content")
async def get_content_recommendations(
    content_type: str = Query("posts", description="Type of content to recommend"),
    limit: int = Query(10, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
):
    """Получение рекомендаций контента"""
    try:
        recommendations = ai_service.get_content_recommendations(
            current_user.id, content_type, limit
        )
        return {
            "recommendations": recommendations,
            "user_id": current_user.id,
            "content_type": content_type,
            "total": len(recommendations),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения рекомендаций: {str(e)}"
        )


@router.get("/recommendations/users")
async def get_user_recommendations(
    limit: int = Query(10, description="Number of user recommendations"),
    current_user: User = Depends(get_current_user),
):
    """Получение рекомендаций пользователей для подписки"""
    try:
        recommendations = ai_service.get_user_recommendations(current_user.id, limit)
        return {
            "recommendations": recommendations,
            "user_id": current_user.id,
            "total": len(recommendations),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения рекомендаций пользователей: {str(e)}",
        )


@router.post("/analyze/sentiment")
async def analyze_content_sentiment(
    request: ContentAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """Анализ тональности контента"""
    try:
        analysis = ai_service.analyze_content_sentiment(request.content)
        return {
            "analysis": analysis,
            "content_length": len(request.content),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка анализа тональности: {str(e)}"
        )


@router.post("/analyze/tags")
async def extract_content_tags(
    request: ContentAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """Извлечение тегов из контента"""
    try:
        tags = ai_service.extract_content_tags(request.content)
        return {
            "tags": tags,
            "content_length": len(request.content),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка извлечения тегов: {str(e)}"
        )


@router.post("/analyze/summary")
async def generate_content_summary(
    request: ContentAnalysisRequest,
    max_length: int = Query(200, description="Maximum summary length"),
    current_user: User = Depends(get_current_user),
):
    """Генерация краткого содержания"""
    try:
        summary = ai_service.generate_content_summary(request.content, max_length)
        return {
            "summary": summary,
            "original_length": len(request.content),
            "summary_length": len(summary),
            "compression_ratio": (
                len(summary) / len(request.content) if request.content else 0
            ),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка генерации содержания: {str(e)}"
        )


@router.post("/analyze/spam")
async def detect_spam_content(
    request: ContentAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """Детекция спама в контенте"""
    try:
        spam_analysis = ai_service.detect_spam_content(request.content, current_user.id)
        return {
            "analysis": spam_analysis,
            "content_length": len(request.content),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка детекции спама: {str(e)}")


@router.post("/personalize/feed")
async def personalize_user_feed(
    request: FeedPersonalizationRequest,
    current_user: User = Depends(get_current_user),
):
    """Персонализация ленты пользователя"""
    try:
        personalized_posts = ai_service.personalize_feed(
            current_user.id, request.posts, request.limit
        )
        return {
            "personalized_posts": personalized_posts,
            "original_count": len(request.posts),
            "personalized_count": len(personalized_posts),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка персонализации ленты: {str(e)}"
        )


@router.get("/trending/topics")
async def get_trending_topics(
    time_period: str = Query("24h", description="Time period for trending analysis"),
    current_user: User = Depends(get_current_user),
):
    """Получение трендовых тем"""
    try:
        trending = ai_service.get_trending_topics(time_period)
        return {
            "trending_topics": trending,
            "time_period": time_period,
            "user_id": current_user.id,
            "total": len(trending),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения трендов: {str(e)}"
        )


@router.post("/predict/engagement")
async def predict_user_engagement(
    content: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """Предсказание вовлеченности пользователя"""
    try:
        prediction = ai_service.predict_user_engagement(current_user.id, content)
        return {
            "prediction": prediction,
            "content_id": content.get("id"),
            "user_id": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка предсказания вовлеченности: {str(e)}"
        )


@router.get("/insights/user")
async def get_user_insights(
    current_user: User = Depends(get_current_user),
):
    """Получение AI инсайтов о пользователе"""
    try:
        # В реальном приложении здесь будет анализ поведения пользователя
        insights = {
            "activity_patterns": {
                "most_active_hours": [9, 10, 11, 14, 15, 16],
                "preferred_content_types": ["tutorials", "news", "discussions"],
                "engagement_trends": {
                    "likes_per_day": 15.2,
                    "comments_per_day": 3.1,
                    "shares_per_day": 1.8,
                },
            },
            "content_preferences": {
                "favorite_topics": ["python", "web-development", "data-science"],
                "preferred_length": "medium",
                "sentiment_preference": "positive",
            },
            "social_behavior": {
                "network_growth_rate": 12.5,
                "interaction_frequency": "high",
                "content_creation_rate": "medium",
            },
            "recommendations": {
                "suggested_connections": 5,
                "trending_topics_to_follow": 3,
                "content_ideas": 2,
            },
        }

        return {
            "insights": insights,
            "user_id": current_user.id,
            "generated_at": "2025-01-28T10:00:00Z",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка получения инсайтов: {str(e)}"
        )


@router.get("/health")
async def ai_health_check():
    """Проверка состояния AI сервисов"""
    try:
        # В реальном приложении здесь будет проверка ML моделей
        health_status = {
            "status": "healthy",
            "services": {
                "recommendation_engine": "operational",
                "sentiment_analysis": "operational",
                "content_classification": "operational",
                "spam_detection": "operational",
            },
            "models": {
                "content_recommendations": "v1.2.3",
                "user_recommendations": "v1.1.0",
                "sentiment_analysis": "v2.0.1",
                "spam_detection": "v1.5.2",
            },
            "performance": {
                "avg_response_time_ms": 150,
                "success_rate": 99.8,
                "last_model_update": "2025-01-28T08:00:00Z",
            },
        }

        return health_status

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка проверки состояния: {str(e)}"
        )
