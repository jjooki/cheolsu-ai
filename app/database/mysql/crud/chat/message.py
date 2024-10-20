from sqlalchemy import func
from sqlalchemy.future import select
from typing import Literal

from app.database.mysql.session import AsyncSession
from app.database.mysql.schema.chat import ChatMessage

async def create_chat_message(
    db: AsyncSession,
    chat_room_id: int,
    role: Literal["user", "assistant"],
    message: str
) -> ChatMessage:
    data = ChatMessage(
        chat_room_id=chat_room_id,
        role=role,
        message=message
    )
    db.add(data)
    return data

async def read_chat_messages_by_room_id(db: AsyncSession, chat_room_id: int) -> ChatMessage:
    query = (
        select(ChatMessage)
        .filter(ChatMessage.chat_room_id == chat_room_id,
                ChatMessage.deleted_at.is_(None))
    )
    data = await db.execute(query)
    return data.scalars().all()

async def update_chat_message(
    db: AsyncSession,
    chat_message_id: int,
    message: str
) -> ChatMessage:
    query = (
        select(ChatMessage)
        .filter(ChatMessage.id == chat_message_id,
                ChatMessage.deleted_at.is_(None))
    )
    result = await db.execute(query)
    data = result.first()
    data.message = message
    return data

async def delete_chat_message(
    db: AsyncSession,
    chat_message_id: int
) -> ChatMessage:
    query = (
        select(ChatMessage)
        .filter(ChatMessage.id == chat_message_id,
                ChatMessage.deleted_at.is_(None))
    )
    result = await db.execute(query)
    data = result.first()
    data.deleted_at = func.now()
    return data