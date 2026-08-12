from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class TTSRequest:
    text: str
    voice_id: str = "default"
    output_path: str = ""


@dataclass(frozen=True)
class TTSResponse:
    audio_path: str
    duration_seconds: float


class TTSProvider(Protocol):
    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        ...


def validate_tts_response(response: TTSResponse) -> None:
    if not response.audio_path:
        raise ValueError("TTS provider returned no audio path")
    if response.duration_seconds <= 0:
        raise ValueError("TTS provider returned an invalid duration")
    if not Path(response.audio_path).is_file():
        raise FileNotFoundError(f"TTS audio file does not exist: {response.audio_path}")
