from sqlalchemy import create_engine, Column, Integer, Float, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Создаем подключение к базе данных
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель таблицы offers
class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True, index=True)
    summa = Column(Float, nullable=False)
    valuta = Column(String, nullable=False)
    comment = Column(Text)


# Модель таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)


# Функция для создания таблиц в БД (можно вызвать один раз при старте)
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)