from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models, schemas, config
from security import SecurityUtils


def get_db():
    """Dependency для получения сессии БД"""
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Настройка JWT
SECRET_KEY = config.settings.SECRET_KEY
ALGORITHM = config.settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES

security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return SecurityUtils.verify_password(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return SecurityUtils.get_password_hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создание JWT access токена"""
    return SecurityUtils.create_access_token(data, expires_delta)


def create_refresh_token(data: dict):
    """Создание JWT refresh токена"""
    return SecurityUtils.create_refresh_token(data)


def verify_token(token: str, token_type: str = "access"):
    """Верификация JWT токена"""
    try:
        payload = SecurityUtils.verify_token(token, token_type)
        email: str = payload.get("sub")
        return email
    except HTTPException:
        return None


def authenticate_user(db: Session, email: str, password: str):
    """Аутентификация пользователя"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Получение текущего пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
