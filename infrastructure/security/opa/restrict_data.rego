# infrastructure/security/opa/restrict_data.rego
deny[msg] {
    input.destination.path == "/api/v1/telemetry"
    input.destination.ip != ip_in_eu
    msg := "GDPR violation"
}
