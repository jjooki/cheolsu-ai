import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from app.common.config import config
from app.core.utils.aws.s3 import S3
from app.model.request.character import (
    CharacterInfoRequest,
    CharacterListRequest
)
from app.model.response.character import (
    CharacterResponse,
    CharacterInfoResponse,
    CharacterImageURLResponse,
    CharacterImageResponse,
    CharacterImageURLResponse,
    CharacterImageFileResponse
)
from app.repository.character import CharacterRepository
from app.repository.chat import ChatRepository
from app.service.agent.generator.image import ImageGeneratorService
from app.service.character import CharacterService

DATA_PATH = Path(__file__).parents[1]
DATA_PATH.mkdir(parents=True, exist_ok=True)

class CharacterController:
    def __init__(
        self,
        character_repository: CharacterRepository,
        chat_repository: ChatRepository
    ):
        self.character_repository = character_repository
        self.chat_repository = chat_repository
        self.image_gen_service = ImageGeneratorService()
        self.character_service = CharacterService(bucket_name=config.S3.BUCKET_NAME)
        self.s3 = S3(
            aws_access_key_id=config.S3.ACCESS_KEY_ID,
            aws_secret_access_key=config.S3.SECRET_ACCESS_KEY,
            region_name=config.S3.REGION_NAME,
        )
        self.bucket_name = config.S3.BUCKET_NAME
        self.image_gen_prompt = """Please generate an image of your character based on the prompt below!
    - Name: {name}
    - Description: {description}
    - Tone: Animated
"""
        self.key_name_prefix = 'profile/character'
        self.path = DATA_PATH / 'character'
        self.path.mkdir(parents=True, exist_ok=True)

    async def get_character_info(self, request: CharacterInfoRequest) -> CharacterInfoResponse:
        info = await self.character_repository.info.get_character_by_id(request.character_id)

        return CharacterInfoResponse(
            character_id=info.id,
            name=info.name,
            description=info.description
        )
        
    async def get_character_info_by_name(self, name: str) -> CharacterInfoResponse:
        info = await self.character_repository.info.get_character_by_name(name)
        
        return CharacterInfoResponse(
            character_id=info.id,
            name=info.name,
            description=info.description
        )
        
    async def get_character_with_image(self, request: CharacterInfoRequest) -> CharacterInfoResponse:
        info = await self.character_repository.info.get_character_by_id(request.character_id)
        image = await self.get_random_character_image_url(request)
        
        return CharacterResponse(
            character_id=info.id,
            name=info.name,
            description=info.description,
            character_image_id=image.character_image_id,
            image_url=image.image_url
        )
    
    async def get_random_character_image_url(self, request: CharacterInfoRequest) -> CharacterImageURLResponse:
        images = await self.character_repository.image.get_character_images_by_id(request.character_id)
        
        if images:
            image = images[random.randint(0, len(images)-1)]
            character_image_id = image.id
            image_url = self.character_service.get_character_image_url(image.profile_key_name)
            
        else:
            character_image_id = None
            image_url = None
            
        return CharacterImageURLResponse(
            character_image_id=character_image_id,
            image_url=image_url
        )
        
    async def get_character_info_of_chat_room(self, chat_room_id: int) -> CharacterInfoResponse:
        room_info = await self.chat_repository.room.get_room_info(chat_room_id)
        character_info = await self.character_repository.info.get_character_by_id(room_info.character_id)
        image_info = await self.character_repository.image.get_character_image_by_id(room_info.character_image_id)
        
        return CharacterInfoResponse(
            character_id=character_info.id,
            name=character_info.name,
            description=character_info.description,
            character_image_id=image_info.id,
            image_url=self.character_service.get_character_image_url(image_info.profile_key_name)
        )
    
    async def get_character_info_list(self, request: CharacterListRequest) -> List[CharacterInfoResponse]:
        infos = await self.character_repository.info.get_characters(request.offset, request.num)
        task = [self.get_character_info(CharacterInfoRequest(character_id=info.id)) for info in infos]
        response = await asyncio.gather(*task)
        return response
    
    async def get_characters_by_name(self, name: str):
        return await self.character_repository.info.get_characters_by_name(name)
    
    async def create_character_info(self, name: str, description: str) -> CharacterInfoResponse:
        data = await self.character_repository.info.create_character(name, description)
        return CharacterInfoResponse(
            name=data.name,
            description=data.description
        )
    
    async def update_character_info(
        self,
        character_id: int,
        name: Optional[str]=None,
        description: Optional[str]=None
    ) -> CharacterInfoResponse:
        update = await self.character_repository.info.update_character(character_id, name, description)
        return CharacterInfoResponse(
            character_id=update.id,
            name=update.name,
            description=update.description
        )
    
    async def delete_character_info(self, character_id: int):
        delete = await self.character_repository.info.delete_character(character_id)
        return {"message": f"Character {delete.name} has been deleted."}
    
    async def get_character_prompt(self, character_id: int):
        return await self.character_repository.prompt.get_character_prompt_by_id(character_id)
    
    async def get_character_prompt_by_name(self, name: str):
        return await self.character_repository.prompt.get_character_prompt_by_name(name)
    
    async def get_character_prompts(self, character_id: int):
        return await self.character_repository.prompt.get_character_prompts_by_character_id(character_id)
    
    async def get_character_prompts_by_name(self, name: str):
        return await self.character_repository.prompt.get_character_prompts_by_name(name)
    
    async def get_random_character_prompt(self, character_id: int):
        data = await self.character_repository.prompt.get_character_prompts_by_character_id(character_id)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
        
    async def get_random_character_prompt_by_name(self, name: str):
        data = await self.character_repository.prompt.get_character_prompts_by_name(name)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
    
    async def create_character_prompt_by_id(self, character_id: int, prompt: str):
        return await self.character_repository.prompt.create_character_prompt_by_id(character_id, prompt)
    
    async def create_character_prompt_by_name(self, name: str, prompt: str):
        return await self.character_repository.prompt.create_character_prompt_by_name(name, prompt)
    
    async def create_character_image(self, character_id: int, bucket_name: str, key_name: str):
        return await self.character_repository.image.create_character_image(character_id, bucket_name, key_name)
    
    async def get_character_images_by_id(self, character_id: int):
        return await self.character_repository.image.get_character_images_by_id(character_id)
    
    async def get_character_images_by_name(self, name: str):
        return await self.character_repository.image.get_character_images_by_name(name)
    
    async def get_random_character_image_by_id(self, character_id: int):
        data = await self.character_repository.image.get_character_images_by_id(character_id)
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
    
    async def get_random_character_image_by_name(self, name: str):
        data = await self.character_repository.image.get_character_images_by_name(name)
        
        if data:
            return data[random.randint(0, len(data)-1)]
        else:
            return None
    
    async def get_character_image_url_list(self, character_id: int) -> List[CharacterImageURLResponse]:
        data = await self.character_repository.image.get_character_images_by_id(character_id)
        if data:
            return [
                CharacterImageURLResponse(
                    character_image_id=image.id,
                    image_url=self.character_service.get_character_image_url(image.profile_key_name)
                ) for image in data
            ]
        else:
            return []
        
    async def get_character_image_file_list(self, character_id: int) -> List[CharacterImageFileResponse]:
        def get_image(image):
            obj = self.s3.get_object(image.profile_key_name)
            return CharacterImageFileResponse(
                character_image_id=image.id,
                content=obj.get("content"),
                media_type=obj.get("media_type")
            )
        
        data = await self.character_repository.image.get_character_images_by_id(character_id)
        if data:
            return [get_image(image) for image in data]
        else:
            return []
    
    async def get_random_character_image_url_by_id(self, character_id: int) -> CharacterImageURLResponse:
        data = await self.character_repository.image.get_character_images_by_id(character_id)
        if data:
            image = data[random.randint(0, len(data)-1)]
            return CharacterImageURLResponse(
                character_image_id=image.id,
                image_url=self.character_service.get_character_image_url(image.profile_key_name)
            )
        else:
            return None
        
    async def get_random_character_image_file_by_id(self, character_id: int) -> CharacterImageFileResponse:
        data = await self.character_repository.image.get_character_images_by_id(character_id)
        
        if data:
            image = data[random.randint(0, len(data)-1)]
            obj = self.s3.get_object(image.profile_key_name)
            return CharacterImageFileResponse(
                character_image_id=image.id,
                content=obj.get("content"),
                media_type=obj.get("media_type")
            )
        else:
            return None
        
    async def get_random_character_image_url_by_name(self, name: str) -> CharacterImageURLResponse:
        data = await self.character_repository.image.get_character_images_by_name(name)
        
        if data:
            image = data[random.randint(0, len(data)-1)]
            return CharacterImageURLResponse(
                character_image_id=image.id,
                image_url=self.character_service.get_character_image_url(image.profile_key_name)
            )
        else:
            return None
        
    async def get_random_character_image_file_by_name(self, name: str) -> CharacterImageFileResponse:
        data = await self.character_repository.image.get_character_images_by_name(name)
        
        if data:
            image = data[random.randint(0, len(data)-1)]
            obj = self.s3.get_object(image.profile_key_name)
            return CharacterImageFileResponse(
                character_image_id=image.id,
                content=obj.get("content"),
                media_type=obj.get("media_type")
            )
        else:
            return None
        
    async def generate_character_image(self, character_id: int) -> CharacterImageResponse:
        character = await self.character_repository.info.get_character_by_id(character_id)
        if character:
            # Generate image
            prompt = self.image_gen_prompt.format(name=character.name, description=character.description)
            image = await self.image_gen_service.generate(prompt=prompt, quality='standard')
            
            # Set parameters
            now = datetime.now().strftime('%y%m%d%H%M%S')
            filename = f"{character.name}_{now}.png"
            file_path = self.path / filename
            profile_key_name = f"{self.key_name_prefix}/{character.id}/{filename}"
            
            # Save image
            self.image_gen_service.b64_json_to_png(image, file_path)
            
            # Upload image to S3
            self.character_service.upload_character_image_s3(
                key_name=profile_key_name,
                file_path=file_path
            )
            # Create image s3 info in MySQL
            inserted_data = await self.character_repository.image.create_character_image(
                character_id=character_id,
                bucket_name=self.character_service.bucket_name,
                key_name=profile_key_name
            )
            
            return CharacterImageResponse(
                character_name=character.name,
                profile_bucket_name=inserted_data.profile_bucket_name,
                profile_key_name=inserted_data.profile_key_name
            )
            
        else:
            return None