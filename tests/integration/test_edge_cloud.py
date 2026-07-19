import requests


def test_telemetry_flow(stack):
    payload = {
        "device_id": "test-001",
        "timestamp": "2026-07-18T12:00:00Z",
        "vibration": 4.5,
        "temperature": 60.0,
        "predicted_failure": False,
    }
    resp = requests.post("http://localhost:8080/api/v1/telemetry", json=payload)
    assert resp.status_code == 200
    assert resp.json()["device_id"] == "test-001"
