"""
Сервис оптимизации запросов к базе данных
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timezone
import logging
import asyncio
from functools import wraps
import time

logger = logging.getLogger(__name__)


class QueryOptimizationService:
    """Сервис для оптимизации запросов к базе данных"""

    def __init__(self):
        self.query_stats = {
            "total_queries": 0,
            "slow_queries": 0,
            "optimized_queries": 0,
            "cache_hits": 0,
            "average_query_time": 0.0,
        }

        self.slow_query_threshold = 1.0  # 1 секунда
        self.query_cache = {}  # Кэш для часто используемых запросов

        # Индексы для оптимизации
        self.recommended_indexes = {
            "users": ["email", "username", "created_at"],
            "posts": ["user_id", "created_at", "is_published"],
            "products": ["category", "price", "is_active", "created_at"],
            "orders": ["user_id", "status", "created_at"],
            "comments": ["post_id", "user_id", "created_at"],
        }

    def track_query_performance(self, query_name: str = "unknown"):
        """Декоратор для отслеживания производительности запросов"""

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = await func(*args, **kwargs)

                    # Вычисляем время выполнения
                    execution_time = time.time() - start_time

                    # Обновляем статистику
                    self.query_stats["total_queries"] += 1
                    self.query_stats["average_query_time"] = (
                        self.query_stats["average_query_time"]
                        * (self.query_stats["total_queries"] - 1)
                        + execution_time
                    ) / self.query_stats["total_queries"]

                    # Отмечаем медленные запросы
                    if execution_time > self.slow_query_threshold:
                        self.query_stats["slow_queries"] += 1
                        logger.warning(
                            f"Slow query detected: {query_name} took {execution_time:.2f}s"
                        )

                    # Логируем производительность
                    logger.debug(
                        f"Query {query_name} executed in {execution_time:.3f}s"
                    )

                    return result

                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(
                        f"Query {query_name} failed after {execution_time:.3f}s: {e}"
                    )
                    raise

            return wrapper

        return decorator

    async def optimize_pagination(
        self, page: int, page_size: int, total_count: int
    ) -> Dict[str, Any]:
        """Оптимизация пагинации"""
        try:
            # Ограничиваем размер страницы
            max_page_size = 100
            page_size = min(page_size, max_page_size)

            # Вычисляем офсет
            offset = (page - 1) * page_size

            # Проверяем валидность страницы
            max_page = (total_count + page_size - 1) // page_size
            if page > max_page and max_page > 0:
                page = max_page
                offset = (page - 1) * page_size

            return {
                "page": page,
                "page_size": page_size,
                "offset": offset,
                "total_pages": max_page,
                "has_next": page < max_page,
                "has_prev": page > 1,
            }

        except Exception as e:
            logger.error(f"Error optimizing pagination: {e}")
            return {
                "page": 1,
                "page_size": 20,
                "offset": 0,
                "total_pages": 1,
                "has_next": False,
                "has_prev": False,
            }

    async def optimize_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Оптимизация фильтров запросов"""
        try:
            optimized_filters = {}

            for key, value in filters.items():
                if value is None or value == "":
                    continue

                # Оптимизируем строковые фильтры
                if isinstance(value, str):
                    # Добавляем ILIKE для поиска по части строки
                    if key.endswith("_search") or "search" in key.lower():
                        optimized_filters[f"{key}_ilike"] = f"%{value}%"
                    else:
                        optimized_filters[key] = value

                # Оптимизируем числовые фильтры
                elif isinstance(value, (int, float)):
                    optimized_filters[key] = value

                # Оптимизируем булевы фильтры
                elif isinstance(value, bool):
                    optimized_filters[key] = value

                # Оптимизируем списки
                elif isinstance(value, list):
                    if value:  # Только непустые списки
                        optimized_filters[f"{key}_in"] = value

            return optimized_filters

        except Exception as e:
            logger.error(f"Error optimizing filters: {e}")
            return filters

    async def optimize_sorting(
        self, sort_by: str, sort_order: str = "asc"
    ) -> Dict[str, str]:
        """Оптимизация сортировки"""
        try:
            # Валидируем поле сортировки
            allowed_sort_fields = [
                "id",
                "created_at",
                "updated_at",
                "name",
                "title",
                "email",
                "username",
                "price",
                "status",
                "is_active",
                "views",
                "likes",
                "comments",
            ]

            if sort_by not in allowed_sort_fields:
                sort_by = "created_at"  # По умолчанию

            # Валидируем порядок сортировки
            if sort_order.lower() not in ["asc", "desc"]:
                sort_order = "desc"  # По умолчанию

            return {"sort_by": sort_by, "sort_order": sort_order}

        except Exception as e:
            logger.error(f"Error optimizing sorting: {e}")
            return {"sort_by": "created_at", "sort_order": "desc"}

    async def batch_queries(self, queries: List[Dict[str, Any]]) -> List[Any]:
        """Выполнение пакетных запросов"""
        try:
            # Группируем запросы по типу
            grouped_queries = {}
            for query in queries:
                query_type = query.get("type", "unknown")
                if query_type not in grouped_queries:
                    grouped_queries[query_type] = []
                grouped_queries[query_type].append(query)

            # Выполняем запросы параллельно
            results = []
            tasks = []

            for query_type, type_queries in grouped_queries.items():
                task = asyncio.create_task(
                    self._execute_query_batch(query_type, type_queries)
                )
                tasks.append(task)

            # Ждем завершения всех задач
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Объединяем результаты
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Batch query failed: {result}")
                    results.append(None)
                else:
                    results.extend(result)

            return results

        except Exception as e:
            logger.error(f"Error executing batch queries: {e}")
            return []

    async def _execute_query_batch(
        self, query_type: str, queries: List[Dict[str, Any]]
    ) -> List[Any]:
        """Выполнение пакета запросов одного типа"""
        try:
            # В реальном приложении здесь будет выполнение SQL запросов
            # Пока возвращаем моковые данные
            results = []
            for query in queries:
                # Симулируем выполнение запроса
                await asyncio.sleep(0.01)  # Небольшая задержка
                results.append({"query_id": query.get("id"), "result": "mocked"})

            return results

        except Exception as e:
            logger.error(f"Error executing query batch for type {query_type}: {e}")
            return []

    async def analyze_query_performance(self) -> Dict[str, Any]:
        """Анализ производительности запросов"""
        try:
            total_queries = self.query_stats["total_queries"]
            slow_queries = self.query_stats["slow_queries"]
            slow_query_percentage = (
                (slow_queries / total_queries * 100) if total_queries > 0 else 0
            )

            # Рекомендации по оптимизации
            recommendations = []

            if slow_query_percentage > 10:
                recommendations.append(
                    "Consider adding database indexes for frequently queried fields"
                )

            if self.query_stats["average_query_time"] > 0.5:
                recommendations.append(
                    "Consider implementing query caching for slow operations"
                )

            if total_queries > 1000 and slow_query_percentage > 5:
                recommendations.append("Consider implementing connection pooling")

            return {
                "performance_stats": self.query_stats,
                "slow_query_percentage": round(slow_query_percentage, 2),
                "recommendations": recommendations,
                "recommended_indexes": self.recommended_indexes,
            }

        except Exception as e:
            logger.error(f"Error analyzing query performance: {e}")
            return {}

    async def get_query_recommendations(self, table_name: str) -> List[str]:
        """Получить рекомендации по оптимизации для таблицы"""
        try:
            recommendations = []

            if table_name in self.recommended_indexes:
                indexes = self.recommended_indexes[table_name]
                recommendations.append(
                    f"Consider adding indexes on: {', '.join(indexes)}"
                )

            # Общие рекомендации
            recommendations.extend(
                [
                    "Use LIMIT to restrict result sets",
                    "Avoid SELECT * - specify only needed columns",
                    "Use appropriate data types for columns",
                    "Consider partitioning for large tables",
                    "Regularly analyze and optimize slow queries",
                ]
            )

            return recommendations

        except Exception as e:
            logger.error(f"Error getting query recommendations: {e}")
            return []

    async def optimize_join_queries(
        self, joins: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Оптимизация JOIN запросов"""
        try:
            optimized_joins = []

            for join in joins:
                # Проверяем, что есть индексы для JOIN полей
                table = join.get("table")
                on_field = join.get("on")

                if table in self.recommended_indexes:
                    if on_field in self.recommended_indexes[table]:
                        optimized_joins.append(join)
                    else:
                        # Добавляем рекомендацию по индексу
                        optimized_joins.append(
                            {
                                **join,
                                "recommendation": f"Consider adding index on {table}.{on_field}",
                            }
                        )
                else:
                    optimized_joins.append(join)

            return optimized_joins

        except Exception as e:
            logger.error(f"Error optimizing join queries: {e}")
            return joins

    def reset_stats(self):
        """Сброс статистики запросов"""
        self.query_stats = {
            "total_queries": 0,
            "slow_queries": 0,
            "optimized_queries": 0,
            "cache_hits": 0,
            "average_query_time": 0.0,
        }
        logger.info("Query statistics reset")


# Создаем глобальный экземпляр сервиса
query_optimization_service = QueryOptimizationService()
