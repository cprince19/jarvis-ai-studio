from dataclasses import dataclass


@dataclass(frozen=True)
class SubtitleCue:
    start_seconds: float
    end_seconds: float
    text: str


def build_subtitles(text: str, duration_seconds: float) -> list[SubtitleCue]:
    """Create deterministic caption cues for development and renderer integration."""
    clean = " ".join(text.split())
    if not clean:
        return []
    duration = max(0.1, duration_seconds)
    words = clean.split()
    chunk_size = 8
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    step = duration / len(chunks)
    return [SubtitleCue(i * step, min(duration, (i + 1) * step), chunk) for i, chunk in enumerate(chunks)]
