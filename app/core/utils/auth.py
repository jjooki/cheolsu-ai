from bcrypt import hashpw, gensalt, checkpw
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.common.config import config

@dataclass
class DecodedToken:
    sub: str
    exp: int

class UserAuthUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        return hashed_password.decode()

    @staticmethod
    def verify_password(input_password: str, db_password: str) -> bool:
        return checkpw(input_password.encode(), db_password.encode())

    @staticmethod
    def create_access_token(id: int,
                            expires_delta: int=None) -> str:
        if expires_delta:
            expires_delta = datetime.now(timezone.utc) \
                + timedelta(minutes=expires_delta)
        else:
            expires_delta = datetime.now(timezone.utc) \
                + timedelta(minutes=config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        encode_data = {"sub": f"{id}", "exp": expires_delta}
        encoded_jwt = jwt.encode(encode_data,
                                 config.AUTH.JWT_SECRET_KEY,
                                 algorithm=config.AUTH.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(id: str,
                             expires_delta: int=None,
                             expire_timestamp: int=None) -> str:
        if expires_delta:
            expires_delta = datetime.now(timezone.utc)\
                + timedelta(minutes=expires_delta)
        else:
            if expire_timestamp:
                expires_delta = expire_timestamp
            else:
                expires_delta = datetime.now(timezone.utc)\
                    + timedelta(minutes=config.AUTH.REFRESH_TOKEN_EXPIRE_MINUTES)
                
        encode_data = {"sub": f"{id}:refresh", "exp": expires_delta}
        encoded_jwt = jwt.encode(encode_data,
                                 config.AUTH.JWT_REFRESH_SECRET_KEY,
                                 algorithm=config.AUTH.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str, refresh: bool=False) -> DecodedToken:
        payload = jwt.decode(
            token,
            config.AUTH.JWT_REFRESH_SECRET_KEY if refresh else config.AUTH.JWT_SECRET_KEY,
            algorithms=[config.AUTH.JWT_ALGORITHM]
        )
        return DecodedToken(**payload)