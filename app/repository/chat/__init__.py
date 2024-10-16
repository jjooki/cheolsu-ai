from sqlalchemy.ext.asyncio import AsyncSession

from .message import ChatMessageRepository
from .room import ChatRoomRepository

class ChatRepository:
    def __init__(self, read_session: AsyncSession, write_session: AsyncSession):
        self.room = ChatRoomRepository(read_session, write_session)
        self.message = ChatMessageRepository(read_session, write_session)