from datetime import datetime, timedelta
from typing import Union

from databases import Database
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.config import settings
from app.db import get_db
from app.db.users import get_user_by_name


class OAuth2PasswordCookie(OAuth2PasswordBearer):
    """OAuth2 password flow with token in a httpOnly cookie."""

    def __init__(self, *args, token_name: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_name = token_name or "my-jwt-token"

    async def __call__(self, request: Request) -> str:
        """Extract and return a JWT from the request cookies.
        Raises:
            HTTPException: 403 error if no token cookie is present.
        """

        not_authenticated_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
        
        token = request.cookies.get(self.token_name)
        if not token:
            authorization: str = request.headers.get("Authorization")
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                raise not_authenticated_exception
            token = param
        
        if not token:
            raise not_authenticated_exception
        
        return token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordCookie(tokenUrl=f"/api/auth/sign_in")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_AUTH_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Database = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_AUTH_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    user = await get_user_by_name(username=username, db=db)

    if not user:
        raise credentials_exception

    return user
