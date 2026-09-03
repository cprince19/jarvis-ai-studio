from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal, Slot

from .job import VideoJob
from .media import MediaInfo
from .processor import VideoProcessor


class ProcessingWorker(QObject):
    progress = Signal(str, int, str)
    completed = Signal(object, object)
    failed = Signal(object, str)
    finished = Signal()

    def __init__(self, processor: VideoProcessor | None = None):
        super().__init__()
        self.processor = processor or VideoProcessor()
        self.processor.progress.connect(self.progress)
        self.processor.completed.connect(self._completed)
        self.processor.failed.connect(self._failed)

    @Slot(object)
    def process(self, job: VideoJob) -> None:
        self.processor.process(job)

    @Slot(object, object)
    def _completed(self, job: VideoJob, info: MediaInfo) -> None:
        self.completed.emit(job, info)
        self.finished.emit()

    @Slot(object, str)
    def _failed(self, job: VideoJob, message: str) -> None:
        self.failed.emit(job, message)
        self.finished.emit()


class ProcessingController(QObject):
    progress = Signal(str, int, str)
    completed = Signal(object, object)
    failed = Signal(object, str)

    def __init__(self):
        super().__init__()
        self.thread: QThread | None = None
        self.worker: ProcessingWorker | None = None

    def start(self, job: VideoJob) -> None:
        if self.thread and self.thread.isRunning():
            return
        self.thread = QThread()
        self.worker = ProcessingWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.process(job))
        self.worker.progress.connect(self.progress)
        self.worker.completed.connect(self.completed)
        self.worker.failed.connect(self.failed)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self._cleanup)
        self.thread.start()

    def _cleanup(self) -> None:
        if self.worker:
            self.worker.deleteLater()
        if self.thread:
            self.thread.deleteLater()
        self.worker = None
        self.thread = None
