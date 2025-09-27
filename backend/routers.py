from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, auth, config
from auth import get_db

router = APIRouter()


@router.post("/api/auth/login", response_model=schemas.Token)
def login_or_register(
    user_credentials: schemas.UserLogin, db: Session = Depends(get_db)
):
    """Логин или регистрация пользователя"""
    # Проверяем, существует ли пользователь
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        # Создаем нового пользователя
        username = user_credentials.email.split("@")[0]
        hashed_password = auth.get_password_hash(user_credentials.password)

        user = models.User(
            email=user_credentials.email,
            username=username,
            hashed_password=hashed_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    else:
        # Проверяем пароль существующего пользователя
        if not auth.verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Создаем токен
    access_token_expires = timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Создаем refresh токен
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


@router.get("/api/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok", "message": "API is running"}
