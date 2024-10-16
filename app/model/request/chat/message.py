from pydantic import BaseModel, Field

class ChatMessageRequest(BaseModel):
    chat_room_id: int = Field(
        ...,
        title="Chat Room ID",
        description="Chat Room ID",
        examples=[1]
    )
    message: str = Field(
        ...,
        title="Message",
        description="Messages",
        examples=["Hello, How are you?"]
    )

class UserChatHistoryRequest(BaseModel):
    chat_room_id: int = Field(
        ...,
        title="Chat Room ID",
        description="Chat Room ID",
        examples=[1]
    )
