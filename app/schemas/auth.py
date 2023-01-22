from pydantic import BaseModel, Field


class Auth(BaseModel):
    username: str = Field(..., title="User's username")
    password: str = Field(..., title="User's password")

class Token(BaseModel):
    access_token: str = Field(..., title="Access token")

