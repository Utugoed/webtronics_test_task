from fastapi import APIRouter

from app.api.auth import auth_router
from app.api.likes import likes_router
from app.api.posts import posts_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(posts_router, prefix="/posts")
api_router.include_router(likes_router, prefix="/likes")
