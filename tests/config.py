from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config import settings
from app.db import get_db
from app.main import app


USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
PORT = settings.POSTGRES_PORT
TABLE = "test_table"

POSTGRES_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{TABLE}"


database = Database(POSTGRES_URL)
engine = create_engine(url=POSTGRES_URL)

metadata = MetaData()
metadata.create_all(engine)


def override_get_db():
    return database

app.dependency_overrides[get_db] = override_get_db
