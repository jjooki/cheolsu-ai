from fastapi import APIRouter
from .v1 import v1_router

routers = APIRouter(prefix="/api")
routers.include_router(v1_router, prefix="/v1")