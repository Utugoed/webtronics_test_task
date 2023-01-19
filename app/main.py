from fastapi import FastAPI

from app.api import api_router


app = FastAPI()

app.include_router(api_router)

@app.on_event("startup")
def startup_event():
    from app.db import Base, engine

    Base.metadata.create_all(bind=engine)
    

    