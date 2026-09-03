from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from core.job import VideoJob
from core.watcher import VideoFolderWatcher


class MainWindow(QMainWindow):
    video_detected = Signal(object)

    def __init__(self, app_name: str = "JARVIS AI Studio", incoming_folder: str | Path = "watch/incoming"):
        super().__init__()
        self.setWindowTitle(app_name)
        self.resize(1280, 780)
        self.incoming_folder = Path(incoming_folder)
        self.jobs: dict[str, VideoJob] = {}
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

        brand = QLabel("JARVIS AI")
        brand.setObjectName("brand")
        subtitle = QLabel("YouTube Studio")
        subtitle.setObjectName("subtitle")
        side.addWidget(brand)
        side.addWidget(subtitle)
        side.addSpacing(24)

        self.dashboard_button = QPushButton("Dashboard")
        self.queue_button = QPushButton("Video Queue")
        self.settings_button = QPushButton("Settings")
        for button in (self.dashboard_button, self.queue_button, self.settings_button):
            side.addWidget(button)
        side.addStretch()
        side.addWidget(QLabel("Approval required before upload"))

        self.pages = QStackedWidget()
        self.pages.addWidget(self._dashboard_page())
        self.pages.addWidget(self._queue_page())
        self.pages.addWidget(self._settings_page())

        self.dashboard_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.queue_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.settings_button.clicked.connect(lambda: self.pages.setCurrentIndex(2))

        layout.addWidget(sidebar)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(root)

        status = QStatusBar()
        status.showMessage(f"JARVIS is ready — watching {self.incoming_folder}")
        self.setStatusBar(status)
        self.status = status

    def _dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        layout.addWidget(title)

        cards = QHBoxLayout()
        self.queued_value = QLabel("0")
        self.processing_value = QLabel("0")
        self.approval_value = QLabel("0")
        self.uploaded_value = QLabel("0")
        for heading, value_label in (
            ("Queued", self.queued_value),
            ("Processing", self.processing_value),
            ("Awaiting Approval", self.approval_value),
            ("Uploaded", self.uploaded_value),
        ):
            card = QFrame()
            card.setStyleSheet("QFrame { background:#172033; border:1px solid #263244; border-radius:12px; }")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(heading))
            value_label.setStyleSheet("font-size: 26px; font-weight: 700;")
            card_layout.addWidget(value_label)
            cards.addWidget(card)
        layout.addLayout(cards)
        layout.addSpacing(20)

        self.incoming_label = QLabel()
        self.incoming_label.setWordWrap(True)
        self.incoming_label.setText(f"Incoming folder: {self.incoming_folder.resolve()}")
        layout.addWidget(self.incoming_label)
        info = QLabel("JARVIS watches the Incoming folder for supported video files. Processing will stop at the explicit YouTube upload approval gate.")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()
        return page

    def _queue_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Video Queue")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        layout.addWidget(title)

        self.queue = QListWidget()
        layout.addWidget(self.queue, 1)

        approval = QHBoxLayout()
        approve = QPushButton("Approve Upload")
        approve.setObjectName("primary")
        reject = QPushButton("Reject")
        approve.setEnabled(False)
        reject.setEnabled(False)
        approval.addStretch()
        approval.addWidget(reject)
        approval.addWidget(approve)
        layout.addLayout(approval)
        return page

    def _settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        layout.addWidget(title)
        layout.addWidget(QLabel("YouTube upload settings and AI configuration will be added in the next milestone."))
        layout.addStretch()
        return page

    @Slot(object)
    def _add_video_job(self, job: VideoJob) -> None:
        if job.file_path in {existing.file_path for existing in self.jobs.values()}:
            return
        self.jobs[job.id] = job
        self.queue.addItem(f"QUEUED  •  {job.filename}")
        self.queued_value.setText(str(sum(item.status == "queued" for item in self.jobs.values())))
        self.status.showMessage(f"Video queued: {job.filename}")

    def closeEvent(self, event) -> None:  # noqa: N802
        self.watcher.stop()
        event.accept()
