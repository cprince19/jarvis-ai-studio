from .tts_adapter import TTSAdapter, TTSAdapterConfig
from .tts_config import load_tts_config


def create_tts_adapter() -> TTSAdapter:
    config = load_tts_config()
    return TTSAdapter(
        TTSAdapterConfig(
            provider=config.provider,
            output_dir=config.output_dir,
        )
    )
