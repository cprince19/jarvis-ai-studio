from dataclasses import dataclass
from typing import Literal

AssetType = Literal["image", "video", "b-roll", "text"]


@dataclass(slots=True)
class AssetRequest:
    scene_number: int
    asset_type: AssetType
    prompt: str
    duration_seconds: int


class AssetPlanner:
    def plan(self, scenes: list[dict]) -> list[AssetRequest]:
        assets: list[AssetRequest] = []
        for scene in scenes:
            heading = str(scene.get("heading", f"Scene {scene.get('number', 0)}"))
            prompt = str(scene.get("visual_prompt", "")).strip() or f"Professional cinematic visual for {heading}"
            assets.append(AssetRequest(
                scene_number=int(scene.get("number", 0)),
                asset_type="image",
                prompt=prompt,
                duration_seconds=max(3, int(scene.get("duration_seconds", 8))),
            ))
        return assets
