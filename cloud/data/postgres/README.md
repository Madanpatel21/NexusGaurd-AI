# PostgreSQL

Relational store for devices, maintenance tickets, and aggregated state.

## Schema
- `devices(id, name, location, created_at)`
- `telemetry(device_id, timestamp, vibration, temperature, predicted_failure)`
- `sync_records(device_id, sap_ticket_id, sf_case_id, created_at)`

## Access
- Connection via Vault-injected dynamic credentials.
- Migrations applied by the maintenance-predictor service on startup.
