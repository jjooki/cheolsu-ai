from fastapi import APIRouter, Depends
from langsmith import traceable
from typing import Annotated

from app.controller import ChatController, CharacterController
from app.factory import Factory
from app.model.request.character import CharacterInfoCreateRequest, CharacterInfoRequest, CharacterInfoUpdateRequest
from app.model.response.character import CharacterInfoResponse

router = APIRouter()

@router.post("", response_model=CharacterInfoResponse)
async def create_character(
    request: CharacterInfoCreateRequest,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)],
) -> CharacterInfoResponse:
    return await character_controller.create_character_info(name=request.name,
                                                            description=request.description)

@router.get("/id", response_model=CharacterInfoResponse)
async def get_character_info_by_id(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterInfoResponse:
    return await character_controller.get_character_info(CharacterInfoRequest(character_id=character_id))

@router.get("/name", response_model=CharacterInfoResponse)
async def get_character_info_by_name(
    character_name: str,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterInfoResponse:
    return await character_controller.get_character_info_by_name(character_name)

@router.patch("", response_model=CharacterInfoResponse)
async def update_character_info(
    request: CharacterInfoUpdateRequest,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterInfoResponse:
    return await character_controller.update_character_info(character_id=request.character_id,
                                                            name=request.name,
                                                            description=request.description)

@router.put("", response_model=CharacterInfoResponse)
async def update_whole_character_info(
    request: CharacterInfoUpdateRequest,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterInfoResponse:
    return await character_controller.update_character_info(character_id=request.character_id,
                                                            name=request.name,
                                                            description=request.description)