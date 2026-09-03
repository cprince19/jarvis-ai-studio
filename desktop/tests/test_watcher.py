from pathlib import Path

from core.watcher import VIDEO_EXTENSIONS, VideoFolderHandler


def test_supported_video_extensions():
    assert ".mp4" in VIDEO_EXTENSIONS
    assert ".mov" in VIDEO_EXTENSIONS
    assert ".txt" not in VIDEO_EXTENSIONS


def test_handler_emits_video_job_for_supported_file():
    received = []
    handler = VideoFolderHandler(received.append)

    class Event:
        is_directory = False
        src_path = str(Path("incoming") / "sample.MP4")

    handler.on_created(Event())

    assert len(received) == 1
    assert received[0].filename == "sample.MP4"
    assert received[0].extension == ".mp4"


def test_handler_ignores_non_video_file():
    received = []
    handler = VideoFolderHandler(received.append)

    class Event:
        is_directory = False
        src_path = str(Path("incoming") / "notes.txt")

    handler.on_created(Event())

    assert received == []
