from typing import Optional
from pydantic import BaseModel, Field

class CharacterInfoResponse(BaseModel):
    character_id: Optional[int] = Field(
        None,
        title='character id',
        description='character id',
        examples=[1]
    )
    name: str = Field(
        ...,
        title='name',
        description='character name',
        examples=['Einstein']
    )
    description: Optional[str] = Field(
        None,
        title='description',
        description='description',
        examples=['historical genius physicist']
    )