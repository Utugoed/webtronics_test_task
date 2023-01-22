import aioredis

from app.config import settings


redis_connection = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

async def get_redis():
    return redis_connection