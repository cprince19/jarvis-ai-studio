from dataclasses import asdict

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.production import ProductionPlanner
from app.youtube.scenes import Scene, ScenePlanner

router = APIRouter(prefix="/youtube/production", tags=["youtube-production"])
scene_planner = ScenePlanner()
production_planner = ProductionPlanner()


class ProductionRequest(BaseModel):
    script: str = Field(min_length=20)
    default_duration: int = Field(default=8, ge=3, le=60)
    voice_id: str = "default"
    asset_type: str = "image"
    transition: str = "cut"


@router.post("/plan")
def plan_production(payload: ProductionRequest, _: User = Depends(get_current_user)):
    scenes = scene_planner.plan(payload.script, payload.default_duration)
    shots = production_planner.plan(scenes, payload.voice_id, payload.asset_type, payload.transition)
    return {
        "shot_count": len(shots),
        "total_duration_seconds": sum(s.duration_seconds for s in shots),
        "shots": [asdict(shot) for shot in shots],
    }
