# План модернизации Backend

## 🔍 Анализ текущего состояния

### ✅ Что уже реализовано хорошо
1. **Базовая архитектура FastAPI** - корректная структура приложения
2. **JWT аутентификация** - рабочая система токенов
3. **Модульная структура** - разделение по доменам (ecommerce, social, tasks, content, analytics)
4. **SQLAlchemy модели** - базовые модели для всех модулей
5. **CORS настройки** - корректная настройка для frontend
6. **База данных** - PostgreSQL с правильными связями

### ❌ Критические пробелы

#### 1. **Отсутствие Pydantic схем для модулей**
- Только схемы для аутентификации
- Нет валидации входных/выходных данных для модулей
- Нет типизации API responses

#### 2. **Неполные API endpoints**
- Много endpoints принимают `dict` вместо типизированных схем
- Отсутствуют endpoints для многих функций из документации
- Нет пагинации, фильтрации, поиска

#### 3. **Отсутствие бизнес-логики**
- Нет сервисного слоя
- Вся логика в роутерах
- Нет обработки сложных операций

#### 4. **Слабая обработка ошибок**
- Базовые HTTPException
- Нет кастомных исключений
- Нет логирования ошибок

#### 5. **Отсутствие дополнительных функций**
- Нет email верификации
- Нет восстановления пароля
- Нет ролей и прав доступа
- Нет rate limiting

## 🎯 План модернизации

### Фаза 1: Схемы и валидация (Критично)

#### 1.1 Создать Pydantic схемы для всех модулей
```python
# schemas/ecommerce.py
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[str] = None
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    shipping_address: str
    payment_method: str

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: str
    created_at: datetime
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
```

#### 1.2 Создать схемы для Social Network
```python
# schemas/social.py
class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None
    is_public: bool = True

class PostUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None
    is_public: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    content: str
    image_url: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    author: UserResponse
    likes_count: int
    comments_count: int
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserResponse
    
    class Config:
        from_attributes = True
```

#### 1.3 Создать схемы для Task Management
```python
# schemas/tasks.py
class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class BoardResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_public: bool
    created_at: datetime
    cards: List[CardResponse]
    
    class Config:
        from_attributes = True

class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None

class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

class CardResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    assigned_to: Optional[UserResponse]
    comments: List[CardCommentResponse]
    
    class Config:
        from_attributes = True
```

### Фаза 2: Улучшение API endpoints (Высокий приоритет)

#### 2.1 E-commerce модуль
```python
# api/ecommerce.py - улучшенные endpoints
@router.get("/api/ecommerce/products", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, 
    limit: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Получить список товаров с фильтрацией и поиском"""
    query = db.query(ecommerce_models.Product).filter(
        ecommerce_models.Product.is_active == True
    )
    
    if category:
        query = query.filter(ecommerce_models.Product.category == category)
    if search:
        query = query.filter(
            or_(
                ecommerce_models.Product.name.ilike(f"%{search}%"),
                ecommerce_models.Product.description.ilike(f"%{search}%")
            )
        )
    if min_price:
        query = query.filter(ecommerce_models.Product.price >= min_price)
    if max_price:
        query = query.filter(ecommerce_models.Product.price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.post("/api/ecommerce/products", response_model=ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новый товар"""
    db_product = ecommerce_models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/api/ecommerce/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить товар"""
    product = db.query(ecommerce_models.Product).filter(
        ecommerce_models.Product.id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/api/ecommerce/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить товар (мягкое удаление)"""
    product = db.query(ecommerce_models.Product).filter(
        ecommerce_models.Product.id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/api/ecommerce/cart", response_model=List[CartItemResponse])
def get_cart(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить корзину пользователя"""
    cart_items = (
        db.query(ecommerce_models.CartItem)
        .filter(ecommerce_models.CartItem.user_id == current_user.id)
        .all()
    )
    return cart_items

@router.post("/api/ecommerce/cart", response_model=CartItemResponse)
def add_to_cart(
    cart_item: schemas.CartItemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Добавить товар в корзину"""
    # Проверяем существование товара
    product = db.query(ecommerce_models.Product).filter(
        ecommerce_models.Product.id == cart_item.product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Проверяем наличие на складе
    if product.stock_quantity < cart_item.quantity:
        raise HTTPException(
            status_code=400, 
            detail="Not enough stock available"
        )
    
    # Проверяем, есть ли уже такой товар в корзине
    existing_item = (
        db.query(ecommerce_models.CartItem)
        .filter(
            ecommerce_models.CartItem.user_id == current_user.id,
            ecommerce_models.CartItem.product_id == cart_item.product_id,
        )
        .first()
    )
    
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        new_item = ecommerce_models.CartItem(
            user_id=current_user.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@router.put("/api/ecommerce/cart/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновить количество товара в корзине"""
    cart_item = (
        db.query(ecommerce_models.CartItem)
        .filter(
            ecommerce_models.CartItem.id == item_id,
            ecommerce_models.CartItem.user_id == current_user.id
        )
        .first()
    )
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return {"message": "Item removed from cart"}
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/api/ecommerce/cart/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удалить товар из корзины"""
    cart_item = (
        db.query(ecommerce_models.CartItem)
        .filter(
            ecommerce_models.CartItem.id == item_id,
            ecommerce_models.CartItem.user_id == current_user.id
        )
        .first()
    )
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.post("/api/ecommerce/checkout", response_model=OrderResponse)
def checkout(
    order_data: schemas.OrderCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Оформить заказ"""
    # Получаем товары из корзины
    cart_items = (
        db.query(ecommerce_models.CartItem)
        .filter(ecommerce_models.CartItem.user_id == current_user.id)
        .all()
    )
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Рассчитываем общую сумму
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    
    # Создаем заказ
    order = ecommerce_models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending",
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method
    )
    db.add(order)
    db.flush()  # Получаем ID заказа
    
    # Создаем элементы заказа
    for item in cart_items:
        order_item = ecommerce_models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)
    
    # Очищаем корзину
    db.query(ecommerce_models.CartItem).filter(
        ecommerce_models.CartItem.user_id == current_user.id
    ).delete()
    
    db.commit()
    db.refresh(order)
    return order
```

