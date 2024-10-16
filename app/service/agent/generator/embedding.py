from openai import AsyncOpenAI, OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Literal, List

from app.common.config import config
from app.service.agent.exception import ahandle_openai_exception, handle_openai_exception

class TextEmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI.API_KEY)
        self.aclient = AsyncOpenAI(api_key=config.OPENAI.API_KEY)
        self.model = config.OPENAI.EMBEDDING_MODEL
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @handle_openai_exception
    def embedding(
        self,
        input: str | List[str],
        **kwargs
    ) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=input,
            **kwargs
        )
        return response.data[0].embedding

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    @ahandle_openai_exception
    async def aembedding(
        self,
        input: str | List[str],
        **kwargs
    ) -> List[float]:
        response = await self.aclient.embeddings.create(
            model=self.model,
            input=input,
            **kwargs
        )
        return response.data[0].embedding