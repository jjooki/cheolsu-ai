from fastapi import APIRouter

# from .auth import router as auth_router
from .message import router as message_router
from .room import router as room_router

chat_router = APIRouter()
chat_router.include_router(message_router, prefix="/message", tags=["chat_message"])
chat_router.include_router(room_router, prefix="/room", tags=["chat_room"])