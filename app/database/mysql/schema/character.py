from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, CHAR, ForeignKey, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.mysql.session import Base

class Character(Base):
    __tablename__ = 'character'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False, comment='character name')
    description = Column(String(500), comment='character system prompt')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Character(name={self.name}, description={self.description})>"
    
class CharacterPrompt(Base):
    __tablename__ = 'character_prompt'
    
    id = Column(Integer, primary_key=True, nullable=False)
    character_id = Column(Integer, nullable=False, comment='character.id')
    prompt = Column(Text, nullable=False, comment='character system prompt')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<CharacterPrompt(character_id={self.character_id}, prompt={self.prompt})>"

class CharacterImage(Base):
    __tablename__ = 'character_image'
    
    id = Column(Integer, primary_key=True, nullable=False)
    character_id = Column(Integer, nullable=False)
    profile_bucket_name = Column(String(200), comment='S3 bucket name')
    profile_key_name = Column(String(200), comment='S3 key name')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<CharacterImage(character_id={self.character_id})>"

class UserCharacterImage(Base):
    __tablename__ = 'user_character_image'
    
    id = Column(Integer, primary_key=True, nullable=False)
    character_image_id = Column(Integer, nullable=False, comment='character_image.id')
    user_id = Column(BigInteger, nullable=False, comment='user.id')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<UserCharacterImage(user_id={self.user_id}, character_image_id={self.character_image_id})>"