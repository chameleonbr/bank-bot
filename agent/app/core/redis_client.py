import redis.asyncio as aioredis
from app.core.config import settings

_pool: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    global _pool
    if _pool is None:
        _pool = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    return _pool


async def get_session(session_id: str) -> dict:
    r = get_redis()
    data = await r.hgetall(f"session:{session_id}")
    return data or {}


async def set_session(session_id: str, data: dict, ttl: int = 1800) -> None:
    """TTL defaults to 30 minutes as per PRD."""
    r = get_redis()
    await r.hset(f"session:{session_id}", mapping={k: str(v) for k, v in data.items()})
    await r.expire(f"session:{session_id}", ttl)


async def delete_session(session_id: str) -> None:
    r = get_redis()
    await r.delete(f"session:{session_id}")
