"""
Сервис для E-commerce модуля
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

import models_package.ecommerce as ecommerce_models
from models import User
from schemas.ecommerce import (
    ProductCreate,
    ProductUpdate,
    ProductFilters,
    CartItemCreate,
    OrderCreate,
    OrderUpdate,
)
from utils.database import QueryBuilder, PaginationHelper, SearchHelper
from utils.exceptions import (
    ProductNotFoundError,
    InsufficientStockError,
    CartEmptyError,
    BusinessLogicError,
)


class EcommerceService:
    """Сервис для работы с e-commerce данными"""

    def __init__(self, db: Session):
        self.db = db

    # Products methods
    def get_products(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[ProductFilters] = None,
    ) -> Dict[str, Any]:
        """Получить список товаров с фильтрацией"""
        query = self.db.query(ecommerce_models.Product).filter(
            ecommerce_models.Product.is_active == True
        )

        if filters:
            # Фильтр по категории
            if filters.category:
                query = query.filter(
                    ecommerce_models.Product.category == filters.category
                )

            # Фильтр по цене
            if filters.min_price is not None:
                query = query.filter(
                    ecommerce_models.Product.price >= filters.min_price
                )
            if filters.max_price is not None:
                query = query.filter(
                    ecommerce_models.Product.price <= filters.max_price
                )

            # Фильтр по наличию
            if filters.in_stock:
                query = query.filter(ecommerce_models.Product.stock_quantity > 0)

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    ecommerce_models.Product,
                    filters.search,
                    ["name", "description"],
                )

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(ecommerce_models.Product.created_at.desc())

        return PaginationHelper.paginate_query(query, skip, limit)

    def get_product(self, product_id: int) -> ecommerce_models.Product:
        """Получить товар по ID"""
        product = (
            self.db.query(ecommerce_models.Product)
            .filter(
                and_(
                    ecommerce_models.Product.id == product_id,
                    ecommerce_models.Product.is_active == True,
                )
            )
            .first()
        )

        if not product:
            raise ProductNotFoundError(str(product_id))

        return product

    def create_product(
        self, product_data: ProductCreate, user: User
    ) -> ecommerce_models.Product:
        """Создать новый товар"""
        product = ecommerce_models.Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(
        self, product_id: int, product_data: ProductUpdate, user: User
    ) -> ecommerce_models.Product:
        """Обновить товар"""
        product = self.get_product(product_id)

        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int, user: User) -> bool:
        """Удалить товар (мягкое удаление)"""
        product = self.get_product(product_id)
        product.is_active = False
        self.db.commit()
        return True

    def get_categories(self) -> List[str]:
        """Получить список категорий"""
        categories = (
            self.db.query(ecommerce_models.Product.category)
            .filter(ecommerce_models.Product.is_active == True)
            .distinct()
            .all()
        )
        return [cat[0] for cat in categories]

    # Cart methods
    def get_cart(self, user: User) -> Dict[str, Any]:
        """Получить корзину пользователя"""
        cart_items = (
            self.db.query(ecommerce_models.CartItem)
            .filter(ecommerce_models.CartItem.user_id == user.id)
            .all()
        )

        total_items = sum(item.quantity for item in cart_items)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        return {
            "items": cart_items,
            "total_items": total_items,
            "total_amount": total_amount,
        }

    def add_to_cart(
        self, cart_item_data: CartItemCreate, user: User
    ) -> ecommerce_models.CartItem:
        """Добавить товар в корзину"""
        # Проверяем существование товара
        product = self.get_product(cart_item_data.product_id)

        # Проверяем наличие на складе
        if product.stock_quantity < cart_item_data.quantity:
            raise InsufficientStockError(
                product.name, product.stock_quantity, cart_item_data.quantity
            )

        # Проверяем, есть ли уже такой товар в корзине
        existing_item = (
            self.db.query(ecommerce_models.CartItem)
            .filter(
                and_(
                    ecommerce_models.CartItem.user_id == user.id,
                    ecommerce_models.CartItem.product_id == cart_item_data.product_id,
                )
            )
            .first()
        )

        if existing_item:
            existing_item.quantity += cart_item_data.quantity
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            new_item = ecommerce_models.CartItem(
                user_id=user.id,
                product_id=cart_item_data.product_id,
                quantity=cart_item_data.quantity,
            )
            self.db.add(new_item)
            self.db.commit()
            self.db.refresh(new_item)
            return new_item

    def update_cart_item(
        self, item_id: int, quantity: int, user: User
    ) -> Optional[ecommerce_models.CartItem]:
        """Обновить количество товара в корзине"""
        cart_item = (
            self.db.query(ecommerce_models.CartItem)
            .filter(
                and_(
                    ecommerce_models.CartItem.id == item_id,
                    ecommerce_models.CartItem.user_id == user.id,
                )
            )
            .first()
        )

        if not cart_item:
            return None

        if quantity <= 0:
            self.db.delete(cart_item)
            self.db.commit()
            return None

        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    def remove_from_cart(self, item_id: int, user: User) -> bool:
        """Удалить товар из корзины"""
        cart_item = (
            self.db.query(ecommerce_models.CartItem)
            .filter(
                and_(
                    ecommerce_models.CartItem.id == item_id,
                    ecommerce_models.CartItem.user_id == user.id,
                )
            )
            .first()
        )

        if not cart_item:
            return False

        self.db.delete(cart_item)
        self.db.commit()
        return True

    def clear_cart(self, user: User) -> bool:
        """Очистить корзину"""
        self.db.query(ecommerce_models.CartItem).filter(
            ecommerce_models.CartItem.user_id == user.id
        ).delete()
        self.db.commit()
        return True

    # Orders methods
    def get_orders(self, user: User, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Получить заказы пользователя"""
        query = self.db.query(ecommerce_models.Order).filter(
            ecommerce_models.Order.user_id == user.id
        )

        return PaginationHelper.paginate_query(query, skip, limit)

    def get_order(self, order_id: int, user: User) -> ecommerce_models.Order:
        """Получить заказ по ID"""
        order = (
            self.db.query(ecommerce_models.Order)
            .filter(
                and_(
                    ecommerce_models.Order.id == order_id,
                    ecommerce_models.Order.user_id == user.id,
                )
            )
            .first()
        )

        if not order:
            raise ProductNotFoundError(f"Order {order_id}")

        return order

    def create_order(
        self, order_data: OrderCreate, user: User
    ) -> ecommerce_models.Order:
        """Создать заказ"""
        # Получаем товары из корзины
        cart_items = (
            self.db.query(ecommerce_models.CartItem)
            .filter(ecommerce_models.CartItem.user_id == user.id)
            .all()
        )

        if not cart_items:
            raise CartEmptyError()

        # Рассчитываем общую сумму
        total_amount = 0
        for item in cart_items:
            total_amount += item.product.price * item.quantity

        # Создаем заказ
        order = ecommerce_models.Order(
            user_id=user.id,
            total_amount=total_amount,
            status="pending",
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
        )
        self.db.add(order)
        self.db.flush()  # Получаем ID заказа

        # Создаем элементы заказа
        for item in cart_items:
            order_item = ecommerce_models.OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price,
            )
            self.db.add(order_item)

        # Очищаем корзину
        self.db.query(ecommerce_models.CartItem).filter(
            ecommerce_models.CartItem.user_id == user.id
        ).delete()

        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order(
        self, order_id: int, order_data: OrderUpdate, user: User
    ) -> ecommerce_models.Order:
        """Обновить заказ"""
        order = self.get_order(order_id, user)

        update_data = order_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)

        self.db.commit()
        self.db.refresh(order)
        return order

    def cancel_order(self, order_id: int, user: User) -> ecommerce_models.Order:
        """Отменить заказ"""
        order = self.get_order(order_id, user)

        if order.status not in ["pending", "confirmed"]:
            raise BusinessLogicError(
                f"Нельзя отменить заказ со статусом {order.status}"
            )

        order.status = "cancelled"
        self.db.commit()
        self.db.refresh(order)
        return order

    # Analytics methods
    def get_sales_stats(
        self,
        user: User,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Получить статистику продаж"""
        query = self.db.query(ecommerce_models.Order).filter(
            ecommerce_models.Order.user_id == user.id
        )

        if date_from:
            query = query.filter(ecommerce_models.Order.created_at >= date_from)
        if date_to:
            query = query.filter(ecommerce_models.Order.created_at <= date_to)

        orders = query.all()

        total_orders = len(orders)
        total_revenue = sum(order.total_amount for order in orders)
        completed_orders = len([o for o in orders if o.status == "delivered"])

        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "completed_orders": completed_orders,
            "average_order_value": (
                total_revenue / total_orders if total_orders > 0 else 0
            ),
        }
