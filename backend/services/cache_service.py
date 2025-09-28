"""
Сервис кэширования для оптимизации производительности
"""

from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta, timezone
import json
import logging
import hashlib
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)


class CacheService:
    """Сервис кэширования для оптимизации производительности"""

    def __init__(self):
        # В реальном приложении здесь будет Redis или другой кэш
        self.memory_cache = {}  # In-memory кэш
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "expired": 0,
        }

        # Настройки кэширования
        self.default_ttl = 3600  # 1 час по умолчанию
        self.max_memory_items = 1000  # Максимум элементов в памяти

        # Запускаем очистку истекших элементов
        asyncio.create_task(self._cleanup_expired())

    async def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        try:
            if key in self.memory_cache:
                cache_item = self.memory_cache[key]

                # Проверяем срок действия
                if (
                    cache_item["expires_at"]
                    and datetime.now(timezone.utc) > cache_item["expires_at"]
                ):
                    del self.memory_cache[key]
                    self.cache_stats["expired"] += 1
                    self.cache_stats["misses"] += 1
                    return None

                self.cache_stats["hits"] += 1
                logger.debug(f"Cache hit for key: {key}")
                return cache_item["value"]

            self.cache_stats["misses"] += 1
            logger.debug(f"Cache miss for key: {key}")
            return None

        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Установить значение в кэш"""
        try:
            ttl = ttl or self.default_ttl
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)

            # Очищаем старые элементы если достигли лимита
            if len(self.memory_cache) >= self.max_memory_items:
                await self._evict_oldest()

            self.memory_cache[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": datetime.now(timezone.utc),
            }

            self.cache_stats["sets"] += 1
            logger.debug(f"Cache set for key: {key}, TTL: {ttl}s")
            return True

        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Удалить значение из кэша"""
        try:
            if key in self.memory_cache:
                del self.memory_cache[key]
                self.cache_stats["deletes"] += 1
                logger.debug(f"Cache delete for key: {key}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """Удалить все ключи по паттерну"""
        try:
            deleted_count = 0
            keys_to_delete = [key for key in self.memory_cache.keys() if pattern in key]

            for key in keys_to_delete:
                del self.memory_cache[key]
                deleted_count += 1

            self.cache_stats["deletes"] += deleted_count
            logger.debug(f"Cache delete pattern '{pattern}': {deleted_count} items")
            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting pattern from cache: {e}")
            return 0

    async def clear(self) -> bool:
        """Очистить весь кэш"""
        try:
            self.memory_cache.clear()
            logger.info("Cache cleared")
            return True

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """Получить статистику кэша"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (
            (self.cache_stats["hits"] / total_requests * 100)
            if total_requests > 0
            else 0
        )

        return {
            **self.cache_stats,
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
            "memory_items": len(self.memory_cache),
            "memory_usage_mb": self._get_memory_usage(),
        }

    def _get_memory_usage(self) -> float:
        """Получить использование памяти в МБ"""
        try:
            import sys

            total_size = 0
            for item in self.memory_cache.values():
                total_size += sys.getsizeof(item)
            return round(total_size / 1024 / 1024, 2)
        except:
            return 0.0

    async def _evict_oldest(self):
        """Удалить самые старые элементы"""
        try:
            if not self.memory_cache:
                return

            # Сортируем по времени создания и удаляем 20% самых старых
            sorted_items = sorted(
                self.memory_cache.items(), key=lambda x: x[1]["created_at"]
            )

            items_to_remove = len(sorted_items) // 5  # 20%
            for key, _ in sorted_items[:items_to_remove]:
                del self.memory_cache[key]

            logger.info(f"Evicted {items_to_remove} oldest cache items")

        except Exception as e:
            logger.error(f"Error evicting oldest items: {e}")

    async def _cleanup_expired(self):
        """Очистка истекших элементов (запускается в фоне)"""
        while True:
            try:
                await asyncio.sleep(300)  # Каждые 5 минут

                current_time = datetime.now(timezone.utc)
                expired_keys = []

                for key, item in self.memory_cache.items():
                    if item["expires_at"] and current_time > item["expires_at"]:
                        expired_keys.append(key)

                for key in expired_keys:
                    del self.memory_cache[key]
                    self.cache_stats["expired"] += 1

                if expired_keys:
                    logger.info(f"Cleaned up {len(expired_keys)} expired cache items")

            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")

    def generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Генерировать ключ кэша на основе аргументов"""
        try:
            # Создаем строку из аргументов
            key_parts = [prefix]

            # Добавляем позиционные аргументы
            for arg in args:
                if isinstance(arg, (dict, list)):
                    key_parts.append(json.dumps(arg, sort_keys=True))
                else:
                    key_parts.append(str(arg))

            # Добавляем именованные аргументы
            if kwargs:
                sorted_kwargs = sorted(kwargs.items())
                key_parts.append(json.dumps(sorted_kwargs, sort_keys=True))

            # Создаем хэш
            key_string = "|".join(key_parts)
            return hashlib.md5(key_string.encode()).hexdigest()

        except Exception as e:
            logger.error(f"Error generating cache key: {e}")
            return f"{prefix}_{hash(str(args) + str(kwargs))}"


def cache_result(ttl: int = 3600, key_prefix: str = ""):
    """Декоратор для кэширования результатов функций"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Генерируем ключ кэша
            cache_key = cache_service.generate_cache_key(
                key_prefix or func.__name__, *args, **kwargs
            )

            # Пытаемся получить из кэша
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for function {func.__name__}")
                return cached_result

            # Выполняем функцию и кэшируем результат
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, ttl)
            logger.debug(f"Cached result for function {func.__name__}")

            return result

        return wrapper

    return decorator


# Создаем глобальный экземпляр сервиса
cache_service = CacheService()
