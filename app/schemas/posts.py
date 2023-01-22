from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreatePostModel(BaseModel):
    title: str = Field(..., title="Post title")
    content: str = Field(..., title="Post body")

class UpdatePostModel(BaseModel):
    title: Optional[str] = Field(None, title="Post title")
    content: Optional[str] = Field(None, title="Post body")

class PostModel(CreatePostModel):
    id: int = Field(..., tilte="Post ID")
    owner_id: int = Field(..., title="User ID")
    created_at: datetime = Field(..., title="Post creation date")
    likes_amount: int = Field(0, title="Amount of likes")
    dislikes_amount: int = Field(0, title="Amount of dislikes")
