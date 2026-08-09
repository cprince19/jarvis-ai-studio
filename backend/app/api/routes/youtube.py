from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.generator import YouTubeContentGenerator

router = APIRouter(prefix="/youtube", tags=["youtube"])
generator = YouTubeContentGenerator()


class YouTubeRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    audience: str = Field(default="general audience", max_length=200)
    language: str = Field(default="English", max_length=50)
    tone: str = Field(default="professional and engaging", max_length=100)
    provider: str = "mock"
    model: str | None = None


@router.post("/workflow/preview")
async def preview_workflow(payload: YouTubeRequest, _: User = Depends(get_current_user)):
    return {"topic": payload.topic, "stages": ["research", "script", "metadata"], "provider": payload.provider}


@router.post("/workflow/run")
async def run_workflow(payload: YouTubeRequest, _: User = Depends(get_current_user)):
    package = await generator.generate(payload.topic, payload.audience, payload.language, payload.tone, payload.provider, payload.model)
    return {"topic": payload.topic, "research": package.research, "script": package.script, "title": package.title, "description": package.description, "tags": package.tags}
