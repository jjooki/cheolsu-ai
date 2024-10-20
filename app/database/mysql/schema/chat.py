from sqlalchemy import (
    Column, Integer, BigInteger, VARCHAR, DateTime, CHAR
)
from sqlalchemy.sql import func

from app.database.mysql.session import Base, base_engine

class ChatMessage(Base):
    __tablename__ = 'chat_message'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_room_id = Column(BigInteger, nullable=False)
    role = Column(VARCHAR(8), nullable=False, comment='user, assistant')
    content = Column(VARCHAR(2000))
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now()
    )
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
    character_prompt_id = Column(Integer, nullable=False)
    character_image_id = Column(Integer, nullable=False)
    model_name = Column(VARCHAR(100), nullable=False, comment='ex) gpt-4o-mini, gpt-3.5-turbo')
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now()
    )
    deleted_at = Column(DateTime)
    
    def __repr__(self):
        return f"<ChatRoom(name={self.name}, uuid={self.uuid})>"

Base.metadata.create_all(bind=base_engine)