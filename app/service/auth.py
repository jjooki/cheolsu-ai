import logging

from typing import Annotated
from fastapi import HTTPException, Depends, status
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
from app.common.config import config
from app.database.mysql.crud.auth import get_refresh_token, get_admin
from app.database.mysql.session import AsyncSession, get_read_session, get_session
from app.model.response.auth import UserResponse
from app.core.utils.auth import UserAuthUtils

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    description="username에 이메일, password에 비밀번호를 입력해주세요"
)
auth = UserAuthUtils()

def authenticate_user(db: AsyncSession, email: str, password: str) -> UserResponse:
    user = get_admin(db, email=email)
    logging.debug(f"Admin: {user}")
    if not user:
        logging.warning("> Not found user")
        return False
    if not auth.verify_password(password, user.password):
        logging.warning("> Password is incorrect")
        return False
    return user

## This is the function that will be used to validate the token
async def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_read_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    logging.debug(f"> [validate refresh token]Token: {token}")
    
    try:
        ## Access token으로 Refresh token을 만들어서 Refresh token이 유효한지 확인
        token_data = auth.decode_token(token, refresh=False)
        refresh_exp = token_data.exp + (config.AUTH.REFRESH_TOKEN_EXPIRE_MINUTES - config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES) * 60
        refresh_token = auth.create_refresh_token(id=token_data.sub,
                                                  expire_timestamp=refresh_exp)
        
        ## 역추산한 Refresh token이 DB에 있는지 확인
        exist_refresh_token = get_refresh_token(db, refresh_token=refresh_token)
        if exist_refresh_token:
            payload = auth.decode_token(exist_refresh_token, refresh=True)
            id: int = int(payload.sub.split(":")[0])
            if id is None:
                raise credentials_exception
            
        else:
            raise credentials_exception
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_admin(db, id=id)
    if user is None:
        raise credentials_exception
    
    return user, token

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_read_session)
) -> UserResponse:
    logging.debug(f"> Token: {token}")
    try:
        payload = auth.decode_token(token, refresh=False)
        logging.debug(f"> Payload: {payload}")
        id: int = int(payload.sub)
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
        
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = get_admin(db, id=id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user


class GradeChecker:
    def __init__(self, allowed_grade: str):
        grade_table = {
            "master": ["master"],
            "owner": ["master", "owner"],
            "manager": ["master", "owner", "manager"],
            "developer": ["master", "owner", "manager", "developer"],
        }
        self.allowed_grades = grade_table[allowed_grade]

    def __call__(self, user: Annotated[UserResponse, Depends(get_current_user)]) -> bool:
        if user.grade in self.allowed_grades:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You don't have enough permissions"
        )