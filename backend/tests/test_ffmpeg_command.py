from pathlib import Path

import pytest

from app.youtube.ffmpeg_command import build_render_command


def test_empty_timeline_rejected():
    with pytest.raises(ValueError, match="Timeline cannot be empty"):
        build_render_command("ffmpeg", [], "/tmp/out.mp4")


def test_invalid_duration_rejected():
    with pytest.raises(ValueError, match="Timeline duration"):
        build_render_command("ffmpeg", [{"duration_seconds": 0}], "/tmp/out.mp4")


def test_missing_assets_use_safe_fallbacks():
    command = build_render_command("ffmpeg", [{"scene_id": "s1", "duration_seconds": 2}], "/tmp/out.mp4")
    assert command[0] == "ffmpeg"
    assert "color=c=black" in " ".join(command)
    assert "anullsrc" in " ".join(command)
    assert "-map" in command
    assert "[vout]" in command
    assert "[aout]" in command


def test_existing_media_and_audio_are_inputs(tmp_path: Path):
    media = tmp_path / "scene.mp4"
    audio = tmp_path / "scene.wav"
    subtitle = tmp_path / "scene.srt"
    for path in (media, audio, subtitle):
        path.write_bytes(b"placeholder")

    command = build_render_command(
        "ffmpeg",
        [{"scene_id": "s1", "duration_seconds": 2, "media_path": str(media), "audio_path": str(audio), "subtitle_path": str(subtitle)}],
        "/tmp/out.mp4",
    )
    joined = " ".join(command)
    assert str(media) in command
    assert str(audio) in command
    assert "subtitles=" in joined
    assert "-c:v" in command
    assert "libx264" in command
    assert "-c:a" in command
    assert "aac" in command
