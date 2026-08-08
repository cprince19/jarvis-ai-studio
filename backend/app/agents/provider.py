from abc import ABC, abstractmethod

from app.agents.base import AgentResult


class AIProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, prompt: str, model: str | None = None) -> AgentResult:
        raise NotImplementedError
