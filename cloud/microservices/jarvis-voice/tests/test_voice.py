from unittest import mock

import sys

import pytest


@pytest.fixture
def processor(monkeypatch):
    sys.path.insert(0, "src")
    import voice_processor as vp

    fake_model = mock.MagicMock()
    fake_model.transcribe.return_value = {"text": "Stop edge-001 immediately."}
    monkeypatch.setattr(vp, "_load_model", lambda: fake_model)
    monkeypatch.setattr(vp, "_model", None)
    return vp, fake_model


def test_transcribe_audio(processor):
    vp, fake_model = processor
    text = vp.transcribe_audio("stop_cmd.wav")
    assert "Stop edge-001" in text
    fake_model.transcribe.assert_called_once()


def test_process_voice_command(processor, monkeypatch):
    vp, _ = processor

    resp = mock.MagicMock()
    resp.json.return_value = {"response": "Stopping edge-001."}

    import requests
    with mock.patch.object(requests, "post", return_value=resp):
        out = vp.process_voice_command("Stop edge-001", "edge-001")
    assert out == "Stopping edge-001."
