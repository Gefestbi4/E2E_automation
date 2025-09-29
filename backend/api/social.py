from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.social as social_models
import models
from typing import List, Optional
from websocket_notifications import ws_notifications

from schemas.social import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostListResponse,
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentListResponse,
    FollowCreate,
    FollowResponse,
    FollowListResponse,
    UserProfileResponse,
    PostFilters,
)
from services.social_service import SocialService
from utils.exceptions import PostNotFoundError, NotFoundError

router = APIRouter()


# Posts endpoints
@router.get("/api/social/posts", response_model=PostListResponse)
def get_posts(
    skip: int = Query(0, ge=0, description="Количество пропущенных постов"),
    limit: int = Query(20, ge=1, le=100, description="Количество постов на странице"),
    author_id: Optional[int] = Query(None, description="Фильтр по автору"),
    is_public: Optional[bool] = Query(None, description="Фильтр по публичности"),
    search: Optional[str] = Query(None, min_length=1, description="Поисковый запрос"),
    date_from: Optional[str] = Query(None, description="Посты с даты"),
    date_to: Optional[str] = Query(None, description="Посты до даты"),
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить список постов с фильтрацией"""
    filters = PostFilters(
        author_id=author_id,
        is_public=is_public,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )

    service = SocialService(db)
    result = service.get_posts(
        skip=skip, limit=limit, filters=filters, user=current_user
    )

    posts = []
    for item in result["items"]:
        posts.append(
            PostResponse(
                id=item["post"].id,
                content=item["post"].content,
                image_url=item["post"].image_url,
                is_public=item["post"].is_public,
                created_at=item["post"].created_at,
                updated_at=item["post"].updated_at,
                author=item["post"].user,
                likes_count=item["likes_count"],
                comments_count=item["comments_count"],
                is_liked=item["is_liked"],
            )
        )

    return PostListResponse(
        items=posts,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/social/posts/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить пост по ID"""
    service = SocialService(db)
    result = service.get_post(post_id, current_user)

    return PostResponse(
        id=result["post"].id,
        content=result["post"].content,
        image_url=result["post"].image_url,
        is_public=result["post"].is_public,
        created_at=result["post"].created_at,
        updated_at=result["post"].updated_at,
        author=result["post"].user,
        likes_count=result["likes_count"],
        comments_count=result["comments_count"],
        is_liked=result["is_liked"],
    )


@router.post("/api/social/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый пост"""
    service = SocialService(db)
    post = service.create_post(post_data, current_user)

    # Отправляем WebSocket уведомление
    await ws_notifications.send_social_update(
        "post_created",
        {
            "post_id": post.id,
            "author_id": current_user.id,
            "author_name": current_user.username,
            "content": (
                post.content[:100] + "..." if len(post.content) > 100 else post.content
            ),
            "is_public": post.is_public,
        },
    )

    return PostResponse(
        id=post.id,
        content=post.content,
        image_url=post.image_url,
        is_public=post.is_public,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=post.user,
        likes_count=0,
        comments_count=0,
        is_liked=False,
    )


@router.put("/api/social/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить пост"""
    service = SocialService(db)
    post = service.update_post(post_id, post_data, current_user)

    # Получаем обновленную статистику
    result = service.get_post(post_id, current_user)

    return PostResponse(
        id=post.id,
        content=post.content,
        image_url=post.image_url,
        is_public=post.is_public,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=post.user,
        likes_count=result["likes_count"],
        comments_count=result["comments_count"],
        is_liked=result["is_liked"],
    )


@router.delete("/api/social/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить пост"""
    service = SocialService(db)
    service.delete_post(post_id, current_user)
    return {"message": "Post deleted successfully"}


@router.post("/api/social/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Поставить лайк посту"""
    service = SocialService(db)
    success = service.like_post(post_id, current_user)

    if not success:
        return {"message": "Already liked"}

    return {"message": "Post liked"}


@router.delete("/api/social/posts/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Убрать лайк с поста"""
    service = SocialService(db)
    success = service.unlike_post(post_id, current_user)

    if not success:
        return {"message": "Not liked"}

    return {"message": "Post unliked"}


# Comments endpoints
@router.get("/api/social/posts/{post_id}/comments", response_model=CommentListResponse)
def get_comments(
    post_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных комментариев"),
    limit: int = Query(
        20, ge=1, le=100, description="Количество комментариев на странице"
    ),
    db: Session = Depends(get_db),
):
    """Получить комментарии к посту"""
    service = SocialService(db)
    result = service.get_comments(post_id, skip=skip, limit=limit)

    comments = []
    for comment in result["items"]:
        comments.append(
            CommentResponse(
                id=comment.id,
                content=comment.content,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                author=comment.user,
                post_id=comment.post_id,
            )
        )

    return CommentListResponse(
        items=comments,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.post("/api/social/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать комментарий к посту"""
    service = SocialService(db)
    comment = service.create_comment(comment_data, current_user)

    return CommentResponse(
        id=comment.id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        author=comment.user,
        post_id=comment.post_id,
    )


@router.put("/api/social/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить комментарий"""
    service = SocialService(db)
    comment = service.update_comment(comment_id, comment_data, current_user)

    return CommentResponse(
        id=comment.id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        author=comment.user,
        post_id=comment.post_id,
    )


@router.delete("/api/social/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить комментарий"""
    service = SocialService(db)
    success = service.delete_comment(comment_id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment deleted successfully"}


# Follow endpoints
@router.post("/api/social/follow", response_model=FollowResponse)
def follow_user(
    follow_data: FollowCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Подписаться на пользователя"""
    service = SocialService(db)
    follow = service.follow_user(follow_data, current_user)

    return FollowResponse(
        id=follow.id,
        follower=follow.follower,
        following=follow.following,
        created_at=follow.created_at,
        updated_at=follow.updated_at,
    )


@router.delete("/api/social/follow/{following_id}")
def unfollow_user(
    following_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Отписаться от пользователя"""
    service = SocialService(db)
    success = service.unfollow_user(following_id, current_user)

    if not success:
        return {"message": "Not following"}

    return {"message": "Unfollowed successfully"}


@router.get("/api/social/users/{user_id}/followers", response_model=FollowListResponse)
def get_followers(
    user_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных подписчиков"),
    limit: int = Query(
        20, ge=1, le=100, description="Количество подписчиков на странице"
    ),
    db: Session = Depends(get_db),
):
    """Получить подписчиков пользователя"""
    service = SocialService(db)
    result = service.get_followers(user_id, skip=skip, limit=limit)

    follows = []
    for follow in result["items"]:
        follows.append(
            FollowResponse(
                id=follow.id,
                follower=follow.follower,
                following=follow.following,
                created_at=follow.created_at,
                updated_at=follow.updated_at,
            )
        )

    return FollowListResponse(
        items=follows,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


@router.get("/api/social/users/{user_id}/following", response_model=FollowListResponse)
def get_following(
    user_id: int,
    skip: int = Query(0, ge=0, description="Количество пропущенных подписок"),
    limit: int = Query(20, ge=1, le=100, description="Количество подписок на странице"),
    db: Session = Depends(get_db),
):
    """Получить подписки пользователя"""
    service = SocialService(db)
    result = service.get_following(user_id, skip=skip, limit=limit)

    follows = []
    for follow in result["items"]:
        follows.append(
            FollowResponse(
                id=follow.id,
                follower=follow.follower,
                following=follow.following,
                created_at=follow.created_at,
                updated_at=follow.updated_at,
            )
        )

    return FollowListResponse(
        items=follows,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )


# Profile endpoints
@router.get("/api/social/users/{user_id}/profile", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    current_user: Optional[models.User] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить профиль пользователя"""
    service = SocialService(db)
    result = service.get_user_profile(user_id, current_user)

    return UserProfileResponse(
        id=result["user"].id,
        email=result["user"].email,
        username=result["user"].username,
        full_name=result["user"].full_name,
        is_active=result["user"].is_active,
        is_verified=result["user"].is_verified,
        created_at=result["user"].created_at,
        updated_at=result["user"].updated_at,
        posts_count=result["posts_count"],
        followers_count=result["followers_count"],
        following_count=result["following_count"],
        is_following=result["is_following"],
    )


# Feed endpoints
@router.get("/api/social/feed", response_model=PostListResponse)
def get_feed(
    skip: int = Query(0, ge=0, description="Количество пропущенных постов"),
    limit: int = Query(20, ge=1, le=100, description="Количество постов на странице"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить ленту пользователя"""
    service = SocialService(db)
    result = service.get_feed(current_user, skip=skip, limit=limit)

    posts = []
    for item in result["items"]:
        posts.append(
            PostResponse(
                id=item["post"].id,
                content=item["post"].content,
                image_url=item["post"].image_url,
                is_public=item["post"].is_public,
                created_at=item["post"].created_at,
                updated_at=item["post"].updated_at,
                author=item["post"].user,
                likes_count=item["likes_count"],
                comments_count=item["comments_count"],
                is_liked=item["is_liked"],
            )
        )

    return PostListResponse(
        items=posts,
        total=result["total"],
        skip=result["skip"],
        limit=result["limit"],
    )
