"""
Сервис для Social Network модуля
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

import models_package.social as social_models
from models import User
from schemas.social import (
    PostCreate,
    PostUpdate,
    PostFilters,
    CommentCreate,
    CommentUpdate,
    FollowCreate,
)
from utils.database import QueryBuilder, PaginationHelper, SearchHelper
from utils.exceptions import PostNotFoundError, NotFoundError


class SocialService:
    """Сервис для работы с социальной сетью"""

    def __init__(self, db: Session):
        self.db = db

    # Posts methods
    def get_posts(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[PostFilters] = None,
        user: Optional[User] = None,
    ) -> Dict[str, Any]:
        """Получить список постов с фильтрацией"""
        query = self.db.query(social_models.Post)

        if filters:
            # Фильтр по автору
            if filters.author_id:
                query = query.filter(social_models.Post.user_id == filters.author_id)

            # Фильтр по публичности
            if filters.is_public is not None:
                query = query.filter(social_models.Post.is_public == filters.is_public)

            # Поиск
            if filters.search:
                query = SearchHelper.add_search_filters(
                    query,
                    social_models.Post,
                    filters.search,
                    ["content"],
                )

            # Фильтр по дате
            if filters.date_from:
                query = query.filter(social_models.Post.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(social_models.Post.created_at <= filters.date_to)

        # Сортировка по дате создания (новые сначала)
        query = query.order_by(social_models.Post.created_at.desc())

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем дополнительную информацию для каждого поста
        posts_with_stats = []
        for post in result["items"]:
            # Подсчитываем лайки и комментарии
            likes_count = (
                self.db.query(social_models.PostLike)
                .filter(social_models.PostLike.post_id == post.id)
                .count()
            )

            comments_count = (
                self.db.query(social_models.Comment)
                .filter(social_models.Comment.post_id == post.id)
                .count()
            )

            # Проверяем, лайкнул ли текущий пользователь
            is_liked = False
            if user:
                is_liked = (
                    self.db.query(social_models.PostLike)
                    .filter(
                        and_(
                            social_models.PostLike.post_id == post.id,
                            social_models.PostLike.user_id == user.id,
                        )
                    )
                    .first()
                    is not None
                )

            posts_with_stats.append(
                {
                    "post": post,
                    "likes_count": likes_count,
                    "comments_count": comments_count,
                    "is_liked": is_liked,
                }
            )

        result["items"] = posts_with_stats
        return result

    def get_post(self, post_id: int, user: Optional[User] = None) -> Dict[str, Any]:
        """Получить пост по ID"""
        post = (
            self.db.query(social_models.Post)
            .filter(social_models.Post.id == post_id)
            .first()
        )

        if not post:
            raise PostNotFoundError(str(post_id))

        # Подсчитываем статистику
        likes_count = (
            self.db.query(social_models.PostLike)
            .filter(social_models.PostLike.post_id == post.id)
            .count()
        )

        comments_count = (
            self.db.query(social_models.Comment)
            .filter(social_models.Comment.post_id == post.id)
            .count()
        )

        # Проверяем, лайкнул ли текущий пользователь
        is_liked = False
        if user:
            is_liked = (
                self.db.query(social_models.PostLike)
                .filter(
                    and_(
                        social_models.PostLike.post_id == post.id,
                        social_models.PostLike.user_id == user.id,
                    )
                )
                .first()
                is not None
            )

        return {
            "post": post,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": is_liked,
        }

    def create_post(self, post_data: PostCreate, user: User) -> social_models.Post:
        """Создать новый пост"""
        post = social_models.Post(
            user_id=user.id,
            content=post_data.content,
            image_url=post_data.image_url,
            is_public=post_data.is_public,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update_post(
        self, post_id: int, post_data: PostUpdate, user: User
    ) -> social_models.Post:
        """Обновить пост"""
        post = self.get_post(post_id, user)["post"]

        # Проверяем, что пользователь является автором поста
        if post.user_id != user.id:
            raise NotFoundError("Post", str(post_id))

        update_data = post_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)

        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post(self, post_id: int, user: User) -> bool:
        """Удалить пост"""
        post = self.get_post(post_id, user)["post"]

        # Проверяем, что пользователь является автором поста
        if post.user_id != user.id:
            raise NotFoundError("Post", str(post_id))

        self.db.delete(post)
        self.db.commit()
        return True

    def like_post(self, post_id: int, user: User) -> bool:
        """Поставить лайк посту"""
        post = self.get_post(post_id)["post"]

        # Проверяем, не лайкнул ли уже
        existing_like = (
            self.db.query(social_models.PostLike)
            .filter(
                and_(
                    social_models.PostLike.post_id == post_id,
                    social_models.PostLike.user_id == user.id,
                )
            )
            .first()
        )

        if existing_like:
            return False  # Уже лайкнул

        like = social_models.PostLike(user_id=user.id, post_id=post_id)
        self.db.add(like)
        self.db.commit()
        return True

    def unlike_post(self, post_id: int, user: User) -> bool:
        """Убрать лайк с поста"""
        like = (
            self.db.query(social_models.PostLike)
            .filter(
                and_(
                    social_models.PostLike.post_id == post_id,
                    social_models.PostLike.user_id == user.id,
                )
            )
            .first()
        )

        if not like:
            return False  # Не лайкал

        self.db.delete(like)
        self.db.commit()
        return True

    # Comments methods
    def get_comments(
        self, post_id: int, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить комментарии к посту"""
        query = (
            self.db.query(social_models.Comment)
            .filter(social_models.Comment.post_id == post_id)
            .order_by(social_models.Comment.created_at.desc())
        )

        return PaginationHelper.paginate_query(query, skip, limit)

    def create_comment(
        self, comment_data: CommentCreate, user: User
    ) -> social_models.Comment:
        """Создать комментарий к посту"""
        # Проверяем, что пост существует
        post = self.get_post(comment_data.post_id)["post"]

        comment = social_models.Comment(
            user_id=user.id,
            post_id=comment_data.post_id,
            content=comment_data.content,
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update_comment(
        self, comment_id: int, comment_data: CommentUpdate, user: User
    ) -> social_models.Comment:
        """Обновить комментарий"""
        comment = (
            self.db.query(social_models.Comment)
            .filter(social_models.Comment.id == comment_id)
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

    def delete_comment(self, comment_id: int, user: User) -> bool:
        """Удалить комментарий"""
        comment = (
            self.db.query(social_models.Comment)
            .filter(social_models.Comment.id == comment_id)
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

    # Follow methods
    def follow_user(
        self, follow_data: FollowCreate, user: User
    ) -> social_models.Follow:
        """Подписаться на пользователя"""
        # Проверяем, что пользователь не подписывается сам на себя
        if follow_data.following_id == user.id:
            raise ValueError("Cannot follow yourself")

        # Проверяем, не подписан ли уже
        existing_follow = (
            self.db.query(social_models.Follow)
            .filter(
                and_(
                    social_models.Follow.follower_id == user.id,
                    social_models.Follow.following_id == follow_data.following_id,
                )
            )
            .first()
        )

        if existing_follow:
            return existing_follow

        follow = social_models.Follow(
            follower_id=user.id,
            following_id=follow_data.following_id,
        )
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def unfollow_user(self, following_id: int, user: User) -> bool:
        """Отписаться от пользователя"""
        follow = (
            self.db.query(social_models.Follow)
            .filter(
                and_(
                    social_models.Follow.follower_id == user.id,
                    social_models.Follow.following_id == following_id,
                )
            )
            .first()
        )

        if not follow:
            return False

        self.db.delete(follow)
        self.db.commit()
        return True

    def get_followers(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить подписчиков пользователя"""
        query = (
            self.db.query(social_models.Follow)
            .filter(social_models.Follow.following_id == user_id)
            .order_by(social_models.Follow.created_at.desc())
        )

        return PaginationHelper.paginate_query(query, skip, limit)

    def get_following(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Получить подписки пользователя"""
        query = (
            self.db.query(social_models.Follow)
            .filter(social_models.Follow.follower_id == user_id)
            .order_by(social_models.Follow.created_at.desc())
        )

        return PaginationHelper.paginate_query(query, skip, limit)

    def get_user_profile(
        self, user_id: int, current_user: Optional[User] = None
    ) -> Dict[str, Any]:
        """Получить профиль пользователя с статистикой"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User", str(user_id))

        # Подсчитываем статистику
        posts_count = (
            self.db.query(social_models.Post)
            .filter(social_models.Post.user_id == user_id)
            .count()
        )

        followers_count = (
            self.db.query(social_models.Follow)
            .filter(social_models.Follow.following_id == user_id)
            .count()
        )

        following_count = (
            self.db.query(social_models.Follow)
            .filter(social_models.Follow.follower_id == user_id)
            .count()
        )

        # Проверяем, подписан ли текущий пользователь
        is_following = False
        if current_user and current_user.id != user_id:
            is_following = (
                self.db.query(social_models.Follow)
                .filter(
                    and_(
                        social_models.Follow.follower_id == current_user.id,
                        social_models.Follow.following_id == user_id,
                    )
                )
                .first()
                is not None
            )

        return {
            "user": user,
            "posts_count": posts_count,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        }

    def get_feed(self, user: User, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Получить ленту пользователя (посты от подписок)"""
        # Получаем ID пользователей, на которых подписан текущий пользователь
        following_ids = [
            follow.following_id
            for follow in self.db.query(social_models.Follow)
            .filter(social_models.Follow.follower_id == user.id)
            .all()
        ]

        # Добавляем собственные посты
        following_ids.append(user.id)

        # Получаем посты
        query = (
            self.db.query(social_models.Post)
            .filter(social_models.Post.user_id.in_(following_ids))
            .filter(social_models.Post.is_public == True)
            .order_by(social_models.Post.created_at.desc())
        )

        result = PaginationHelper.paginate_query(query, skip, limit)

        # Добавляем статистику для каждого поста
        posts_with_stats = []
        for post in result["items"]:
            likes_count = (
                self.db.query(social_models.PostLike)
                .filter(social_models.PostLike.post_id == post.id)
                .count()
            )

            comments_count = (
                self.db.query(social_models.Comment)
                .filter(social_models.Comment.post_id == post.id)
                .count()
            )

            # Проверяем, лайкнул ли текущий пользователь
            is_liked = (
                self.db.query(social_models.PostLike)
                .filter(
                    and_(
                        social_models.PostLike.post_id == post.id,
                        social_models.PostLike.user_id == user.id,
                    )
                )
                .first()
                is not None
            )

            posts_with_stats.append(
                {
                    "post": post,
                    "likes_count": likes_count,
                    "comments_count": comments_count,
                    "is_liked": is_liked,
                }
            )

        result["items"] = posts_with_stats
        return result
