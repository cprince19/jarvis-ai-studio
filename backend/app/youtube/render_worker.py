from app.youtube.render_jobs import RenderJobStore, RenderStatus
from app.youtube.renderer import FFmpegRenderer


class RenderWorker:
    """Worker service boundary; Celery can call process() without coupling to HTTP."""

    def __init__(self, store: RenderJobStore | None = None, renderer: FFmpegRenderer | None = None) -> None:
        self.store = store or RenderJobStore()
        self.renderer = renderer or FFmpegRenderer()

    def process(self, job_id: str, clips: list[dict], output_path: str) -> dict:
        job = self.store.get(job_id)
        if job is None:
            raise KeyError(f"Unknown render job: {job_id}")
        self.store.update(job_id, status=RenderStatus.RUNNING, progress=10)
        try:
            self.store.update(job_id, progress=50)
            result = self.renderer.render(clips, output_path)
            self.store.update(job_id, status=RenderStatus.COMPLETED, progress=100, output_path=result.output_path)
            return {"job_id": job_id, "status": "completed", "output_path": result.output_path, "duration_seconds": result.duration_seconds}
        except Exception as exc:
            self.store.update(job_id, status=RenderStatus.FAILED, progress=100, error=str(exc))
            raise
