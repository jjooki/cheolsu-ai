import re

from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

class GuestCreateModel(BaseModel):
    imei: Optional[str] = Field(
        None,
        description="identified number of mobile device"
    )
    device_type: str = Field(
        "mobile",
        description="The type of device, pc or mobile"
    )
    mac_address : str = Field(
        None,
        description="MAC address"
    )

class UserCreateModel(BaseModel):
    email: str = Field(
        ...,
        description='Email of the admin user',
        examples=['abc123@def.com']
    )
    password: str = Field(
        ...,
        description='Password of the admin user. Must be at least 8 characters long and contain at least one digit and one uppercase letter.',
        examples=['Abc12345']
    )
    enterprise_id: int = Field(
        ...,
        description='Enterprise ID of the admin user',
        examples=[1]
    )
    name: Optional[str] = Field(
        None,
        description='Name of the admin user',
        examples=['cjpark']
    )
    phone: Optional[str] = Field(
        None,
        description='Phone number of the admin user',
        examples=['01012345678']
    )
    country_code: Optional[int] = Field(
        '82',
        description='Country code of the phone number',
        examples=['82']
    )
    role: Literal['master', 'admin', 'user', 'guest'] = Field(
        'developer',
        description='Grade of the admin user',
        examples=['owner']
    )
    
    @field_validator('email')
    def check_email(cls, v):
        if v == '' or v is None:
            raise HTTPException(status_code=400, detail='Email cannot be empty')
            
        elif not isinstance(v, str):
            raise HTTPException(status_code=422, detail='Invalid email type')
        
        elif not email_regex.match(v):
            raise HTTPException(status_code=422, detail='Invalid email format')
        return v
    
    @field_validator('password')
    def check_password(cls, v):
        if v == '' or v is None:
            raise ValueError('Password cannot be empty')
        
        elif not isinstance(v, str):
            raise ValueError('Invalid password type')
        
        elif len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        
        elif not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        
        elif not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        return v
    
    @field_validator('enterprise_id')
    def check_enterprise_id(cls, v):
        if v is None:
            raise ValueError('Enterprise ID cannot be empty')
        
        elif  v < 1:
            raise ValueError('Invalid enterprise ID')
        
        elif not isinstance(v, int):
            raise ValueError('Invalid enterprise ID type')
        
        return v

class AdminUpdateModel(BaseModel):
    name: Optional[str] = Field(
        None,
        description='Name of the admin user',
        examples=['cjpark']
    )
    phone: Optional[str] = Field(
        None,
        descripion='Phone number of the admin user',
        examples=['01012345678']
    )
    country_code: Optional[str] = Field(
        None,
        description='Country code of the phone number',
        examples=['82']
    )

class AdminModel(BaseModel):
    id: int | None = None
    email: str
    password: str
    enterprise_id: int
    name: str | None = None
    phone: str | None = None
    country_code: str | None = None
    grade: Literal['master', 'owner', 'manager', 'developer']
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    
class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None

class TokenData(BaseModel):
    id: int | None = None