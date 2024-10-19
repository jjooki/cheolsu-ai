from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.sql.expression import select
from redis.asyncio.client import Redis

from app.database.mysql.session import AsyncSession, get_session, get_read_session
from app.database.mongodb.session import MongoHandler
from app.database.redis.session import get_session

router = APIRouter()

@router.get("/ping")
async def api_health():
    return {"status": "ok"}

@router.get("/mysql")
async def mysql_ping(
    read_session: Annotated[AsyncSession, Depends(get_read_session)],
    write_session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        query = (
            select(1)
        )
        await read_session.scalar(query)
        await write_session.scalar(query)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/redis")
async def redis_ping(
    session: Annotated[Redis, Depends(get_session)]
):
    try:
        await session.ping()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@router.get("/mongodb")
async def mongodb_ping():
    with MongoHandler(
        db_name="cheolsu", collection_name="chat_log"
    ) as mongo:
        if mongo.ping():
            return {"status": "ok"}
        else:
            return {"status": "error"}

@router.get("")
async def total_health():
    return {"status": "ok"}