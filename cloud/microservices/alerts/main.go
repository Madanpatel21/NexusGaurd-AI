package main

import (
	"log"
	"net/http"
	"os"
)

// AlertsService notifies operators and downstream systems of detected anomalies.
func main() {
	log.Printf("Alerts Service starting...")

	channel := os.Getenv("ALERTS_CHANNEL")
	if channel == "" {
		channel = "anomaly.detected"
	}

	jarvisURL := os.Getenv("JARVIS_URL")
	if jarvisURL == "" {
		jarvisURL = "http://nexusguard-jarvis:8081"
	}

	log.Printf("Listening on channel '%s' for anomaly events", channel)
	// In production: subscribe to Kafka 'anomaly.detected', dispatch to
	// email/Slack/PagerDuty and SAP/Salesforce via enterprise-sync.
	// For context-aware alerting, batches of raw alerts are summarized by
	// JARVIS via POST {jarvisURL}/api/v1/jarvis/summarize.

	_ = jarvisURL
	_ = http.DefaultClient
	select {}
}
