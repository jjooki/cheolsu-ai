from sqlalchemy.future import select
from typing import List, Literal

from app.database.mysql.schema.chat import ChatMessage, ChatLike
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
    
    async def get_message_like_unlike(self, chat_message_id: int) -> ChatLike:
        query = (
            select(ChatLike)
            .filter(ChatLike.chat_message_id == chat_message_id)
            .order_by(ChatLike.id.desc())
            .limit(1)
        )
        return await self._one_or_none(query)
    
    async def create_message_like(self, chat_message_id: int) -> ChatLike:
        data = ChatLike(chat_message_id=chat_message_id, like=1)
        return await self._add(data)
    
    async def create_message_unlike(self, chat_message_id: int) -> ChatLike:
        data = ChatLike(chat_message_id=chat_message_id, like=-1)
        return await self._add(data)
    
    async def cancel_message_like_unlike(self, chat_message_id: int) -> ChatLike:
        data = ChatLike(chat_message_id=chat_message_id, like=0)
        return await self._add(data)