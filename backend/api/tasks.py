from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.tasks as tasks_models
import models
from typing import List, Optional

from schemas.tasks import (
    BoardCreate,
    BoardUpdate,
    BoardResponse,
    BoardListResponse,
    CardCreate,
    CardUpdate,
    CardResponse,
    CardListResponse,
    CardCommentCreate,
    CardCommentUpdate,
    CardCommentResponse,
    CardCommentListResponse,
    BoardFilters,
    CardFilters,
)
from services.tasks_service import TasksService
from utils.exceptions import (
    BoardNotFoundError,
    CardNotFoundError,
    NotFoundError,
)

router = APIRouter()


# Boards endpoints
@router.get("/api/tasks/boards", response_model=BoardListResponse)
def get_boards(
    skip: int = Query(0, ge=0, description="Количество пропущенных досок"),
    limit: int = Query(20, ge=1, le=100, description="Количество досок на странице"),
    user_id: Optional[int] = Query(None, description="Фильтр по владельцу"),
    is_public: Optional[bool] = Query(None, description="Фильтр по публичности"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить список досок с фильтрацией"""
    filters = BoardFilters(
        user_id=user_id,
        is_public=is_public,
        search=search,
    )

    service = TasksService(db)
    result = service.get_boards(
        skip=skip, limit=limit, filters=filters, user=current_user
    )

    boards = []
    for item in result["items"]:
        boards.append(
            BoardResponse(
                id=item["board"].id,
                name=item["board"].name,
                description=item["board"].description,
                is_public=item["board"].is_public,
                created_at=item["board"].created_at,
                updated_at=item["board"].updated_at,
                user=item["board"].user,
                cards_count=item["cards_count"],
                todo_count=item["todo_count"],
                in_progress_count=item["in_progress_count"],
                done_count=item["done_count"],
            )
        )

    return BoardListResponse(
        items=boards,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/tasks/boards/{board_id}", response_model=BoardResponse)
def get_board(
    board_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить доску по ID"""
    service = TasksService(db)
    result = service.get_board(board_id, current_user)

    return BoardResponse(
        id=result["board"].id,
        name=result["board"].name,
        description=result["board"].description,
        is_public=result["board"].is_public,
        created_at=result["board"].created_at,
        updated_at=result["board"].updated_at,
        user=result["board"].user,
        cards_count=result["cards_count"],
        todo_count=result["todo_count"],
        in_progress_count=result["in_progress_count"],
        done_count=result["done_count"],
    )


@router.post("/api/tasks/boards", response_model=BoardResponse)
def create_board(
    board_data: BoardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую доску"""
    service = TasksService(db)
    board = service.create_board(board_data, current_user)

    return BoardResponse(
        id=board.id,
        name=board.name,
        description=board.description,
        is_public=board.is_public,
        created_at=board.created_at,
        updated_at=board.updated_at,
        user=board.user,
        cards_count=0,
        todo_count=0,
        in_progress_count=0,
        done_count=0,
    )


@router.put("/api/tasks/boards/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    board_data: BoardUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить доску"""
    service = TasksService(db)
    board = service.update_board(board_id, board_data, current_user)

    # Получаем обновленную статистику
    result = service.get_board(board_id, current_user)

    return BoardResponse(
        id=board.id,
        name=board.name,
        description=board.description,
        is_public=board.is_public,
        created_at=board.created_at,
        updated_at=board.updated_at,
        user=board.user,
        cards_count=result["cards_count"],
        todo_count=result["todo_count"],
        in_progress_count=result["in_progress_count"],
        done_count=result["done_count"],
    )


@router.delete("/api/tasks/boards/{board_id}")
def delete_board(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить доску"""
    service = TasksService(db)
    service.delete_board(board_id, current_user)
    return {"message": "Board deleted successfully"}


# Cards endpoints
@router.get("/api/tasks/boards/{board_id}/cards", response_model=CardListResponse)
def get_board_cards(
    board_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных карточек"),
    limit: int = Query(20, ge=1, le=100, description="Количество карточек на странице"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    priority: Optional[str] = Query(None, description="Фильтр по приоритету"),
    assigned_to_id: Optional[int] = Query(None, description="Фильтр по исполнителю"),
    due_date_from: Optional[str] = Query(
        None, description="Карточки с даты выполнения"
    ),
    due_date_to: Optional[str] = Query(None, description="Карточки до даты выполнения"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить карточки доски с фильтрацией"""
    filters = CardFilters(
        status=status,
        priority=priority,
        assigned_to_id=assigned_to_id,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        search=search,
    )

    service = TasksService(db)
    result = service.get_cards(
        board_id, skip=skip, limit=limit, filters=filters, user=current_user
    )

    cards = []
    for item in result["items"]:
        cards.append(
            CardResponse(
                id=item["card"].id,
                title=item["card"].title,
                description=item["card"].description,
                status=item["card"].status.value,
                priority=item["card"].priority.value,
                assigned_to=item["card"].assigned_to,
                due_date=item["card"].due_date,
                created_at=item["card"].created_at,
                updated_at=item["card"].updated_at,
                board_id=item["card"].board_id,
                comments_count=item["comments_count"],
                is_overdue=item["is_overdue"],
            )
        )

    return CardListResponse(
        items=cards,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/tasks/cards/{card_id}", response_model=CardResponse)
def get_card(
    card_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить карточку по ID"""
    service = TasksService(db)
    result = service.get_card(card_id, current_user)

    return CardResponse(
        id=result["card"].id,
        title=result["card"].title,
        description=result["card"].description,
        status=result["card"].status.value,
        priority=result["card"].priority.value,
        assigned_to=result["card"].assigned_to,
        due_date=result["card"].due_date,
        created_at=result["card"].created_at,
        updated_at=result["card"].updated_at,
        board_id=result["card"].board_id,
        comments_count=result["comments_count"],
        is_overdue=result["is_overdue"],
    )


@router.post("/api/tasks/cards", response_model=CardResponse)
def create_card(
    card_data: CardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новую карточку"""
    service = TasksService(db)
    card = service.create_card(card_data, current_user)

    return CardResponse(
        id=card.id,
        title=card.title,
        description=card.description,
        status=card.status.value,
        priority=card.priority.value,
        assigned_to=card.assigned_to,
        due_date=card.due_date,
        created_at=card.created_at,
        updated_at=card.updated_at,
        board_id=card.board_id,
        comments_count=0,
        is_overdue=False,
    )


@router.put("/api/tasks/cards/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    card_data: CardUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить карточку"""
    service = TasksService(db)
    card = service.update_card(card_id, card_data, current_user)

    # Получаем обновленную информацию
    result = service.get_card(card_id, current_user)

    return CardResponse(
        id=card.id,
        title=card.title,
        description=card.description,
        status=card.status.value,
        priority=card.priority.value,
        assigned_to=card.assigned_to,
        due_date=card.due_date,
        created_at=card.created_at,
        updated_at=card.updated_at,
        board_id=card.board_id,
        comments_count=result["comments_count"],
        is_overdue=result["is_overdue"],
    )


@router.delete("/api/tasks/cards/{card_id}")
def delete_card(
    card_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить карточку"""
    service = TasksService(db)
    service.delete_card(card_id, current_user)
    return {"message": "Card deleted successfully"}


@router.post("/api/tasks/cards/{card_id}/move")
def move_card(
    card_id: int,
    new_status: str = Query(..., description="Новый статус карточки"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Переместить карточку в другой статус"""
    service = TasksService(db)

    # Преобразуем строку в enum
    try:
        status_enum = tasks_models.TaskStatus(new_status)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {[s.value for s in tasks_models.TaskStatus]}",
        )

    card = service.move_card(card_id, status_enum, current_user)

    return CardResponse(
        id=card.id,
        title=card.title,
        description=card.description,
        status=card.status.value,
        priority=card.priority.value,
        assigned_to=card.assigned_to,
        due_date=card.due_date,
        created_at=card.created_at,
        updated_at=card.updated_at,
        board_id=card.board_id,
        comments_count=0,
        is_overdue=False,
    )


# Comments endpoints
@router.get(
    "/api/tasks/cards/{card_id}/comments", response_model=CardCommentListResponse
)
def get_card_comments(
    card_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных комментариев"),
    limit: int = Query(
        20, ge=1, le=100, description="Количество комментариев на странице"
    ),
    db: Session = Depends(get_db),
):
    """Получить комментарии к карточке"""
    service = TasksService(db)
    result = service.get_card_comments(card_id, skip=skip, limit=limit)

    comments = []
    for comment in result["items"]:
        comments.append(
            CardCommentResponse(
                id=comment.id,
                content=comment.content,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                user=comment.user,
                card_id=comment.card_id,
            )
        )

    return CardCommentListResponse(
        items=comments,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.post("/api/tasks/cards/{card_id}/comments", response_model=CardCommentResponse)
def create_card_comment(
    card_id: int,
    comment_data: CardCommentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать комментарий к карточке"""
    service = TasksService(db)
    comment = service.create_card_comment(comment_data, current_user)

    return CardCommentResponse(
        id=comment.id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=comment.user,
        card_id=comment.card_id,
    )


@router.put("/api/tasks/comments/{comment_id}", response_model=CardCommentResponse)
def update_card_comment(
    comment_id: int,
    comment_data: CardCommentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить комментарий к карточке"""
    service = TasksService(db)
    comment = service.update_card_comment(comment_id, comment_data, current_user)

    return CardCommentResponse(
        id=comment.id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=comment.user,
        card_id=comment.card_id,
    )


@router.delete("/api/tasks/comments/{comment_id}")
def delete_card_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить комментарий к карточке"""
    service = TasksService(db)
    success = service.delete_card_comment(comment_id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment deleted successfully"}


# Analytics endpoints
@router.get("/api/tasks/boards/{board_id}/analytics")
def get_board_analytics(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить аналитику доски"""
    service = TasksService(db)
    analytics = service.get_board_analytics(board_id, current_user)
    return analytics


@router.get("/api/tasks/my-tasks", response_model=CardListResponse)
def get_user_tasks(
    skip: int = Query(0, ge=0, description="Количество пропущенных задач"),
    limit: int = Query(20, ge=1, le=100, description="Количество задач на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить задачи пользователя"""
    service = TasksService(db)
    result = service.get_user_tasks(current_user, skip=skip, limit=limit)

    cards = []
    for item in result["items"]:
        cards.append(
            CardResponse(
                id=item["card"].id,
                title=item["card"].title,
                description=item["card"].description,
                status=item["card"].status.value,
                priority=item["card"].priority.value,
                assigned_to=item["card"].assigned_to,
                due_date=item["card"].due_date,
                created_at=item["card"].created_at,
                updated_at=item["card"].updated_at,
                board_id=item["card"].board_id,
                comments_count=0,
                is_overdue=item["is_overdue"],
            )
        )

    return CardListResponse(
        items=cards,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )
