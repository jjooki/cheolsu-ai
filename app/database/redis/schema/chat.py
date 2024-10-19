from typing import List
from redis_om import JsonModel, EmbeddedJsonModel
from app.database.redis.session import RedisOMConnection

class ChatMessage(EmbeddedJsonModel):
    role: str
    content: str
    created_at: str
    
    class Meta:
        database = RedisOMConnection.get_connection()  # 비동기 Redis 커넥션 사용
    
class ChatMessageHistory(JsonModel):
    room_uuid: str
    messages: List[ChatMessage]
    
    class Meta:
        database = RedisOMConnection.get_connection()  # 비동기 Redis 커넥션 사용