from openai import AsyncOpenAI

from app.ai.providers.base import AIResult, AIProvider
from app.core.config import settings


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, prompt: str, model: str | None = None) -> AIResult:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        selected_model = model or settings.openai_model
        response = await self.client.responses.create(model=selected_model, input=prompt)
        return AIResult(content=response.output_text, provider=self.name, model=selected_model)
