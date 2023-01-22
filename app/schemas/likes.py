from pydantic import BaseModel, Field


class NewLike(BaseModel):
    post_id: int = Field(..., title="Liked Post")
    like: bool = Field(
        ..., title="Like or Dislike", description="True if like, False if not"
    )