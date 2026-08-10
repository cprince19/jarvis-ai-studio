from dataclasses import dataclass
from pathlib import Path

from .voice import VoiceRequest, VoiceResult


@dataclass(frozen=True)
class TTSAdapterConfig:
    provider: str = "stub"
    output_dir: str = "/app/media/audio"


class TTSAdapter:
    """Provider-neutral TTS boundary.

    Only configured providers are allowed to generate audio. The default stub
    returns metadata and never creates a fake audio file.
    """

    def __init__(self, config: TTSAdapterConfig | None = None):
        self.config = config or TTSAdapterConfig()

    async def synthesize(self, request: VoiceRequest, scene_id: str) -> VoiceResult:
        scene_id = scene_id.strip()
        text = request.text.strip()
        if not scene_id:
            raise ValueError("Scene ID cannot be empty")
        if not text:
            raise ValueError("Voice text cannot be empty")
        if self.config.provider == "stub":
            path = Path(self.config.output_dir) / f"{scene_id}.wav"
            return VoiceResult(audio_path=str(path), duration_seconds=max(1.0, len(text.split()) / 2.5))
        raise RuntimeError(f"TTS provider '{self.config.provider}' is not configured")
