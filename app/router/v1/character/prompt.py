from fastapi import APIRouter, Depends
from langsmith import traceable
from typing import Annotated

from app.controller import ChatController, CharacterController
from app.factory import Factory
from app.model.request.character import CharacterPromptRequest
from app.model.response.character import CharacterInfoResponse

router = APIRouter()

@router.post("", response_model=CharacterInfoResponse)
async def create_character_prompt(
    request: CharacterInfoCreateRequest,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)],
) -> CharacterInfoResponse:
    return await character_controller.create_character_info(name=request.name,
                                                            description=request.description)