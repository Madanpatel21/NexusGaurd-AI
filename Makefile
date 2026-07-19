.PHONY: build test deploy clean

build:
	@echo "Building Edge Firmware..."
	cd edge/firmware && mkdir -p build && cd build && cmake .. && make
	@echo "Building Cloud Backend..."
	cd cloud/microservices/maintenance-predictor && go build -o /tmp/api ./main.go
	@echo "Building Edge Agent..."
	docker build -t nexusguard/edge-agent ./edge/edge-agent

test:
	@echo "Running Unit Tests..."
	cd edge/edge-agent && pytest tests/
	cd cloud/microservices/maintenance-predictor && go test ./...
	@echo "Running Integration Tests..."
	docker-compose up -d
	sleep 10
	pytest tests/integration/
	docker-compose down

deploy:
	@echo "Deploying to Kubernetes..."
	helm upgrade --install nexusguard ./infrastructure/helm/nexusguard-core

clean:
	rm -rf edge/firmware/build
	rm -rf cloud/microservices/maintenance-predictor/*.out
	docker-compose down
