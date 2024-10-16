from pydantic import BaseModel, Field

class CharacterPromptRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
    )
    
class CharacterPromptListRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
    )
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