from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.subtitles import SubtitleBuilder

router = APIRouter(prefix="/youtube/subtitles", tags=["youtube-subtitles"])
builder = SubtitleBuilder()

class SubtitleRequest(BaseModel):
    clips: list[dict] = Field(min_length=1)
    max_words: int = Field(default=12, ge=3, le=30)

@router.post("/srt")
def build_srt(payload: SubtitleRequest, _: User = Depends(get_current_user)):
    cues = builder.build(payload.clips, payload.max_words)
    return {"cue_count": len(cues), "srt": builder.to_srt(cues)}
