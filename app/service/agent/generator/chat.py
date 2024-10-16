import json
import os

from datetime import datetime
from openai import OpenAI, AsyncOpenAI
from openai.types.completion import Completion
from openai.types.chat.chat_completion import ChatCompletion, ChatCompletionMessage
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Any, List, Optional, Union

from app.common.config import config
from app.core.decorator import calc_cost_chat, acalc_cost_chat
from app.model.chat import ChatMessage
from app.model.response.chat import ChatMessageResponse
from app.service.agent.exception import ahandle_openai_exception, handle_openai_exception

class ChatGeneratorService:
    def __init__(
        self,
        chat_model: Optional[str] = None,
        completion_model: Optional[str] = None
    ):
        self.client = OpenAI(api_key=config.OPENAI.API_KEY)
        self.aclient = AsyncOpenAI(api_key=config.OPENAI.API_KEY)
        self.chat_model = chat_model or config.OPENAI.CHAT_MODEL
        self.completion_model = completion_model or config.OPENAI.COMPLETION_MODEL

    def set_chat_to_response(self, chat: str) -> ChatMessageResponse:
        return ChatMessageResponse(role='assistant', message=chat, created_at=datetime.now())
    
    def run_chat(
        self,
        messages: Union[List[ChatMessage], List[ChatCompletionMessage]],
        **kwargs: Any
    ) -> ChatMessageResponse:
        response = self.chat(messages, **kwargs)
        return self.set_chat_to_response(response.choices[0].message)
    
    async def arun_chat(
        self,
        messages: Union[List[ChatMessage], List[ChatCompletionMessage]],
        **kwargs: Any
    ) -> ChatMessageResponse:
        response = await self.achat(messages, **kwargs)
        return self.set_chat_to_response(response.choices[0].message)
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    @ahandle_openai_exception
    async def arun_function_calling(self, input: str, tools: List[Any], functions: List[Any]):
        response = None
        messages = [{"role": "user", "content": input}]
        openai_response = await self.aclient.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat"),
            messages=messages,  # type: ignore
            tools=tools,
            tool_choice="auto",
        )

        openai_response_message = openai_response.choices[0].message
        tool_calls = openai_response_message.tool_calls

        if tool_calls:
            messages.append(openai_response_message)  # type: ignore

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # fix function name due to gpt's typo
                if function_name == "search_information_on_milkabu_jp":
                    function_name = "search_information_on_minkabu_jp"
                function_to_call = functions[function_name]  # type: ignore
                function_args: dict = json.loads(tool_call.function.arguments)
                if "search_string" in function_args.keys():
                    function_args.update({"search_query": function_args.pop("search_string")})
                function_response = function_to_call(**function_args)

                response = function_response
        else:
            response = None

        return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    @ahandle_openai_exception
    @acalc_cost_chat
    async def achat(self, model: str, messages: List[ChatCompletionMessage], **kwargs: Any) -> ChatCompletion:
        response: ChatCompletion = await self.aclient.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    @ahandle_openai_exception
    @acalc_cost_chat
    async def acompletion(self, input, **kwargs) -> Completion:
        response: Completion = await self.aclient.completions.create(
            model=config.OPENAI.COMPLETION_MODEL,
            prompt=input,
            **kwargs
        )
        raise response
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    @handle_openai_exception
    @calc_cost_chat
    def chat(
        self,
        messages: List[ChatCompletionMessage],
        model: Optional[str] = None,
        **kwargs: Any
    ) -> ChatCompletion:
        response = self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        return response
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    @handle_openai_exception
    @calc_cost_chat
    def completion(self, input, **kwargs):
        response: Completion = self.client.completions.create(
            model=config.OPENAI.COMPLETION_MODEL,
            prompt=input,
            **kwargs
        )
        raise response