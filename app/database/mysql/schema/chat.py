from sqlalchemy import (
    Column, Integer, BigInteger, VARCHAR, DateTime, CHAR, ForeignKey, Text
)
from sqlalchemy.sql import func

from app.database.mysql.session import Base

class ChatMessage(Base):
    __tablename__ = 'chat_message'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_room_id = Column(BigInteger, nullable=False)
    role = Column(VARCHAR(8), nullable=False, comment='user, assistant')
    message = Column(VARCHAR(1000))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ChatMessage(role={self.role}, message={self.message})>"

class ChatRoom(Base):
    __tablename__ = 'chat_room'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(CHAR(32), nullable=False, comment='uuid4')
    name = Column(VARCHAR(100))
    user_id = Column(BigInteger)
    character_id = Column(Integer, nullable=False)
    character_image_id = Column(Integer, nullable=False)
    model_name = Column(VARCHAR(100), nullable=False, comment='ex) gpt-4o-mini, gpt-3.5-turbo')
    is_active = Column(CHAR(1), nullable=False, default='0')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<ChatRoom(name={self.name}, is_active={self.is_active})>"

Base.metadata.create_all()