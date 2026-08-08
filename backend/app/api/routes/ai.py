from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.ai.registry import get_provider, list_providers
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    provider: str = "mock"
    model: str | None = None


@router.get("/providers")
def providers(_: User = Depends(get_current_user)) -> dict[str, list[str]]:
    return {"providers": list_providers()}


@router.post("/generate")
async def generate(payload: GenerateRequest, _: User = Depends(get_current_user)) -> dict[str, str]:
    try:
        provider = get_provider(payload.provider)
        result = await provider.generate(payload.prompt, payload.model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"content": result.content, "provider": result.provider, "model": result.model}
