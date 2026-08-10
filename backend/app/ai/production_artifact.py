from dataclasses import dataclass, field
from .subtitles import SubtitleCue
from .production_media import MediaAsset
from .voice import VoiceResult


@dataclass(frozen=True)
class ProductionArtifact:
    scene_id: str
    title: str
    duration_seconds: float
    narration: str
    voice: VoiceResult
    subtitles: list[SubtitleCue] = field(default_factory=list)
    media: MediaAsset | None = None


def build_artifact(scene: dict[str, object], voice: VoiceResult, subtitles: list[SubtitleCue], media: MediaAsset | None = None) -> ProductionArtifact:
    scene_id = str(scene.get("id") or scene.get("scene_id") or "")
    title = str(scene.get("title") or "Untitled scene")
    narration = str(scene.get("narration") or "")
    duration = float(scene.get("duration_seconds") or voice.duration_seconds or 1.0)
    if not scene_id:
        raise ValueError("Scene ID cannot be empty")
    return ProductionArtifact(scene_id, title, max(0.1, duration), narration, voice, subtitles, media)
