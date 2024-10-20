from pydantic import BaseModel, Field

class CharacterPromptResponse(BaseModel):
    character_id: int = Field(
        ...,
        title='character id',
        description='character id',
        examples=[1]
    )
    prompt: str = Field(
        ...,
        title='prompt',
        description='prompt',
        examples=['What is the meaning of life?']
    )