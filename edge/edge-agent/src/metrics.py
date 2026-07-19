from prometheus_client import Counter, start_http_server
import time

TELEMETRY_SENT = Counter('edge_telemetry_sent_total', 'Total telemetry sent')
ANOMALY_DETECTED = Counter('edge_anomaly_detected_total', 'Total anomalies detected')

def run():
    start_http_server(8000) # Expose metrics on port 8000
    while True:
        # ... existing logic ...
        TELEMETRY_SENT.inc()
        if data['predicted_failure']:
            ANOMALY_DETECTED.inc()
        time.sleep(2)
