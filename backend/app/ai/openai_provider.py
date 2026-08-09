from openai import AsyncOpenAI

from app.ai.base import AIProvider, AIResponse
from app.core.config import settings


class OpenAIProvider(AIProvider):
    name = "openai"

    async def generate(self, prompt: str, model: str | None = None) -> AIResponse:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        selected_model = model or settings.openai_model
        response = await client.responses.create(model=selected_model, input=prompt)
        return AIResponse(content=response.output_text, provider=self.name, model=selected_model)
