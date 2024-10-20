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
        examples=[
            {"role": "user", "content": "Hello, How are you?"},
            {"role": "assistant", "content": "I am fine, thank you!"},
            {"role": "user", "content": "What are you doing?"}
        ]
    )

class ChatHistoryRequest(BaseModel):
    room_uuid: int = Field(
        ...,
        title="Chat Room ID",
        description="Chat Room ID",
        examples=[1]
    )
