# Kafka

Event streaming backbone for decoupled, resilient communication.

## Topics
- `telemetry.raw` — raw sensor readings from edge agents.
- `anomaly.detected` — emitted when a device is flagged for predictive failure.
- `federated.update` — model weight updates published to the FL orchestrator.

## Notes
- Partitions: 6 per topic. Replication factor: 3.
- Consumers: maintenance-predictor, enterprise-sync, federated-learning.
