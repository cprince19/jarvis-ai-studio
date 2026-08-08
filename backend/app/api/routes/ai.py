from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.registry import get_provider, list_providers
from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.models.ai_run import AIRun
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    provider: str = "mock"
    model: str | None = None


@router.get("/providers")
def providers(_: User = Depends(get_current_user)) -> dict[str, list[str]]:
    return {"providers": list_providers()}


@router.get("/runs")
def runs(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    items = db.scalars(select(AIRun).where(AIRun.user_id == user.id).order_by(AIRun.id.desc()).limit(50)).all()
    return [{"id": item.id, "provider": item.provider, "model": item.model, "prompt": item.prompt, "output": item.output, "status": item.status} for item in items]


@router.post("/generate")
async def generate(payload: GenerateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        provider = get_provider(payload.provider)
        result = await provider.generate(payload.prompt, payload.model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    db.add(AIRun(user_id=user.id, provider=result.provider, model=result.model, prompt=payload.prompt, output=result.content))
    db.commit()
    return {"content": result.content, "provider": result.provider, "model": result.model}
