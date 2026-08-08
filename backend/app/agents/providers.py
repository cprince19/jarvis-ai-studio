from app.agents.base import AgentResult
from app.agents.mock import MockAgent
from app.agents.provider import AIProvider


class MockProvider(AIProvider):
    name = "mock"

    async def generate(self, prompt: str, model: str | None = None) -> AgentResult:
        return await MockAgent().run(prompt)


PROVIDERS: dict[str, AIProvider] = {
    "mock": MockProvider(),
}


def get_provider(name: str = "mock") -> AIProvider:
    try:
        return PROVIDERS[name]
    except KeyError as exc:
        raise ValueError(f"Unsupported AI provider: {name}") from exc
