from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, app_name: str = "JARVIS AI Studio"):
        super().__init__()
        self.setWindowTitle(app_name)
        self.resize(1280, 780)
        self._build_ui()

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
        status.showMessage("JARVIS is ready — waiting for videos")
        self.setStatusBar(status)

    def _dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        layout.addWidget(title)

        cards = QHBoxLayout()
        for heading, value in (("Queued", "0"), ("Processing", "0"), ("Awaiting Approval", "0"), ("Uploaded", "0")):
            card = QFrame()
            card.setStyleSheet("QFrame { background:#172033; border:1px solid #263244; border-radius:12px; }")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(heading))
            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 26px; font-weight: 700;")
            card_layout.addWidget(value_label)
            cards.addWidget(card)
        layout.addLayout(cards)
        layout.addSpacing(20)

        info = QLabel("Drop a video into the Incoming folder to begin. JARVIS will process it and stop at the upload approval gate.")
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
        self.queue.addItem("No videos queued")
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
