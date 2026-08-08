from app.agents.base import AgentResult, BaseAgent


class MockAgent(BaseAgent):
    name = "mock"

    async def run(self, prompt: str) -> AgentResult:
        return AgentResult(
            output=f"Jarvis received: {prompt}",
            provider="mock",
            model="foundation",
        )
