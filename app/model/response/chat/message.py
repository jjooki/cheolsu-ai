from pydantic import BaseModel, Field

class ChatMessageResponse(BaseModel):
    role: str = Field(
        ...,
        title="Role",
        description="Role",
        examples=["user", "assistant"],
    )
    message: str = Field(
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