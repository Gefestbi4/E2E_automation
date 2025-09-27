from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.ecommerce as ecommerce_models
import models
from typing import List

router = APIRouter()


# Products endpoints
@router.get("/api/ecommerce/products")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список товаров"""
    products = (
        db.query(ecommerce_models.Product)
        .filter(ecommerce_models.Product.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return products


@router.get("/api/ecommerce/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID"""
    product = (
        db.query(ecommerce_models.Product)
        .filter(ecommerce_models.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/api/ecommerce/products")
def create_product(
    product_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый товар"""
    product = ecommerce_models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# Cart endpoints
@router.get("/api/ecommerce/cart")
def get_cart(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить корзину пользователя"""
    cart_items = (
        db.query(ecommerce_models.CartItem)
        .filter(ecommerce_models.CartItem.user_id == current_user.id)
        .all()
    )
    return cart_items


@router.post("/api/ecommerce/cart")
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Добавить товар в корзину"""
    # Проверяем, есть ли уже такой товар в корзине
    existing_item = (
        db.query(ecommerce_models.CartItem)
        .filter(
            ecommerce_models.CartItem.user_id == current_user.id,
            ecommerce_models.CartItem.product_id == product_id,
        )
        .first()
    )

    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = ecommerce_models.CartItem(
            user_id=current_user.id, product_id=product_id, quantity=quantity
        )
        db.add(cart_item)

    db.commit()
    return {"message": "Product added to cart"}


# Orders endpoints
@router.get("/api/ecommerce/orders")
def get_orders(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить заказы пользователя"""
    orders = (
        db.query(ecommerce_models.Order)
        .filter(ecommerce_models.Order.user_id == current_user.id)
        .all()
    )
    return orders


@router.post("/api/ecommerce/orders")
def create_order(
    order_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый заказ"""
    order = ecommerce_models.Order(
        user_id=current_user.id,
        total_amount=order_data.get("total_amount", 0),
        status="pending",
        shipping_address=order_data.get("shipping_address"),
        payment_method=order_data.get("payment_method"),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
