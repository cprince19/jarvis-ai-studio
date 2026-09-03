from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AppConfig:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.data = {}
            return
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    @property
    def app_name(self) -> str:
        return str(self.get("app_name", "JARVIS AI Studio"))

    @property
    def approval_required(self) -> bool:
        return bool(self.get("approval_required_for_upload", True))
