# Schemas package
from .base import BaseSchema, TimestampMixin
from .auth import *
from .ecommerce import *
from .social import *
from .tasks import *
from .content import *
from .analytics import *

__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampMixin",
    # Auth schemas
    "UserBase",
    "UserRegistration",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "ChangePassword",
    "EmailVerification",
    "Token",
    "RefreshToken",
    "TokenData",
    # E-commerce schemas
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "CartItemCreate",
    "CartItemUpdate",
    "CartItemResponse",
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderItemResponse",
    # Social schemas
    "PostCreate",
    "PostUpdate",
    "PostResponse",
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    "PostLikeResponse",
    "FollowCreate",
    "FollowResponse",
    # Tasks schemas
    "BoardCreate",
    "BoardUpdate",
    "BoardResponse",
    "CardCreate",
    "CardUpdate",
    "CardResponse",
    "CardCommentCreate",
    "CardCommentResponse",
    # Content schemas
    "ArticleCreate",
    "ArticleUpdate",
    "ArticleResponse",
    "CategoryCreate",
    "CategoryResponse",
    # Analytics schemas
    "DashboardCreate",
    "DashboardUpdate",
    "DashboardResponse",
    "ReportCreate",
    "ReportResponse",
    "MetricResponse",
]
