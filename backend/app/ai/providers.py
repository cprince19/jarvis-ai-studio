from .contracts import ResearchRequest, ResearchResult, ResearchSource, ScriptProvider, ScriptRequest, ScriptResult


class StubResearchProvider:
    """Deterministic provider for development and tests; never calls an external AI service."""

    async def research(self, request: ResearchRequest) -> ResearchResult:
        topic = request.topic.strip()
        if not topic:
            raise ValueError("Topic cannot be empty")
        return ResearchResult(
            topic=topic,
            summary=f"Research is ready to be generated for: {topic}",
            sources=[ResearchSource(title="Jarvis research placeholder", url="about:blank")],
        )


class StubScriptProvider:
    """Deterministic script provider used until a configured AI provider is selected."""

    async def generate_script(self, request: ScriptRequest) -> ScriptResult:
        topic = request.topic.strip()
        if not topic:
            raise ValueError("Topic cannot be empty")
        return ScriptResult(
            title=topic,
            hook=f"What you need to know about {topic}",
            script=request.research.summary,
            scenes=[{"title": topic, "duration_seconds": min(request.target_duration_seconds, 10)}],
        )
