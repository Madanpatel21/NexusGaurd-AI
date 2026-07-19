package models

// SensorReading represents a single telemetry sample from an industrial device.
type SensorReading struct {
	DeviceID    string  `json:"device_id" gorm:"primaryKey"`
	Timestamp   int64   `json:"timestamp" gorm:"primaryKey"`
	Vibration   float64 `json:"vibration"`
	Temperature float64 `json:"temperature"`
	Predicted   bool    `json:"predicted_failure"`
}

// Device is the registered asset metadata.
type Device struct {
	ID   string `json:"id" gorm:"primaryKey"`
	Name string `json:"name"`
}

// SyncRecord links a device anomaly to its enterprise tickets.
type SyncRecord struct {
	DeviceID     string `json:"device_id"`
	SAPTicketID  string `json:"sap_ticket_id"`
	SFCaseID     string `json:"sf_case_id"`
}
