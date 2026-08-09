from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.voice import VoicePlanner

router = APIRouter(prefix="/youtube/voice", tags=["youtube-voice"])
planner = VoicePlanner()


class VoicePlanRequest(BaseModel):
    scenes: list[dict] = Field(min_length=1)
    voice_id: str = Field(default="default", max_length=100)
    language: str = Field(default="English", max_length=50)
    speed: float = Field(default=1.0, gt=0.1, le=3.0)


@router.post("/plan")
def plan_voice(payload: VoicePlanRequest, _: User = Depends(get_current_user)):
    segments = planner.plan(payload.scenes, payload.voice_id, payload.language, payload.speed)
    return {
        "segment_count": len(segments),
        "total_duration_seconds": sum(s.estimated_duration_seconds for s in segments),
        "segments": [{"scene_number": s.scene_number, "text": s.text, "voice_id": s.voice_id, "language": s.language, "speed": s.speed, "estimated_duration_seconds": s.estimated_duration_seconds} for s in segments],
    }
