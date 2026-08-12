from types import SimpleNamespace

from app.tasks import render_video as render_task_module


def test_render_task_missing_job_fails(monkeypatch):
    class FakeDB:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def scalar(self, *_args): return None
    monkeypatch.setattr(render_task_module, "SessionLocal", lambda: FakeDB())

    try:
        render_task_module.render_video("missing", [], "/tmp/out.mp4")
    except ValueError as exc:
        assert "Render job not found" in str(exc)
    else:
        raise AssertionError("Expected missing render job failure")


def test_render_task_updates_job_on_success(monkeypatch, tmp_path):
    job = SimpleNamespace(status="", progress=0, started_at=None, completed_at=None, output_path=None, error=None)

    class FakeDB:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def scalar(self, *_args): return job
        def commit(self): pass

    class FakeRenderer:
        def available(self): return True
        def render(self, clips, output_path):
            return SimpleNamespace(output_path=output_path, duration_seconds=2.0)

    monkeypatch.setattr(render_task_module, "SessionLocal", lambda: FakeDB())
    monkeypatch.setattr(render_task_module, "FFmpegRenderer", FakeRenderer)

    result = render_task_module.render_video("job-1", [{"duration_seconds": 2}], str(tmp_path / "out.mp4"))

    assert result["status"] == "completed"
    assert job.status == "completed"
    assert job.progress == 100
    assert job.output_path.endswith("out.mp4")
