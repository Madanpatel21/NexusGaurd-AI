import requests


def test_prometheus_scrape(stack):
    resp = requests.get("http://localhost:8080/metrics")
    assert resp.status_code == 200
    assert "nexusguard_telemetry_ingested_total" in resp.text
