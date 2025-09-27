from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.ecommerce as ecommerce_models
import models
from typing import List, Optional

from schemas.ecommerce import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartResponse,
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    ProductFilters,
)
from services.ecommerce_service import EcommerceService
from utils.exceptions import (
    ProductNotFoundError,
    InsufficientStockError,
    CartEmptyError,
)

router = APIRouter()


# Products endpoints
@router.get("/api/ecommerce/products", response_model=ProductListResponse)
def get_products(
    skip: int = Query(0, ge=0, description="Количество пропущенных товаров"),
    limit: int = Query(20, ge=1, le=100, description="Количество товаров на странице"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    in_stock: Optional[bool] = Query(None, description="Только в наличии"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    db: Session = Depends(get_db),
):
    """Получить список товаров с фильтрацией и поиском"""
    filters = ProductFilters(
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        search=search,
    )

    service = EcommerceService(db)
    result = service.get_products(skip=skip, limit=limit, filters=filters)

    return ProductListResponse(
        items=[ProductResponse.model_validate(item) for item in result["items"]],
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/ecommerce/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID"""
    service = EcommerceService(db)
    product = service.get_product(product_id)
    return ProductResponse.model_validate(product)


@router.post("/api/ecommerce/products", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый товар"""
    service = EcommerceService(db)
    product = service.create_product(product_data, current_user)
    return ProductResponse.model_validate(product)


@router.put("/api/ecommerce/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить товар"""
    service = EcommerceService(db)
    product = service.update_product(product_id, product_data, current_user)
    return ProductResponse.model_validate(product)


@router.delete("/api/ecommerce/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить товар (мягкое удаление)"""
    service = EcommerceService(db)
    service.delete_product(product_id, current_user)
    return {"message": "Product deleted successfully"}


@router.get("/api/ecommerce/categories")
def get_categories(db: Session = Depends(get_db)):
    """Получить список категорий товаров"""
    service = EcommerceService(db)
    categories = service.get_categories()
    return {"categories": categories}


# Cart endpoints
@router.get("/api/ecommerce/cart", response_model=CartResponse)
def get_cart(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить корзину пользователя"""
    service = EcommerceService(db)
    cart_data = service.get_cart(current_user)

    cart_items = []
    for item in cart_data["items"]:
        cart_items.append(
            CartItemResponse(
                id=item.id,
                product=ProductResponse.model_validate(item.product),
                quantity=item.quantity,
                total_price=item.product.price * item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        )

    return CartResponse(
        items=cart_items,
        total_items=cart_data["total_items"],
        total_amount=cart_data["total_amount"],
    )


@router.post("/api/ecommerce/cart", response_model=CartItemResponse)
def add_to_cart(
    cart_item_data: CartItemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Добавить товар в корзину"""
    service = EcommerceService(db)
    cart_item = service.add_to_cart(cart_item_data, current_user)

    return CartItemResponse(
        id=cart_item.id,
        product=ProductResponse.model_validate(cart_item.product),
        quantity=cart_item.quantity,
        total_price=cart_item.product.price * cart_item.quantity,
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at,
    )


@router.put("/api/ecommerce/cart/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    quantity: int = Query(..., gt=0, description="Новое количество товара"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить количество товара в корзине"""
    service = EcommerceService(db)
    cart_item = service.update_cart_item(item_id, quantity, current_user)

    if not cart_item:
        return {"message": "Item removed from cart"}

    return CartItemResponse(
        id=cart_item.id,
        product=ProductResponse.model_validate(cart_item.product),
        quantity=cart_item.quantity,
        total_price=cart_item.product.price * cart_item.quantity,
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at,
    )


@router.delete("/api/ecommerce/cart/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить товар из корзины"""
    service = EcommerceService(db)
    success = service.remove_from_cart(item_id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Item removed from cart"}


@router.delete("/api/ecommerce/cart")
def clear_cart(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Очистить корзину"""
    service = EcommerceService(db)
    service.clear_cart(current_user)
    return {"message": "Cart cleared"}


# Orders endpoints
@router.get("/api/ecommerce/orders", response_model=OrderListResponse)
def get_orders(
    skip: int = Query(0, ge=0, description="Количество пропущенных заказов"),
    limit: int = Query(20, ge=1, le=100, description="Количество заказов на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить заказы пользователя"""
    service = EcommerceService(db)
    result = service.get_orders(current_user, skip=skip, limit=limit)

    orders = []
    for order in result["items"]:
        order_items = []
        for item in order.order_items:
            order_items.append(
                {
                    "id": item.id,
                    "product": ProductResponse.from_orm(item.product),
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.price * item.quantity,
                    "created_at": item.created_at,
                }
            )

        orders.append(
            OrderResponse(
                id=order.id,
                user=current_user,
                total_amount=order.total_amount,
                status=order.status,
                shipping_address=order.shipping_address,
                payment_method=order.payment_method,
                order_items=order_items,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
        )

    return OrderListResponse(
        items=orders,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/ecommerce/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить заказ по ID"""
    service = EcommerceService(db)
    order = service.get_order(order_id, current_user)

    order_items = []
    for item in order.order_items:
        order_items.append(
            {
                "id": item.id,
                "product": ProductResponse.from_orm(item.product),
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.price * item.quantity,
                "created_at": item.created_at,
            }
        )

    return OrderResponse(
        id=order.id,
        user=current_user,
        total_amount=order.total_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        order_items=order_items,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.post("/api/ecommerce/orders", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый заказ"""
    service = EcommerceService(db)
    order = service.create_order(order_data, current_user)

    order_items = []
    for item in order.order_items:
        order_items.append(
            {
                "id": item.id,
                "product": ProductResponse.from_orm(item.product),
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.price * item.quantity,
                "created_at": item.created_at,
            }
        )

    return OrderResponse(
        id=order.id,
        user=current_user,
        total_amount=order.total_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        order_items=order_items,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.put("/api/ecommerce/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить заказ"""
    service = EcommerceService(db)
    order = service.update_order(order_id, order_data, current_user)

    order_items = []
    for item in order.order_items:
        order_items.append(
            {
                "id": item.id,
                "product": ProductResponse.from_orm(item.product),
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.price * item.quantity,
                "created_at": item.created_at,
            }
        )

    return OrderResponse(
        id=order.id,
        user=current_user,
        total_amount=order.total_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        order_items=order_items,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.post("/api/ecommerce/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Отменить заказ"""
    service = EcommerceService(db)
    order = service.cancel_order(order_id, current_user)

    order_items = []
    for item in order.order_items:
        order_items.append(
            {
                "id": item.id,
                "product": ProductResponse.from_orm(item.product),
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.price * item.quantity,
                "created_at": item.created_at,
            }
        )

    return OrderResponse(
        id=order.id,
        user=current_user,
        total_amount=order.total_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        order_items=order_items,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


# Analytics endpoints
@router.get("/api/ecommerce/analytics/sales")
def get_sales_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить статистику продаж"""
    service = EcommerceService(db)
    stats = service.get_sales_stats(current_user)
    return stats
