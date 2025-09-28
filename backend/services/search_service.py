"""
Сервис поиска и фильтрации
"""

import re
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """Сервис для поиска и фильтрации контента"""

    def __init__(self):
        self.search_history = {}  # В реальном приложении - БД
        self.popular_searches = {}  # В реальном приложении - БД
        self.search_suggestions = {}  # В реальном приложении - БД

    def search_posts(
        self,
        query: str,
        user_id: int,
        filters: Optional[Dict] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Поиск постов по тексту и фильтрам"""
        try:
            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые данные с учетом фильтров

            # Сохраняем поисковый запрос
            self._save_search_query(query, user_id)

            # Применяем фильтры
            filtered_posts = self._apply_post_filters(filters or {})

            # Ищем по тексту
            if query:
                filtered_posts = self._search_in_posts(filtered_posts, query)

            # Пагинация
            total = len(filtered_posts)
            start = (page - 1) * per_page
            end = start + per_page
            posts = filtered_posts[start:end]

            return {
                "posts": posts,
                "total": total,
                "page": page,
                "per_page": per_page,
                "query": query,
                "filters": filters,
            }

        except Exception as e:
            logger.error(f"Error searching posts: {e}")
            raise Exception(f"Ошибка поиска постов: {str(e)}")

    def search_users(
        self,
        query: str,
        user_id: int,
        filters: Optional[Dict] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Поиск пользователей по имени, email, username"""
        try:
            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые данные

            # Сохраняем поисковый запрос
            self._save_search_query(query, user_id)

            # Применяем фильтры
            filtered_users = self._apply_user_filters(filters or {})

            # Ищем по тексту
            if query:
                filtered_users = self._search_in_users(filtered_users, query)

            # Пагинация
            total = len(filtered_users)
            start = (page - 1) * per_page
            end = start + per_page
            users = filtered_users[start:end]

            return {
                "users": users,
                "total": total,
                "page": page,
                "per_page": per_page,
                "query": query,
                "filters": filters,
            }

        except Exception as e:
            logger.error(f"Error searching users: {e}")
            raise Exception(f"Ошибка поиска пользователей: {str(e)}")

    def search_tags(
        self,
        query: str,
        user_id: int,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Поиск тегов"""
        try:
            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые данные

            # Сохраняем поисковый запрос
            self._save_search_query(query, user_id)

            # Моковые теги
            all_tags = [
                {"name": "python", "count": 150, "popularity": 0.9},
                {"name": "javascript", "count": 200, "popularity": 0.95},
                {"name": "react", "count": 180, "popularity": 0.88},
                {"name": "vue", "count": 120, "popularity": 0.75},
                {"name": "angular", "count": 100, "popularity": 0.7},
                {"name": "nodejs", "count": 160, "popularity": 0.85},
                {"name": "fastapi", "count": 80, "popularity": 0.6},
                {"name": "django", "count": 90, "popularity": 0.65},
                {"name": "flask", "count": 70, "popularity": 0.55},
                {"name": "sqlalchemy", "count": 60, "popularity": 0.5},
            ]

            # Фильтруем по запросу
            if query:
                filtered_tags = [
                    tag for tag in all_tags if query.lower() in tag["name"].lower()
                ]
            else:
                filtered_tags = all_tags

            # Сортируем по популярности
            filtered_tags.sort(key=lambda x: x["popularity"], reverse=True)

            # Пагинация
            total = len(filtered_tags)
            start = (page - 1) * per_page
            end = start + per_page
            tags = filtered_tags[start:end]

            return {
                "tags": tags,
                "total": total,
                "page": page,
                "per_page": per_page,
                "query": query,
            }

        except Exception as e:
            logger.error(f"Error searching tags: {e}")
            raise Exception(f"Ошибка поиска тегов: {str(e)}")

    def get_search_suggestions(
        self, query: str, user_id: int, limit: int = 10
    ) -> List[str]:
        """Получение предложений для автодополнения"""
        try:
            if len(query) < 2:
                return []

            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые предложения

            suggestions = [
                "python programming",
                "javascript tutorial",
                "react hooks",
                "vue components",
                "angular services",
                "nodejs backend",
                "fastapi async",
                "django models",
                "flask routes",
                "sqlalchemy queries",
            ]

            # Фильтруем по запросу
            filtered_suggestions = [
                suggestion
                for suggestion in suggestions
                if query.lower() in suggestion.lower()
            ]

            return filtered_suggestions[:limit]

        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return []

    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение популярных поисковых запросов"""
        try:
            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые данные

            popular = [
                {"query": "python", "count": 150, "trend": "up"},
                {"query": "javascript", "count": 200, "trend": "up"},
                {"query": "react", "count": 180, "trend": "stable"},
                {"query": "vue", "count": 120, "trend": "down"},
                {"query": "angular", "count": 100, "trend": "stable"},
                {"query": "nodejs", "count": 160, "trend": "up"},
                {"query": "fastapi", "count": 80, "trend": "up"},
                {"query": "django", "count": 90, "trend": "stable"},
                {"query": "flask", "count": 70, "trend": "down"},
                {"query": "sqlalchemy", "count": 60, "trend": "stable"},
            ]

            return popular[:limit]

        except Exception as e:
            logger.error(f"Error getting popular searches: {e}")
            return []

    def get_user_search_history(self, user_id: int, limit: int = 20) -> List[str]:
        """Получение истории поиска пользователя"""
        try:
            # В реальном приложении здесь будет запрос к БД
            # Пока возвращаем моковые данные

            history = self.search_history.get(user_id, [])
            return history[-limit:] if history else []

        except Exception as e:
            logger.error(f"Error getting search history: {e}")
            return []

    def clear_search_history(self, user_id: int) -> bool:
        """Очистка истории поиска пользователя"""
        try:
            if user_id in self.search_history:
                del self.search_history[user_id]
            return True

        except Exception as e:
            logger.error(f"Error clearing search history: {e}")
            return False

    def _save_search_query(self, query: str, user_id: int) -> None:
        """Сохранение поискового запроса"""
        if not query or len(query.strip()) < 2:
            return

        query = query.strip().lower()

        # Сохраняем в историю пользователя
        if user_id not in self.search_history:
            self.search_history[user_id] = []

        # Удаляем дубликаты
        if query in self.search_history[user_id]:
            self.search_history[user_id].remove(query)

        # Добавляем в начало
        self.search_history[user_id].insert(0, query)

        # Ограничиваем размер истории
        if len(self.search_history[user_id]) > 50:
            self.search_history[user_id] = self.search_history[user_id][:50]

        # Обновляем статистику популярных запросов
        if query not in self.popular_searches:
            self.popular_searches[query] = 0
        self.popular_searches[query] += 1

    def _apply_post_filters(self, filters: Dict) -> List[Dict]:
        """Применение фильтров к постам"""
        # В реальном приложении здесь будет запрос к БД с WHERE условиями
        # Пока возвращаем моковые данные

        mock_posts = [
            {
                "id": 1,
                "title": "Python Programming Tips",
                "content": "Learn advanced Python techniques...",
                "author": {"id": 1, "name": "John Doe", "username": "johndoe"},
                "tags": ["python", "programming", "tutorial"],
                "created_at": "2025-01-28T10:00:00Z",
                "likes_count": 25,
                "comments_count": 5,
                "views_count": 150,
                "category": "programming",
                "is_published": True,
            },
            {
                "id": 2,
                "title": "React Hooks Guide",
                "content": "Complete guide to React hooks...",
                "author": {"id": 2, "name": "Jane Smith", "username": "janesmith"},
                "tags": ["react", "javascript", "hooks"],
                "created_at": "2025-01-27T15:30:00Z",
                "likes_count": 40,
                "comments_count": 8,
                "views_count": 200,
                "category": "programming",
                "is_published": True,
            },
            {
                "id": 3,
                "title": "Vue.js Components",
                "content": "Building reusable Vue components...",
                "author": {"id": 3, "name": "Bob Wilson", "username": "bobwilson"},
                "tags": ["vue", "javascript", "components"],
                "created_at": "2025-01-26T09:15:00Z",
                "likes_count": 30,
                "comments_count": 3,
                "views_count": 120,
                "category": "programming",
                "is_published": True,
            },
        ]

        # Применяем фильтры
        filtered_posts = mock_posts

        # Фильтр по категории
        if "category" in filters and filters["category"]:
            filtered_posts = [
                post
                for post in filtered_posts
                if post.get("category") == filters["category"]
            ]

        # Фильтр по тегам
        if "tags" in filters and filters["tags"]:
            tag_list = (
                filters["tags"]
                if isinstance(filters["tags"], list)
                else [filters["tags"]]
            )
            filtered_posts = [
                post
                for post in filtered_posts
                if any(tag in post.get("tags", []) for tag in tag_list)
            ]

        # Фильтр по дате
        if "date_from" in filters and filters["date_from"]:
            # В реальном приложении здесь будет сравнение дат
            pass

        if "date_to" in filters and filters["date_to"]:
            # В реальном приложении здесь будет сравнение дат
            pass

        # Фильтр по автору
        if "author_id" in filters and filters["author_id"]:
            filtered_posts = [
                post
                for post in filtered_posts
                if post.get("author", {}).get("id") == filters["author_id"]
            ]

        # Фильтр по статусу публикации
        if "is_published" in filters:
            filtered_posts = [
                post
                for post in filtered_posts
                if post.get("is_published") == filters["is_published"]
            ]

        return filtered_posts

    def _apply_user_filters(self, filters: Dict) -> List[Dict]:
        """Применение фильтров к пользователям"""
        # В реальном приложении здесь будет запрос к БД с WHERE условиями
        # Пока возвращаем моковые данные

        mock_users = [
            {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "bio": "Python developer with 5 years experience",
                "location": "New York, USA",
                "followers_count": 150,
                "following_count": 75,
                "posts_count": 25,
                "is_verified": True,
                "created_at": "2024-01-15T10:00:00Z",
            },
            {
                "id": 2,
                "username": "janesmith",
                "email": "jane@example.com",
                "full_name": "Jane Smith",
                "bio": "React developer and UI/UX designer",
                "location": "San Francisco, USA",
                "followers_count": 200,
                "following_count": 100,
                "posts_count": 30,
                "is_verified": True,
                "created_at": "2024-02-20T14:30:00Z",
            },
            {
                "id": 3,
                "username": "bobwilson",
                "email": "bob@example.com",
                "full_name": "Bob Wilson",
                "bio": "Vue.js enthusiast and full-stack developer",
                "location": "London, UK",
                "followers_count": 80,
                "following_count": 50,
                "posts_count": 15,
                "is_verified": False,
                "created_at": "2024-03-10T09:15:00Z",
            },
        ]

        # Применяем фильтры
        filtered_users = mock_users

        # Фильтр по верификации
        if "is_verified" in filters:
            filtered_users = [
                user
                for user in filtered_users
                if user.get("is_verified") == filters["is_verified"]
            ]

        # Фильтр по локации
        if "location" in filters and filters["location"]:
            filtered_users = [
                user
                for user in filtered_users
                if filters["location"].lower() in user.get("location", "").lower()
            ]

        # Фильтр по количеству подписчиков
        if "min_followers" in filters:
            filtered_users = [
                user
                for user in filtered_users
                if user.get("followers_count", 0) >= filters["min_followers"]
            ]

        return filtered_users

    def _search_in_posts(self, posts: List[Dict], query: str) -> List[Dict]:
        """Поиск по тексту в постах"""
        query_lower = query.lower()
        results = []

        for post in posts:
            # Поиск в заголовке
            if query_lower in post.get("title", "").lower():
                results.append(post)
                continue

            # Поиск в содержимом
            if query_lower in post.get("content", "").lower():
                results.append(post)
                continue

            # Поиск в тегах
            if any(query_lower in tag.lower() for tag in post.get("tags", [])):
                results.append(post)
                continue

            # Поиск в имени автора
            if query_lower in post.get("author", {}).get("name", "").lower():
                results.append(post)
                continue

        return results

    def _search_in_users(self, users: List[Dict], query: str) -> List[Dict]:
        """Поиск по тексту в пользователях"""
        query_lower = query.lower()
        results = []

        for user in users:
            # Поиск в username
            if query_lower in user.get("username", "").lower():
                results.append(user)
                continue

            # Поиск в полном имени
            if query_lower in user.get("full_name", "").lower():
                results.append(user)
                continue

            # Поиск в email
            if query_lower in user.get("email", "").lower():
                results.append(user)
                continue

            # Поиск в bio
            if query_lower in user.get("bio", "").lower():
                results.append(user)
                continue

        return results


# Глобальный экземпляр сервиса
search_service = SearchService()
