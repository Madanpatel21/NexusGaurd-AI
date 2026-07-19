// cloud/microservices/maintenance-predictor/main.go
package main

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type SensorData struct {
	DeviceID    string    `json:"device_id"`
	Timestamp   time.Time `json:"timestamp"`
	Vibration   float64   `json:"vibration"`
	Temperature float64   `json:"temperature"`
	Predicted   bool      `json:"predicted_failure"`
}

var (
	telemetryIngested = prometheus.NewCounterVec(
		prometheus.CounterOpts{Name: "nexusguard_telemetry_ingested_total", Help: "Total telemetry messages"},
		[]string{"device_id", "status"},
	)
	anomalyDetected = prometheus.NewCounter(
		prometheus.CounterOpts{Name: "nexusguard_anomalies_total", Help: "Total anomalies"},
	)
)

func init() {
	// Register metrics with the default registry so /metrics exposes them.
	prometheus.MustRegister(telemetryIngested, anomalyDetected)
}

// redisClient is shared across replicas so the latest telemetry survives pod restarts.
var redisClient *redis.Client

const telemetryKeyPrefix = "device:telemetry:"

func telemetryKey(deviceID string) string {
	return telemetryKeyPrefix + deviceID
}

// saveTelemetry stores the latest reading in Redis (TTL keeps cache bounded).
func saveTelemetry(ctx context.Context, data SensorData) error {
	b, err := json.Marshal(data)
	if err != nil {
		return err
	}
	return redisClient.Set(ctx, telemetryKey(data.DeviceID), b, 5*time.Minute).Err()
}

// loadTelemetry fetches the latest reading for a device from Redis.
func loadTelemetry(ctx context.Context, deviceID string) (SensorData, bool) {
	val, err := redisClient.Get(ctx, telemetryKey(deviceID)).Result()
	if err != nil {
		return SensorData{}, false
	}
	var data SensorData
	if err := json.Unmarshal([]byte(val), &data); err != nil {
		return SensorData{}, false
	}
	return data, true
}

func main() {
	// Init DB
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		dbURL = "root:root@tcp(localhost:3306)/nexusguard?charset=utf8mb4&parseTime=True&loc=Local"
	}
	if _, err := gorm.Open(mysql.Open(dbURL), &gorm.Config{}); err != nil {
		log.Fatalf("Failed to connect to MySQL: %v", err)
	}

	// Init Redis (shared cache across replicas)
	redisClient = redis.NewClient(&redis.Options{
		Addr: os.Getenv("REDIS_ADDR"),
	})
	if err := redisClient.Ping(context.Background()).Err(); err != nil {
		log.Printf("WARNING: Redis unavailable, telemetry cache disabled: %v", err)
	}

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "healthy", "version": "1.0.0"})
	})
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))
	r.POST("/api/v1/telemetry", ingestTelemetry)
	r.GET("/api/v1/telemetry/:device_id", getTelemetry)
	r.Run()
}

func ingestTelemetry(c *gin.Context) {
	var data SensorData
	if err := c.ShouldBindJSON(&data); err != nil {
		c.JSON(400, gin.H{"error": "Invalid payload"})
		return
	}

	// Cache latest reading in Redis (survives across replicas).
	if redisClient != nil {
		if err := saveTelemetry(c.Request.Context(), data); err != nil {
			log.Printf("redis save failed: %v", err)
		}
	}

	telemetryIngested.WithLabelValues(data.DeviceID, "success").Inc()
	if data.Predicted {
		anomalyDetected.Inc()
		go triggerFederatedUpdate(data.DeviceID)
	}
	c.JSON(200, gin.H{"status": "received", "device_id": data.DeviceID})
}

func getTelemetry(c *gin.Context) {
	deviceID := c.Param("device_id")
	data, ok := loadTelemetry(c.Request.Context(), deviceID)
	if !ok {
		c.JSON(404, gin.H{"error": "no telemetry for device", "device_id": deviceID})
		return
	}
	c.JSON(200, data)
}

func triggerFederatedUpdate(deviceID string) {
	// In production: publish to Kafka -> Federated Orchestrator.
	log.Printf("Anomaly detected on %s. Triggering federated learning cycle.", deviceID)
}
