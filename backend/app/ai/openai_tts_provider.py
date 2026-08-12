import asyncio
from pathlib import Path

from openai import AsyncOpenAI

from .tts_provider import TTSRequest, TTSResponse


class OpenAITTSProvider:
    """OpenAI TTS implementation for the provider-neutral TTS contract."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini-tts") -> None:
        if not api_key.strip():
            raise ValueError("OpenAI API key is required")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        output = Path(request.output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        response = await self.client.audio.speech.create(
            model=self.model,
            voice=request.voice_id,
            input=request.text,
            response_format="wav",
        )
        await asyncio.to_thread(response.write_to_file, str(output))
        # Duration is intentionally not guessed here. The artifact validator
        # requires a positive duration; callers should obtain it with ffprobe.
        raise RuntimeError("OpenAI TTS audio generated; duration must be measured with ffprobe before accepting the artifact")
