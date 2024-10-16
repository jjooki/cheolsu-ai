from sqlalchemy.future import select
from typing import Optional

from app.database.mysql.schema.character import Character, CharacterPrompt
from app.core.repository import BaseRepository

class CharacterPromptRepository(BaseRepository):
    async def create_character_prompt_by_id(
        self,
        character_id: int,
        prompt: str
    ) -> CharacterPrompt:
        data = CharacterPrompt(
            character_id=character_id,
            prompt=prompt
        )
        result = await self._add(data)
        return result

    async def create_character_prompt_by_name(
        self,
        name: str,
        prompt: str
    ) -> CharacterPrompt:
        query = (
            select(Character)
            .filter(Character.name == name)
        )
        character: Character = await self._one_or_none(query)
        if character:
            data = CharacterPrompt(
                character_id=character.id,
                prompt=prompt
            )
        else:
            raise ValueError(f'Character not found: {name}')
        
        result = await self._add(data)
        return result

    async def get_character_prompt_by_id(self, character_id: int) -> CharacterPrompt:
        query = (
            select(CharacterPrompt)
            .filter(CharacterPrompt.character_id == character_id,
                    CharacterPrompt.deleted_at.is_(None))
            .order_by(CharacterPrompt.id.desc())
            .limit(1)
        )
        return await self._one_or_none(query)

    async def get_character_prompt_by_name(self, name: str) -> CharacterPrompt:
        query = (
            select(CharacterPrompt)
            .join(Character, Character.id == CharacterPrompt.character_id)
            .filter(Character.name == name, CharacterPrompt.deleted_at.is_(None))
            .order_by(CharacterPrompt.id.desc())
            .limit(1)
        )
        return await self._one_or_none(query)

    async def get_character_prompts_by_id(self, character_id: int) -> CharacterPrompt:
        query = (
            select(CharacterPrompt)
            .filter(CharacterPrompt.character_id == character_id,
                    CharacterPrompt.deleted_at.is_(None))
        )
        return await self._all(query)

    async def get_character_prompts_by_name(self, name: str) -> CharacterPrompt:
        query = (
            select(CharacterPrompt)
            .join(Character)
            .filter(Character.name == name)
        )
        return await self._all(query)