from databases import Database

from app.db.models import users
from app.schemas.auth import Auth


async def add_new_user(user_data: Auth, db: Database):   
    new_user = {
        "username": user_data["username"],
        "hashed_password": user_data["hashed_password"],
    }
    
    query = users.insert()
    await db.execute(query=query, values=new_user)


async def get_user_by_name(username: str, db: Database):
    query = users.select().where(users.c.username==username)
    user = await db.fetch_one(query=query)
    return user
