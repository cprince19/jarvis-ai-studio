import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TTSConfig:
    provider: str
    output_dir: str
    api_key: str | None
    voice_id: str


def load_tts_config() -> TTSConfig:
    provider = os.getenv("JARVIS_TTS_PROVIDER", "stub").strip().lower()
    output_dir = os.getenv("JARVIS_TTS_OUTPUT_DIR", "/app/media/audio").strip()
    api_key = os.getenv("JARVIS_TTS_API_KEY") or None
    voice_id = os.getenv("JARVIS_TTS_VOICE_ID", "default").strip()
    return TTSConfig(provider, output_dir, api_key, voice_id)
