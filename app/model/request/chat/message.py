from typing import List, Optional
from pydantic import BaseModel, Field

from app.model.chat import ChatMessage
    
class ChatMessageRequest(BaseModel):
    room_uuid: str = Field(
        ...,
        title="Room ID",
        description="Room ID",
        examples=["47110f3b8b194b419de0c557e9cf259d"]
    )
    messages: List[ChatMessage] = Field(
        ...,
        title="Messages",
        description="Messages",
        examples=[[
            {"role": "user", "content": "Hello, How are you?", "created_at": "2024-10-15T00:00:00+09:00"},
            {"role": "assistant", "content": "I am fine, thank you!", "created_at": "2024-10-15T00:00:00+09:00"},
            {"role": "user", "content": "What are you doing?", "created_at": "2024-10-15T00:00:00+09:00"}
        ]]
    )

class ChatHistoryRequest(BaseModel):
    room_uuid: int = Field(
        ...,
        title="Chat Room ID",
        description="Chat Room ID",
        examples=[1]
    )
    
class ChatLike(BaseModel):
    message_id: int = Field(
        ...,
        title="Message ID",
        description="Message ID",
        examples=[1]
    )
    like: int = Field(
        ...,
        title="Like",
        description="1: Like, -1: Unlike, 0: Cancel",
        examples=[1, -1, 0]
    )