### Фаза 3: Сервисный слой (Средний приоритет)

#### 3.1 Создать сервисы для каждого модуля
```python
# services/ecommerce_service.py
class EcommerceService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_products(
        self, 
        skip: int = 0, 
        limit: int = 20,
        filters: Optional[dict] = None
    ) -> List[Product]:
        """Получить товары с фильтрацией"""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        if filters:
            if filters.get("category"):
                query = query.filter(Product.category == filters["category"])
            if filters.get("search"):
                query = query.filter(
                    or_(
                        Product.name.ilike(f"%{filters['search']}%"),
                        Product.description.ilike(f"%{filters['search']}%")
                    )
                )
            if filters.get("min_price"):
                query = query.filter(Product.price >= filters["min_price"])
            if filters.get("max_price"):
                query = query.filter(Product.price <= filters["max_price"])
        
        return query.offset(skip).limit(limit).all()
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Создать товар"""
        product = Product(**product_data.dict())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Обновить товар"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """Удалить товар (мягкое удаление)"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.is_active = False
        self.db.commit()
        return True
```

### Фаза 4: Дополнительные функции (Низкий приоритет)

#### 4.1 Email верификация
```python
# services/email_service.py
class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
    
    def send_verification_email(self, user: User, token: str):
        """Отправить email для верификации"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        # Реализация отправки email
    
    def send_password_reset_email(self, user: User, token: str):
        """Отправить email для сброса пароля"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        # Реализация отправки email
```

#### 4.2 Роли и права доступа
```python
# models/roles.py
class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    permissions = Column(JSON)  # Список разрешений
    
class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### 4.3 Rate Limiting
```python
# middleware/rate_limiting.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# В роутерах
@router.post("/api/auth/login")
@limiter.limit("5/minute")
def login_user(request: Request, ...):
    # Логика входа
```

### Фаза 5: Мониторинг и логирование (Низкий приоритет)

#### 5.1 Логирование
```python
# utils/logging.py
import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger
```

#### 5.2 Метрики
```python
# middleware/metrics.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

## 🚀 План реализации

### Неделя 1: Схемы и валидация
- [ ] Создать все Pydantic схемы
- [ ] Обновить существующие endpoints
- [ ] Добавить валидацию данных

### Неделя 2: E-commerce модуль
- [ ] Полная реализация E-commerce API
- [ ] Добавить фильтрацию и поиск
- [ ] Реализовать корзину и заказы

### Неделя 3: Social Network модуль
- [ ] Полная реализация Social API
- [ ] Добавить лайки и комментарии
- [ ] Реализовать подписки

### Неделя 4: Task Management модуль
- [ ] Полная реализация Tasks API
- [ ] Добавить Kanban функциональность
- [ ] Реализовать назначение задач

### Неделя 5: Content Management модуль
- [ ] Полная реализация Content API
- [ ] Добавить управление статьями
- [ ] Реализовать медиа библиотеку

### Неделя 6: Analytics модуль
- [ ] Полная реализация Analytics API
- [ ] Добавить дашборды и отчеты
- [ ] Реализовать экспорт данных

### Неделя 7: Интеграция и тестирование
- [ ] Интеграционные тесты
- [ ] Performance тестирование
- [ ] Документация API

## 📊 Ожидаемые результаты

### Функциональность
- ✅ Полное соответствие документации
- ✅ Типизированные API responses
- ✅ Валидация всех входных данных
- ✅ Обработка ошибок

### Производительность
- ✅ Время ответа API < 500ms
- ✅ Поддержка пагинации
- ✅ Кэширование запросов

### Безопасность
- ✅ JWT токены
- ✅ Rate limiting
- ✅ Валидация данных
- ✅ Роли и права доступа

### Мониторинг
- ✅ Логирование всех операций
- ✅ Метрики производительности
- ✅ Health checks

## 🔧 Технические требования

### Зависимости
```txt
# Новые зависимости
slowapi==0.1.9  # Rate limiting
python-multipart==0.0.6  # File uploads
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4  # Password hashing
python-json-logger==2.0.7  # JSON logging
prometheus-client==0.19.0  # Metrics
```

### Конфигурация
```python
# config.py - дополнительные настройки
class Settings(BaseSettings):
    # ... существующие настройки ...
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
```

Этот план обеспечит полное соответствие backend'а документации пользовательских сценариев, сохраняя при этом существующую логику авторизации.
