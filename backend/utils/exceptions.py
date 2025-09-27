"""
Кастомные исключения для приложения
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class BaseAPIException(HTTPException):
    """Базовое исключение API"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        field: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.field = field
        self.metadata = metadata or {}


class ValidationError(BaseAPIException):
    """Ошибка валидации данных"""

    def __init__(
        self, detail: str, field: Optional[str] = None, errors: Optional[list] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
            field=field,
            metadata={"errors": errors or []},
        )


class AuthenticationError(BaseAPIException):
    """Ошибка аутентификации"""

    def __init__(self, detail: str = "Ошибка аутентификации"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR",
        )


class AuthorizationError(BaseAPIException):
    """Ошибка авторизации"""

    def __init__(self, detail: str = "Недостаточно прав доступа"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_ERROR",
        )


class NotFoundError(BaseAPIException):
    """Ошибка - ресурс не найден"""

    def __init__(self, resource: str = "Ресурс", resource_id: Optional[str] = None):
        detail = f"{resource} не найден"
        if resource_id:
            detail += f" (ID: {resource_id})"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail, error_code="NOT_FOUND"
        )


class ConflictError(BaseAPIException):
    """Ошибка конфликта данных"""

    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT_ERROR",
            field=field,
        )


class BusinessLogicError(BaseAPIException):
    """Ошибка бизнес-логики"""

    def __init__(self, detail: str, error_code: str = "BUSINESS_LOGIC_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )


class RateLimitError(BaseAPIException):
    """Ошибка превышения лимита запросов"""

    def __init__(
        self, detail: str = "Превышен лимит запросов", retry_after: Optional[int] = None
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_ERROR",
            metadata={"retry_after": retry_after},
        )


class ExternalServiceError(BaseAPIException):
    """Ошибка внешнего сервиса"""

    def __init__(self, service: str, detail: str = "Ошибка внешнего сервиса"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"{service}: {detail}",
            error_code="EXTERNAL_SERVICE_ERROR",
            metadata={"service": service},
        )


class DatabaseError(BaseAPIException):
    """Ошибка базы данных"""

    def __init__(self, detail: str = "Ошибка базы данных"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR",
        )


class FileUploadError(BaseAPIException):
    """Ошибка загрузки файла"""

    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FILE_UPLOAD_ERROR",
            field=field,
        )


class EmailError(BaseAPIException):
    """Ошибка отправки email"""

    def __init__(self, detail: str = "Ошибка отправки email"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="EMAIL_ERROR",
        )


# Специфичные исключения для модулей


class UserNotFoundError(NotFoundError):
    """Пользователь не найден"""

    def __init__(self, user_id: Optional[str] = None):
        super().__init__("Пользователь", user_id)


class UserAlreadyExistsError(ConflictError):
    """Пользователь уже существует"""

    def __init__(self, field: str = "email"):
        super().__init__(f"Пользователь с таким {field} уже существует", field=field)


class ProductNotFoundError(NotFoundError):
    """Товар не найден"""

    def __init__(self, product_id: Optional[str] = None):
        super().__init__("Товар", product_id)


class InsufficientStockError(BusinessLogicError):
    """Недостаточно товара на складе"""

    def __init__(self, product_name: str, available: int, requested: int):
        super().__init__(
            f"Недостаточно товара '{product_name}'. Доступно: {available}, запрошено: {requested}",
            "INSUFFICIENT_STOCK",
        )


class CartEmptyError(BusinessLogicError):
    """Корзина пуста"""

    def __init__(self):
        super().__init__("Корзина пуста", "CART_EMPTY")


class PostNotFoundError(NotFoundError):
    """Пост не найден"""

    def __init__(self, post_id: Optional[str] = None):
        super().__init__("Пост", post_id)


class BoardNotFoundError(NotFoundError):
    """Доска не найдена"""

    def __init__(self, board_id: Optional[str] = None):
        super().__init__("Доска", board_id)


class CardNotFoundError(NotFoundError):
    """Карточка не найдена"""

    def __init__(self, card_id: Optional[str] = None):
        super().__init__("Карточка", card_id)


class ArticleNotFoundError(NotFoundError):
    """Статья не найдена"""

    def __init__(self, article_id: Optional[str] = None):
        super().__init__("Статья", article_id)


class CategoryNotFoundError(NotFoundError):
    """Категория не найдена"""

    def __init__(self, category_id: Optional[str] = None):
        super().__init__("Категория", category_id)


class DashboardNotFoundError(NotFoundError):
    """Дашборд не найден"""

    def __init__(self, dashboard_id: Optional[str] = None):
        super().__init__("Дашборд", dashboard_id)


class ReportNotFoundError(NotFoundError):
    """Отчет не найден"""

    def __init__(self, report_id: Optional[str] = None):
        super().__init__("Отчет", report_id)


class AlertNotFoundError(NotFoundError):
    """Алерт не найден"""

    def __init__(self, alert_id: Optional[str] = None):
        super().__init__("Алерт", alert_id)


class MetricNotFoundError(NotFoundError):
    """Метрика не найдена"""

    def __init__(self, metric_id: Optional[str] = None):
        super().__init__("Метрика", metric_id)
