import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from analytics import (
    TelemetryWindow,
    describe,
    vibration_temperature_correlation,
    health_score,
    estimate_rul,
    risk_score,
    recommend,
)


def _series(n=20, vib_base=4.0, slope=0.1, temp=55.0):
    return [
        {
            "device_id": "edge-001",
            "vibration": vib_base + i * slope,
            "temperature": temp + i * 0.2,
            "predicted_failure": False,
        }
        for i in range(n)
    ]


def test_describe():
    s = _series()
    d = describe(s)
    assert d.count == 20
    assert d.mean_vibration > 0


def test_correlation_positive_trend():
    s = _series(slope=0.2)
    corr = vibration_temperature_correlation(s)
    assert corr > 0.9  # both rise together


def test_health_score_high_when_nominal():
    s = _series(vib_base=3.0, slope=0.02)
    assert health_score(s) > 80


def test_rul_decreasing_when_increasing():
    s = _series(vib_base=10.0, slope=0.2)
    rul = estimate_rul(s)
    assert rul["rul_hours"] is not None
    assert rul["trend"] == "increasing"


def test_recommend_prescriptive():
    s = _series(vib_base=13.0, slope=0.1)
    rec = recommend(s)
    assert "maintenance" in rec.lower() or "load" in rec.lower()


def test_window_analyze():
    w = TelemetryWindow()
    for r in _series():
        w.push(r)
    out = w.analyze()
    assert "risk_score" in out
    assert "recommendation" in out
