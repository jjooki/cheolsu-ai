from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, CHAR, ForeignKey, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.mysql.session import Base

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    
    token = Column(String(200), primary_key=True, nullable=False, comment='refresh token')
    created_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<RefreshToken(token={self.token})>"

class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String(100), nullable=False, comment='role name')
    description = Column(String(300), nullable=True, comment='description')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Role(role_name={self.role_name})>"

class User(Base):
    __tablename__ = 'user'
    
    id = Column(BigInteger, primary_key=True, nullable=False)
    role_id = Column(Integer, nullable=False)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    name = Column(String(100), nullable=True)
    nickname = Column(String(100), nullable=True)
    ci = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    country_code = Column(CHAR(3), nullable=True)
    mobile_number = Column(String(50), nullable=True)
    mobile_os_type = Column(CHAR(3), nullable=True)
    birthday = Column(DateTime, nullable=True)
    profile_bucket_name = Column(String(200), nullable=True)
    profile_key_name = Column(String(200), nullable=True)
    introduce = Column(String(500), nullable=True)
    sns_login_type = Column(CHAR(1), nullable=True)
    imei = Column(String(100), nullable=True)
    recommend_code = Column(CHAR(10), nullable=True)
    is_marketing_push_agree = Column(CHAR(1), nullable=False, default='1')
    is_pause = Column(CHAR(1), nullable=False, default='0')
    is_out = Column(CHAR(1), nullable=False, default='0')
    marketing_push_agreed_at = Column(DateTime, nullable=True)
    out_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(email={self.email}, name={self.name})>"