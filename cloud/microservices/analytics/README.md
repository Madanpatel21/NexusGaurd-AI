# NexusGuard Analytics Service

Advanced telemetry analytics for predictive maintenance.

## Capabilities
- **Descriptive**: rolling aggregates (mean/max/std vibration, anomaly rate)
- **Diagnostic**: vibration↔temperature Pearson correlation (thermo-mechanical wear indicator)
- **Predictive**: Remaining Useful Life (RUL) via linear drift model, composite risk score [0–100]
- **Prescriptive**: recommended operator action per device
- **Streaming**: per-device sliding-window aggregation

## API (port 8095)
- `POST /api/v1/analytics/ingest` — push a single reading
- `GET  /api/v1/analytics/device/{id}` — full analytics for a device window
- `POST /api/v1/analytics/batch` — analytics over an arbitrary series
- `GET  /health`

## Run
```bash
pip install -r requirements.txt
python src/main.py
```
