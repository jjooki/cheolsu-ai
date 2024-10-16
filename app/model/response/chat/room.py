from pydantic import BaseModel, Field
from typing import Optional

class ChatRoomResponse(BaseModel):
    room_id: int = Field(
        ...,
        title="Chat Room ID",
        description="Chat Room ID",
        examples=[1]
    )
    room_name: str = Field(
        ...,
        title="Room Name",
        description="Room Name",
        examples=["Talk with einstein"]
    )
    user_name: str = Field(
        ...,
        title="User Name",
        description="User Name",
        examples=["Guest_roomId"]
    )
    user_profile_image: bytes = Field(
        ...,
        title="User Image",
        description="User Image",
        examples=["bytes"]
    )
    character_name: int = Field(
        1,
        title="Character ID",
        description="Character ID",
        examples=[1]
    )
    character_profile_image: bytes = Field(
        ...,
        title="Character Image",
        description="Character Image",
        examples=["bytes"]
    )
    created_at: str = Field(
        ...,
        title="Created At",
        description="Created At",
        examples=["2024-10-12T12:00:00+09:00"]
    )
    updated_at: str = Field(
        ...,
        title="Updated At",
        description="Updated At",
        examples=["2024-10-12T12:00:00+09:00"]
    )
    
class UserChatRoomRequest(BaseModel):
    room_id: int = Field(
        ...,
        title="Room ID",
        description="Room ID",
        examples=[1]
    )
    user_id: int = Field(
        ...,
        title="User ID",
        description="User ID",
        examples=[1]
    )
    
class UserChatRoomListRequest(BaseModel):
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