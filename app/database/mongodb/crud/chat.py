from typing import List

from app.database.mongodb.schema.chat import ChatHistory
from app.database.mongodb.session import MongoHandler

def insert_chat_response(chat_history: ChatHistory) -> str:
    with MongoHandler(db_name="cheolsu", collection_name="chat_log") as mongo:
        # Get the latest message_id
        chat_log = read_chat_response(room_id=chat_history.room_id)
        if chat_log:
            message_id = chat_log[0].message_id + 1
            chat_history.message_id = message_id
        else:
            chat_history.message_id = 0
        
        # Insert the chat history
        result = mongo.insert_one(data=chat_history.__dict__)
    
    return result

def read_chat_response(room_id: int) -> List[ChatHistory]:
    with MongoHandler(db_name="cheolsu", collection_name="chat_log") as mongo:
        result = mongo.find_many(condition={"room_id": room_id}, sort=[("message_id", -1)])
        
    if result:
        new_result = []
        for data in result:
            data.pop("_id")
            new_result.append(ChatHistory(**data))
        
        return new_result
    
    else:
        return []