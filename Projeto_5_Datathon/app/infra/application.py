from fastapi import FastAPI

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_:FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

# Cria uma instância de FastAPI
app = FastAPI(
    title="1MLET - API O Globo",
    description="API para o sistema de recomendação de matérias do O Globo",
    version="0.1.0",
    lifespan=lifespan
)

