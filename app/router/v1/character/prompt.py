from fastapi import APIRouter, Depends
from langsmith import traceable
from typing import Annotated, List

from app.controller import ChatController, CharacterController
from app.factory import Factory
from app.model.request.character import CharacterPromptRequest, CharacterPromptCreateRequest
from app.model.response.character import CharacterPromptResponse

router = APIRouter()

@router.post("", response_model=CharacterPromptResponse)
async def create_character_prompt(
    request: CharacterPromptCreateRequest,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)],
) -> CharacterPromptResponse:
    return await character_controller.create_character_prompt_by_id(
        character_id=request.character_id,
        prompt=request.prompt
    )
    
@router.get("", response_model=CharacterPromptResponse)
async def get_character_prompt(
    character_prompt_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterPromptResponse:
    return await character_controller.get_character_prompt(character_prompt_id)

@router.get("/random", response_model=CharacterPromptResponse)
async def get_character_random_prompt(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterPromptResponse:
    return await character_controller.get_random_character_prompt(character_id)

@router.get("/random/name", response_model=CharacterPromptResponse)
async def get_character_random_prompt_by_name(
    character_name: str,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterPromptResponse:
    return await character_controller.get_random_character_prompt_by_name(name=character_name)

@router.get("/list", response_model=List[CharacterPromptResponse])
async def get_character_all_prompts(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> List[CharacterPromptResponse]:
    return await character_controller.get_character_prompts_by_character_id(character_id)

@router.get("/list/name", response_model=List[CharacterPromptResponse])
async def get_character_all_prompts_by_name(
    character_name: str,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> List[CharacterPromptResponse]:
    return await character_controller.get_character_prompts_by_name(name=character_name)