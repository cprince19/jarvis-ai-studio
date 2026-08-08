from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.agents.mock import MockAgent
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/agents", tags=["agents"])
agent = MockAgent()


class AgentRunRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)


@router.post("/run")
async def run_agent(payload: AgentRunRequest, _: User = Depends(get_current_user)) -> dict[str, str]:
    result = await agent.run(payload.prompt)
    return {"output": result.output, "provider": result.provider, "model": result.model}
