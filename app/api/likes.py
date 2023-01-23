from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from redis import Redis
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.posts import Posts
from app.helpers.auth import get_current_user
from app.redis import get_redis
from app.redis.likes import Likes
from app.schemas.likes import NewLike
from app.schemas.responses import ResponseModel


likes_router = APIRouter()


@likes_router.post("/", response_model=ResponseModel)
async def new_like(
    input_data: NewLike,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    post = await Posts.get_post(post_id=input_data.post_id, db=db)

    if post.owner_id == user.id:
        return {
            "OK": "False",
            "detail": "You can't like your own posts"
        }
    
    await Likes.new_like(
        post_id=input_data.post_id, user_id=user.id, like=input_data.like, db=redis
    )
    
    return {"OK": True}
