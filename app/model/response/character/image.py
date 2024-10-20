from pydantic import BaseModel, Field

class CharacterImageURLResponse(BaseModel):
    character_image_id: int = Field(
        ...,
        title='character image id',
        description='character image id',
        examples=[1]
    )
    image_url: str = Field(
        ...,
        title='image url',
        description='image url',
        examples=['https://example.com/image.png']
    )
    
class CharacterImageFileResponse(BaseModel):
    character_image_id: int = Field(
        ...,
        title='character image id',
        description='character image id',
        examples=[1]
    )
    content: bytes = Field(
        ...,
        title='content',
        description='image content',
        examples=[b'bytes']
    )
    media_type: str = Field(
        ...,
        title='media type',
        description='media type',
        examples=['image/png']
    )
    
class CharacterImageResponse(BaseModel):
    character_name: str = Field(
        ...,
        title='character name',
        description='character name',
        examples=['Einstein']
    )
    profile_bucket_name: str = Field(
        ...,
        title='profile bucket name',
        description='S3 bucket name',
        examples=['example-bucket']
    )
    profile_key_name: str = Field(
        ...,
        title='profile key name',
        description='S3 key name',
        examples=['example-key/image.png']
    )
