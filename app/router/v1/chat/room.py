import json
import os
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from langsmith import traceable
from datetime import datetime
from typing import Iterable, List, Annotated

from app.common.config import config
from app.controller import ChatController, CharacterController
from app.factory import Factory
from app.model.request.chat import ChatRoomCreateRequest, ChatRoomRequest, ChatHistoryRequest
from app.model.response.chat import ChatRoomResponse, ChatMessageHistoryResponse
router = APIRouter()

@router.post("", response_model=ChatRoomResponse)
async def post_chat_room(
    request: ChatRoomCreateRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
    # auth: Annotated[str, Depends(get_user)],
):
    pass

@router.post("/guest", response_model=ChatRoomResponse)
async def post_guest_room(
    request: ChatRoomCreateRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
) -> ChatRoomResponse:
    response = await chat_controller.create_chat_room(request=request)
    return response

@router.get("/guest", response_model=ChatRoomResponse)
async def get_guest_room(
    request: ChatRoomRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
) -> ChatRoomResponse:
    response = await chat_controller.get_chat_room(request=request)
    return response

@router.get("/guest/history", response_model=ChatMessageHistoryResponse)
async def get_guest_chat_history(
    request: ChatHistoryRequest,
    chat_controller: Annotated[ChatController, Depends(Factory().get_chat_controller)],
) -> ChatMessageHistoryResponse:
    response = await chat_controller.get_user_chat_history(request=request)
    return response