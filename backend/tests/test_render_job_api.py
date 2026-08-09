from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_render_job_requires_authentication() -> None:
    response = client.post(
        "/api/v1/youtube/render-jobs",
        json={"timeline": [{"duration_seconds": 1}]},
    )
    assert response.status_code in {401, 403}


def test_render_job_rejects_invalid_output_name() -> None:
    response = client.post(
        "/api/v1/youtube/render-jobs",
        json={"timeline": [{"duration_seconds": 1}], "output_name": "../escape.mp4"},
    )
    assert response.status_code in {401, 403, 422}
