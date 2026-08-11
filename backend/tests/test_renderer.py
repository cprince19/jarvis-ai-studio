from pathlib import Path

import pytest

from app.youtube.renderer import FFmpegRenderer


def test_renderer_rejects_empty_timeline(tmp_path: Path) -> None:
    renderer = FFmpegRenderer(ffmpeg_bin="definitely-not-installed")
    with pytest.raises(ValueError, match="Timeline cannot be empty"):
        renderer.render([], str(tmp_path / "empty.mp4"))


def test_renderer_rejects_zero_duration(tmp_path: Path) -> None:
    renderer = FFmpegRenderer(ffmpeg_bin="definitely-not-installed")
    with pytest.raises(ValueError, match="greater than zero"):
        renderer.render([{"duration_seconds": 0}], str(tmp_path / "zero.mp4"))


def test_renderer_reports_missing_ffmpeg(tmp_path: Path) -> None:
    renderer = FFmpegRenderer(ffmpeg_bin="definitely-not-installed")
    with pytest.raises(RuntimeError, match="FFmpeg is not installed"):
        renderer.render([{"duration_seconds": 1}], str(tmp_path / "missing.mp4"))


@pytest.mark.skipif(not FFmpegRenderer().available(), reason="FFmpeg not installed")
def test_renderer_creates_mp4(tmp_path: Path) -> None:
    output = tmp_path / "fixture.mp4"
    result = FFmpegRenderer().render(
        [{"duration_seconds": 1}, {"duration_seconds": 1}], str(output)
    )
    assert output.exists()
    assert output.stat().st_size > 0
    assert result.output_path == str(output)
    assert result.duration_seconds == 2
