from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import get_current_user, get_db
import models_package.social as social_models
import models
from typing import List

router = APIRouter()


# Posts endpoints
@router.get("/api/social/posts")
def get_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Получить ленту постов"""
    posts = (
        db.query(social_models.Post)
        .filter(social_models.Post.is_public == True)
        .order_by(social_models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.post("/api/social/posts")
def create_post(
    post_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать новый пост"""
    post = social_models.Post(
        user_id=current_user.id,
        content=post_data.get("content"),
        image_url=post_data.get("image_url"),
        is_public=post_data.get("is_public", True),
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/api/social/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Получить пост по ID"""
    post = db.query(social_models.Post).filter(social_models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/api/social/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Лайкнуть пост"""
    # Проверяем, не лайкнул ли уже пользователь этот пост
    existing_like = (
        db.query(social_models.PostLike)
        .filter(
            social_models.PostLike.user_id == current_user.id,
            social_models.PostLike.post_id == post_id,
        )
        .first()
    )

    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")

    like = social_models.PostLike(user_id=current_user.id, post_id=post_id)
    db.add(like)
    db.commit()
    return {"message": "Post liked"}


@router.post("/api/social/posts/{post_id}/comment")
def comment_post(
    post_id: int,
    comment_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Добавить комментарий к посту"""
    comment = social_models.Comment(
        user_id=current_user.id, post_id=post_id, content=comment_data.get("content")
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# Users endpoints
@router.get("/api/social/users")
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Получить список пользователей"""
    users = (
        db.query(models.User)
        .filter(models.User.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users


@router.post("/api/social/users/{user_id}/follow")
def follow_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Подписаться на пользователя"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    # Проверяем, не подписан ли уже
    existing_follow = (
        db.query(social_models.Follow)
        .filter(
            social_models.Follow.follower_id == current_user.id,
            social_models.Follow.following_id == user_id,
        )
        .first()
    )

    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")

    follow = social_models.Follow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()
    return {"message": "User followed"}
