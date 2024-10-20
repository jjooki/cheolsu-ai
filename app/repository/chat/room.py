from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.schema.chat import ChatRoom
from app.core.repository import BaseRepository

class ChatRoomRepository(BaseRepository):
    async def create_chat_room(
        self,
        uuid: str,
        room_name: str,
        character_id: int,
        character_image_id: int,
        model_name: str,
        user_id: Optional[int] = None
    ) -> ChatRoom:
        data = ChatRoom(
            uuid=uuid,
            name=room_name,
            user_id=user_id,
            character_id=character_id,
            character_image_id=character_image_id,
            model_name=model_name
        )
        result = await self._add(data)
        return result
    
    async def get_user_room(self, user_id: int) -> ChatRoom:
        query = (
            select(ChatRoom)
            .filter(ChatRoom.user_id == user_id,
                    ChatRoom.deleted_at.is_(None))
        )
        return await self._one_or_none(query)
    
    async def get_room_info(self, uuid: str) -> ChatRoom:
        query = (
            select(ChatRoom)
            .filter(ChatRoom.uuid == uuid)
        )
        return await self._one_or_none(query)