from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.render_job import RenderJob, RenderJobStatus
from app.youtube.renderer import FFmpegRenderer


@celery_app.task(bind=True, name="youtube.render_video")
def render_video(self, job_id: str, clips: list[dict], output_path: str) -> dict:
    with SessionLocal() as db:
        job = db.scalar(select(RenderJob).where(RenderJob.id == job_id))
        if job is None:
            raise ValueError(f"Render job not found: {job_id}")
        job.status = RenderJobStatus.RUNNING.value
        job.progress = 10
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        try:
            renderer = FFmpegRenderer()
            if not renderer.available():
                raise RuntimeError("FFmpeg is not installed or not available on PATH")
            job.progress = 50
            db.commit()
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            result = renderer.render(clips, output_path)
            job.status = RenderJobStatus.COMPLETED.value
            job.progress = 100
            job.output_path = result.output_path
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            return {"job_id": job_id, "status": job.status, "output_path": result.output_path, "duration_seconds": result.duration_seconds}
        except Exception as exc:
            job.status = RenderJobStatus.FAILED.value
            job.progress = 100
            job.error = str(exc)
            job.completed_at = datetime.now(timezone.utc)
            db.commit()
            raise
