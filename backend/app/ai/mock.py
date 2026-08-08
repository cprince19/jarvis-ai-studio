from app.ai.base import AIProvider, AIResponse


class MockProvider(AIProvider):
    name = "mock"

    async def generate(self, prompt: str, model: str | None = None) -> AIResponse:
        return AIResponse(
            content=f"Jarvis received your request: {prompt}",
            provider=self.name,
            model=model or "foundation",
        )
