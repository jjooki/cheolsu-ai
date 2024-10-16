from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.schema.chat import ChatRoom, ChatMessage
from app.core.repository import BaseRepository

class ChatMessageRepository(BaseRepository):
    async def create_chat_message(
        self,
        chat_room_id: int,
        user_id: int,
        message: str
    ) -> ChatMessage:
        data = ChatMessage(
            chat_room_id=chat_room_id,
            user_id=user_id,
            message=message
        )
        result = await self._add(data)
        return result
    
    async def get_chat_messages(
        self,
        chat_room_id: int,
        offset: int = 0,
        limit: int = 10
    ) -> ChatMessage:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.chat_room_id == chat_room_id)
            .offset(offset)
            .limit(limit)
        )
        return await self._all(query)
    
    async def update_chat_message(
        self,
        message_id: int,
        message: str
    ) -> ChatMessage:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.id == message_id)
        )
        data = await self._first(query, read_only=False)
        data.message = message
        return data
    
    async def delete_chat_message(self, message_id: int) -> ChatMessage:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.id == message_id)
        )
        data = await self._first(query, read_only=False)
        await self._delete(data)
        return data