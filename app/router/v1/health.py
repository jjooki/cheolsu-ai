from fastapi import APIRouter
from app.database.mysql.session import read_engine
from app.database.mongodb.session import MongoHandler

router = APIRouter()

@router.get("/ping")
async def api_health():
    return {"status": "ok"}

@router.get("/mysql")
async def mysql_ping():
    if await read_engine.connect():
        return {"status": "ok"}
    else:
        return {"status": "error"}

@router.get("/redis")
async def redis_ping():
    return {"status": "ok"}

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