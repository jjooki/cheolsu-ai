import json
import os
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from langsmith import traceable
from datetime import datetime
from typing import Iterable, List, Annotated

from app.common.config import config
from app.database.mysql.crud.chat.room import create_guest_room
from app.database.mysql.crud.character import get_random_character_image_by_id
from app.database.mysql.session import AsyncSession, get_session, get_read_session
from app.model.request.chat import ChatRoomCreateRequest, ChatRoomRequest
from app.model.response.chat import ChatRoomResponse
router = APIRouter()

@router.post("", response_model=ChatRoomResponse)
async def post_chat_room(
    request: ChatRoomCreateRequest,
    db: Annotated[AsyncSession, Depends(get_session)],
    # auth: Annotated[str, Depends(get_token_header)],
):
    pass

@router.post("/guest", response_model=ChatRoomResponse)
async def post_guest_room(
    request: ChatRoomCreateRequest,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    character_image = await get_random_character_image_by_id(db, request.character_id)
    data = await create_guest_room(
        db=db,
        room_name=request.room_name,
        character_id=request.character_id,
        character_image_id=character_image.id,
        model_name=request.model_name or config.OPENAI.CHAT_MODEL,
    )
    return data