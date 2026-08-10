from dataclasses import dataclass
from pathlib import Path
from .render_manifest import RenderManifest


@dataclass(frozen=True)
class ValidationIssue:
    scene_id: str
    field: str
    message: str


def validate_manifest(manifest: RenderManifest, require_files: bool = True) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not manifest.scenes:
        issues.append(ValidationIssue("", "scenes", "Render manifest contains no scenes"))
    for scene in manifest.scenes:
        if not scene.scene_id.strip():
            issues.append(ValidationIssue(scene.scene_id, "scene_id", "Scene ID is required"))
        if scene.duration_seconds <= 0:
            issues.append(ValidationIssue(scene.scene_id, "duration_seconds", "Duration must be greater than zero"))
        if not scene.narration.strip():
            issues.append(ValidationIssue(scene.scene_id, "narration", "Narration is empty"))
        if require_files:
            if scene.audio_path and not Path(scene.audio_path).is_file():
                issues.append(ValidationIssue(scene.scene_id, "audio_path", "Audio file does not exist"))
            if scene.media_path and scene.media_path.startswith(("/", ".")) and not Path(scene.media_path).is_file():
                issues.append(ValidationIssue(scene.scene_id, "media_path", "Media file does not exist"))
            if scene.subtitle_path and not Path(scene.subtitle_path).is_file():
                issues.append(ValidationIssue(scene.scene_id, "subtitle_path", "Subtitle file does not exist"))
    return issues


def assert_valid_manifest(manifest: RenderManifest, require_files: bool = True) -> None:
    issues = validate_manifest(manifest, require_files=require_files)
    if issues:
        details = "; ".join(f"{i.scene_id or 'manifest'}.{i.field}: {i.message}" for i in issues)
        raise ValueError(f"Invalid render manifest: {details}")
