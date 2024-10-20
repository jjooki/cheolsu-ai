from asyncer import asyncify
from fastapi.responses import StreamingResponse
from openai.types.chat import ChatCompletionMessage
from typing import List, Optional

from app.model.request.chat import (
    ChatRoomCreateRequest,
    ChatRoomListRequest,
    ChatRoomRequest,
    ChatMessage,
    ChatMessageRequest,
    ChatHistoryRequest,
)
from app.model.response.chat import (
    ChatRoomResponse,
    ChatMessageResponse,
    ChatMessageHistoryResponse
)
from app.repository.character import CharacterRepository
from app.repository.chat import ChatRepository
from app.service.agent.generator.chat import ChatGeneratorService
from app.service.character import CharacterService
from app.service.chat.room import ChatRoomService

class ChatController:
    def __init__(
        self,
        character_repository: CharacterRepository,
        chat_repository: ChatRepository,
    ):
        self.character_repository = character_repository
        self.chat_repository = chat_repository
        self.character_service = CharacterService()
        self.chat_gen_service = ChatGeneratorService()
        self.chat_room_service = ChatRoomService(
            chat_repository=chat_repository,
            character_repository=character_repository,
        )
    
    async def make_full_prompt(
        self,
        messages: List[ChatMessage],
        character_id: Optional[int]=None,
        character_prompt_id: Optional[int]=None
    ) -> List[ChatCompletionMessage]:
        assert character_id or character_prompt_id, 'Either character_id or character_prompt_id must be provided'
        
        messages = [
            ChatCompletionMessage(role=message.role, content=message.content)\
                for message in messages
        ]
        
        if character_prompt_id:
            prompt = await self.character_repository.prompt.get_character_prompt_by_id(character_prompt_id=character_prompt_id)
        elif character_id:
            prompt = await self.character_repository.prompt.get_character_prompt_by_character_id(character_id=character_id)
            
        if prompt:
            system_prompt = ChatCompletionMessage(
                role='system',
                content=prompt.prompt,
            )
            return [system_prompt] + messages
        
        else:
            return messages
    
    async def create_chat_room(self,
                               request: ChatRoomCreateRequest,
                               user_id: Optional[int]=None) -> ChatRoomResponse:
        response = await self.chat_room_service.create_chat_room(
            character_id=request.character_id,
            user_id=user_id,
            room_name=request.room_name,
            llm_model_name=request.llm_model_name,
        )
        return response
    
    async def get_chat_room(self, request: ChatRoomRequest) -> ChatRoomResponse:
        room_info = await self.chat_room_service.get_chat_room(uuid=request.room_uuid)
        return room_info
    
    async def generate_chat_message(self, request: ChatMessageRequest) -> ChatMessageResponse:
        room_info = await self.chat_repository.room.get_room_info(uuid=request.room_uuid)
        if len(request.messages) > 10:
            request.messages = request.messages[-10:]
            
        full_prompt = await self.make_full_prompt(request.messages, character_prompt_id=room_info.character_prompt_id)
        
        # Run the chat generation    
        completion = await self.chat_gen_service.arun_chat(full_prompt)
        return completion
    
    async def generate_chat_message_stream(self, request: ChatMessageRequest) -> StreamingResponse:
        room_info = await self.chat_repository.room.get_room_info(uuid=request.room_uuid)
        full_prompt = await self.make_full_prompt(request.messages, character_prompt_id=room_info.character_prompt_id)
        
        async def generate(messages):
            async for chunk in self.chat_gen_service.arun_chat_stream(messages):
                yield chunk
        
        return await asyncify(StreamingResponse)(
            generate(full_prompt),
            media_type="text/event-stream",
            status_code=200,
        )
    
    async def get_user_chat_history(self, request: ChatHistoryRequest) -> ChatMessageHistoryResponse:
        return await self.chat_room_service.get_chat_room_history(uuid=request.room_uuid)
        