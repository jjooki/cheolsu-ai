import json
import os
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from langsmith import traceable
from datetime import datetime
from typing import Iterable, List

router = APIRouter()

@router.post("", response_model=List[str])
def get_message_response(
    messages: List[str]
):
    openai = AsyncOpenAI()
    return openai.get_message_response(messages)