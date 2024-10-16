from pydantic import BaseModel, Field


class CharacterInfoRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
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