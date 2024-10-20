import base64
import io

from openai import AsyncOpenAI, OpenAI
from openai.types.images_response import ImagesResponse
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Literal, Optional

from app.common.config import config
from app.service.agent.exception import ahandle_openai_exception, handle_openai_exception

class ImageGeneratorService:
    def __init__(self, model: Optional[str] = None):
        self.client = OpenAI(api_key=config.OPENAI.API_KEY)
        self.aclient = AsyncOpenAI(api_key=config.OPENAI.API_KEY)
        self.model = model or config.OPENAI.IMAGE_MODEL

    def run_generate(self, prompt: str, quality: str, **kwargs) -> bytes:
        response = self.generate(prompt, quality, **kwargs)
        response = self.b64_json_to_bytes(response)
        return response
    
    async def arun_generate(self, prompt: str, quality: str, **kwargs) -> bytes:
        response = await self.agenerate(prompt, quality, **kwargs)
        response = self.b64_json_to_bytes(response)
        return response
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @handle_openai_exception
    def generate(
        self,
        prompt: str,
        quality: Literal["standard", "hd"],
        **kwargs
    ) -> str:
        response: ImagesResponse = self.client.images.generate(
            prompt=prompt,
            model=self.model,
            quality=quality,
            response_format='b64_json',
            **kwargs
        )
        return response.data[0].b64_json

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @ahandle_openai_exception
    async def agenerate(
        self,
        prompt: str,
        quality: Literal["standard", "hd"],
        num: int = 1,
        **kwargs
    ) -> str:
        response: ImagesResponse = self.client.images.generate(
            prompt=prompt,
            model=self.model,
            quality=quality,
            response_format='b64_json',
            n=num,
            **kwargs
        )
        return response.data[0].b64_json
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @handle_openai_exception
    def edit(
        self,
        image: bytes,
        prompt: str,
        **kwargs
    ) -> str:
        response = self.client.images.edit(
            image=image,
            model=self.model,
            prompt=prompt,
            response_format='b64_json',
            **kwargs
        )
        return response.data[0].b64_json
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @ahandle_openai_exception
    async def aedit(
        self,
        image: bytes,
        prompt: str,
        **kwargs
    ) -> str:
        response = await self.aclient.images.edit(
            image=image,
            model=self.model,
            prompt=prompt,
            response_format='b64_json',
            **kwargs
        )
        return response.data[0].b64_json

    def b64_json_to_bytes(self, b64_json: str) -> bytes:
        """
        Converts base64 JSON string to bytes.

        :param b64_json: Base64 encoded image string from OpenAI API response
        :return: Decoded image bytes
        """
        # base64 디코딩
        image_bytes = base64.b64decode(b64_json)
        return image_bytes
    
    def b64_json_to_png(self, b64_json: str, file_path: str) -> bytes:
        """
        Converts image bytes to PNG format.

        :param image_bytes: Image bytes
        :return: PNG image bytes
        """
        # 이미지 바이트를 PNG로 변환
        image_bytes = base64.b64decode(b64_json)
        image = Image.open(io.BytesIO(image_bytes))
        image.save(file_path, format='PNG')
        return image_bytes