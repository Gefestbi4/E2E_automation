"""
Тесты для Pydantic схем
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas import (
    # Auth schemas
    UserRegistration,
    UserLogin,
    UserResponse,
    UserUpdate,
    ChangePassword,
    # E-commerce schemas
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    CartItemCreate,
    OrderCreate,
    # Social schemas
    PostCreate,
    PostUpdate,
    PostResponse,
    CommentCreate,
    # Tasks schemas
    BoardCreate,
    BoardUpdate,
    CardCreate,
    CardUpdate,
    # Content schemas
    ArticleCreate,
    ArticleUpdate,
    CategoryCreate,
    # Analytics schemas
    DashboardCreate,
    ReportCreate,
)


class TestAuthSchemas:
    """Тесты схем аутентификации"""

    def test_user_registration_valid(self):
        """Тест валидной регистрации пользователя"""
        data = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "full_name": "Test User",
        }
        user = UserRegistration(**data)
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_registration_password_mismatch(self):
        """Тест несовпадения паролей"""
        data = {
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "different123",
            "full_name": "Test User",
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegistration(**data)
        assert "Пароли не совпадают" in str(exc_info.value)

    def test_user_registration_short_password(self):
        """Тест короткого пароля"""
        data = {
            "email": "test@example.com",
            "password": "123",
            "confirm_password": "123",
            "full_name": "Test User",
        }
        with pytest.raises(ValidationError) as exc_info:
            UserRegistration(**data)
        assert "should have at least 8 characters" in str(exc_info.value)

    def test_user_login_valid(self):
        """Тест валидного входа"""
        data = {"email": "test@example.com", "password": "password123"}
        login = UserLogin(**data)
        assert login.email == "test@example.com"
        assert login.password == "password123"


class TestEcommerceSchemas:
    """Тесты схем e-commerce"""

    def test_product_create_valid(self):
        """Тест создания товара"""
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "category": "Electronics",
            "image_url": "https://example.com/image.jpg",
            "stock_quantity": 10,
        }
        product = ProductCreate(**data)
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.stock_quantity == 10

    def test_product_create_negative_price(self):
        """Тест отрицательной цены"""
        data = {"name": "Test Product", "price": -10.0, "category": "Electronics"}
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(**data)
        assert "greater than 0" in str(exc_info.value)

    def test_cart_item_create_valid(self):
        """Тест добавления в корзину"""
        data = {"product_id": 1, "quantity": 2}
        cart_item = CartItemCreate(**data)
        assert cart_item.product_id == 1
        assert cart_item.quantity == 2

    def test_order_create_valid(self):
        """Тест создания заказа"""
        data = {
            "shipping_address": "123 Main St, City, Country",
            "payment_method": "card",
        }
        order = OrderCreate(**data)
        assert order.shipping_address == "123 Main St, City, Country"
        assert order.payment_method == "card"

    def test_order_create_invalid_payment_method(self):
        """Тест недопустимого способа оплаты"""
        data = {
            "shipping_address": "123 Main St, City, Country",
            "payment_method": "invalid_method",
        }
        with pytest.raises(ValidationError) as exc_info:
            OrderCreate(**data)
        assert "Способ оплаты должен быть одним из" in str(exc_info.value)


class TestSocialSchemas:
    """Тесты схем социальной сети"""

    def test_post_create_valid(self):
        """Тест создания поста"""
        data = {
            "content": "This is a test post",
            "image_url": "https://example.com/image.jpg",
            "is_public": True,
        }
        post = PostCreate(**data)
        assert post.content == "This is a test post"
        assert post.is_public is True

    def test_post_create_empty_content(self):
        """Тест пустого контента"""
        data = {"content": "", "is_public": True}
        with pytest.raises(ValidationError) as exc_info:
            PostCreate(**data)
        assert "at least 1 character" in str(exc_info.value)

    def test_comment_create_valid(self):
        """Тест создания комментария"""
        data = {"post_id": 1, "content": "This is a comment"}
        comment = CommentCreate(**data)
        assert comment.post_id == 1
        assert comment.content == "This is a comment"


class TestTasksSchemas:
    """Тесты схем управления задачами"""

    def test_board_create_valid(self):
        """Тест создания доски"""
        data = {
            "name": "Test Board",
            "description": "Test Description",
            "is_public": False,
        }
        board = BoardCreate(**data)
        assert board.name == "Test Board"
        assert board.is_public is False

    def test_card_create_valid(self):
        """Тест создания карточки"""
        data = {
            "board_id": 1,
            "title": "Test Card",
            "description": "Test Description",
            "priority": "high",
            "status": "todo",
        }
        card = CardCreate(**data)
        assert card.title == "Test Card"
        assert card.priority == "high"
        assert card.status == "todo"

    def test_card_create_invalid_priority(self):
        """Тест недопустимого приоритета"""
        data = {"board_id": 1, "title": "Test Card", "priority": "invalid_priority"}
        with pytest.raises(ValidationError) as exc_info:
            CardCreate(**data)
        assert "Приоритет должен быть одним из" in str(exc_info.value)

    def test_card_create_invalid_status(self):
        """Тест недопустимого статуса"""
        data = {"board_id": 1, "title": "Test Card", "status": "invalid_status"}
        with pytest.raises(ValidationError) as exc_info:
            CardCreate(**data)
        assert "Статус должен быть одним из" in str(exc_info.value)


class TestContentSchemas:
    """Тесты схем управления контентом"""

    def test_article_create_valid(self):
        """Тест создания статьи"""
        data = {
            "title": "Test Article",
            "excerpt": "Test Excerpt",
            "content": "This is the article content",
            "slug": "test-article",
            "status": "draft",
            "category_id": 1,
            "tags": ["test", "article"],
        }
        article = ArticleCreate(**data)
        assert article.title == "Test Article"
        assert article.slug == "test-article"
        assert article.tags == ["test", "article"]

    def test_article_create_invalid_status(self):
        """Тест недопустимого статуса статьи"""
        data = {
            "title": "Test Article",
            "content": "This is the article content",
            "slug": "test-article",
            "status": "invalid_status",
        }
        with pytest.raises(ValidationError) as exc_info:
            ArticleCreate(**data)
        assert "should be 'draft', 'published' or 'archived'" in str(exc_info.value)

    def test_category_create_valid(self):
        """Тест создания категории"""
        data = {
            "name": "Test Category",
            "description": "Test Description",
            "slug": "test-category",
        }
        category = CategoryCreate(**data)
        assert category.name == "Test Category"
        assert category.slug == "test-category"


class TestAnalyticsSchemas:
    """Тесты схем аналитики"""

    def test_dashboard_create_valid(self):
        """Тест создания дашборда"""
        data = {
            "name": "Test Dashboard",
            "description": "Test Description",
            "is_public": False,
            "is_default": False,
        }
        dashboard = DashboardCreate(**data)
        assert dashboard.name == "Test Dashboard"
        assert dashboard.is_public is False

    def test_report_create_valid(self):
        """Тест создания отчета"""
        data = {
            "name": "Test Report",
            "description": "Test Description",
            "type": "sales",
            "parameters": {"period": "monthly"},
            "schedule": "daily",
        }
        report = ReportCreate(**data)
        assert report.name == "Test Report"
        assert report.type == "sales"
        assert report.parameters == {"period": "monthly"}


class TestValidationUtils:
    """Тесты утилит валидации"""

    def test_email_validation(self):
        """Тест валидации email"""
        from utils.validation import ValidationUtils

        assert ValidationUtils.validate_email("test@example.com") is True
        assert ValidationUtils.validate_email("invalid-email") is False
        assert ValidationUtils.validate_email("") is False

    def test_password_strength_validation(self):
        """Тест валидации силы пароля"""
        from utils.validation import ValidationUtils

        # Слабый пароль
        result = ValidationUtils.validate_password_strength("123")
        assert result["is_valid"] is False
        assert "Пароль должен содержать минимум 8 символов" in result["feedback"]

        # Сильный пароль
        result = ValidationUtils.validate_password_strength("Password123!")
        assert result["is_valid"] is True
        assert result["score"] >= 3

    def test_username_validation(self):
        """Тест валидации имени пользователя"""
        from utils.validation import ValidationUtils

        assert ValidationUtils.validate_username("testuser") is True
        assert ValidationUtils.validate_username("test_user123") is True
        assert ValidationUtils.validate_username("ab") is False  # Слишком короткий
        assert (
            ValidationUtils.validate_username("test@user") is False
        )  # Недопустимые символы


if __name__ == "__main__":
    pytest.main([__file__])
