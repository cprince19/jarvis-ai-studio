from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum


class RenderStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class RenderJob:
    id: str
    status: RenderStatus
    progress: int = 0
    output_path: str | None = None
    error: str | None = None
    created_at: datetime = datetime.now(timezone.utc)


class RenderJobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, RenderJob] = {}

    def create(self, job_id: str) -> RenderJob:
        job = RenderJob(id=job_id, status=RenderStatus.QUEUED, created_at=datetime.now(timezone.utc))
        self._jobs[job_id] = job
        return job

    def get(self, job_id: str) -> RenderJob | None:
        return self._jobs.get(job_id)

    def update(self, job_id: str, **changes) -> RenderJob:
        job = self._jobs[job_id]
        for key, value in changes.items():
            setattr(job, key, value)
        return job
