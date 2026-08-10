from .render_manifest import RenderManifest
from .validate import assert_valid_manifest


def manifest_to_timeline(manifest: RenderManifest, require_files: bool = False) -> list[dict]:
    """Adapt the media-engine manifest to the existing Celery renderer contract."""
    assert_valid_manifest(manifest, require_files=require_files)
    return [
        {
            "id": scene.scene_id,
            "title": scene.title,
            "duration_seconds": scene.duration_seconds,
            "narration": scene.narration,
            "audio_path": scene.audio_path,
            "subtitle_path": scene.subtitle_path,
            "media_path": scene.media_path,
        }
        for scene in manifest.scenes
    ]
