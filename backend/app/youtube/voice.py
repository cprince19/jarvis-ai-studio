from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class VoiceSegment:
    scene_number: int
    text: str
    voice_id: str
    language: str
    speed: float = 1.0
    estimated_duration_seconds: int = 8


class TTSProvider(Protocol):
    async def synthesize(self, segment: VoiceSegment) -> bytes: ...


class MockTTSProvider:
    async def synthesize(self, segment: VoiceSegment) -> bytes:
        return f"MOCK_AUDIO scene={segment.scene_number} voice={segment.voice_id}".encode()


class VoicePlanner:
    def plan(self, scenes: list[dict], voice_id: str = "default", language: str = "English", speed: float = 1.0) -> list[VoiceSegment]:
        if speed <= 0:
            raise ValueError("speed must be greater than zero")
        segments: list[VoiceSegment] = []
        for scene in scenes:
            number = int(scene.get("number", 0))
            text = str(scene.get("narration", "")).strip()
            duration = max(3, int(scene.get("duration_seconds", 8)))
            segments.append(VoiceSegment(number, text, voice_id, language, speed, duration))
        return segments
