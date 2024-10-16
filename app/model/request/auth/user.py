import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

class UserCreateRequest(BaseModel):
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
    role_name: str = Field(
        'developer',
        description='Grade of the admin user',
        examples=['owner']
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

class UserUpdateRequest(BaseModel):
    password: Optional[str] = Field(
        None,
        description='Password of the admin user',
        examples=['Abc12345']
    )
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