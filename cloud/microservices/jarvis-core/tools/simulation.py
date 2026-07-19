# cloud/microservices/jarvis-core/tools/simulation.py
"""Digital-twin / predictive simulation tool for JARVIS."""
import random


def run_digital_twin(device_id: str, scenario: str) -> str:
    """Runs a lightweight physics-informed simulation for a scenario.

    Returns a human-readable prediction. In production this would drive a
    PINN or a numerical model; here we approximate with a heuristic.
    """
    load_increase = "load" in scenario.lower() or "increase" in scenario.lower()
    temperature_spike = "temp" in scenario.lower() or "temperature" in scenario.lower()

    predicted_vibration = round(random.uniform(4.0, 14.5), 1)
    risk = 0.2
    if load_increase:
        predicted_vibration += 2.0
        risk += 0.4
    if temperature_spike:
        risk += 0.3

    risk_pct = int(min(risk, 0.99) * 100)
    verdict = "Failure likely" if risk > 0.7 else "Stable within margin"

    return (
        f"Simulation for {device_id} under '{scenario}': "
        f"predicted vibration spike to {predicted_vibration} in ~18h. "
        f"Risk of failure: {risk_pct}%. Recommendation: reduce load now. "
        f"Verdict: {verdict}."
    )


if __name__ == "__main__":
    print(run_digital_twin("edge-002", "10% load increase"))
