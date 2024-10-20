from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langsmith import traceable
from typing import Annotated, List

from app.controller import CharacterController
from app.factory import Factory
from app.model.response.character import CharacterImageResponse, CharacterImageURLResponse

router = APIRouter()

@router.post("/{character_id}", response_model=CharacterImageResponse)
async def create_character_image(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)],
) -> CharacterImageResponse:
    return await character_controller.generate_character_image(character_id=character_id)

@router.get("/url/{character_id}", response_model=CharacterImageURLResponse)
async def get_character_image(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> CharacterImageURLResponse:
    return await character_controller.get_random_character_image_url_by_id(character_id=character_id)

@router.get("/url/list/{character_id}", response_model=List[CharacterImageURLResponse])
async def get_character_image_list(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> List[CharacterImageURLResponse]:
    return await character_controller.get_character_image_url_list(character_id=character_id)

@router.get("/file/{character_id}")
async def get_character_image_file(
    character_id: int,
    character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
) -> StreamingResponse:
    response = await character_controller.get_random_character_image_file_by_id(character_id=character_id)
    return StreamingResponse(content=response.content,
                             media_type=response.media_type,
                             status_code=200)
    
# @router.get("/file/list/{character_id}")
# async def get_character_image_file_list(
#     character_id: int,
#     character_controller: Annotated[CharacterController, Depends(Factory().get_character_controller)]
# ) -> List[StreamingResponse]:
#     response = await character_controller.get_character_image_file_list(character_id=character_id)
#     return [StreamingResponse(content=res.content,
#                               media_type=res.media_type,
#                               status_code=200) for res in response]