from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceRequest:
    text: str
    voice_id: str = "default"
    language: str = "en"


@dataclass(frozen=True)
class VoiceResult:
    audio_path: str
    duration_seconds: float


class VoiceProvider:
    """Provider-neutral voice contract with deterministic development behavior."""

    async def synthesize(self, request: VoiceRequest) -> VoiceResult:
        text = request.text.strip()
        if not text:
            raise ValueError("Voice text cannot be empty")
        # Phase 2 contract only. Real TTS adapters can implement this interface.
        return VoiceResult(audio_path="", duration_seconds=max(1.0, len(text) / 15.0))
