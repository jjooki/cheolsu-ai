from typing import List
from pydantic import BaseModel, Field

from app.model.chat import ChatMessage

class ChatMessageResponse(BaseModel):
    role: str = Field(
        ...,
        title="Role",
        description="Role",
        examples=["user", "assistant"],
    )
    content: str = Field(
        ...,
        title="Message",
        description="Messages",
        examples=["Hello, How are you?"]
    )
    created_at: str = Field(
        ...,
        title="Created At",
        description="Created At",
        examples=["2021-08-01T12:00:00+09:00"]
    )
    
class ChatMessageHistoryResponse(BaseModel):
    room_uuid: str = Field(
        ...,
        title="Room UUID",
        description="Room UUID",
        examples=["47110f3b8b194b419de0c557e9cf259d"]
    )
    messages: List[ChatMessage] = Field(
        ...,
        title="Messages",
        description="Messages"
    )