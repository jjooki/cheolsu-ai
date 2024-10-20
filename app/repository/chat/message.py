from sqlalchemy.future import select
from typing import List, Literal

from app.database.mysql.schema.chat import ChatMessage
from app.core.repository import BaseRepository

class ChatMessageRepository(BaseRepository):
    async def create_chat_message(
        self,
        chat_room_id: int,
        role: Literal['user', 'assistant'],
        content: str
    ) -> ChatMessage:
        data = ChatMessage(
            chat_room_id=chat_room_id,
            role=role,
            message=content
        )
        result = await self._add(data)
        return result
    
    async def get_chat_messages(
        self,
        chat_room_id: int,
        offset: int = 0,
        limit: int = 10
    ) -> List[ChatMessage]:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.chat_room_id == chat_room_id,
                    ChatMessage.deleted_at.is_(None))
            .offset(offset)
            .limit(limit)
        )
        return await self._all(query)
    
    async def get_latest_chat_messages(
        self,
        chat_room_id: int,
        limit: int
    ) -> List[ChatMessage]:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.chat_room_id == chat_room_id,
                    ChatMessage.deleted_at.is_(None))
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        return await self._all(query)
    
    async def update_chat_message(
        self,
        message_id: int,
        content: str
    ) -> ChatMessage:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.id == message_id,
                    ChatMessage.deleted_at.is_(None))
        )
        data = await self._first(query, read_only=False)
        data.content = content
        return data
    
    async def delete_chat_message(self, message_id: int) -> ChatMessage:
        query = (
            select(ChatMessage)
            .filter(ChatMessage.id == message_id,
                    ChatMessage.deleted_at.is_(None))
        )
        data = await self._first(query, read_only=False)
        data.deleted_at = self._get_current_time()
        return data