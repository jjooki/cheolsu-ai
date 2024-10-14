from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChatHistory:
    room_id: int
    messages: List[str]
    output: str
    model_name: str
    input_tokens: int
    cost_usd: float
    cost_krw: float
    created_at: str
    message_id: Optional[int] = None
    cached_tokens: Optional[int] = None