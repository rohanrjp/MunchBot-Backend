from redis.asyncio import Redis
from .config import settings

r_client = Redis(
    host=settings.REDIS_CLOUD_HOST,
    port=settings.REDIS_CLOUD_PORT,
    decode_responses=True,
    username=settings.REDIS_CLOUD_USERNAME,
    password=settings.REDIS_CLOUD_PASSWORD,
)