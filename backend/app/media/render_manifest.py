from dataclasses import asdict, dataclass
from pathlib import Path
import json
from app.ai.production_artifact import ProductionArtifact


@dataclass(frozen=True)
class RenderScene:
    scene_id: str
    title: str
    duration_seconds: float
    narration: str
    audio_path: str = ""
    subtitle_path: str = ""
    media_path: str = ""


@dataclass(frozen=True)
class RenderManifest:
    version: str
    scenes: list[RenderScene]
    total_duration_seconds: float


def build_manifest(artifacts: list[ProductionArtifact], subtitle_paths: dict[str, str] | None = None) -> RenderManifest:
    subtitle_paths = subtitle_paths or {}
    scenes: list[RenderScene] = []
    for artifact in artifacts:
        audio_path = artifact.voice.audio_path
        media_path = artifact.media.url if artifact.media else ""
        scenes.append(RenderScene(artifact.scene_id, artifact.title, artifact.duration_seconds, artifact.narration, audio_path, subtitle_paths.get(artifact.scene_id, ""), media_path))
    return RenderManifest("1.1", scenes, sum(scene.duration_seconds for scene in scenes))


def write_manifest(manifest: RenderManifest, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(manifest), indent=2, ensure_ascii=False), encoding="utf-8")
    return destination
