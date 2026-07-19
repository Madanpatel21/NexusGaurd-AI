# Redis

In-memory cache and session/state store.

## Usage
- Caching edge device last-known state: `device:<id>:last_state` (TTL 5m).
- Pub/Sub channel for real-time anomaly fan-out.
- Rate-limit counters for the API gateway.

## Config
- Maxmemory-policy: `allkeys-lru`.
- Persistence: AOF enabled.
