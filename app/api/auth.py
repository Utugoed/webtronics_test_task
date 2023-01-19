from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.auth import add_new_user
from app.schemas.auth import Auth
from app.schemas.responses import ResponseModel


auth_router = APIRouter()


@auth_router.post("/sign_up", response_model=ResponseModel)
def sign_up(input_data: Auth, db: Session = Depends(get_db)):
    
    result = add_new_user(user_data=input_data, db=db)
    
    if result.get("error") == "registered login":
        return JSONResponse(content={
            "OK": False,
            "detail": "This login is already in use"
        })
    
    return JSONResponse(content={
        "OK": True
    })