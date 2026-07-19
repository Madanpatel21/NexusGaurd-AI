#!/bin/bash
echo "Deploying to K8s..."
helm upgrade --install nexusguard ./infrastructure/helm/nexusguard-core
echo "Deployment complete."
