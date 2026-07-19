#!/bin/bash
# deploy_voice.sh
# Deploy the full NexusGuard stack with JARVIS + Voice enabled.
#
# NOTE: The Helm chart is a SINGLE chart (nexusguard-core). There is no separate
# jarvis-voice chart. Voice is enabled via the `voice.enabled` value.
set -euo pipefail

REGISTRY="${REGISTRY:-ghcr.io}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
NAMESPACE="${NAMESPACE:-nexusguard}"

echo "[deploy] Deploying nexusguard-core with jarvis + voice enabled"
helm upgrade --install nexusguard ./infrastructure/helm/nexusguard-core \
  --namespace "$NAMESPACE" --create-namespace \
  --set global.imageRegistry="$REGISTRY" \
  --set jarvis.enabled=true \
  --set jarvis.image.tag="$IMAGE_TAG" \
  --set jarvis.llm.hf_token="${HF_TOKEN:-}" \
  --set voice.enabled=true \
  --set voice.image.tag="$IMAGE_TAG" \
  --set voice.replicaCount=1

echo "[deploy] Done. Voice service exposed on :8082 inside the cluster."
