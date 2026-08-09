from pathlib import Path
import tempfile

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.media_renderer import MediaRenderer

router = APIRouter(prefix="/youtube/media-render", tags=["youtube-media-render"])
renderer = MediaRenderer()


class MediaRenderRequest(BaseModel):
    clips: list[dict] = Field(min_length=1)
    output_name: str = Field(default="jarvis-video.mp4", pattern=r"^[A-Za-z0-9._-]+$")


@router.post("")
def render_media(payload: MediaRenderRequest, _: User = Depends(get_current_user)):
    if not renderer.available():
        raise HTTPException(status_code=503, detail="FFmpeg is not installed on the worker")
    output = str(Path(tempfile.gettempdir()) / payload.output_name)
    try:
        result = renderer.render(payload.clips, output)
        return {"status": "completed", "output_path": result.output_path, "duration_seconds": result.duration_seconds}
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
