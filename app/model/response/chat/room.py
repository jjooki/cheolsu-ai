from pydantic import BaseModel, Field
from typing import Optional

class ChatRoomResponse(BaseModel):
    room_uuid: str = Field(
        ...,
        title="Chat Room UUID",
        description="Chat Room UUID",
        examples=["47110f3b8b194b419de0c557e9cf259d"]
    )
    room_name: str = Field(
        ...,
        title="Room Name",
        description="Room Name",
        examples=["Talk with einstein"]
    )
    user_name: Optional[str] = Field(
        None,
        title="User Name",
        description="User Name",
        examples=["Guest_roomId"]
    )
    user_profile_image_url: Optional[str] = Field(
        None,
        title="User Profile Image URL",
        description="User Profile Image URL",
        examples=["https://example.com/user_image.png"]
    )
    character_name: Optional[str] = Field(
        None,
        title="Character Name",
        description="Character Name",
        examples=["Einstein"]
    )
    character_profile_image_url: Optional[str] = Field(
        None,
        title="Character Profile Image URL",
        description="Character Profile Image URL",
        examples=["https://example.com/character_image.png"]
    )
    created_at: Optional[str] = Field(
        None,
        title="Created At",
        description="Created At",
        examples=["2024-10-12T12:00:00+09:00"]
    )
    updated_at: Optional[str] = Field(
        None,
        title="Updated At",
        description="Updated At",
        examples=["2024-10-12T12:00:00+09:00"]
    )