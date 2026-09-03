from __future__ import annotations

import json
import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MediaInfo:
    path: str
    duration: float = 0.0
    width: int = 0
    height: int = 0
    fps: float = 0.0
    has_video: bool = False
    has_audio: bool = False
    size_bytes: int = 0


class MediaProbeError(RuntimeError):
    pass


class MediaProbe:
    def __init__(self, ffprobe: str | None = None):
        self.ffprobe = ffprobe or shutil.which("ffprobe") or "ffprobe"
        self.logger = logging.getLogger(__name__)

    def inspect(self, path: str | Path) -> MediaInfo:
        file_path = Path(path)
        if not file_path.exists():
            raise MediaProbeError(f"Media file not found: {file_path}")
        if not file_path.is_file():
            raise MediaProbeError(f"Media path is not a file: {file_path}")

        command = [
            self.ffprobe,
            "-v", "error",
            "-show_entries", "format=duration:stream=index,codec_type,width,height,r_frame_rate",
            "-of", "json",
            str(file_path),
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        except (subprocess.SubprocessError, OSError) as exc:
            raise MediaProbeError(f"ffprobe failed for {file_path}: {exc}") from exc

        try:
            payload = json.loads(result.stdout or "{}")
        except json.JSONDecodeError as exc:
            raise MediaProbeError("ffprobe returned invalid JSON") from exc

        streams = payload.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
        duration = float(payload.get("format", {}).get("duration") or 0.0)

        fps = 0.0
        if video and video.get("r_frame_rate"):
            try:
                numerator, denominator = video["r_frame_rate"].split("/", 1)
                if float(denominator):
                    fps = float(numerator) / float(denominator)
            except (ValueError, ZeroDivisionError):
                self.logger.warning("Unable to parse FPS for %s", file_path)

        return MediaInfo(
            path=str(file_path),
            duration=duration,
            width=int((video or {}).get("width") or 0),
            height=int((video or {}).get("height") or 0),
            fps=fps,
            has_video=video is not None,
            has_audio=audio is not None,
            size_bytes=file_path.stat().st_size,
        )
