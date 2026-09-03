from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.config import AppConfig
from core.logger import configure_logging
from ui.main_window import MainWindow
from ui.theme import APP_STYLESHEET


ROOT = Path(__file__).resolve().parent


def _runtime_path(config: AppConfig, key: str, default: str) -> Path:
    value = Path(str(config.get(key, default)))
    return value if value.is_absolute() else ROOT / value


def main() -> int:
    config = AppConfig(ROOT / "config.json")
    logger = configure_logging(ROOT / "logs")
    logger.info("Starting %s", config.app_name)

    incoming = _runtime_path(config, "watch_folder", "watch/incoming")
    processing = _runtime_path(config, "processing_folder", "watch/processing")
    completed = _runtime_path(config, "completed_folder", "watch/completed")
    archive = _runtime_path(config, "archive_folder", "archive")
    database = _runtime_path(config, "database", "data/jarvis.db")
    for folder in (incoming, processing, completed, archive, database.parent):
        folder.mkdir(parents=True, exist_ok=True)

    app = QApplication(sys.argv)
    app.setApplicationName(config.app_name)
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow(config.app_name, incoming)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
