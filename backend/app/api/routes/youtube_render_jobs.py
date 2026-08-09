from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.dependencies import get_current_user
from app.models.user import User
from app.youtube.render_jobs import RenderJobStore

router = APIRouter(prefix="/youtube/render-jobs", tags=["youtube-render-jobs"])
store = RenderJobStore()


class RenderJobRequest(BaseModel):
    timeline: list[dict] = Field(min_length=1)


@router.post("")
def create_render_job(payload: RenderJobRequest, _: User = Depends(get_current_user)):
    job_id = str(uuid4())
    job = store.create(job_id)
    return {"job_id": job.id, "status": job.status, "progress": job.progress}


@router.get("/{job_id}")
def get_render_job(job_id: str, _: User = Depends(get_current_user)):
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")
    return {"job_id": job.id, "status": job.status, "progress": job.progress, "output_path": job.output_path, "error": job.error}
