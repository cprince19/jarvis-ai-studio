from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class AIResult:
    content: str
    provider: str
    model: str


class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def generate(self, prompt: str, model: str | None = None) -> AIResult:
        raise NotImplementedError
