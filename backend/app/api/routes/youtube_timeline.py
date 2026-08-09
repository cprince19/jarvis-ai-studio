from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.timeline import TimelineBuilder

router = APIRouter(prefix="/youtube/timeline", tags=["youtube-timeline"])
builder = TimelineBuilder()


class TimelineRequest(BaseModel):
    scenes: list[dict] = Field(min_length=1)
    audio_assets: dict[int, str] = {}
    visual_assets: dict[int, str] = {}


@router.post("/build")
def build_timeline(payload: TimelineRequest, _: User = Depends(get_current_user)):
    clips = builder.build(payload.scenes, payload.audio_assets, payload.visual_assets)
    total = sum(c.duration_seconds for c in clips)
    return {"clip_count": len(clips), "duration_seconds": total, "clips": builder.serialize(clips)}
