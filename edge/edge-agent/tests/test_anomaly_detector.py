import sys
from unittest import mock

import pytest


@pytest.fixture
def detector(monkeypatch):
    import numpy as np
    monkeypatch.setitem(sys.modules, "numpy", np)

    dummy_interp = mock.MagicMock()
    dummy_interp.get_tensor.return_value = [0.9]  # > 0.8 -> anomaly

    with mock.patch("src.anomaly_detector.Interpreter", return_value=dummy_interp):
        from src.anomaly_detector import AnomalyDetector
        return AnomalyDetector("fake_model.tflite")


def test_detect_anomaly_high(monkeypatch, detector):
    assert detector.detect(15.0, 95.0) is True


def test_detect_normal(monkeypatch, detector):
    detector.interpreter.get_tensor.return_value = [0.1]  # < 0.8 -> normal
    assert detector.detect(4.5, 60.0) is False
