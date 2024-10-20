from typing import Optional
from pydantic import BaseModel, Field

class CharacterInfoCreateRequest(BaseModel):
    name: str = Field(
        ...,
        title='name',
        description='name',
        examples=['Einstein']
    )
    description: str = Field(
        ...,
        title='Description',
        description='Description',
        examples=["A genius physicist"]
    )
    
class CharacterInfoRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
    )
    
class CharacterInfoUpdateRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
    )
    name: Optional[str] = Field(
        None,
        title='name',
        description='name',
        examples=['Einstein']
    )
    description: Optional[str] = Field(
        None,
        title='Description',
        description='Description',
        examples=["A genius physicist"]
    )
    
class CharacterListRequest(BaseModel):
    offset: int = Field(
        0,
        title='offset',
        description='offset',
        examples=[0]
    )
    num: int = Field(
        10,
        title='num',
        description='num',
        examples=[10]
    )