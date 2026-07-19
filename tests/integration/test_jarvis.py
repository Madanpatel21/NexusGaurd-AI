import pytest
import requests


def test_jarvis_chat():
    # Requires running JARVIS core (docker-compose up). Skips if unavailable.
    try:
        resp = requests.post(
            "http://localhost:8081/api/v1/jarvis/chat",
            json={"query": "What is the current status of edge-001?", "device_id": "edge-001"},
            timeout=2,
        )
    except requests.RequestException:
        pytest.skip("JARVIS core not running")
    assert resp.status_code == 200
    assert "status" in resp.json()


def test_jarvis_rag():
    try:
        resp = requests.post(
            "http://localhost:8081/api/v1/jarvis/chat",
            json={"query": "How do I reset the actuator?"},
            timeout=2,
        )
    except requests.RequestException:
        pytest.skip("JARVIS core not running")
    assert "reset" in resp.json()["response"].lower()
