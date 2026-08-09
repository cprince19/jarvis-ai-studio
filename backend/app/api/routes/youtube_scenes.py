from dataclasses import asdict

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.scenes import ScenePlanner

router = APIRouter(prefix="/youtube/scenes", tags=["youtube-scenes"])
planner = ScenePlanner()


class ScenePlanRequest(BaseModel):
    script: str = Field(min_length=20)
    default_duration: int = Field(default=8, ge=3, le=60)


@router.post("/plan")
async def plan_scenes(payload: ScenePlanRequest, _: User = Depends(get_current_user)):
    scenes = planner.plan(payload.script, payload.default_duration)
    return {
        "scene_count": len(scenes),
        "total_duration_seconds": sum(s.duration_seconds for s in scenes),
        "scenes": [asdict(scene) for scene in scenes],
    }
