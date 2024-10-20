from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langsmith import traceable
from typing import Annotated

from app.controller import ChatController
from app.factory import Factory
from app.model.request.chat import ChatMessageRequest
from app.model.response.chat import ChatMessageResponse

router = APIRouter()

@router.post("", response_model=ChatMessageResponse)
async def create_chat_message(
    request: ChatMessageRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
) -> ChatMessageResponse:
    return await chat_controller.generate_chat_message(request=request)

@router.post("/stream")
async def create_chat_message(
    request: ChatMessageRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
) -> StreamingResponse:
    return await chat_controller.generate_chat_message_stream(request=request)