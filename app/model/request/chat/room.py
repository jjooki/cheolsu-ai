from pydantic import BaseModel, Field
from typing import Optional
    
class ChatRoomCreateRequest(BaseModel):
    character_id: int = Field(
        1,
        title="Character ID",
        description="Character ID",
        examples=[1]
    )
    room_name: Optional[str] = Field(
        None,
        title="Room Name",
        description="Room Name",
        examples=["Talk with einstein"]
    )
    llm_model_name: Optional[str] = Field(
        None,
        title="LLM Model Name",
        description="Model Name",
        examples=["gpt-4o-mini", "gpt-3.5-turbo"]
    )
    
class ChatRoomRequest(BaseModel):
    room_uuid: int = Field(
        ...,
        title="Room ID",
        description="Room ID",
        examples=["47110f3b8b194b419de0c557e9cf259d"]
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