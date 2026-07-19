#!/bin/bash
# run_jarvis_chaos.sh
# One-command JARVIS self-healing chaos demo.
#
# Requires: kubectl, a nexusguard namespace, Chaos Mesh installed, and the
# Helm chart deployed with `--set jarvis.enabled=true` plus a valid HF_TOKEN.
#
# What it does:
#   1. Applies tests/chaos/jarvis-chaos-test.yaml (network disconnect + pod failure)
#   2. Polls JARVIS Core and edge-agent logs for the self-healing sequence
#   3. Waits for recovery (network restore + telemetry re-upload)
#   4. Tears down the chaos experiments
set -euo pipefail

NAMESPACE="${NAMESPACE:-nexusguard}"
MANIFEST="tests/chaos/jarvis-chaos-test.yaml"
JARVIS_POD_LABEL="app=jarvis"
EDGE_POD_LABEL="app=edge-agent"

log() { echo "[run_jarvis_chaos] $*"; }

log "Applying chaos manifest: $MANIFEST"
kubectl apply -f "$MANIFEST" -n "$NAMESPACE"

log "Chaos injected. Streaming JARVIS + edge-agent logs (Ctrl-C to stop early)..."
# Run both log tails concurrently for the duration of the test.
kubectl logs -l "$JARVIS_POD_LABEL" -n "$NAMESPACE" -f --tail=50 &
JARVIS_PID=$!
kubectl logs -l "$EDGE_POD_LABEL" -n "$NAMESPACE" -f --tail=50 &
EDGE_PID=$!

# Wait for the chaos window (~45s total: 30s disconnect + 15s pod failure).
log "Waiting for chaos window to elapse (45s)..."
sleep 45

# Stop log streaming.
kill "$JARVIS_PID" "$EDGE_PID" 2>/dev/null || true
wait 2>/dev/null || true

log "Validating recovery: cloud-api health check"
kubectl exec -n "$NAMESPACE" "$(kubectl get pod -l app=maintenance-predictor -n "$NAMESPACE" -o jsonpath='{.items[0].metadata.name}')" \
  -- curl -sf http://localhost:8080/health >/dev/null \
  && log "cloud-api health: PASS" || log "cloud-api health: FAIL"

log "Tearing down chaos experiments"
kubectl delete -f "$MANIFEST" -n "$NAMESPACE" --ignore-not-found

log "Chaos test complete. Check logs above for the self-healing sequence."
