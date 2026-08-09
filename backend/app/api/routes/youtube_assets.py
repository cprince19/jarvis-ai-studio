from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.assets import AssetPlanner

router = APIRouter(prefix="/youtube/assets", tags=["youtube-assets"])
planner = AssetPlanner()


class AssetPlanRequest(BaseModel):
    scenes: list[dict] = Field(min_length=1)


@router.post("/plan")
def plan_assets(payload: AssetPlanRequest, _: User = Depends(get_current_user)):
    assets = planner.plan(payload.scenes)
    return {"asset_count": len(assets), "assets": [{"scene_number": a.scene_number, "asset_type": a.asset_type, "prompt": a.prompt, "duration_seconds": a.duration_seconds} for a in assets]}
