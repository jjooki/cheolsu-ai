from sqlalchemy import func
from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.session import AsyncSession
from app.database.mysql.schema.character import Character

async def create_character(
    db: AsyncSession,
    name: str,
    description: str
) -> Character:
    data = Character(
        name=name,
        description=description,
    )
    db.add(data)
    return data

async def get_character_by_id(db: AsyncSession, character_id: int) -> Character:
    query = (
        select(Character)
        .filter(Character.id == character_id)
    )
    data = await db.execute(query)
    return data.scalars().first()

async def get_characters_by_name(db: AsyncSession, name: str) -> Character:
    query = (
        select(Character)
        .filter(Character.name.like(f'%{name}%'))
        .order_by(Character.name.asc())
    )
    data = await db.execute(query)
    return data.scalars().all()

async def update_character(
    db: AsyncSession,
    character_id: int,
    name: Optional[str]=None,
    description: Optional[str]=None
) -> Character:
    query = (
        select(Character)
        .filter(Character.id == character_id)
    )
    result = await db.execute(query)
    data = result.first()
    if name:
        data.name = name
    if description:
        data.description = description
    return data

async def delete_character(
    db: AsyncSession,
    character_id: int
) -> Character:
    query = (
        select(Character)
        .filter(Character.id == character_id)
    )
    result = await db.execute(query)
    data = result.first()
    db.delete(data)
    return data