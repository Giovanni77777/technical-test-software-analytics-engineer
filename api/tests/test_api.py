import jwt
import pytest
from fastapi.testclient import TestClient

from app import main
from app.auth import SECRET_KEY


class FakeCursor:
    def __init__(self, results):
        self._results = list(results)
        self.description = []

    def execute(self, query, params=None):
        self._current = self._results.pop(0)

    def fetchall(self):
        return self._current


class FakeConnection:
    def __init__(self, results):
        self._cursor = FakeCursor(results)

    def cursor(self):
        return self._cursor


@pytest.fixture
def token():
    return jwt.encode({"sub": "researcher@example.org", "studies": ["ONC-101"]}, SECRET_KEY, algorithm="HS256")


def test_health():
    client = TestClient(main.app)
    assert client.get("/health").json() == {"status": "ok"}


def test_symptom_summary(monkeypatch, token):
    monkeypatch.setattr(main, "load_studies", lambda: {"ONC-101": {"study_code": "ONC-101", "study_name": "Study"}})
    results = [
        [("P1",), ("P2",)],
        [("1",), ("3",)],
        [("0",), ("1",)],
    ]
    monkeypatch.setattr(main, "get_connection", lambda: FakeConnection(results))

    client = TestClient(main.app)
    response = client.get(
        "/studies/ONC-101/symptoms/GENERAL_PAIN/summary",
        params={"start_date": "2026-01-01", "end_date": "2026-06-30"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["prevalence"] == 0.5
    assert response.json()["mean_grade"] == 1.25
