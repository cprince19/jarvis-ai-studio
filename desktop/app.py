from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.config import AppConfig
from core.logger import configure_logging
from ui.main_window import MainWindow
from ui.theme import APP_STYLESHEET


ROOT = Path(__file__).resolve().parent


def main() -> int:
    config = AppConfig(ROOT / "config.json")
    logger = configure_logging(ROOT / "logs")
    logger.info("Starting %s", config.app_name)

    app = QApplication(sys.argv)
    app.setApplicationName(config.app_name)
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow(config.app_name)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
