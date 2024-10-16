from pydantic import BaseModel, Field
from typing import Optional

class ChatMessage(BaseModel):
    role: str = Field(
        ...,
        title="Role",
        description="Role",
        examples=["user", "assistant", "system"],
    )
    content: str = Field(
        ...,
        title="Content",
        description="Content",
        examples=["Hello, How are you?"]
    )
    created_at: Optional[str] = Field(
        ...,
        title="Created At",
        description="Created At",
        examples=["2024-10-12T12:00:00+09:00"]
    )
    