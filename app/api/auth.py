from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import settings
from app.db import get_db
from app.db.users import add_new_user, get_user_by_name
from app.helpers.auth import (
    create_access_token,
    get_password_hash,
    reusable_oauth2,
    verify_password
)
from app.schemas.auth import Auth, Token
from app.schemas.responses import ResponseModel


auth_router = APIRouter()


@auth_router.post("/sign_up", response_model=ResponseModel)
async def sign_up(input_data: Auth, db: Session = Depends(get_db)):
    
    existing_user = await get_user_by_name(username=input_data.username, db=db)

    if existing_user:
        return JSONResponse(content={
            "OK": False,
            "detail": "This username is already in use"
        })
    
    hashed_password = get_password_hash(input_data.password)
    user_data = input_data.dict()
    user_data.update({"hashed_password": hashed_password})
    
    await add_new_user(user_data=user_data, db=db)
    
    return JSONResponse(content={
        "OK": True
    })


@auth_router.post("/sign_in", response_model=Token)
async def sign_in(
    form_data: Auth, db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = await get_user_by_name(
        username=form_data.username, db=db
    )

    if not user:
        raise credentials_exception

    password_verification = verify_password(
        form_data.password, user.hashed_password
    )
    
    if not password_verification:
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key=reusable_oauth2.token_name, value=access_token, httponly=True
    )
    return response