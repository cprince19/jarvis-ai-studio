from dataclasses import dataclass
from pathlib import Path

from .tts_provider import TTSProvider, TTSRequest, TTSResponse, validate_tts_response
from .voice import VoiceRequest, VoiceResult


@dataclass(frozen=True)
class TTSAdapterConfig:
    provider: str = "stub"
    output_dir: str = "/app/media/audio"


class TTSAdapter:
    """Provider-neutral TTS boundary with strict artifact validation."""

    def __init__(self, config: TTSAdapterConfig | None = None, provider: TTSProvider | None = None):
        self.config = config or TTSAdapterConfig()
        self.provider = provider

    async def synthesize(self, request: VoiceRequest, scene_id: str) -> VoiceResult:
        scene_id = scene_id.strip()
        text = request.text.strip()
        if not scene_id:
            raise ValueError("Scene ID cannot be empty")
        if not text:
            raise ValueError("Voice text cannot be empty")

        output_path = str(Path(self.config.output_dir) / f"{scene_id}.wav")
        if self.provider is None:
            if self.config.provider == "stub":
                return VoiceResult(audio_path=output_path, duration_seconds=max(1.0, len(text.split()) / 2.5))
            raise RuntimeError(f"TTS provider '{self.config.provider}' is not configured")

        response: TTSResponse = await self.provider.synthesize(
            TTSRequest(text=text, voice_id=request.voice_id, output_path=output_path)
        )
        validate_tts_response(response)
        return VoiceResult(audio_path=response.audio_path, duration_seconds=response.duration_seconds)
