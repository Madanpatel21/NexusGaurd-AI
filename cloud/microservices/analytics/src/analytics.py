"""Core analytics primitives for NexusGuard telemetry.

This module provides advanced, production-grade analytics over industrial
sensor telemetry: descriptive aggregates, diagnostic correlation, predictive
Remaining-Useful-Life (RUL) estimation, risk scoring, and prescriptive
recommendations. Pure-Python + numpy so it runs without heavy ML deps.
"""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from typing import List, Sequence

import numpy as np


@dataclass
class WindowStats:
    count: int
    mean_vibration: float
    mean_temperature: float
    max_vibration: float
    std_vibration: float
    anomaly_rate: float


def describe(series: Sequence[dict]) -> WindowStats:
    """Descriptive statistics over a telemetry window."""
    if not series:
        return WindowStats(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    vib = np.array([s["vibration"] for s in series], dtype=float)
    temp = np.array([s["temperature"] for s in series], dtype=float)
    anomalies = sum(1 for s in series if s.get("predicted_failure"))
    return WindowStats(
        count=len(series),
        mean_vibration=float(np.mean(vib)),
        mean_temperature=float(np.mean(temp)),
        max_vibration=float(np.max(vib)),
        std_vibration=float(np.std(vib)),
        anomaly_rate=anomalies / len(series),
    )


def vibration_temperature_correlation(series: Sequence[dict]) -> float:
    """Diagnostic: Pearson correlation between vibration and temperature.

    A high positive correlation suggests thermo-mechanical wear (bearing
    degradation), a leading indicator of impending failure.
    """
    if len(series) < 3:
        return 0.0
    vib = np.array([s["vibration"] for s in series], dtype=float)
    temp = np.array([s["temperature"] for s in series], dtype=float)
    if np.std(vib) == 0 or np.std(temp) == 0:
        return 0.0
    return float(np.corrcoef(vib, temp)[0, 1])


def health_score(series: Sequence[dict]) -> float:
    """Composite device health score in [0, 100].

    Lower vibration variance, lower peak vibration, and lower anomaly rate
    yield a higher score. Weighted toward recent peaks.
    """
    stats = describe(series)
    if stats.count == 0:
        return 100.0
    # Normalized penalties
    vib_penalty = min(stats.max_vibration / 15.0, 1.0) * 50.0
    var_penalty = min(stats.std_vibration / 5.0, 1.0) * 25.0
    anomaly_penalty = min(stats.anomaly_rate * 4.0, 1.0) * 25.0
    return max(0.0, 100.0 - (vib_penalty + var_penalty + anomaly_penalty))


def estimate_rul(series: Sequence[dict]) -> dict:
    """Predictive: Remaining Useful Life estimate (hours).

    Uses a simple physics-informed linear drift model: project the recent
    vibration trend to the failure threshold (15.0). If vibration is stable
    or decreasing, RUL is capped (healthy). Returns point estimate + trend.
    """
    if len(series) < 3:
        return {"rul_hours": None, "trend": "insufficient_data"}
    vib = np.array([s["vibration"] for s in series], dtype=float)
    x = np.arange(len(vib))
    slope, _ = np.polyfit(x, vib, 1)
    last = float(vib[-1])
    if slope <= 0 or last >= 15.0:
        return {"rul_hours": None, "trend": "stable_or_over_threshold"}
    # hours = (threshold - last) / (per-sample slope * samples_per_hour)
    samples_per_hour = 1800.0  # 0.5s sampling -> 1800 samples/hour
    hours = (15.0 - last) / (max(slope, 1e-6) * samples_per_hour)
    return {"rul_hours": round(hours, 2), "trend": "increasing" if slope > 0 else "stable"}


def risk_score(series: Sequence[dict]) -> float:
    """Predictive risk in [0, 100] combining health, RUL, and correlation."""
    health = health_score(series)
    rul = estimate_rul(series).get("rul_hours")
    corr = abs(vibration_temperature_correlation(series))
    risk = (100 - health) * 0.6
    if rul is not None:
        risk += max(0.0, (72 - rul) / 72.0) * 100 * 0.3
    risk += corr * 10.0
    return min(100.0, risk)


def recommend(series: Sequence[dict]) -> str:
    """Prescriptive: recommended operator action based on analytics."""
    stats = describe(series)
    corr = vibration_temperature_correlation(series)
    rul = estimate_rul(series).get("rul_hours")
    if stats.max_vibration > 12.0:
        return "Reduce motor load by 20% and schedule maintenance within 24h."
    if rul is not None and rul < 72:
        return f"Schedule intervention in {int(rul)}h (RUL threshold breached)."
    if corr > 0.7:
        return "Investigate thermo-mechanical wear; inspect bearings."
    if stats.anomaly_rate > 0.1:
        return "Elevated anomaly rate; enable Local Autonomous Mode."
    return "Nominal. Continue monitoring."


@dataclass
class TelemetryWindow:
    """Sliding window aggregator for streaming analytics."""

    maxlen: int = 500
    _buf: deque = field(default_factory=deque)

    def push(self, reading: dict) -> None:
        self._buf.append(reading)
        while len(self._buf) > self.maxlen:
            self._buf.popleft()

    def snapshot(self) -> List[dict]:
        return list(self._buf)

    def analyze(self) -> dict:
        s = self.snapshot()
        return {
            "describe": describe(s).__dict__,
            "correlation": vibration_temperature_correlation(s),
            "health_score": health_score(s),
            "rul": estimate_rul(s),
            "risk_score": risk_score(s),
            "recommendation": recommend(s),
        }
