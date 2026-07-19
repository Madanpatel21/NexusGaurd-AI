# Stage 1: Build
FROM golang:1.22-alpine AS builder

# Install dependencies
RUN apk add --no-cache git gcc musl-dev

WORKDIR /app

# Copy go mod files (cache layer)
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build binary with CGO enabled (for C bindings if needed)
RUN CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s -X main.version=1.0.0" \
    -o /app/maintenance-predictor \
    ./main.go

# Stage 2: Run (Alpine for minimal size)
FROM alpine:3.19

# Security: Non-root user
RUN addgroup -g 1000 nexusguard && \
    adduser -u 1000 -G nexusguard -s /bin/sh -D nexusguard

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/maintenance-predictor /app/maintenance-predictor

# Copy CA certificates for HTTPS
RUN apk add --no-cache ca-certificates

# Run as non-root
USER nexusguard

EXPOSE 8080

CMD ["/app/maintenance-predictor"]
