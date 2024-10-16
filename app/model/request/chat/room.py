from pydantic import BaseModel, Field
from typing import Optional
    
class ChatRoomCreateRequest(BaseModel):
    room_name: str = Field(
        ...,
        title="Room Name",
        description="Room Name",
        examples=["Talk with einstein"]
    )
    character_id: int = Field(
        1,
        title="Character ID",
        description="Character ID",
        examples=[1]
    )
    llm_model_name: Optional[str] = Field(
        None,
        title="LLM Model Name",
        description="Model Name",
        examples=["gpt-4o-mini", "gpt-3.5-turbo"]
    )
    image_model_name: Optional[str] = Field(
        None,
        title="Image AI Model Name",
        description="Image AI Model Name",
        examples=["dall-e-3"]
    )
    
class ChatRoomRequest(BaseModel):
    room_id: int = Field(
        ...,
        title="Room ID",
        description="Room ID",
        examples=[1]
    )
    
class ChatRoomListRequest(BaseModel):
    user_id: int = Field(
        ...,
        title="User ID",
        description="User ID",
        examples=[1]
    )
    charcter_id: Optional[int] = Field(
        None,
        title="Character ID",
        description="Character ID",
        examples=[1]
    )