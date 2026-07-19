package main

import "github.com/prometheus/client_golang/prometheus"

var federatedUpdateLatency = prometheus.NewHistogram(prometheus.HistogramOpts{
	Name:    "nexusguard_federated_update_latency_seconds",
	Help:    "Time taken to aggregate federated model updates.",
	Buckets: prometheus.DefBuckets,
})

// recordTelemetry increments the per-device telemetry counter.
func recordTelemetry(deviceID string, status string) {
	telemetryIngested.WithLabelValues(deviceID, status).Inc()
}
