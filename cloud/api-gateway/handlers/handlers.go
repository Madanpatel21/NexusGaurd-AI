package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// HealthHandler returns service health status.
func HealthHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

// TelemetryHandler is a placeholder for cloud telemetry ingestion.
func TelemetryHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "received"})
}
