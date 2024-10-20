from sqlalchemy.future import select
from typing import List, Optional

from app.database.mysql.schema.character import Character
from app.core.repository import BaseRepository

class CharacterInfoRepository(BaseRepository):
    async def create_character(self, name: str, description: str) -> Character:
        data = Character(
            name=name,
            description=description,
        )
        await self._add(data)
        return data
        
    async def get_character_by_id(self, character_id: int) -> Character:
        query = (
            select(Character)
            .filter(Character.id == character_id)
        )
        return await self._one_or_none(query)
    
    async def get_characters(self, offset: int = 0, limit: int = 10) -> List[Character]:
        query = (
            select(Character)
            .order_by(Character.name.asc())
            .offset(offset)
            .limit(limit)
        )
        return await self._all(query)
    
    async def get_character_by_name(self, name: str) -> Character:
        query = (
            select(Character)
            .filter(Character.name == name)
        )
        return await self._one_or_none(query)
    
    async def get_characters_by_name(self, name: str) -> List[Character]:
        query = (
            select(Character)
            .filter(Character.name.like(f'%{name}%'))
            .order_by(Character.name.asc())
        )
        return await self._all(query)
    
    async def update_character(
        self,
        character_id: int,
        name: Optional[str]=None,
        description: Optional[str]=None
    ) -> Character:
        query = (
            select(Character)
            .filter(Character.id == character_id)
        )
        data = await self._first(query, read_only=False)
        if name:
            data.name = name
        if description:
            data.description = description
        return data

    async def delete_character(self, character_id: int) -> Character:
        query = (
            select(Character)
            .filter(Character.id == character_id)
        )
        data = await self._first(query, read_only=False)
        await self._delete(data)
        return data