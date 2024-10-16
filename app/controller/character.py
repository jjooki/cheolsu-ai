import random
from typing import Optional

from app.model.request.character import *
from app.model.response.character import *
from app.repository.character import CharacterRepository
from app.service.agent.generator.image import ImageGeneratorService
from app.service.character import CharacterService

class CharacterController:
    def __init__(self, character_repository: CharacterRepository):
        self.repository = character_repository
        self.image_gen_service = ImageGeneratorService()
        self.character_service = CharacterService()

    async def get_character_info(self, character_id: int):
        return await self.repository.info.get_character_by_id(character_id)
    
    async def get_characters_by_name(self, name: str):
        return await self.repository.info.get_characters_by_name(name)
    
    async def create_character(self, name: str, description: str):
        return await self.repository.info.create_character(name, description)
    
    async def update_character(
        self,
        character_id: int,
        name: Optional[str]=None,
        description: Optional[str]=None
    ):
        return await self.repository.info.update_character(character_id, name, description)
    
    async def delete_character(self, character_id: int):
        return await self.repository.info.delete_character(character_id)
    
    async def get_character_prompt(self, character_id: int):
        return await self.repository.prompt.get_character_prompt_by_id(character_id)
    
    async def get_character_prompt_by_name(self, name: str):
        return await self.repository.prompt.get_character_prompt_by_name(name)
    
    async def get_character_prompts(self, character_id: int):
        return await self.repository.prompt.get_character_prompts_by_id(character_id)
    
    async def get_character_prompts_by_name(self, name: str):
        return await self.repository.prompt.get_character_prompts_by_name(name)
    
    async def get_random_character_prompt(self, character_id: int):
        data = await self.repository.prompt.get_character_prompts_by_id(character_id)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
        
    async def get_random_character_prompt_by_name(self, name: str):
        data = await self.repository.prompt.get_character_prompts_by_name(name)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
        
    async def create_character_prompt_by_id(self, character_id: int, prompt: str):
        return await self.repository.prompt.create_character_prompt_by_id(character_id, prompt)
    
    async def create_character_prompt_by_name(self, name: str, prompt: str):
        return await self.repository.prompt.create_character_prompt_by_name(name, prompt)
    
    async def create_character_image(self, character_id: int, bucket_name: str, key_name: str):
        return await self.repository.image.create_character_image(character_id, bucket_name, key_name)
    
    async def get_character_images_by_id(self, character_id: int):
        return await self.repository.image.get_character_images_by_id(character_id)
    
    async def get_character_images_by_name(self, name: str):
        return await self.repository.image.get_character_images_by_name(name)
    
    async def get_random_character_image_by_id(self, character_id: int):
        data = await self.repository.image.get_character_images_by_id(character_id)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
        
    async def get_random_character_image_by_name(self, name: str):
        data = await self.repository.image.get_character_images_by_name(name)
        
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None