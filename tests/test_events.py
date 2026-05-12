"""Tests for the /events endpoint and /health probe."""

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from llm_cost_tracker.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _valid_payload() -> dict[str, object]:
    return {
        "model_id": "claude-opus-4-7",
        "tenant_id": "tenant-a",
        "tokens_in": 1200,
        "tokens_out": 350,
        "timestamp": datetime.now(UTC).isoformat(),
    }


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_event_valid(client: TestClient) -> None:
    response = client.post("/events", json=_valid_payload())
    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}


def test_post_event_negative_tokens_in_rejected(client: TestClient) -> None:
    payload = _valid_payload() | {"tokens_in": -1}
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_post_event_negative_tokens_out_rejected(client: TestClient) -> None:
    payload = _valid_payload() | {"tokens_out": -1}
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_post_event_missing_field_rejected(client: TestClient) -> None:
    payload = _valid_payload()
    del payload["tenant_id"]
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_post_event_extra_field_rejected(client: TestClient) -> None:
    payload = _valid_payload() | {"unexpected": "field"}
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_post_event_naive_timestamp_rejected(client: TestClient) -> None:
    payload = _valid_payload() | {"timestamp": "2026-05-14T10:00:00"}
    response = client.post("/events", json=payload)
    assert response.status_code == 422
