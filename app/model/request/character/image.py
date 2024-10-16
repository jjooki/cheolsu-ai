from pydantic import BaseModel, Field

class CharacterImageFileRequest(BaseModel):
    chat_room_id: int = Field(
        1,
        title='chat_room id',
        description='chat_room id',
        examples=[1]
    )
    
class CharacterImageFileListRequest(BaseModel):
    character_id: int = Field(
        1,
        title='character id',
        description='character id',
        examples=[1]
    )