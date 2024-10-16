import random
from typing import Optional

from app.repository.character import CharacterRepository
from app.repository.chat import ChatRepository
from app.service.agent.generator.image import ImageGeneratorService
from app.service.agent.generator.chat import ChatGeneratorService

class ChatController:
    def __init__(
        self,
        character_repository: CharacterRepository,
        chat_repository: ChatRepository
    ):
        self.character_repository = character_repository
        self.chat_repository = chat_repository
        
    