import uuid

from sqlalchemy import func
from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.schema.chat import ChatRoom
from app.database.mysql.session import AsyncSession

async def create_guest_room(
    db: AsyncSession,
    room_name: str,
    character_id: int,
    character_image_id: int,
    model_name: str,
    user_id: Optional[int] = None
) -> ChatRoom:
    _uuid = uuid.uuid4().hex
    data = ChatRoom(
        uuid=_uuid,
        name=room_name,
        user_id=user_id,
        character_id=character_id,
        character_image_id=character_image_id,
        model_name=model_name
    )
    db.add(data)
    return data

async def get_user_room(
    db: AsyncSession,
    user_id: int
) -> ChatRoom:
    query = (
        select(ChatRoom)
        .filter(ChatRoom.user_id == user_id,
                ChatRoom.deleted_at.is_(None))
    )
    data = await db.execute(query)
    return data.scalars().first()