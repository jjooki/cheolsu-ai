import os
from typing import AsyncGenerator

from app.common.config import config
from redis.asyncio import Redis, ConnectionPool

pool = ConnectionPool(
    max_connections=config.CACHE.MAX_CONNECTIONS,
    host=config.CACHE.HOST,
    port=config.CACHE.REDIS_PORT,
    db=config.CACHE.DB,
    decode_responses=True
)

async def get_session() -> AsyncGenerator[Redis, None]:
    session = Redis(connection_pool=pool)
    print(type(session))
    try:
        yield session
    except Exception as e:
        print(e)
        await session.close()
        raise e
    finally:
        await session.close()
        
# Redis-OM 모델에서 사용하는 연결 풀 설정
class RedisOMConnection:
    @staticmethod
    def get_connection():
        return Redis(connection_pool=pool)