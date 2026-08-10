from dataclasses import dataclass
from pathlib import Path

from .voice import VoiceRequest, VoiceResult


@dataclass(frozen=True)
class TTSAdapterConfig:
    provider: str = "stub"
    output_dir: str = "/app/media/audio"


class TTSAdapter:
    """Safe TTS boundary. Real providers can be added without changing orchestration."""

    def __init__(self, config: TTSAdapterConfig | None = None):
        self.config = config or TTSAdapterConfig()

    async def synthesize(self, request: VoiceRequest, scene_id: str) -> VoiceResult:
        if not scene_id.strip():
            raise ValueError("Scene ID cannot be empty")
        if not request.text.strip():
            raise ValueError("Voice text cannot be empty")
        destination = Path(self.config.output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        # Do not create a fake audio file. The adapter returns a deterministic
        # target path until a real TTS provider is configured.
        path = destination / f"{scene_id}.wav"
        return VoiceResult(audio_path=str(path), duration_seconds=max(1.0, len(request.text.split()) / 2.5))
