# Incident Response & Disaster Recovery Runbook

## 1. Severity Levels
- **SEV1**: Full platform outage / data loss.
- **SEV2**: Partial outage, degraded inference.
- **SEV3**: Minor degradation, no user impact.

## 2. Detection
Alerts originate from Grafana (SLO breaches), Prometheus (high latency/anomaly
spikes), and Kubernetes (pod crash loops). All logs are centralized in ELK.

## 3. Triage
1. Acknowledge in on-call tool within 15 min (SEV1).
2. Check `kubectl get pods -n nexusguard` for crash loops.
3. Inspect recent deploys: `helm history nexusguard-core -n nexusguard`.

## 4. Mitigation
- **Rolling back a deploy**:
  ```bash
  helm rollback nexusguard-core <revision> -n nexusguard
  ```
- **Edge firmware rollback**: re-tag the previous firmware image in the edge
  deployment overlay and apply via GitOps.
- **Database failover**: promote the standby, update `DATABASE_URL` via Vault.

## 5. Federated Learning Recovery
If the FL orchestrator is down, edges fall back to local TF Lite models. Restart the
orchestrator and trigger a re-aggregation once healthy.

## 6. Post-Incident
- Write a blameless postmortem within 48h.
- File corrective actions as GitHub issues linked to the alert.

## 7. Contacts
On-call: see PagerDuty. Security issues: follow SECURITY.md.
