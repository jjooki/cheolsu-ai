from sqlalchemy.future import select
from typing import List

from app.database.mysql.schema.character import Character, CharacterImage
from app.core.repository import BaseRepository

class CharacterImageRepository(BaseRepository):
    async def create_character_image(
        self,
        character_id: int,
        bucket_name: str,
        key_name: str
    ) -> CharacterImage:
        data = CharacterImage(
            character_id=character_id,
            profile_bucket_name=bucket_name,
            profile_key_name=key_name
        )   
        result = await self._add(data)
        return result

    async def get_character_images_by_id(self, character_id: int) -> List[CharacterImage]:
        query = (
            select(CharacterImage)
            .filter(CharacterImage.character_id == character_id)
            .order_by(CharacterImage.id.desc())
        )
        return await self._all(query)

    async def get_character_images_by_name(self, name: str) -> List[CharacterImage]:
        query = (
            select(CharacterImage)
            .join(Character, Character.id == CharacterImage.character_id)
            .filter(Character.name == name)
            .order_by(CharacterImage.id.desc())
        )
        return await self._all(query)
    
    async def get_character_image_by_id(self, character_image_id: int) -> CharacterImage:
        query = (
            select(CharacterImage)
            .filter(CharacterImage.id == character_image_id)
        )
        return await self._one_or_none(query)