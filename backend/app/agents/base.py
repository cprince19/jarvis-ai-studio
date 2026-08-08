from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class AgentResult:
    output: str
    provider: str
    model: str


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, prompt: str) -> AgentResult:
        raise NotImplementedError
