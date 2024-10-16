from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langsmith import traceable
from datetime import datetime
from typing import Iterable, List

from app.model.request.chat import ChatMessageRequest
from app.model.response.chat import ChatMessageResponse

router = APIRouter()

@router.post("", response_model=ChatMessageResponse)
async def create_chatbot_message(
    room_id: str,
    message: str
) -> ChatMessageResponse:
    pass

@router.post("/guest", response_model=ChatMessageResponse)
async def create_guest_chatbot_message(
    room_id: str,
    message: str
) -> ChatMessageResponse:
    pass

@router.post("/stream")
async def create_chatbot_stream_message(
    room_id: str,
    message: str
) -> StreamingResponse:
    pass

@router.post("/stream/guest")
async def create_chatbot_stream_message(
    room_id: str,
    message: str
) -> StreamingResponse:
    pass