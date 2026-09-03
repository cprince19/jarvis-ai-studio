from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from .job import VideoJob
from .media import MediaInfo, MediaProbe, MediaProbeError


class VideoProcessor(QObject):
    progress = Signal(str, int, str)
    completed = Signal(object, object)
    failed = Signal(object, str)

    def __init__(self, probe: MediaProbe | None = None):
        super().__init__()
        self.probe = probe or MediaProbe()
        self.logger = logging.getLogger(__name__)

    @Slot(object)
    def process(self, job: VideoJob) -> None:
        job.status = "processing"
        self.progress.emit(job.id, 10, "Inspecting video")
        try:
            info = self.probe.inspect(Path(job.file_path))
            if not info.has_video:
                raise MediaProbeError("Input file contains no video stream")
            self.progress.emit(job.id, 100, "Video analysis complete")
            job.status = "ready"
            self.completed.emit(job, info)
        except Exception as exc:  # noqa: BLE001
            job.status = "failed"
            self.logger.exception("Processing failed for %s", job.file_path)
            self.failed.emit(job, str(exc))
