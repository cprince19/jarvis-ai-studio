from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

from .ffmpeg_command import build_render_command


@dataclass(slots=True)
class RenderResult:
    output_path: str
    duration_seconds: float


class FFmpegRenderer:
    """Render a timeline with optional visual media, audio and subtitles."""

    def __init__(self, ffmpeg_bin: str = "ffmpeg") -> None:
        self.ffmpeg_bin = ffmpeg_bin

    def available(self) -> bool:
        return shutil.which(self.ffmpeg_bin) is not None

    def render(self, clips: list[dict], output_path: str) -> RenderResult:
        if not clips:
            raise ValueError("Timeline cannot be empty")

        duration = sum(float(c.get("duration_seconds", 0)) for c in clips)
        if duration <= 0:
            raise ValueError("Timeline duration must be greater than zero")

        if not self.available():
            raise RuntimeError("FFmpeg is not installed or not available on PATH")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        command = build_render_command(self.ffmpeg_bin, clips, output_path)
        subprocess.run(command, check=True, capture_output=True, text=True)
        return RenderResult(output_path=output_path, duration_seconds=duration)
