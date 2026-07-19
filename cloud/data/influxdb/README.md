# InfluxDB

Time-series storage for high-frequency sensor telemetry (vibration, temperature).

## Usage
- Retention: 90 days hot, downsampled to 1m for cold storage.
- Measurement: `sensor_readings` (tags: `device_id`; fields: `vibration`, `temperature`).
- Ingested via the maintenance-predictor service and Kafka bridge.
