from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class ResearchRequest:
    topic: str
    audience: str = "general"
    language: str = "en"


@dataclass(frozen=True)
class ResearchSource:
    title: str
    url: str
    snippet: str = ""


@dataclass(frozen=True)
class ResearchResult:
    topic: str
    summary: str
    sources: list[ResearchSource] = field(default_factory=list)


@dataclass(frozen=True)
class ScriptRequest:
    topic: str
    research: ResearchResult
    target_duration_seconds: int = 600
    language: str = "en"


@dataclass(frozen=True)
class ScriptResult:
    title: str
    hook: str
    script: str
    scenes: list[dict[str, object]] = field(default_factory=list)


class ResearchProvider(Protocol):
    async def research(self, request: ResearchRequest) -> ResearchResult: ...


class ScriptProvider(Protocol):
    async def generate_script(self, request: ScriptRequest) -> ScriptResult: ...
