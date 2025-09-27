"""
Утилиты для работы с базой данных
"""

from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class DatabaseUtils:
    """Утилиты для работы с базой данных"""

    @staticmethod
    def safe_commit(db: Session) -> bool:
        """Безопасное сохранение изменений в БД"""
        try:
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database commit error: {e}")
            return False

    @staticmethod
    def safe_refresh(db: Session, instance: Any) -> bool:
        """Безопасное обновление объекта из БД"""
        try:
            db.refresh(instance)
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database refresh error: {e}")
            return False

    @staticmethod
    def safe_delete(db: Session, instance: Any) -> bool:
        """Безопасное удаление объекта из БД"""
        try:
            db.delete(instance)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database delete error: {e}")
            return False


class QueryBuilder:
    """Построитель запросов"""

    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
        self.query = db.query(model)

    def filter_by(self, **filters) -> "QueryBuilder":
        """Добавить фильтры к запросу"""
        for key, value in filters.items():
            if value is not None:
                if hasattr(self.model, key):
                    self.query = self.query.filter(getattr(self.model, key) == value)
        return self

    def filter_like(self, field: str, value: str) -> "QueryBuilder":
        """Добавить LIKE фильтр"""
        if value and hasattr(self.model, field):
            self.query = self.query.filter(
                getattr(self.model, field).ilike(f"%{value}%")
            )
        return self

    def filter_range(
        self, field: str, min_value: Any = None, max_value: Any = None
    ) -> "QueryBuilder":
        """Добавить диапазонный фильтр"""
        if hasattr(self.model, field):
            if min_value is not None:
                self.query = self.query.filter(getattr(self.model, field) >= min_value)
            if max_value is not None:
                self.query = self.query.filter(getattr(self.model, field) <= max_value)
        return self

    def filter_in(self, field: str, values: List[Any]) -> "QueryBuilder":
        """Добавить IN фильтр"""
        if values and hasattr(self.model, field):
            self.query = self.query.filter(getattr(self.model, field).in_(values))
        return self

    def order_by(self, field: str, desc: bool = False) -> "QueryBuilder":
        """Добавить сортировку"""
        if hasattr(self.model, field):
            order_field = getattr(self.model, field)
            if desc:
                order_field = order_field.desc()
            self.query = self.query.order_by(order_field)
        return self

    def paginate(self, skip: int = 0, limit: int = 20) -> "QueryBuilder":
        """Добавить пагинацию"""
        self.query = self.query.offset(skip).limit(limit)
        return self

    def execute(self) -> List[T]:
        """Выполнить запрос"""
        return self.query.all()

    def first(self) -> Optional[T]:
        """Получить первый результат"""
        return self.query.first()

    def count(self) -> int:
        """Получить количество результатов"""
        return self.query.count()


class CRUDBase:
    """Базовый CRUD класс"""

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, **kwargs) -> T:
        """Создать объект"""
        instance = self.model(**kwargs)
        db.add(instance)
        DatabaseUtils.safe_commit(db)
        DatabaseUtils.safe_refresh(db, instance)
        return instance

    def get(self, db: Session, id: int) -> Optional[T]:
        """Получить объект по ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[T]:
        """Получить список объектов"""
        query = db.query(self.model)

        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, **kwargs) -> Optional[T]:
        """Обновить объект"""
        instance = self.get(db, id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            DatabaseUtils.safe_commit(db)
            DatabaseUtils.safe_refresh(db, instance)
        return instance

    def delete(self, db: Session, id: int) -> bool:
        """Удалить объект"""
        instance = self.get(db, id)
        if instance:
            return DatabaseUtils.safe_delete(db, instance)
        return False

    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Получить количество объектов"""
        query = db.query(self.model)

        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        return query.count()


class PaginationHelper:
    """Помощник для пагинации"""

    @staticmethod
    def paginate_query(
        query: Query, skip: int = 0, limit: int = 20, max_limit: int = 100
    ) -> Dict[str, Any]:
        """Пагинация запроса"""
        # Ограничиваем максимальный лимит
        limit = min(limit, max_limit)

        # Получаем общее количество
        total = query.count()

        # Применяем пагинацию
        items = query.offset(skip).limit(limit).all()

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_next": skip + limit < total,
            "has_prev": skip > 0,
            "pages": (total + limit - 1) // limit if limit > 0 else 0,
            "current_page": (skip // limit) + 1 if limit > 0 else 1,
        }

    @staticmethod
    def create_pagination_response(
        items: List[Any],
        total: int,
        skip: int,
        limit: int,
        schema_class: Type[BaseModel],
    ) -> Dict[str, Any]:
        """Создать ответ с пагинацией"""
        return {
            "items": [schema_class.from_orm(item) for item in items],
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_next": skip + limit < total,
            "has_prev": skip > 0,
            "pages": (total + limit - 1) // limit if limit > 0 else 0,
            "current_page": (skip // limit) + 1 if limit > 0 else 1,
        }


class SearchHelper:
    """Помощник для поиска"""

    @staticmethod
    def add_search_filters(
        query: Query, model: Type[T], search_term: str, search_fields: List[str]
    ) -> Query:
        """Добавить фильтры поиска"""
        if not search_term or not search_fields:
            return query

        from sqlalchemy import or_

        search_conditions = []
        for field in search_fields:
            if hasattr(model, field):
                search_conditions.append(
                    getattr(model, field).ilike(f"%{search_term}%")
                )

        if search_conditions:
            query = query.filter(or_(*search_conditions))

        return query

    @staticmethod
    def add_date_range_filters(
        query: Query,
        model: Type[T],
        date_field: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Query:
        """Добавить фильтры по дате"""
        if not hasattr(model, date_field):
            return query

        field = getattr(model, date_field)

        if date_from:
            query = query.filter(field >= date_from)

        if date_to:
            query = query.filter(field <= date_to)

        return query
