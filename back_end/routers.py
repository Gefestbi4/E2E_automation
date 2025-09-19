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