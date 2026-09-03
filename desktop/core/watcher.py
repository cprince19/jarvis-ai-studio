from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .job import VideoJob


VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}


class VideoFolderHandler(FileSystemEventHandler):
    def __init__(self, on_video: Callable[[VideoJob], None], logger: logging.Logger | None = None):
        super().__init__()
        self.on_video = on_video
        self.logger = logger or logging.getLogger(__name__)

    def on_created(self, event) -> None:  # noqa: ANN001
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in VIDEO_EXTENSIONS:
            return
        job = VideoJob(file_path=str(path))
        self.logger.info("Video detected: %s", path)
        self.on_video(job)


class VideoFolderWatcher:
    def __init__(self, folder: str | Path, on_video: Callable[[VideoJob], None]):
        self.folder = Path(folder)
        self.on_video = on_video
        self.logger = logging.getLogger(__name__)
        self.observer: Observer | None = None

    def start(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        if self.observer is not None:
            return
        self.observer = Observer()
        self.observer.schedule(VideoFolderHandler(self.on_video, self.logger), str(self.folder), recursive=False)
        self.observer.start()
        self.logger.info("Watching incoming folder: %s", self.folder)

    def stop(self) -> None:
        if self.observer is None:
            return
        self.observer.stop()
        self.observer.join(timeout=5)
        self.observer = None
        self.logger.info("Stopped incoming folder watcher")
