# Flower FL Config

Configuration for the Flower federated learning server used by the
`federated-learning` orchestrator.

## Strategy
- Aggregation: Federated Averaging (FedAvg).
- Server address: `0.0.0.0:8080` (override via `FL_PORT`).
- Min clients: 2, fraction fit: 0.5.

## Notes
The orchestrator (`src/orchestrator.py`) performs secure aggregation across
factory edge clients. This folder holds Flower-specific strategy/client
definitions if the project migrates from the custom PyTorch implementation.
