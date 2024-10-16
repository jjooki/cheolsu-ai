from sqlalchemy.ext.asyncio import AsyncSession

from .image import CharacterImageRepository
from .info import CharacterInfoRepository
from .prompt import CharacterPromptRepository

class CharacterRepository:
    def __init__(self, read_session: AsyncSession, write_session: AsyncSession):
        self.image = CharacterImageRepository(read_session, write_session)
        self.info = CharacterInfoRepository(read_session, write_session)
        self.prompt = CharacterPromptRepository(read_session, write_session)