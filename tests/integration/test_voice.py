import os

import pytest
import requests


VOICE_URL = os.getenv("VOICE_URL", "http://localhost:8082")


def _service_available():
    try:
        requests.get(f"{VOICE_URL}/health", timeout=2)
        return True
    except requests.RequestException:
        return False


@pytest.fixture
def live():
    if not _service_available():
        pytest.skip("jarvis-voice service not running")
    return True


def test_voice_health(live):
    resp = requests.get(f"{VOICE_URL}/health", timeout=5)
    assert resp.status_code == 200
    assert resp.json().get("status") == "Voice Interface Online"


def test_voice_command_contract(live):
    """Asserts the endpoint returns the expected contract for a recorded
    .wav file. Requires a real audio sample at VOICE_SAMPLE_WAV."""
    sample = os.getenv("VOICE_SAMPLE_WAV")
    if not sample or not os.path.exists(sample):
        pytest.skip("VOICE_SAMPLE_WAV not provided (need a recorded .wav)")

    with open(sample, "rb") as f:
        resp = requests.post(
            f"{VOICE_URL}/api/v1/voice/command",
            files={"file": (os.path.basename(sample), f, "audio/wav")},
            data={"device_id": "edge-001"},
            timeout=60,
        )
    assert resp.status_code == 200
    body = resp.json()
    # Contract: transcription + jarvis_response keys are always present.
    assert "transcription" in body
    assert "jarvis_response" in body
