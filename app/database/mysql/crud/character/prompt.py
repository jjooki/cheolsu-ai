import random
from sqlalchemy import func
from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.session import AsyncSession
from app.database.mysql.schema.character import Character, CharacterPrompt

async def create_character_prompt_by_id(
    db: AsyncSession,
    character_id: int,
    prompt: str
) -> Character:
    data = CharacterPrompt(
        character_id=character_id,
        prompt=prompt
    )   
    db.add(data)
    return data

async def create_character_prompt_by_name(
    db: AsyncSession,
    name: str,
    prompt: str
) -> Character:
    query = (
        select(Character)
        .filter(Character.name == name)
    )
    result = await db.execute(query)
    character = result.first()
    if character:
        data = CharacterPrompt(
            character_id=character.id,
            prompt=prompt
        )
    else:
        raise ValueError(f'Character not found: {name}')
    
    db.add(data)
    return data

async def get_character_prompt_by_id(db: AsyncSession, character_id: int) -> CharacterPrompt:
    query = (
        select(CharacterPrompt)
        .filter(CharacterPrompt.character_id == character_id,
                CharacterPrompt.deleted_at.is_(None))
        .order_by(CharacterPrompt.id.desc())
        .limit(1)
    )
    data = await db.execute(query)
    return data.scalars().first()

async def get_character_prompt_by_name(db: AsyncSession, name: str) -> CharacterPrompt:
    query = (
        select(CharacterPrompt)
        .join(Character, Character.id == CharacterPrompt.character_id)
        .filter(Character.name == name, CharacterPrompt.deleted_at.is_(None))
        .order_by(CharacterPrompt.id.desc())
        .limit(1)
    )
    data = await db.execute(query)
    return data.scalars().first()

async def get_character_prompts_by_id(db: AsyncSession, character_id: int) -> CharacterPrompt:
    query = (
        select(CharacterPrompt)
        .filter(CharacterPrompt.character_id == character_id,
                CharacterPrompt.deleted_at.is_(None))
    )
    data = await db.execute(query)
    return data.scalars().all()

async def get_character_prompts_by_name(db: AsyncSession, name: str) -> CharacterPrompt:
    query = (
        select(CharacterPrompt)
        .join(Character)
        .filter(Character.name == name)
    )
    data = await db.execute(query)
    return data.scalars().all()