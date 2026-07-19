package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func TestHealthCheck(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "healthy", "version": "1.0.0"})
	})

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/health", nil)
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	var body map[string]interface{}
	_ = json.Unmarshal(w.Body.Bytes(), &body)
	if body["status"] != "healthy" {
		t.Fatalf("expected healthy status, got %v", body["status"])
	}
}

func TestTelemetryIngestion(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.POST("/api/v1/telemetry", ingestTelemetry)

	body := `{"device_id":"test-001","timestamp":"2026-07-18T12:00:00Z","vibration":4.5,"temperature":60.0,"predicted_failure":false}`
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/telemetry", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
}

func TestFederatedTrigger(t *testing.T) {
	// ingestTelemetry with predicted_failure=true must not panic when
	// triggering the federated update goroutine.
	gin.SetMode(gin.TestMode)
	r := gin.New()
	r.POST("/api/v1/telemetry", ingestTelemetry)

	body := `{"device_id":"test-002","timestamp":"2026-07-18T12:00:00Z","vibration":14.0,"temperature":95.0,"predicted_failure":true}`
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("POST", "/api/v1/telemetry", bytes.NewBufferString(body))
	req.Header.Set("Content-Type", "application/json")
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
}

func TestMetricsExposure(t *testing.T) {
	prometheus.MustRegister(telemetryIngested, anomalyDetected)
	handler := promhttp.Handler()

	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/metrics", nil)
	handler.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", w.Code)
	}
	if !bytes.Contains(w.Body.Bytes(), []byte("nexusguard_telemetry_ingested_total")) {
		t.Fatalf("expected metrics to expose nexusguard_telemetry_ingested_total")
	}
}
