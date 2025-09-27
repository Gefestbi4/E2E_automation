from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas, auth, config
from auth import get_db

# Import all API routers
from api import ecommerce, social, tasks, content, analytics

router = APIRouter()

# Include all API routers
router.include_router(ecommerce.router, tags=["ecommerce"])
router.include_router(social.router, tags=["social"])
router.include_router(tasks.router, tags=["tasks"])
router.include_router(content.router, tags=["content"])
router.include_router(analytics.router, tags=["analytics"])


# Auth endpoints
@router.post("/api/auth/register", response_model=schemas.UserResponse)
def register_user(
    user_registration: schemas.UserRegistration, db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    # Проверяем, не существует ли уже пользователь с таким email
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user_registration.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )

    # Создаем username из email
    username = user_registration.email.split("@")[0]

    # Проверяем уникальность username
    username_counter = 1
    original_username = username
    while db.query(models.User).filter(models.User.username == username).first():
        username = f"{original_username}{username_counter}"
        username_counter += 1

    # Хешируем пароль
    hashed_password = auth.get_password_hash(user_registration.password)

    # Создаем пользователя
    user = models.User(
        email=user_registration.email,
        username=username,
        full_name=user_registration.full_name,
        hashed_password=hashed_password,
        is_verified=False,  # Требует подтверждения email
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email или username уже существует",
        )


@router.post("/api/auth/login", response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Вход в систему"""
    # Проверяем, существует ли пользователь
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем пароль
    if not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, активен ли пользователь
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Аккаунт деактивирован"
        )

    # Создаем токены
    access_token_expires = timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token = auth.create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/api/auth/refresh", response_model=schemas.Token)
def refresh_access_token(
    refresh_token: schemas.RefreshToken, db: Session = Depends(get_db)
):
    """Обновление access токена с помощью refresh токена"""
    # Проверяем refresh токен
    email = auth.verify_token(refresh_token.refresh_token, "refresh")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, что пользователь существует
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем новый access токен
    access_token_expires = timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token.refresh_token,  # Возвращаем тот же refresh токен
        "token_type": "bearer",
        "expires_in": config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/api/auth/logout")
def logout(current_user: models.User = Depends(auth.get_current_user)):
    """Выход из системы (в будущем можно добавить blacklist токенов)"""
    return {"message": "Successfully logged out"}


@router.get("/api/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Получение информации о текущем пользователе"""
    return current_user


@router.put("/api/auth/me", response_model=schemas.UserResponse)
def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """Обновление профиля пользователя"""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    if user_update.username is not None:
        # Проверяем уникальность username
        existing_user = (
            db.query(models.User)
            .filter(
                models.User.username == user_update.username,
                models.User.id != current_user.id,
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким username уже существует",
            )
        current_user.username = user_update.username

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/api/auth/change-password")
def change_password(
    password_data: schemas.ChangePassword,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """Смена пароля пользователя"""
    # Проверяем текущий пароль
    if not auth.verify_password(
        password_data.current_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный текущий пароль"
        )

    # Обновляем пароль
    current_user.hashed_password = auth.get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Пароль успешно изменен"}


@router.post("/api/auth/verify-email")
def verify_email(
    verification_data: schemas.EmailVerification, db: Session = Depends(get_db)
):
    """Подтверждение email (заглушка для демонстрации)"""
    # В реальном приложении здесь была бы проверка токена подтверждения
    # Пока что просто возвращаем успех
    return {"message": "Email успешно подтвержден"}


@router.get("/api/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok", "message": "API is running"}
