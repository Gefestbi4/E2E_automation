# Utils package
from .validation import (
    ValidationUtils,
    PaginationValidator,
    DataValidator,
    validate_and_raise,
)
from .exceptions import *
from .database import (
    DatabaseUtils,
    QueryBuilder,
    CRUDBase,
    PaginationHelper,
    SearchHelper,
)
from .logging import (
    LoggerSetup,
    RequestLogger,
    DatabaseLogger,
    BusinessLogicLogger,
    SecurityLogger,
    get_logger,
    setup_app_logging,
)

__all__ = [
    # Validation
    "ValidationUtils",
    "PaginationValidator",
    "DataValidator",
    "validate_and_raise",
    # Exceptions
    "BaseAPIException",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "BusinessLogicError",
    "RateLimitError",
    "ExternalServiceError",
    "DatabaseError",
    "FileUploadError",
    "EmailError",
    # Module-specific exceptions
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "ProductNotFoundError",
    "InsufficientStockError",
    "CartEmptyError",
    "PostNotFoundError",
    "BoardNotFoundError",
    "CardNotFoundError",
    "ArticleNotFoundError",
    "CategoryNotFoundError",
    "DashboardNotFoundError",
    "ReportNotFoundError",
    "AlertNotFoundError",
    "MetricNotFoundError",
    # Database
    "DatabaseUtils",
    "QueryBuilder",
    "CRUDBase",
    "PaginationHelper",
    "SearchHelper",
    # Logging
    "LoggerSetup",
    "RequestLogger",
    "DatabaseLogger",
    "BusinessLogicLogger",
    "SecurityLogger",
    "get_logger",
    "setup_app_logging",
]
