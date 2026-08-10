from dataclasses import dataclass
from .production_artifact import ProductionArtifact, build_artifact
from .production_media import MediaAssetProvider
from .subtitles import build_subtitles
from .voice import VoiceProvider, VoiceRequest


@dataclass(frozen=True)
class OrchestrationResult:
    artifacts: list[ProductionArtifact]
    total_duration_seconds: float


class ProductionOrchestrator:
    def __init__(self, voice_provider: VoiceProvider | None = None, media_provider: MediaAssetProvider | None = None):
        self.voice_provider = voice_provider or VoiceProvider()
        self.media_provider = media_provider or MediaAssetProvider()

    async def build(self, scenes: list[dict[str, object]], language: str = "en") -> OrchestrationResult:
        artifacts: list[ProductionArtifact] = []
        for scene in scenes:
            narration = str(scene.get("narration") or "")
            duration = float(scene.get("duration_seconds") or 1.0)
            voice = await self.voice_provider.synthesize(VoiceRequest(narration, str(scene.get("voice_id") or "default"), language))
            subtitles = build_subtitles(narration, duration)
            media = await self.media_provider.resolve(str(scene.get("id") or scene.get("scene_id") or ""), str(scene.get("asset_type") or "image"))
            artifacts.append(build_artifact(scene, voice, subtitles, media))
        return OrchestrationResult(artifacts, sum(a.duration_seconds for a in artifacts))
