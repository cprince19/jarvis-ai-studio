from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_shape() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/system/readiness")
    assert response.status_code == 200
    payload = response.json()
    assert "ready" in payload
    assert set(payload["checks"]) == {"postgresql", "redis", "ffmpeg"}
