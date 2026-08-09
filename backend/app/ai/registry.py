from app.ai.base import AIProvider
from app.ai.mock import MockProvider
from app.ai.openai_provider import OpenAIProvider

_PROVIDERS: dict[str, AIProvider] = {
    "mock": MockProvider(),
    "openai": OpenAIProvider(),
}


def get_provider(name: str) -> AIProvider:
    try:
        return _PROVIDERS[name]
    except KeyError as exc:
        raise ValueError(f"Unsupported AI provider: {name}") from exc


def list_providers() -> list[str]:
    return sorted(_PROVIDERS)
