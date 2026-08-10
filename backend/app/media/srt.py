from pathlib import Path
from typing import Iterable
from app.ai.subtitles import SubtitleCue


def _timestamp(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(cues: Iterable[SubtitleCue], path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines.extend([str(index), f"{_timestamp(cue.start_seconds)} --> {_timestamp(cue.end_seconds)}", cue.text.strip(), ""])
    destination.write_text("\n".join(lines), encoding="utf-8")
    return destination
