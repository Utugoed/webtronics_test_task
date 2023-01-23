from databases import Database
from sqlalchemy import create_engine, MetaData

from app.config import settings


USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
PORT = settings.POSTGRES_PORT
TABLE = "webtronics"

POSTGRES_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{TABLE}"


database = Database(POSTGRES_URL)
engine = create_engine(url=POSTGRES_URL)

metadata = MetaData()
metadata.create_all(engine)


def get_db():
    return database
