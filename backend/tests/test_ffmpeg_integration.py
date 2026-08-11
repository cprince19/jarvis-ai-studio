from pathlib import Path
import shutil
import subprocess

import pytest

from app.youtube.renderer import FFmpegRenderer


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg not installed")
def test_render_with_generated_media_audio_and_srt(tmp_path: Path):
    media = tmp_path / "scene.mp4"
    audio = tmp_path / "scene.wav"
    subtitle = tmp_path / "scene.srt"
    output = tmp_path / "final.mp4"

    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=640x360:r=30",
        "-t", "1", "-pix_fmt", "yuv420p", str(media)
    ], check=True, capture_output=True)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
        "-t", "1", "-c:a", "pcm_s16le", str(audio)
    ], check=True, capture_output=True)
    subtitle.write_text(
        "1\n00:00:00,000 --> 00:00:00,900\nJarvis AI Studio\n",
        encoding="utf-8",
    )

    result = FFmpegRenderer().render([
        {
            "scene_id": "scene-001",
            "duration_seconds": 1,
            "media_path": str(media),
            "audio_path": str(audio),
            "subtitle_path": str(subtitle),
        }
    ], str(output))

    assert output.exists()
    assert output.stat().st_size > 0
    assert result.duration_seconds == 1

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(output)],
        check=True, capture_output=True, text=True,
    )
    stream_types = set(probe.stdout.splitlines())
    assert "video" in stream_types
    assert "audio" in stream_types
