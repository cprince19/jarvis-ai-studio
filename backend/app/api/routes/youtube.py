from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.workflows.engine import WorkflowEngine
from app.workflows.templates.youtube import YouTubeContentRequest, build_youtube_workflow

router = APIRouter(prefix="/youtube", tags=["youtube"])
engine = WorkflowEngine()


class YouTubeRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=500)
    audience: str = Field(default="general audience", max_length=200)
    language: str = Field(default="English", max_length=50)
    tone: str = Field(default="professional and engaging", max_length=100)


@router.post("/workflow/preview")
async def preview_workflow(payload: YouTubeRequest, _: User = Depends(get_current_user)):
    request = YouTubeContentRequest(**payload.model_dump())
    steps = build_youtube_workflow(request)
    return {"steps": [{"id": s.id, "type": s.type, "config": s.config} for s in steps]}


@router.post("/workflow/run")
async def run_workflow(payload: YouTubeRequest, _: User = Depends(get_current_user)):
    request = YouTubeContentRequest(**payload.model_dump())
    result = await engine.run(build_youtube_workflow(request))
    return result
