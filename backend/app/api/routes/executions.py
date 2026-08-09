from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.workflows.engine import WorkflowEngine, WorkflowStep

router = APIRouter(prefix="/executions", tags=["executions"])
engine = WorkflowEngine()


class WorkflowStepRequest(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=50)
    config: dict = Field(default_factory=dict)


class ExecuteRequest(BaseModel):
    steps: list[WorkflowStepRequest] = Field(min_length=1, max_length=100)
    context: dict = Field(default_factory=dict)


@router.post("/workflow")
async def execute_workflow(payload: ExecuteRequest, _: User = Depends(get_current_user)):
    steps = [WorkflowStep(id=s.id, type=s.type, config=s.config) for s in payload.steps]
    return await engine.run(steps, payload.context)
