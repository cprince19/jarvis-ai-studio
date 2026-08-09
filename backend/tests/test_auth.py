from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_protected_endpoint_requires_token() -> None:
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_agent_requires_token() -> None:
    response = client.post("/api/v1/agents/run", json={"prompt": "hello"})
    assert response.status_code == 401
