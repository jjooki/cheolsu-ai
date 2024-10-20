from typing import Optional
from pydantic import BaseModel, Field
from .prompt import CharacterPromptResponse
from .image import CharacterImageFileResponse, CharacterImageURLResponse, CharacterImageResponse
from .info import CharacterInfoResponse

class CharacterResponse(BaseModel):
    character_id: int = Field(
        ...,
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
    character_image_id: Optional[int] = Field(
        None,
        title='character image id',
        description='character image id',
        examples=[1]
    )
    character_image_url: Optional[str] = Field(
        None,
        title='profile image url',
        description='profile image url',
        examples=['https://example.com/image.png']
    )

__all__ = [
    'CharacterImageFileResponse',
    'CharacterImageURLResponse',
    'CharacterImageResponse',
    'CharacterInfoResponse'
]