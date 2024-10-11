from dataclasses import dataclass
from typing import List

@dataclass
class ChatHistory:
    room_id: str
    chat_message_id: str
    user_query: str
    messages: List[str]
    output: str
    model_name: str
    token: str
    cost_usd: float
    cost_krw: float
    created_at: str
    updated_at: str
    
class ImageHistory:
    room_id: str
    chat_message_id: str
    user_query: str
    messages: List[str]
    output: bytes
    model_name: str
    cost_usd: float
    cost_krw: float
    created_at: str
    updated_at: str