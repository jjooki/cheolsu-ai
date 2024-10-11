from sqlalchemy import (
    VARCHAR, Column, Integer, BigInteger, DateTime, CHAR
)
from sqlalchemy.sql import func

from app.database.mysql.session import Base

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    
    token = Column(VARCHAR(200), primary_key=True, autoincrement=True, comment='refresh token')
    created_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<RefreshToken(token={self.token})>"

class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(VARCHAR(100), nullable=False, comment='role name')
    description = Column(VARCHAR(300), comment='description')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Role(role_name={self.role_name})>"

class User(Base):
    __tablename__ = 'user'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(Integer, nullable=False)
    email = Column(VARCHAR(100))
    password = Column(VARCHAR(100))
    name = Column(VARCHAR(100))
    nickname = Column(VARCHAR(100))
    ci = Column(VARCHAR(100))
    address = Column(VARCHAR(255))
    country_code = Column(CHAR(3))
    mobile_number = Column(VARCHAR(50))
    device_type = Column(CHAR(1), comment='1: PC, 2: Mobile')
    mobile_os_type = Column(CHAR(3), comment='aos: Android, ios: iOS')
    birthday = Column(DateTime)
    profile_bucket_name = Column(VARCHAR(200))
    profile_key_name = Column(VARCHAR(200))
    introduce = Column(VARCHAR(500))
    sns_login_type = Column(CHAR(1))
    imei = Column(VARCHAR(100))
    mac_address = Column(VARCHAR(100))
    recommend_code = Column(CHAR(10))
    is_marketing_push_agree = Column(CHAR(1), nullable=False, default='1')
    is_pause = Column(CHAR(1), nullable=False, default='0')
    is_out = Column(CHAR(1), nullable=False, default='0')
    marketing_push_agreed_at = Column(DateTime)
    out_at = Column(DateTime)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(email={self.email}, name={self.name})>"
    
Base.metadata.create_all()