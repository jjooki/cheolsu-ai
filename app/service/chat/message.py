import pytz
import random
import uuid

from datetime import datetime
from typing import List, Optional

from app.common.config import config
from app.core.utils.aws import S3
from app.database.mysql.schema.character import CharacterImage, CharacterPrompt
from app.model.response.chat import ChatRoomResponse, ChatMessageResponse, ChatMessageHistoryResponse
from app.repository.character import CharacterRepository
from app.repository.chat import ChatRepository

class ChatMessageService:
    def __init__(self,
                 chat_repository: ChatRepository,
                 character_repository: CharacterRepository):
        self.chat_repository = chat_repository
        self.character_repository = character_repository
    
    def get_random_character_prompt(self, prompts: List[CharacterPrompt]) -> CharacterPrompt:
        if prompts:
            return random.choice(prompts)
        else:
            return None
    
    def get_random_character_image(self, images: List[CharacterImage]) -> CharacterImage:
        if images:
            return random.choice(images)
        else:
            return None
    
    async def create_chat_room(
        self,
        character_id: int,
        user_id: Optional[int]=None,
        room_name: Optional[str]=None,
        llm_model_name: Optional[str]=None,
    ) -> ChatRoomResponse:
        character_info = await self.character_repository.info.get_character_by_id(character_id=character_id)
        prompts = await self.character_repository.prompt.get_character_prompts_by_character_id(character_id=character_id)
        images = await self.character_repository.image.get_character_images_by_id(character_id=character_id)
        
        # Generate a unique UUID for the chat room
        _uuid = uuid.uuid4().hex
        # Get the current time in the specified timezone
        now = datetime.now(pytz.timezone(config.TIMEZONE)).isoformat(timespec='seconds')

        # Select a random prompt and image
        prompt = self.get_random_character_prompt(prompts)
        image = self.get_random_character_image(images)
        
        # If room_name is not provided, use the character's name
        room_name = room_name or f'Talk with {character_info.name}'
        
        if user_id:
            # To-do: Get user name and profile image
            user_name = "User"
            user_profile_image_url = None
        else:
            user_name = "Guest"
            user_profile_image_url = self.s3.get_object_url(bucket_name=self.bucket_name,
                                                            key_name="profile/user/default/profile.png",
                                                            expiration=config.S3.EXPIRATION)
        
        character_image_url = self.s3.get_object_url(bucket_name=self.bucket_name,
                                                     key_name=image.profile_key_name,
                                                     expiration=config.S3.EXPIRATION)
        # Insert chat room info into the database
        room_info = await self.chat_repository.room.create_chat_room(
            uuid=_uuid,
            room_name=room_name,
            character_id=character_id,
            character_prompt_id=prompt.id,
            character_image_id=image.id,
            model_name=llm_model_name,
            user_id=user_id,
        )
        
        return ChatRoomResponse(
            room_uuid=room_info.uuid,
            room_name=room_info.name,
            user_name=user_name,
            user_profile_image_url=user_profile_image_url,
            character_name=character_info.name,
            character_profile_image_url=character_image_url,
            created_at=now,
        )
    
    async def get_chat_room(self, uuid: str) -> ChatRoomResponse:
        room_info = await self.chat_repository.room.get_room_info(uuid)
        
        character_info = await self.character_repository.info.get_character_by_id(
            character_id=room_info.character_id
        )
        prompt = await self.character_repository.prompt.get_character_prompt_by_id(
            character_prompt_id=room_info.character_prompt_id
        )
        image = await self.character_repository.image.get_character_image_by_id(
            character_image_id=room_info.character_image_id
        )
        
        if room_info.user_id:
            # To-do: Get user name and profile image
            user_name = "User"
            user_profile_image_url = None
        else:
            user_name = "Guest"
            user_profile_image_url = self.s3.get_object_url(
                bucket_name=self.bucket_name,
                key_name="profile/user/default/profile.png",
                expiration=config.S3.EXPIRATION
            )
            
        character_image_url = self.s3.get_object_url(
            bucket_name=self.bucket_name,
            key_name=image.profile_key_name,
            expiration=config.S3.EXPIRATION
        )
        
        return ChatRoomResponse(
            room_uuid=room_info.uuid,
            room_name=room_info.name,
            user_name=user_name,
            user_profile_image_url=user_profile_image_url,
            character_name=character_info.name,
            character_prompt_id=prompt.id,
            character_profile_image_url=character_image_url,
            created_at=room_info.created_at,
            updated_at=room_info.updated_at,
        )
        
    async def get_chat_room_history(self, uuid: str, limit: int=100) -> ChatMessageHistoryResponse:
        room_info = await self.chat_repository.room.get_room_info(uuid)
        messages = await self.chat_repository.message.get_latest_chat_messages(
            chat_room_id=room_info.id,
            limit=limit
        )
        messages = [
            ChatMessageResponse(
                role=message.role,
                content=message.content,
                created_at=message.created_at,
            ) for message in messages
        ]
        return ChatMessageHistoryResponse(
            room_uuid=room_info.uuid,
            messages=messages,
        )