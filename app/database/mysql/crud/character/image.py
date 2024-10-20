import random
from sqlalchemy import func
from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.session import AsyncSession
from app.database.mysql.schema.character import Character, CharacterImage

async def create_character_image(
    db: AsyncSession,
    character_id: int,
    bucket_name: str,
    key_name: str
) -> Character:
    data = CharacterImage(
        character_id=character_id,
        profile_bucket_name=bucket_name,
        profile_key_name=key_name
    )   
    db.add(data)
    return data

async def get_character_images_by_id(db: AsyncSession, character_id: int) -> CharacterImage:
    query = (
        select(CharacterImage)
        .filter(CharacterImage.character_id == character_id)
        .order_by(CharacterImage.id.desc())
    )
    data = await db.execute(query)
    return data.scalars().all()

async def get_character_images_by_name(db: AsyncSession, name: str) -> CharacterImage:
    query = (
        select(CharacterImage)
        .join(Character, Character.id == CharacterImage.character_id)
        .filter(Character.name == name)
        .order_by(CharacterImage.id.desc())
    )
    data = await db.execute(query)
    return data.scalars().all()