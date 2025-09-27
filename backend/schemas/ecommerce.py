"""
Схемы для E-commerce модуля
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from .base import BaseSchema, TimestampMixin
from .auth import UserResponse


class ProductBase(BaseSchema):
    """Базовая схема товара"""

    name: str = Field(..., min_length=1, max_length=255, description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: float = Field(..., gt=0, description="Цена товара")
    category: str = Field(
        ..., min_length=1, max_length=100, description="Категория товара"
    )
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL изображения"
    )
    stock_quantity: int = Field(0, ge=0, description="Количество на складе")


class ProductCreate(ProductBase):
    """Схема создания товара"""

    pass


class ProductUpdate(BaseSchema):
    """Схема обновления товара"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Название товара"
    )
    description: Optional[str] = Field(None, description="Описание товара")
    price: Optional[float] = Field(None, gt=0, description="Цена товара")
    category: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Категория товара"
    )
    image_url: Optional[str] = Field(
        None, max_length=500, description="URL изображения"
    )
    stock_quantity: Optional[int] = Field(
        None, ge=0, description="Количество на складе"
    )
    is_active: Optional[bool] = Field(None, description="Активен ли товар")


class ProductResponse(ProductBase, TimestampMixin):
    """Схема ответа с данными товара"""

    id: int = Field(..., description="ID товара")
    is_active: bool = Field(..., description="Активен ли товар")

    model_config = {"from_attributes": True}


class ProductListResponse(BaseSchema):
    """Схема ответа со списком товаров"""

    items: List[ProductResponse] = Field(..., description="Список товаров")
    total: int = Field(..., description="Общее количество товаров")
    skip: int = Field(..., description="Количество пропущенных товаров")
    limit: int = Field(..., description="Лимит товаров")


class CartItemCreate(BaseSchema):
    """Схема добавления товара в корзину"""

    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(1, gt=0, description="Количество товара")


class CartItemUpdate(BaseSchema):
    """Схема обновления товара в корзине"""

    quantity: int = Field(..., gt=0, description="Количество товара")


class CartItemResponse(BaseSchema, TimestampMixin):
    """Схема ответа с данными товара в корзине"""

    id: int = Field(..., description="ID записи в корзине")
    product: ProductResponse = Field(..., description="Данные товара")
    quantity: int = Field(..., description="Количество товара")
    total_price: float = Field(..., description="Общая цена товара")


class CartResponse(BaseSchema):
    """Схема ответа с корзиной"""

    items: List[CartItemResponse] = Field(..., description="Товары в корзине")
    total_items: int = Field(..., description="Общее количество товаров")
    total_amount: float = Field(..., description="Общая сумма корзины")


class OrderItemResponse(BaseSchema, TimestampMixin):
    """Схема ответа с данными товара в заказе"""

    id: int = Field(..., description="ID записи в заказе")
    product: ProductResponse = Field(..., description="Данные товара")
    quantity: int = Field(..., description="Количество товара")
    price: float = Field(..., description="Цена товара на момент заказа")
    total_price: float = Field(..., description="Общая цена товара")


class OrderCreate(BaseSchema):
    """Схема создания заказа"""

    shipping_address: str = Field(
        ..., min_length=10, max_length=500, description="Адрес доставки"
    )
    payment_method: str = Field(
        ..., min_length=1, max_length=100, description="Способ оплаты"
    )

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, v):
        allowed_methods = ["card", "cash", "bank_transfer", "paypal"]
        if v.lower() not in allowed_methods:
            raise ValueError(
                f"Способ оплаты должен быть одним из: {', '.join(allowed_methods)}"
            )
        return v.lower()


class OrderUpdate(BaseSchema):
    """Схема обновления заказа"""

    status: Optional[str] = Field(None, description="Статус заказа")
    shipping_address: Optional[str] = Field(
        None, min_length=10, max_length=500, description="Адрес доставки"
    )
    payment_method: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Способ оплаты"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v:
            allowed_statuses = [
                "pending",
                "confirmed",
                "shipped",
                "delivered",
                "cancelled",
            ]
            if v.lower() not in allowed_statuses:
                raise ValueError(
                    f"Статус должен быть одним из: {', '.join(allowed_statuses)}"
                )
            return v.lower()
        return v


class OrderResponse(BaseSchema, TimestampMixin):
    """Схема ответа с данными заказа"""

    id: int = Field(..., description="ID заказа")
    user: UserResponse = Field(..., description="Данные пользователя")
    total_amount: float = Field(..., description="Общая сумма заказа")
    status: str = Field(..., description="Статус заказа")
    shipping_address: str = Field(..., description="Адрес доставки")
    payment_method: str = Field(..., description="Способ оплаты")
    order_items: List[OrderItemResponse] = Field(..., description="Товары в заказе")


class OrderListResponse(BaseSchema):
    """Схема ответа со списком заказов"""

    items: List[OrderResponse] = Field(..., description="Список заказов")
    total: int = Field(..., description="Общее количество заказов")
    skip: int = Field(..., description="Количество пропущенных заказов")
    limit: int = Field(..., description="Лимит заказов")


class ProductFilters(BaseSchema):
    """Схема фильтров для товаров"""

    category: Optional[str] = Field(None, description="Фильтр по категории")
    min_price: Optional[float] = Field(None, ge=0, description="Минимальная цена")
    max_price: Optional[float] = Field(None, ge=0, description="Максимальная цена")
    in_stock: Optional[bool] = Field(None, description="Только в наличии")
    search: Optional[str] = Field(None, min_length=1, description="Поисковый запрос")

    @field_validator("max_price")
    @classmethod
    def validate_price_range(cls, v, info):
        if (
            v
            and "min_price" in info.data
            and info.data["min_price"]
            and v < info.data["min_price"]
        ):
            raise ValueError("Максимальная цена не может быть меньше минимальной")
        return v
