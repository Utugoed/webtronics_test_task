from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(..., title="User's ID")
    login: str = Field(..., title="User's login")


class UserDBModel(User):
    password_hash: str = Field(..., title="Password hash")
