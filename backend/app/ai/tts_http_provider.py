import json
from pathlib import Path
from urllib.request import Request, urlopen

from .tts_provider import TTSRequest, TTSResponse, TTSProvider, validate_tts_response


class HttpTTSProvider:
    """Provider-neutral HTTP TTS adapter.

    The endpoint must accept JSON and return either raw audio bytes or JSON
    containing an audio_path. Provider-specific authentication stays in the
    runtime environment and is never committed.
    """

    def __init__(self, endpoint: str, api_key: str | None = None):
        self.endpoint = endpoint.strip()
        self.api_key = api_key
        if not self.endpoint:
            raise ValueError("TTS endpoint is required")

    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        if not request.text.strip():
            raise ValueError("TTS text cannot be empty")
        if not request.output_path:
            raise ValueError("TTS output_path is required")

        payload = json.dumps({"text": request.text, "voice_id": request.voice_id}).encode("utf-8")
        headers = {"Content-Type": "application/json", "Accept": "audio/wav,application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = urlopen(Request(self.endpoint, data=payload, headers=headers, method="POST"), timeout=120)
        body = response.read()
        content_type = response.headers.get("Content-Type", "")

        destination = Path(request.output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if "application/json" in content_type:
            data = json.loads(body.decode("utf-8"))
            audio_path = str(data.get("audio_path", ""))
            result = TTSResponse(audio_path=audio_path, duration_seconds=float(data.get("duration_seconds", 0)))
        else:
            destination.write_bytes(body)
            result = TTSResponse(audio_path=str(destination), duration_seconds=0.0)

        validate_tts_response(result)
        return result
