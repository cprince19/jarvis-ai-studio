from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .job import VideoJob
from .media import MediaInfo


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def initialize(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                duration REAL DEFAULT 0,
                width INTEGER DEFAULT 0,
                height INTEGER DEFAULT 0,
                fps REAL DEFAULT 0,
                has_audio INTEGER DEFAULT 0,
                has_video INTEGER DEFAULT 0,
                size_bytes INTEGER DEFAULT 0,
                error TEXT
            )
            """
        )
        self.connection.commit()

    def add_job(self, job: VideoJob) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO jobs(id, file_path, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (job.id, job.file_path, job.status, job.created_at, job.created_at),
        )
        self.connection.commit()

    def update_job(self, job: VideoJob, info: MediaInfo | None = None, error: str | None = None) -> None:
        now = datetime.now(timezone.utc).isoformat()
        values = {
            "duration": info.duration if info else None,
            "width": info.width if info else None,
            "height": info.height if info else None,
            "fps": info.fps if info else None,
            "has_audio": int(info.has_audio) if info else None,
            "has_video": int(info.has_video) if info else None,
            "size_bytes": info.size_bytes if info else None,
        }
        self.connection.execute(
            """
            UPDATE jobs SET status=?, updated_at=?, error=?,
                duration=COALESCE(?, duration), width=COALESCE(?, width), height=COALESCE(?, height),
                fps=COALESCE(?, fps), has_audio=COALESCE(?, has_audio), has_video=COALESCE(?, has_video),
                size_bytes=COALESCE(?, size_bytes)
            WHERE id=?
            """,
            (job.status, now, error, values["duration"], values["width"], values["height"], values["fps"], values["has_audio"], values["has_video"], values["size_bytes"], job.id),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
