# MySQL

Primary relational store for devices, maintenance tickets, and aggregated state.

## Credentials
- User: `root` / Password: `root`
- Database: `nexusguard`
- Port: `3306`

## Schema
- `devices(id, name, location, created_at)`
- `telemetry(device_id, timestamp, vibration, temperature, predicted_failure)`
- `sync_records(device_id, sap_ticket_id, sf_case_id, created_at)`

## Access
- Connection via GORM MySQL driver: `root:root@tcp(mysql:3306)/nexusguard`.
- Migrations applied by the maintenance-predictor service on startup.
