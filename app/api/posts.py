from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.posts import Posts
from app.helpers.auth import get_current_user
from app.redis import get_redis
from app.redis.likes import Likes
from app.schemas.posts import CreatePostModel, PostModel, UpdatePostModel
from app.schemas.responses import ResponseModel


posts_router = APIRouter()


@posts_router.post("/", response_model=ResponseModel)
async def create_post(
    input_data: CreatePostModel,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post_data = input_data.dict()
    post_data.update({
        "created_at": datetime.now(),
        "owner_id": user.id
    })

    await Posts.create_post(post_data=post_data, db=db)
    
    return {"OK": True}


@posts_router.get("/user_{user_id}", response_model=List[PostModel])
async def get_user_posts(
    user_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    posts_recs = await Posts.get_user_posts(owner_id=user_id, db=db)
    posts = []
    
    for post_rec in posts_recs:
        post = PostModel.parse_obj(post_rec)
        post_likes = await Likes.get_post_likes(post_id=post.id, db=redis)
        post.likes_amount = post_likes.likes_amount
        post.dislikes_amount = post_likes.dislikes_amount
        posts.append(post)
    
    return posts


@posts_router.get("/{post_id}", response_model=PostModel)
async def get_post_by_id(
    post_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    post_rec = await Posts.get_post(post_id=post_id, db=db)
    if post_rec is None:
        return {
            "OK": False,
            "detail": "Post not found"
        }
    
    post = PostModel.parse_obj(post_rec)
    post_likes = await Likes.get_post_likes(post_id=post.id, db=redis)
    
    post.likes_amount = post_likes.likes_amount
    post.dislikes_amount = post_likes.dislikes_amount
    
    return post


@posts_router.patch("/{post_id}", response_model=ResponseModel)
async def update_post(
    post_id: int,
    input_data: UpdatePostModel,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    input_dict = input_data.dict(exclude_none=True)
    if not input_dict:
        return {
            "OK": False,
            "detail": "Input data is empty"
        }
    
    post = await Posts.get_post(post_id=post_id, db=db)
    if post is None:
        return {
            "OK": False,
            "detail": "Post not found"
        }
    
    await Posts.update_post(
        post_id=post_id,
        new_data=input_dict,
        db=db
    )
     
    return {"OK": True}


@posts_router.delete("/{post_id}", response_model=ResponseModel)
async def delete_post(
    post_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    post = await Posts.get_post(post_id=post_id, db=db)
    if post is None:
        return {
            "OK": False,
            "detail": "Post not found"
        }

    await Likes.delete_post_likes(post_id=post_id, db=redis)
    await Posts.delete_post(post_id=post_id, db=db)

    return {"OK": True}
