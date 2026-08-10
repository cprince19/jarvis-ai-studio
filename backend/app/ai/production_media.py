from dataclasses import dataclass


@dataclass(frozen=True)
class MediaAsset:
    scene_id: str
    asset_type: str
    url: str
    source: str = "generated"
    attribution: str = ""


class MediaAssetProvider:
    """Provider-neutral media contract for scene assets."""

    async def resolve(self, scene_id: str, asset_type: str = "image") -> MediaAsset:
        if not scene_id.strip():
            raise ValueError("Scene ID cannot be empty")
        return MediaAsset(scene_id=scene_id, asset_type=asset_type, url="", source="pending")
