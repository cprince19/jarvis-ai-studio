from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


@dataclass(slots=True)
class VideoJob:
    file_path: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "queued"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def filename(self) -> str:
        return Path(self.file_path).name

    @property
    def extension(self) -> str:
        return Path(self.file_path).suffix.lower()
