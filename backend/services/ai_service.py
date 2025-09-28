"""
AI и Machine Learning сервис
Рекомендации, анализ контента, персонализация
"""

import json
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import hashlib

logger = logging.getLogger(__name__)


class AIService:
    """Сервис для AI и машинного обучения"""

    def __init__(self):
        # В реальном приложении здесь будут ML модели
        self.user_preferences = {}
        self.content_embeddings = {}
        self.recommendation_models = {}
        self.analytics_data = {}

    def get_content_recommendations(
        self, user_id: int, content_type: str = "posts", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Получение рекомендаций контента для пользователя"""
        try:
            # В реальном приложении здесь будет ML модель
            # Пока возвращаем персонализированные рекомендации

            # Получаем предпочтения пользователя
            preferences = self._get_user_preferences(user_id)

            # Генерируем рекомендации на основе предпочтений
            recommendations = self._generate_recommendations(
                user_id, content_type, preferences, limit
            )

            return recommendations

        except Exception as e:
            logger.error(f"Error getting content recommendations: {e}")
            return []

    def get_user_recommendations(
        self, user_id: int, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Рекомендации пользователей для подписки"""
        try:
            # В реальном приложении здесь будет анализ социального графа
            recommendations = [
                {
                    "id": 2,
                    "username": "janesmith",
                    "full_name": "Jane Smith",
                    "bio": "React developer and UI/UX designer",
                    "avatar_url": "https://via.placeholder.com/150/007bff/ffffff?text=JS",
                    "followers_count": 200,
                    "mutual_friends": 5,
                    "similarity_score": 0.85,
                    "reason": "Similar interests in programming",
                },
                {
                    "id": 3,
                    "username": "bobwilson",
                    "full_name": "Bob Wilson",
                    "bio": "Vue.js enthusiast and full-stack developer",
                    "avatar_url": "https://via.placeholder.com/150/28a745/ffffff?text=BW",
                    "followers_count": 80,
                    "mutual_friends": 3,
                    "similarity_score": 0.72,
                    "reason": "Works with similar technologies",
                },
                {
                    "id": 4,
                    "username": "alicebrown",
                    "full_name": "Alice Brown",
                    "bio": "Python data scientist and ML engineer",
                    "avatar_url": "https://via.placeholder.com/150/dc3545/ffffff?text=AB",
                    "followers_count": 150,
                    "mutual_friends": 2,
                    "similarity_score": 0.68,
                    "reason": "Shared interest in data science",
                },
            ]

            return recommendations[:limit]

        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")
            return []

    def analyze_content_sentiment(self, content: str) -> Dict[str, Any]:
        """Анализ тональности контента"""
        try:
            # В реальном приложении здесь будет NLP модель
            # Простая эвристика для демонстрации

            positive_words = [
                "хорошо",
                "отлично",
                "прекрасно",
                "замечательно",
                "великолепно",
                "good",
                "great",
                "excellent",
                "amazing",
                "wonderful",
                "awesome",
            ]
            negative_words = [
                "плохо",
                "ужасно",
                "отвратительно",
                "кошмар",
                "проблема",
                "bad",
                "terrible",
                "awful",
                "horrible",
                "problem",
                "issue",
            ]

            content_lower = content.lower()
            positive_count = sum(1 for word in positive_words if word in content_lower)
            negative_count = sum(1 for word in negative_words if word in content_lower)

            if positive_count > negative_count:
                sentiment = "positive"
                confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
            elif negative_count > positive_count:
                sentiment = "negative"
                confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
            else:
                sentiment = "neutral"
                confidence = 0.5

            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "positive_words": positive_count,
                "negative_words": negative_count,
                "analysis_date": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error analyzing content sentiment: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": str(e),
            }

    def extract_content_tags(self, content: str) -> List[str]:
        """Извлечение тегов из контента"""
        try:
            # В реальном приложении здесь будет NLP модель
            # Простое извлечение ключевых слов

            tech_keywords = [
                "python",
                "javascript",
                "react",
                "vue",
                "angular",
                "nodejs",
                "fastapi",
                "django",
                "flask",
                "sqlalchemy",
                "postgresql",
                "mongodb",
                "redis",
                "docker",
                "kubernetes",
                "aws",
                "azure",
            ]

            content_lower = content.lower()
            found_tags = [
                keyword for keyword in tech_keywords if keyword in content_lower
            ]

            # Добавляем общие теги на основе длины контента
            if len(content) > 500:
                found_tags.append("long-read")
            if len(content) < 100:
                found_tags.append("short")

            return found_tags[:10]  # Ограничиваем количество тегов

        except Exception as e:
            logger.error(f"Error extracting content tags: {e}")
            return []

    def generate_content_summary(self, content: str, max_length: int = 200) -> str:
        """Генерация краткого содержания"""
        try:
            # В реальном приложении здесь будет NLP модель
            # Простое извлечение первых предложений

            sentences = content.split(". ")
            summary_sentences = []
            current_length = 0

            for sentence in sentences:
                if current_length + len(sentence) > max_length:
                    break
                summary_sentences.append(sentence)
                current_length += len(sentence) + 2  # +2 for ". "

            summary = ". ".join(summary_sentences)
            if summary and not summary.endswith("."):
                summary += "..."

            return summary

        except Exception as e:
            logger.error(f"Error generating content summary: {e}")
            return (
                content[:max_length] + "..." if len(content) > max_length else content
            )

    def detect_spam_content(self, content: str, user_id: int) -> Dict[str, Any]:
        """Детекция спама в контенте"""
        try:
            # В реальном приложении здесь будет ML модель
            # Простые эвристики для демонстрации

            spam_indicators = {
                "excessive_caps": content.upper() == content and len(content) > 10,
                "excessive_links": content.count("http") > 3,
                "repeated_chars": any(char * 5 in content for char in "!@#$%^&*()"),
                "suspicious_words": any(
                    word in content.lower()
                    for word in [
                        "click here",
                        "free money",
                        "urgent",
                        "act now",
                        "limited time",
                    ]
                ),
            }

            spam_score = sum(spam_indicators.values()) / len(spam_indicators)
            is_spam = spam_score > 0.3

            return {
                "is_spam": is_spam,
                "spam_score": spam_score,
                "indicators": spam_indicators,
                "confidence": min(0.95, spam_score + 0.1),
                "analysis_date": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error detecting spam content: {e}")
            return {
                "is_spam": False,
                "spam_score": 0.0,
                "error": str(e),
            }

    def personalize_feed(
        self, user_id: int, posts: List[Dict], limit: int = 20
    ) -> List[Dict]:
        """Персонализация ленты пользователя"""
        try:
            # В реальном приложении здесь будет ML модель ранжирования
            preferences = self._get_user_preferences(user_id)

            # Сортируем постов по релевантности
            scored_posts = []
            for post in posts:
                score = self._calculate_relevance_score(post, preferences)
                scored_posts.append((post, score))

            # Сортируем по убыванию релевантности
            scored_posts.sort(key=lambda x: x[1], reverse=True)

            # Возвращаем топ постов
            personalized_posts = [post for post, score in scored_posts[:limit]]

            return personalized_posts

        except Exception as e:
            logger.error(f"Error personalizing feed: {e}")
            return posts[:limit]

    def get_trending_topics(self, time_period: str = "24h") -> List[Dict[str, Any]]:
        """Получение трендовых тем"""
        try:
            # В реальном приложении здесь будет анализ временных рядов
            trending = [
                {
                    "topic": "AI and Machine Learning",
                    "mentions": 1250,
                    "growth": 15.5,
                    "sentiment": "positive",
                    "related_hashtags": ["#AI", "#ML", "#MachineLearning"],
                },
                {
                    "topic": "Web Development",
                    "mentions": 980,
                    "growth": 8.2,
                    "sentiment": "positive",
                    "related_hashtags": ["#WebDev", "#JavaScript", "#React"],
                },
                {
                    "topic": "Data Science",
                    "mentions": 750,
                    "growth": 12.1,
                    "sentiment": "positive",
                    "related_hashtags": ["#DataScience", "#Python", "#Analytics"],
                },
                {
                    "topic": "Cybersecurity",
                    "mentions": 650,
                    "growth": 20.3,
                    "sentiment": "neutral",
                    "related_hashtags": ["#Security", "#Cybersecurity", "#Privacy"],
                },
            ]

            return trending

        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []

    def predict_user_engagement(
        self, user_id: int, content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Предсказание вовлеченности пользователя"""
        try:
            # В реальном приложении здесь будет ML модель
            preferences = self._get_user_preferences(user_id)

            # Простая эвристика для демонстрации
            base_engagement = 0.3

            # Увеличиваем вероятность на основе интересов
            if any(
                tag in preferences.get("interests", [])
                for tag in content.get("tags", [])
            ):
                base_engagement += 0.3

            # Увеличиваем для короткого контента
            if content.get("content", "").count(" ") < 50:
                base_engagement += 0.1

            # Увеличиваем для популярных авторов
            if content.get("author", {}).get("followers_count", 0) > 1000:
                base_engagement += 0.2

            predicted_engagement = min(0.95, base_engagement)

            return {
                "likelihood_to_like": predicted_engagement,
                "likelihood_to_comment": predicted_engagement * 0.3,
                "likelihood_to_share": predicted_engagement * 0.1,
                "confidence": 0.7,
                "factors": [
                    "User interests match",
                    "Content length",
                    "Author popularity",
                ],
            }

        except Exception as e:
            logger.error(f"Error predicting user engagement: {e}")
            return {
                "likelihood_to_like": 0.3,
                "likelihood_to_comment": 0.1,
                "likelihood_to_share": 0.05,
                "confidence": 0.0,
                "error": str(e),
            }

    def _get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Получение предпочтений пользователя"""
        if user_id not in self.user_preferences:
            # Генерируем случайные предпочтения для демонстрации
            self.user_preferences[user_id] = {
                "interests": random.sample(
                    [
                        "python",
                        "javascript",
                        "react",
                        "vue",
                        "data-science",
                        "machine-learning",
                        "web-development",
                        "mobile-development",
                    ],
                    k=random.randint(2, 5),
                ),
                "preferred_content_length": random.choice(["short", "medium", "long"]),
                "active_hours": list(range(9, 18)),  # 9 AM to 6 PM
                "engagement_history": {
                    "avg_likes_per_day": random.randint(5, 50),
                    "avg_comments_per_day": random.randint(1, 10),
                    "avg_shares_per_day": random.randint(0, 5),
                },
            }

        return self.user_preferences[user_id]

    def _generate_recommendations(
        self, user_id: int, content_type: str, preferences: Dict, limit: int
    ) -> List[Dict[str, Any]]:
        """Генерация рекомендаций на основе предпочтений"""
        # Моковые рекомендации
        mock_recommendations = [
            {
                "id": 1,
                "title": "Advanced Python Techniques",
                "content": "Learn advanced Python programming techniques...",
                "author": {"name": "John Doe", "username": "johndoe"},
                "tags": ["python", "programming", "tutorial"],
                "likes_count": 25,
                "comments_count": 5,
                "relevance_score": 0.95,
                "recommendation_reason": "Matches your interest in Python",
            },
            {
                "id": 2,
                "title": "React Hooks Deep Dive",
                "content": "Complete guide to React hooks...",
                "author": {"name": "Jane Smith", "username": "janesmith"},
                "tags": ["react", "javascript", "hooks"],
                "likes_count": 40,
                "comments_count": 8,
                "relevance_score": 0.88,
                "recommendation_reason": "Popular in your network",
            },
            {
                "id": 3,
                "title": "Machine Learning Basics",
                "content": "Introduction to machine learning concepts...",
                "author": {"name": "Bob Wilson", "username": "bobwilson"},
                "tags": ["machine-learning", "data-science", "ai"],
                "likes_count": 30,
                "comments_count": 3,
                "relevance_score": 0.82,
                "recommendation_reason": "Trending in your interests",
            },
        ]

        return mock_recommendations[:limit]

    def _calculate_relevance_score(self, post: Dict, preferences: Dict) -> float:
        """Расчет релевантности поста для пользователя"""
        score = 0.0

        # Проверяем совпадение интересов
        post_tags = post.get("tags", [])
        user_interests = preferences.get("interests", [])

        if post_tags and user_interests:
            common_tags = set(post_tags) & set(user_interests)
            score += len(common_tags) * 0.2

        # Учитываем популярность
        likes = post.get("likes_count", 0)
        score += min(0.3, likes / 100)

        # Учитываем время публикации (свежий контент)
        # В реальном приложении здесь будет анализ даты
        score += 0.1

        return min(1.0, score)


# Глобальный экземпляр сервиса
ai_service = AIService()
