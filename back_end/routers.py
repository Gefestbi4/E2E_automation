import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from . import models, schemas
from .config import settings

router = APIRouter()


# Dependency для получения сессии БД
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def send_telegram_notification(offer: schemas.Offer):
    """Отправляет уведомление в Telegram."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    # Обрезаем комментарий для краткости
    comment_short = (offer.comment[:75] + '...') if offer.comment and len(offer.comment) > 75 else offer.comment

    message = (
        f"Новый оффер!\n\n"
        f"Сумма: {offer.summa} {offer.valuta.value}\n"
        f"Комментарий: {comment_short or 'Нет комментария'}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # В реальном проекте здесь нужно логирование ошибки
        print(f"Ошибка отправки уведомления в Telegram: {e}")


@router.post("/offers/", response_model=schemas.Offer, status_code=status.HTTP_201_CREATED)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    """
    Создает новый оффер, сохраняет в БД и отправляет уведомление в Telegram.
    """
    db_offer = models.Offer(**offer.model_dump())

    try:
        db.add(db_offer)
        db.commit()  # Транзакционная запись
        db.refresh(db_offer)
    except Exception as e:
        db.rollback()
        # Логирование ошибки базы данных
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении данных в базу."
        )

    # Отправляем уведомление после успешного сохранения
    send_telegram_notification(schemas.Offer.model_validate(db_offer))

    return db_offer


# --- User Routes ---
user_router = APIRouter()


@user_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # В реальном приложении пароль нужно хешировать
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, name=user.name, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None


@router.get("/offers/{offer_id}", response_model=schemas.Offer)
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    return db_offer
