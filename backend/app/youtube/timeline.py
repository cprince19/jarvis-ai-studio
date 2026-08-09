from dataclasses import asdict, dataclass


@dataclass(slots=True)
class TimelineClip:
    scene_number: int
    start_seconds: float
    duration_seconds: float
    narration: str
    audio_asset: str | None
    visual_asset: str | None
    transition: str = "cut"


class TimelineBuilder:
    def build(self, scenes: list[dict], audio_assets: dict[int, str] | None = None, visual_assets: dict[int, str] | None = None) -> list[TimelineClip]:
        audio_assets = audio_assets or {}
        visual_assets = visual_assets or {}
        clips: list[TimelineClip] = []
        cursor = 0.0
        for scene in scenes:
            number = int(scene.get("number", 0))
            duration = max(0.1, float(scene.get("duration_seconds", 8)))
            clips.append(TimelineClip(
                scene_number=number,
                start_seconds=cursor,
                duration_seconds=duration,
                narration=str(scene.get("narration", "")),
                audio_asset=audio_assets.get(number),
                visual_asset=visual_assets.get(number),
                transition=str(scene.get("transition", "cut")),
            ))
            cursor += duration
        return clips

    @staticmethod
    def serialize(clips: list[TimelineClip]) -> list[dict]:
        return [asdict(clip) for clip in clips]
