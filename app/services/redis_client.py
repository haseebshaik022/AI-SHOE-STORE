from upstash_redis.asyncio import Redis
from app.core.config import settings

rd = Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)
