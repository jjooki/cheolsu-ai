from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def api_health():
    return {"status": "ok"}

@router.get("/mysql")
async def mysql_ping():
    return {"status": "ok"}

@router.get("/redis")
async def redis_ping():
    return {"status": "ok"}

@router.get("")
async def total_health():
    return {"status": "ok"}