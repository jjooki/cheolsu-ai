from fastapi import APIRouter

# from .auth import router as auth_router
from .character import character_router
from .chat import chat_router
from .health import router as health_router

v1_router = APIRouter()
# v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(character_router, prefix="/character")
v1_router.include_router(chat_router, prefix="/chat")
v1_router.include_router(health_router, prefix="/health", tags=["health"])
