from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import tempfile


@dataclass(slots=True)
class MediaRenderResult:
    output_path: str
    duration_seconds: float


class MediaRenderer:
    """Compose timeline clips with optional image/video and audio assets."""

    def __init__(self, ffmpeg_bin: str = "ffmpeg") -> None:
        self.ffmpeg_bin = ffmpeg_bin

    def available(self) -> bool:
        return shutil.which(self.ffmpeg_bin) is not None

    def render(self, clips: list[dict], output_path: str) -> MediaRenderResult:
        if not clips:
            raise ValueError("Timeline cannot be empty")
        if not self.available():
            raise RuntimeError("FFmpeg is not installed or not available on PATH")

        work = Path(tempfile.mkdtemp(prefix="jarvis-render-"))
        segments: list[Path] = []
        try:
            for index, clip in enumerate(clips):
                duration = float(clip.get("duration_seconds", 0))
                if duration <= 0:
                    raise ValueError(f"Invalid duration for clip {index + 1}")
                visual = clip.get("visual_asset")
                audio = clip.get("audio_asset")
                segment = work / f"segment-{index:04d}.mp4"
                command = [self.ffmpeg_bin, "-y"]
                if visual and Path(visual).is_file():
                    command += ["-loop", "1", "-i", str(visual)]
                else:
                    command += ["-f", "lavfi", "-i", "color=c=black:s=1280x720:r=30"]
                if audio and Path(audio).is_file():
                    command += ["-i", str(audio)]
                command += ["-t", str(duration), "-c:v", "libx264", "-pix_fmt", "yuv420p"]
                if audio and Path(audio).is_file():
                    command += ["-c:a", "aac", "-shortest"]
                else:
                    command += ["-an"]
                command += [str(segment)]
                subprocess.run(command, check=True, capture_output=True, text=True)
                segments.append(segment)

            concat = work / "concat.txt"
            concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([self.ffmpeg_bin, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", output_path], check=True, capture_output=True, text=True)
            return MediaRenderResult(output_path, sum(float(c.get("duration_seconds", 0)) for c in clips))
        finally:
            shutil.rmtree(work, ignore_errors=True)
