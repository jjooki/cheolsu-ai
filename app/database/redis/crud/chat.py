from typing import List

from app.database.redis.session import Redis, get_session
from app.database.redis.schema.chat import ChatMessage, ChatMessageHistory

async def set_chat_messages(
    room_uuid: str,
    messages: List[ChatMessage]
) -> None:
    ChatMessageHistory(room_uuid=room_uuid, messages=messages).save()
    
async def get_chat_messages(
    room_uuid: str
) -> ChatMessageHistory:
    return ChatMessageHistory.find(ChatMessageHistory.room_uuid == room_uuid)