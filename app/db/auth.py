from sqlalchemy.orm import Session

from app.db import models
from app.helpers.auth import get_password_hash
from app.schemas.auth import Auth


def add_new_user(user_data: Auth, db: Session):
    existing_user = db.query(models.User).filter(models.User.login == user_data.login).first()

    if existing_user:
        return {"error": "registered login"}
    
    hashed_password, salt = get_password_hash(user_data.password)
    new_user = models.User(
        login=user_data.login,
        hashed_password=hashed_password,
        salt=salt
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
