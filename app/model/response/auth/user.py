from pydantic import BaseModel, Field
from typing import Optional

class UserResponse(BaseModel):
    id: Optional[int] = Field(
        None,
        description='ID of the admin user',
        examples=[1]
    )
    email: Optional[str] = Field(
        None,
        description='Email of the admin user',
        examples=['aaa@abc.com']
    )
    password: Optional[str] = Field(
        None,
        description='Password of the admin user',
        examples=['Abc12345']
    )
    name: Optional[str] = Field(
        None,
        description='Name of the admin user',
        examples=['John']
    )
    phone: Optional[str] = Field(
        None,
        description='Phone number of the admin user',
        examples=['01012345678']
    )
    country_code: Optional[str] = Field(
        None,
        description='Country code of the admin user',
        examples=['+82']
    )
    role_name: Optional[str] = Field(
        None,
        description='Role name of the user',
        examples=['owner']
    )