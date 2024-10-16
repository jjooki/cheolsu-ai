from functools import wraps
import pytz
from datetime import datetime
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.completion import Completion
from openai.types.create_embedding_response import CreateEmbeddingResponse

from app.common.config import config
from app.core.constant.openai.price import ChatModelsPrice
from app.database.mongodb.crud.chat import ChatHistory, insert_chat_response

CHAT_MODELS = ChatModelsPrice()

# Decorator to calculate the cost of the model
def calc_cost_chat(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timezone = pytz.timezone(config.TIMEZONE)
        
        room_id = kwargs.get("room_id"),
        messages = kwargs.get("messages", [])
        created_at = datetime.now(timezone).isoformat(timespec="seconds")
        
        if isinstance(result, ChatCompletion) or isinstance(result, Completion):
            model_name = result.model
            usage = result.usage
            input_tokens = usage.prompt_tokens
            cached_tokens = usage.prompt_tokens_details.cached_tokens
            output_tokens = usage.completion_tokens
            reasoning_tokens = usage.completion_tokens_details.reasoning_tokens
        
            if isinstance(result, ChatCompletion):
                output = result.choices[0].message
            else:
                output = result.choices[0].text
            
            model = CHAT_MODELS.find_model(model_name)
            cost_usd = model.calculate_usage_price(
                input=input_tokens, output=output_tokens,
                cached_input=cached_tokens, reasoning_output=reasoning_tokens
            )
            cost_krw = model.convert_currency(cost_usd)
        
        else:
            raise ValueError("Invalid return type")
        
        chat_history = ChatHistory(
            room_id=room_id,
            messages=messages,
            output=output,
            model_name=model_name,
            input_tokens=input_tokens,
            cost_usd=cost_usd,
            cost_krw=cost_krw,
            created_at=created_at,
            cached_tokens=cached_tokens
        )
        insert_chat_response(chat_history)
        
        return result
    return wrapper

def acalc_cost_chat(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        timezone = pytz.timezone(config.TIMEZONE)
        
        room_id = kwargs.get("room_id"),
        messages = kwargs.get("messages", [])
        created_at = datetime.now(timezone).isoformat(timespec="seconds")
        
        if isinstance(result, ChatCompletion) or isinstance(result, Completion):
            model_name = result.model
            usage = result.usage
            input_tokens = usage.prompt_tokens
            cached_tokens = usage.prompt_tokens_details.cached_tokens
            output_tokens = usage.completion_tokens
            reasoning_tokens = usage.completion_tokens_details.reasoning_tokens
        
            if isinstance(result, ChatCompletion):
                output = result.choices[0].message
            else:
                output = result.choices[0].text
            
            model = CHAT_MODELS.find_model(model_name)
            cost_usd = model.calculate_usage_price(
                input=input_tokens, output=output_tokens,
                cached_input=cached_tokens, reasoning_output=reasoning_tokens
            )
            cost_krw = model.convert_currency(cost_usd)
        
        else:
            raise ValueError("Invalid return type")
        
        chat_history = ChatHistory(
            room_id=room_id,
            messages=messages,
            output=output,
            model_name=model_name,
            input_tokens=input_tokens,
            cost_usd=cost_usd,
            cost_krw=cost_krw,
            created_at=created_at,
            cached_tokens=cached_tokens
        )
        insert_chat_response(chat_history)
        
        return result
    return wrapper