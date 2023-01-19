from pydantic import BaseModel, Field


class Auth(BaseModel):
    login: str = Field(..., title="User's login")
    password: str = Field(..., title="User's password")

class Token(BaseModel):
    access_token: str = Field(..., title="Access token")
