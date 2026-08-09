from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.dependencies import get_current_user
from app.db.session import SessionLocal
from app.models.render_job import RenderJob, RenderJobStatus
from app.tasks.render_video import render_video
from app.models.user import User

router = APIRouter(prefix="/youtube/render-jobs", tags=["youtube-render-jobs"])


class RenderJobRequest(BaseModel):
    timeline: list[dict] = Field(min_length=1)
    output_name: str = Field(default="jarvis-video.mp4", pattern=r"^[A-Za-z0-9._-]+$")


@router.post("")
def create_render_job(payload: RenderJobRequest, _: User = Depends(get_current_user)):
    with SessionLocal() as db:
        job = RenderJob(status=RenderJobStatus.QUEUED.value, progress=0)
        db.add(job)
        db.commit()
        db.refresh(job)
        job_id = str(job.id)

    output_path = str(Path("/tmp/jarvis-renders") / payload.output_name)
    render_video.delay(job_id, payload.timeline, output_path)
    return {"job_id": job_id, "status": RenderJobStatus.QUEUED.value, "progress": 0}


@router.get("/{job_id}")
def get_render_job(job_id: str, _: User = Depends(get_current_user)):
    try:
        parsed_id = UUID(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid render job ID") from exc
    with SessionLocal() as db:
        job = db.scalar(select(RenderJob).where(RenderJob.id == parsed_id))
        if job is None:
            raise HTTPException(status_code=404, detail="Render job not found")
        return {"job_id": str(job.id), "status": job.status, "progress": job.progress, "output_path": job.output_path, "error": job.error}
