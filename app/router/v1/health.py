from fastapi import APIRouter
from app.database.mysql.session import read_engine

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

@router.get("")
async def total_health():
    return {"status": "ok"}