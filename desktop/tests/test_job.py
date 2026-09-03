from core.job import VideoJob


def test_video_job_metadata():
    job = VideoJob("C:/videos/example.MP4")
    assert job.filename == "example.MP4"
    assert job.extension == ".mp4"
    assert job.status == "queued"
    assert job.id
