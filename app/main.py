import asyncio

from fastapi import FastAPI

from app.api import api_router


app = FastAPI()


app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    from app.db import database, engine, metadata

    await database.connect()


@app.on_event("shutdown")
async def shutdown_event():
    from app.db import database

    await database.disconnect()
