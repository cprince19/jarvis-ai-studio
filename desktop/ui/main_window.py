from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QListWidget, QMainWindow, QPushButton, QStackedWidget, QStatusBar, QVBoxLayout, QWidget

from core.job import VideoJob
from core.media import MediaInfo
from core.processor import VideoProcessor
from core.watcher import VideoFolderWatcher


class MainWindow(QMainWindow):
    video_detected = Signal(object)

    def __init__(self, app_name: str = "JARVIS AI Studio", incoming_folder: str | Path = "watch/incoming"):
        super().__init__()
        self.setWindowTitle(app_name)
        self.resize(1280, 780)
        self.incoming_folder = Path(incoming_folder)
        self.jobs: dict[str, VideoJob] = {}
        self.processors: dict[str, VideoProcessor] = {}
        self._build_ui()
        self.video_detected.connect(self._add_video_job)
        self.watcher = VideoFolderWatcher(self.incoming_folder, self.video_detected.emit)
        self.watcher.start()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame(objectName="sidebar")
        sidebar.setFixedWidth(220)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 24, 18, 18)
        brand = QLabel("JARVIS AI"); brand.setObjectName("brand")
        subtitle = QLabel("YouTube Studio"); subtitle.setObjectName("subtitle")
        side.addWidget(brand); side.addWidget(subtitle); side.addSpacing(24)
        self.dashboard_button = QPushButton("Dashboard")
        self.queue_button = QPushButton("Video Queue")
        self.settings_button = QPushButton("Settings")
        for button in (self.dashboard_button, self.queue_button, self.settings_button): side.addWidget(button)
        side.addStretch(); side.addWidget(QLabel("Approval required before upload"))

        self.pages = QStackedWidget()
        self.pages.addWidget(self._dashboard_page())
        self.pages.addWidget(self._queue_page())
        self.pages.addWidget(self._settings_page())
        self.dashboard_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.queue_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        layout.addWidget(sidebar); layout.addWidget(self.pages, 1); self.setCentralWidget(root)

        self.status = QStatusBar(); self.status.showMessage(f"JARVIS is ready — watching {self.incoming_folder}"); self.setStatusBar(self.status)

    def _dashboard_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page)
        title = QLabel("Dashboard"); title.setStyleSheet("font-size: 28px; font-weight: 700;"); layout.addWidget(title)
        cards = QHBoxLayout()
        self.queued_value, self.processing_value, self.ready_value, self.uploaded_value = (QLabel("0") for _ in range(4))
        for heading, value_label in (("Queued", self.queued_value), ("Processing", self.processing_value), ("Ready", self.ready_value), ("Uploaded", self.uploaded_value)):
            card = QFrame(); card.setStyleSheet("QFrame { background:#172033; border:1px solid #263244; border-radius:12px; }")
            card_layout = QVBoxLayout(card); card_layout.addWidget(QLabel(heading)); value_label.setStyleSheet("font-size: 26px; font-weight: 700;"); card_layout.addWidget(value_label); cards.addWidget(card)
        layout.addLayout(cards); layout.addSpacing(20)
        self.incoming_label = QLabel(f"Incoming folder: {self.incoming_folder.resolve()}"); self.incoming_label.setWordWrap(True); layout.addWidget(self.incoming_label)
        info = QLabel("JARVIS watches the Incoming folder, analyzes supported videos and prepares them for the AI pipeline. YouTube upload remains approval-gated."); info.setWordWrap(True); layout.addWidget(info); layout.addStretch()
        return page

    def _queue_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page)
        title = QLabel("Video Queue"); title.setStyleSheet("font-size: 28px; font-weight: 700;"); layout.addWidget(title)
        self.queue = QListWidget(); layout.addWidget(self.queue, 1)
        approval = QHBoxLayout(); self.approve = QPushButton("Approve Upload"); self.approve.setObjectName("primary"); self.reject = QPushButton("Reject"); self.approve.setEnabled(False); self.reject.setEnabled(False); approval.addStretch(); approval.addWidget(self.reject); approval.addWidget(self.approve); layout.addLayout(approval)
        return page

    def _settings_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); title = QLabel("Settings"); title.setStyleSheet("font-size: 28px; font-weight: 700;"); layout.addWidget(title)
        layout.addWidget(QLabel("YouTube upload settings, AI provider settings and FFmpeg configuration will be added next.")); layout.addStretch(); return page

    @Slot(object)
    def _add_video_job(self, job: VideoJob) -> None:
        if job.file_path in {existing.file_path for existing in self.jobs.values()}: return
        self.jobs[job.id] = job
        self.queue.addItem(f"QUEUED  •  {job.filename}")
        self._refresh_counts()
        self.status.showMessage(f"Video queued: {job.filename}")
        self._start_processing(job)

    def _start_processing(self, job: VideoJob) -> None:
        processor = VideoProcessor()
        self.processors[job.id] = processor
        processor.progress.connect(self._processing_progress)
        processor.completed.connect(self._processing_completed)
        processor.failed.connect(self._processing_failed)
        job.status = "processing"
        self._refresh_counts()
        processor.process(job)

    @Slot(str, int, str)
    def _processing_progress(self, job_id: str, percent: int, message: str) -> None:
        self.status.showMessage(f"{message} ({percent}%)")

    @Slot(object, object)
    def _processing_completed(self, job: VideoJob, info: MediaInfo) -> None:
        job.status = "ready"
        self._refresh_queue_item(job, f"READY  •  {job.filename}  •  {info.width}x{info.height}  •  {info.duration:.1f}s")
        self.status.showMessage(f"Video analysis complete: {job.filename}")
        self.processors.pop(job.id, None)
        self._refresh_counts()

    @Slot(object, str)
    def _processing_failed(self, job: VideoJob, message: str) -> None:
        job.status = "failed"
        self._refresh_queue_item(job, f"FAILED  •  {job.filename}  •  {message}")
        self.status.showMessage(f"Processing failed: {job.filename}")
        self.processors.pop(job.id, None)
        self._refresh_counts()

    def _refresh_queue_item(self, job: VideoJob, text: str) -> None:
        for index in range(self.queue.count()):
            if job.filename in self.queue.item(index).text(): self.queue.item(index).setText(text); return

    def _refresh_counts(self) -> None:
        values = [item.status for item in self.jobs.values()]
        self.queued_value.setText(str(values.count("queued")))
        self.processing_value.setText(str(values.count("processing")))
        self.ready_value.setText(str(values.count("ready")))
        self.uploaded_value.setText(str(values.count("uploaded")))

    def closeEvent(self, event) -> None:  # noqa: N802
        self.watcher.stop()
        event.accept()
