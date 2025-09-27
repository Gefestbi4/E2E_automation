from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from config import settings

# Создаем подключение к базе данных
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # E-commerce relationships
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")

    # Social relationships
    posts = relationship("Post", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    following = relationship(
        "Follow", foreign_keys="Follow.follower_id", back_populates="follower"
    )
    followers = relationship(
        "Follow", foreign_keys="Follow.following_id", back_populates="following"
    )

    # Tasks relationships
    boards = relationship("Board", back_populates="user")
    assigned_cards = relationship("Card", back_populates="assigned_to")
    card_comments = relationship("CardComment", back_populates="user")

    # Content relationships
    articles = relationship("Article", back_populates="author")
    media_files = relationship("MediaFile", back_populates="uploader")

    # Analytics relationships
    reports = relationship("Report", back_populates="created_by")
    dashboards = relationship("Dashboard", back_populates="created_by")
    alerts = relationship("Alert", back_populates="created_by")


# Import all models to register them with SQLAlchemy
# This import is moved to create_db_and_tables() to avoid circular import


# Функция для создания таблиц в БД
def create_db_and_tables():
    # Import all models to register them with SQLAlchemy
    import models_package.ecommerce
    import models_package.social
    import models_package.tasks
    import models_package.content
    import models_package.analytics

    Base.metadata.create_all(bind=engine)
