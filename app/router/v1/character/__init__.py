from fastapi import APIRouter

# from .auth import router as auth_router
from .image import router as image_router
from .info import router as info_router
from .prompt import router as prompt_router

character_router = APIRouter()
character_router.include_router(image_router, prefix="/image", tags=["character_image"])
character_router.include_router(info_router, prefix="/info", tags=["character_info"])
character_router.include_router(prompt_router, prefix="/prompt", tags=["character_prompt"])