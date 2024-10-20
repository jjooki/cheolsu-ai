from fastapi import Depends
from functools import partial

from app.controller import CharacterController, ChatController
from app.database.mysql.session import AsyncSession, get_session, get_read_session
from app.repository import CharacterRepository, ChatRepository

class Factory:
    chat_repository = partial(ChatRepository)
    character_repository = partial(CharacterRepository)
    
    def get_character_controller(
        self,
        write_session: AsyncSession = Depends(get_session),
        read_session: AsyncSession = Depends(get_read_session)
    ) -> CharacterController:
        return CharacterController(
            character_repository=self.character_repository(
                read_session=read_session, write_session=write_session
            ),
            chat_repository=self.chat_repository(
                read_session=read_session, write_session=write_session
            )
        )
        
    def get_chat_controller(
        self,
        write_session: AsyncSession = Depends(get_session),
        read_session: AsyncSession = Depends(get_read_session)
    ) -> ChatController:
        return ChatController(
            character_repository=self.character_repository(
                read_session=read_session, write_session=write_session
            ),
            chat_repository=self.chat_repository(
                read_session=read_session, write_session=write_session
            )
        )