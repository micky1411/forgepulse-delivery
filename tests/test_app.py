from fastapi.testclient import TestClient

from forgepulse.app import app


def test_health_and_release(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    monkeypatch.setenv("GIT_SHA", "abc123")
    client = TestClient(app)
    assert client.get("/health/live").status_code == 200
    release = client.get("/release").json()
    assert release["version"] == "1.2.3"
    assert release["commit"] == "abc123"
