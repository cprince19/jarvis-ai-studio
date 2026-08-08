from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class AIResponse:
    content: str
    provider: str
    model: str


class AIProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, prompt: str, model: str | None = None) -> AIResponse:
        raise NotImplementedError
