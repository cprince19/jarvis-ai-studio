from dataclasses import dataclass

from app.youtube.scenes import Scene


@dataclass(slots=True)
class ProductionShot:
    scene_number: int
    narration: str
    voice_id: str
    visual_prompt: str
    asset_type: str
    duration_seconds: int
    transition: str


class ProductionPlanner:
    """Converts scenes into a renderer-ready production shot list."""

    def plan(self, scenes: list[Scene], voice_id: str = "default", asset_type: str = "image", transition: str = "cut") -> list[ProductionShot]:
        return [ProductionShot(s.number, s.narration, voice_id, s.visual_prompt, asset_type, s.duration_seconds, transition) for s in scenes]
