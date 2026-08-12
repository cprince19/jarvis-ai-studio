from dataclasses import dataclass

from .render_manifest import RenderManifest
from .validate import assert_valid_manifest


@dataclass(frozen=True)
class RenderDispatch:
    manifest_path: str
    output_path: str


def prepare_render_dispatch(
    manifest: RenderManifest,
    manifest_path: str,
    output_path: str,
    *,
    require_files: bool = True,
) -> RenderDispatch:
    """Validate render inputs before handing them to the existing worker.

    This function deliberately does not enqueue a task. The existing Celery
    task remains the single queue entry point; this boundary prevents invalid
    manifests from reaching it and keeps queue ownership in one place.
    """
    assert_valid_manifest(manifest, require_files=require_files)
    if not manifest_path.strip():
        raise ValueError("Manifest path is required")
    if not output_path.strip():
        raise ValueError("Output path is required")
    return RenderDispatch(manifest_path=manifest_path, output_path=output_path)
