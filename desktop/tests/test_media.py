import json
from pathlib import Path

from core.media import MediaProbe


def test_media_probe_parses_ffprobe_output(tmp_path, monkeypatch):
    media = tmp_path / "sample.mp4"
    media.write_bytes(b"video")

    class Result:
        stdout = json.dumps({
            "format": {"duration": "12.5"},
            "streams": [
                {"codec_type": "video", "width": 1920, "height": 1080, "r_frame_rate": "30/1"},
                {"codec_type": "audio"},
            ],
        })

    def fake_run(*args, **kwargs):
        return Result()

    monkeypatch.setattr("core.media.subprocess.run", fake_run)
    info = MediaProbe("ffprobe").inspect(media)

    assert info.duration == 12.5
    assert info.width == 1920
    assert info.height == 1080
    assert info.fps == 30
    assert info.has_video is True
    assert info.has_audio is True
    assert info.size_bytes == 5
