"""
Сервис для Task Management модуля
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

import models_package.tasks as tasks_models
from models import User
from schemas.tasks import (
    BoardCreate,
    BoardUpdate,
    BoardFilters,
    CardCreate,
    CardUpdate,
    CardFilters,
    CardCommentCreate,
    CardCommentUpdate,
)
from utils.database import QueryBuilder, PaginationHelper, SearchHelper
from utils.exceptions import (
    BoardNotFoundError,
    CardNotFoundError,
    NotFoundError,
    BusinessLogicError,
)


class TasksService:
    """Сервис для работы с задачами и досками"""

    def __init__(self, db: Session):
        self.db = db

    # Boards methods
    def get_boards(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[BoardFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список досок с фильтрацией"""
        query = self.db.query(tasks_models.Board)

        if filters:
            # Фильтр по владельцу (используем текущего пользователя)
            if user:
                query = query.filter(tasks_models.Board.user_id == user.id)

            # Фильтр по публичности
            if filters.is_public is not None:
                query = query.filter(tasks_models.Board.is_public == filters.is_public)

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    tasks_models.Board,
                    filters.search,
                    ["name", "description"],
                )

        # Если пользователь не указан, показываем только публичные доски
        if not user:
            query = query.filter(tasks_models.Board.is_public == True)
        else:
            # Показываем доски пользователя и публичные доски
            query = query.filter(
                or_(
                    tasks_models.Board.user_id == user.id,
                    tasks_models.Board.is_public == True,
                )
            )

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(tasks_models.Board.created_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем статистику для каждой доски
        boards_with_stats = []
        for board in result["items"]:
            # Подсчитываем карточки по статусам
            cards_count = (
                self.db.query(tasks_models.Card)
                .filter(tasks_models.Card.board_id == board.id)
                .count()
            )

            todo_count = (
                self.db.query(tasks_models.Card)
                .filter(
                    and_(
                        tasks_models.Card.board_id == board.id,
                        tasks_models.Card.status == tasks_models.TaskStatus.TODO,
                    )
                )
                .count()
            )

            in_progress_count = (
                self.db.query(tasks_models.Card)
                .filter(
                    and_(
                        tasks_models.Card.board_id == board.id,
                        tasks_models.Card.status == tasks_models.TaskStatus.IN_PROGRESS,
                    )
                )
                .count()
            )

            done_count = (
                self.db.query(tasks_models.Card)
                .filter(
                    and_(
                        tasks_models.Card.board_id == board.id,
                        tasks_models.Card.status == tasks_models.TaskStatus.DONE,
                    )
                )
                .count()
            )

            boards_with_stats.append(
                {
                    "board": board,
                    "cards_count": cards_count,
                    "todo_count": todo_count,
                    "in_progress_count": in_progress_count,
                    "done_count": done_count,
                }
            )

        result["items"] = boards_with_stats
        return result

    def get_board(self, board_id: int, user: Optional[User] = None) -> Dict[str, Any]:
        """Получить доску по ID"""
        query = self.db.query(tasks_models.Board).filter(
            tasks_models.Board.id == board_id
        )

        # Проверяем права доступа
        if user:
            query = query.filter(
                or_(
                    tasks_models.Board.user_id == user.id,
                    tasks_models.Board.is_public == True,
                )
            )
        else:
            query = query.filter(tasks_models.Board.is_public == True)

        board = query.first()

        if not board:
            raise BoardNotFoundError(str(board_id))

        # Получаем карточки доски
        cards = (
            self.db.query(tasks_models.Card)
            .filter(tasks_models.Card.board_id == board_id)
            .order_by(tasks_models.Card.created_at.desc())
            .all()
        )

        # Подсчитываем статистику
        cards_count = len(cards)
        todo_count = len([c for c in cards if c.status == tasks_models.TaskStatus.TODO])
        in_progress_count = len(
            [c for c in cards if c.status == tasks_models.TaskStatus.IN_PROGRESS]
        )
        done_count = len([c for c in cards if c.status == tasks_models.TaskStatus.DONE])

        return {
            "board": board,
            "cards": cards,
            "cards_count": cards_count,
            "todo_count": todo_count,
            "in_progress_count": in_progress_count,
            "done_count": done_count,
        }

    def create_board(self, board_data: BoardCreate, user: User) -> tasks_models.Board:
        """Создать новую доску"""
        board = tasks_models.Board(
            name=board_data.name,
            description=board_data.description,
            user_id=user.id,
            is_public=board_data.is_public,
        )
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board

    def update_board(
        self, board_id: int, board_data: BoardUpdate, user: User
    ) -> tasks_models.Board:
        """Обновить доску"""
        board = self.get_board(board_id, user)["board"]

        # Проверяем, что пользователь является владельцем доски
        if board.user_id != user.id:
            raise NotFoundError("Board", str(board_id))

        update_data = board_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(board, field, value)

        self.db.commit()
        self.db.refresh(board)
        return board

    def delete_board(self, board_id: int, user: User) -> bool:
        """Удалить доску"""
        board = self.get_board(board_id, user)["board"]

        # Проверяем, что пользователь является владельцем доски
        if board.user_id != user.id:
            raise NotFoundError("Board", str(board_id))

        # Удаляем все карточки доски
        self.db.query(tasks_models.Card).filter(
            tasks_models.Card.board_id == board_id
        ).delete()

        self.db.delete(board)
        self.db.commit()
        return True

    # Cards methods
    def get_cards(
        self,
        board_id: int,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[CardFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить карточки доски с фильтрацией"""
        # Проверяем доступ к доске
        board = self.get_board(board_id, user)["board"]

        query = self.db.query(tasks_models.Card).filter(
            tasks_models.Card.board_id == board_id
        )

        if filters:
            # Фильтр по статусу
            if filters.status:
                query = query.filter(tasks_models.Card.status == filters.status)

            # Фильтр по приоритету
            if filters.priority:
                query = query.filter(tasks_models.Card.priority == filters.priority)

            # Фильтр по исполнителю
            if filters.assigned_to_id:
                query = query.filter(
                    tasks_models.Card.assigned_to_id == filters.assigned_to_id
                )

            # Фильтр по дате выполнения
            if filters.due_date_from:
                query = query.filter(
                    tasks_models.Card.due_date >= filters.due_date_from
                )
            if filters.due_date_to:
                query = query.filter(tasks_models.Card.due_date <= filters.due_date_to)

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    tasks_models.Card,
                    filters.search,
                    ["title", "description"],
                )

        # Сортировка по приоритету и дате создания
        query = query.order_by(
            tasks_models.Card.priority.desc(),
            tasks_models.Card.created_at.desc(),
        )

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем дополнительную информацию для каждой карточки
        cards_with_stats = []
        for card in result["items"]:
            # Подсчитываем комментарии
            comments_count = (
                self.db.query(tasks_models.CardComment)
                .filter(tasks_models.CardComment.card_id == card.id)
                .count()
            )

            # Проверяем, просрочена ли карточка
            is_overdue = False
            if card.due_date and card.status != tasks_models.TaskStatus.DONE:
                is_overdue = card.due_date < datetime.now()

            cards_with_stats.append(
                {
                    "card": card,
                    "comments_count": comments_count,
                    "is_overdue": is_overdue,
                }
            )

        result["items"] = cards_with_stats
        return result

    def get_card(self, card_id: int, user: Optional[User] = None) -> Dict[str, Any]:
        """Получить карточку по ID"""
        card = (
            self.db.query(tasks_models.Card)
            .filter(tasks_models.Card.id == card_id)
            .first()
        )

        if not card:
            raise CardNotFoundError(str(card_id))

        # Проверяем доступ к доске
        board = self.get_board(card.board_id, user)["board"]

        # Подсчитываем комментарии
        comments_count = (
            self.db.query(tasks_models.CardComment)
            .filter(tasks_models.CardComment.card_id == card_id)
            .count()
        )

        # Проверяем, просрочена ли карточка
        is_overdue = False
        if card.due_date and card.status != tasks_models.TaskStatus.DONE:
            is_overdue = card.due_date < datetime.now()

        return {
            "card": card,
            "comments_count": comments_count,
            "is_overdue": is_overdue,
        }

    def create_card(self, card_data: CardCreate, user: User) -> tasks_models.Card:
        """Создать новую карточку"""
        # Проверяем доступ к доске
        board = self.get_board(card_data.board_id, user)["board"]

        card = tasks_models.Card(
            board_id=card_data.board_id,
            title=card_data.title,
            description=card_data.description,
            status=card_data.status.upper(),  # Конвертируем в uppercase для enum
            priority=card_data.priority.upper(),  # Конвертируем в uppercase для enum
            assigned_to_id=card_data.assigned_to_id,
            due_date=getattr(
                card_data, "due_date", None
            ),  # due_date может отсутствовать
        )
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def update_card(
        self, card_id: int, card_data: CardUpdate, user: User
    ) -> tasks_models.Card:
        """Обновить карточку"""
        card_info = self.get_card(card_id, user)
        card = card_info["card"]

        # Проверяем доступ к доске
        board = self.get_board(card.board_id, user)["board"]

        update_data = card_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(card, field, value)

        self.db.commit()
        self.db.refresh(card)
        return card

    def delete_card(self, card_id: int, user: User) -> bool:
        """Удалить карточку"""
        card_info = self.get_card(card_id, user)
        card = card_info["card"]

        # Проверяем доступ к доске
        board = self.get_board(card.board_id, user)["board"]

        # Удаляем все комментарии карточки
        self.db.query(tasks_models.CardComment).filter(
            tasks_models.CardComment.card_id == card_id
        ).delete()

        self.db.delete(card)
        self.db.commit()
        return True

    def move_card(
        self, card_id: int, new_status: tasks_models.TaskStatus, user: User
    ) -> tasks_models.Card:
        """Переместить карточку в другой статус"""
        card_info = self.get_card(card_id, user)
        card = card_info["card"]

        # Проверяем доступ к доске
        board = self.get_board(card.board_id, user)["board"]

        card.status = new_status
        self.db.commit()
        self.db.refresh(card)
        return card

    # Comments methods
    def get_card_comments(
        self, card_id: int, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить комментарии к карточке"""
        # Проверяем, что карточка существует
        card = self.get_card(card_id)["card"]

        query = (
            self.db.query(tasks_models.CardComment)
            .filter(tasks_models.CardComment.card_id == card_id)
            .order_by(tasks_models.CardComment.created_at.desc())
        )

        return PaginationHelper.paginate_query(query, skip, limit)

    def create_card_comment(
        self, comment_data: CardCommentCreate, user: User
    ) -> tasks_models.CardComment:
        """Создать комментарий к карточке"""
        # Проверяем, что карточка существует
        card = self.get_card(comment_data.card_id)["card"]

        comment = tasks_models.CardComment(
            card_id=comment_data.card_id,
            user_id=user.id,
            content=comment_data.content,
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update_card_comment(
        self, comment_id: int, comment_data: CardCommentUpdate, user: User
    ) -> tasks_models.CardComment:
        """Обновить комментарий к карточке"""
        comment = (
            self.db.query(tasks_models.CardComment)
            .filter(tasks_models.CardComment.id == comment_id)
            .first()
        )

        if not comment:
            raise NotFoundError("Comment", str(comment_id))

        # Проверяем, что пользователь является автором комментария
        if comment.user_id != user.id:
            raise NotFoundError("Comment", str(comment_id))

        comment.content = comment_data.content
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete_card_comment(self, comment_id: int, user: User) -> bool:
        """Удалить комментарий к карточке"""
        comment = (
            self.db.query(tasks_models.CardComment)
            .filter(tasks_models.CardComment.id == comment_id)
            .first()
        )

        if not comment:
            return False

        # Проверяем, что пользователь является автором комментария
        if comment.user_id != user.id:
            raise NotFoundError("Comment", str(comment_id))

        self.db.delete(comment)
        self.db.commit()
        return True

    # Analytics methods
    def get_board_analytics(self, board_id: int, user: User) -> Dict[str, Any]:
        """Получить аналитику доски"""
        board = self.get_board(board_id, user)["board"]

        # Общая статистика карточек
        total_cards = (
            self.db.query(tasks_models.Card)
            .filter(tasks_models.Card.board_id == board_id)
            .count()
        )

        # Карточки по статусам
        status_counts = {}
        for status in tasks_models.TaskStatus:
            count = (
                self.db.query(tasks_models.Card)
                .filter(
                    and_(
                        tasks_models.Card.board_id == board_id,
                        tasks_models.Card.status == status,
                    )
                )
                .count()
            )
            status_counts[status.value] = count

        # Карточки по приоритетам
        priority_counts = {}
        for priority in tasks_models.TaskPriority:
            count = (
                self.db.query(tasks_models.Card)
                .filter(
                    and_(
                        tasks_models.Card.board_id == board_id,
                        tasks_models.Card.priority == priority,
                    )
                )
                .count()
            )
            priority_counts[priority.value] = count

        # Просроченные карточки
        overdue_cards = (
            self.db.query(tasks_models.Card)
            .filter(
                and_(
                    tasks_models.Card.board_id == board_id,
                    tasks_models.Card.due_date < datetime.now(),
                    tasks_models.Card.status != tasks_models.TaskStatus.DONE,
                )
            )
            .count()
        )

        # Карточки без исполнителя
        unassigned_cards = (
            self.db.query(tasks_models.Card)
            .filter(
                and_(
                    tasks_models.Card.board_id == board_id,
                    tasks_models.Card.assigned_to_id.is_(None),
                )
            )
            .count()
        )

        return {
            "board_id": board_id,
            "total_cards": total_cards,
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "overdue_cards": overdue_cards,
            "unassigned_cards": unassigned_cards,
        }

    def get_user_tasks(
        self, user: User, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить задачи пользователя"""
        query = self.db.query(tasks_models.Card).filter(
            tasks_models.Card.assigned_to_id == user.id
        )

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем информацию о досках
        tasks_with_boards = []
        for card in result["items"]:
            board = (
                self.db.query(tasks_models.Board)
                .filter(tasks_models.Board.id == card.board_id)
                .first()
            )

            # Проверяем, просрочена ли карточка
            is_overdue = False
            if card.due_date and card.status != tasks_models.TaskStatus.DONE:
                is_overdue = card.due_date < datetime.now()

            tasks_with_boards.append(
                {
                    "card": card,
                    "board": board,
                    "is_overdue": is_overdue,
                }
            )

        result["items"] = tasks_with_boards
        return result
