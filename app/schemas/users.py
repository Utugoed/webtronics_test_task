from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., title="User's ID")
    login: str = Field(..., title="User's login")


class User(User):
    password_hash: str = Field(..., title="Password hash")

    class Config:
        orm_mode = True