from fastapi.testclient import TestClient

from app import main


def test_health():
    client = TestClient(main.app)
    assert client.get("/health").json() == {"status": "ok"}
