import logging

from app.common.config import config
from app.database.mysql.schema.auth import (
    User, Role, RefreshToken
)
from app.database.mysql.session import AsyncSession
from app.model.response.auth import UserResponse
from app.model.request.auth import UserCreateRequest
from app.core.utils.auth import UserAuthUtils

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

auth = UserAuthUtils()

logger = logging.getLogger(__name__)

def get_user(db: Session, id: int=0, email: str=None) -> UserResponse:
    if isinstance(id, int) and id > 0:
        user = db.query(User).filter(
            and_(
                User.id == id,
                User.is_out == '0'
            )
        ).scalar()
    
    elif email:
        user = db.query(
            User
        ).filter(
            and_(
                User.email == email,
                User.is_out == '0'
            )
        ).scalar()
    
    if user:
        result = UserResponse(**user.__dict__)
        logging.debug(f"> user: {result}")
        return result
    else:
        return None

def create_user(db: Session, user: UserCreateRequest) -> User:
    hashed_password = auth.hash_password(user.password)
    
    db_user = User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    return db_user
    
def get_refresh_token(db: Session, refresh_token: str) -> str:
    return db.query(RefreshToken.token).filter(
        RefreshToken.token == refresh_token
    ).scalar()

def insert_refresh_token(db: Session, refresh_token: str) -> None:
    db_token = RefreshToken(token=refresh_token)
    db.add(db_token)
    db.commit()

def delete_refresh_token(db: Session, refresh_token: str) -> None:
    db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).delete()
    db.commit()
    
def delete_old_refresh_tokens(db: Session) -> None:
    time_ = datetime.now(timezone.utc) - timedelta(minutes=config.AUTH.REFRESH_TOKEN_EXPIRE_MINUTES)
    db.query(RefreshToken).filter(
        RefreshToken.created_at < time_
    ).delete()
    db.commit()