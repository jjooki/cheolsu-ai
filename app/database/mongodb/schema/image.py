from dataclasses import dataclass
from typing import List

@dataclass
class ImageHistory:
    room_id: str
    chat_message_id: str
    input: str
    output: bytes
    model_name: str
    cost_usd: float
    cost_krw: float
    created_at: str