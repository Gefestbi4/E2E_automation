from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.tasks as tasks_models
import models
from typing import List

router = APIRouter()


# Boards endpoints
@router.get("/api/tasks/boards")
def get_boards(
    current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Получить доски пользователя"""
    boards = (
        db.query(tasks_models.Board)
        .filter(tasks_models.Board.user_id == current_user.id)
        .all()
    )
    return boards


@router.post("/api/tasks/boards")
def create_board(
    board_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую доску"""
    board = tasks_models.Board(
        name=board_data.get("name"),
        description=board_data.get("description"),
        user_id=current_user.id,
        is_public=board_data.get("is_public", False),
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.get("/api/tasks/boards/{board_id}")
def get_board(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить доску по ID"""
    board = (
        db.query(tasks_models.Board)
        .filter(
            tasks_models.Board.id == board_id,
            tasks_models.Board.user_id == current_user.id,
        )
        .first()
    )
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


# Cards endpoints
@router.get("/api/tasks/boards/{board_id}/cards")
def get_board_cards(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить карточки доски"""
    board = (
        db.query(tasks_models.Board)
        .filter(
            tasks_models.Board.id == board_id,
            tasks_models.Board.user_id == current_user.id,
        )
        .first()
    )
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    cards = (
        db.query(tasks_models.Card).filter(tasks_models.Card.board_id == board_id).all()
    )
    return cards


@router.post("/api/tasks/cards")
def create_card(
    card_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую карточку"""
    card = tasks_models.Card(
        title=card_data.get("title"),
        description=card_data.get("description"),
        board_id=card_data.get("board_id"),
        assigned_to_id=card_data.get("assigned_to_id"),
        status=card_data.get("status", "todo"),
        priority=card_data.get("priority", "medium"),
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.put("/api/tasks/cards/{card_id}")
def update_card(
    card_id: int,
    card_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить карточку"""
    card = db.query(tasks_models.Card).filter(tasks_models.Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Обновляем поля
    for field, value in card_data.items():
        if hasattr(card, field):
            setattr(card, field, value)

    db.commit()
    db.refresh(card)
    return card


@router.post("/api/tasks/cards/{card_id}/assign")
def assign_card(
    card_id: int,
    assign_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Назначить карточку пользователю"""
    card = db.query(tasks_models.Card).filter(tasks_models.Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.assigned_to_id = assign_data.get("assigned_to_id")
    db.commit()
    db.refresh(card)
    return card
