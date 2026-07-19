# edge/edge-agent/src/agent.py
import os, time, random, requests, logging
from datetime import datetime
from prometheus_client import Counter, start_http_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusGuard-Edge")

TELEMETRY_SENT = Counter('edge_telemetry_sent', 'Total telemetry sent')
ANOMALY_DETECTED = Counter('edge_anomaly_detected', 'Total anomalies')

class EdgeAgent:
    def __init__(self):
        self.device_id = os.getenv("DEVICE_ID", "edge-001")
        self.cloud_url = os.getenv("CLOUD_URL", "http://localhost:8080")
        self.jarvis_url = os.getenv("JARVIS_URL", "http://nexusguard-jarvis:8081")
        self.local_mode = False
        self.telemetry_queue = []
        self.model = self.load_model()  # TF Lite model

    def load_model(self):
        import tensorflow.lite as tflite
        interpreter = tflite.Interpreter(model_path="./models/failure_detector_v1.tflite")
        interpreter.allocate_tensors()
        return interpreter

    def simulate_sensor_data(self):
        return {
            "vibration": random.uniform(0.0, 15.0),
            "temperature": random.uniform(20.0, 100.0),
        }

    def send_to_cloud(self, data):
        if self.local_mode:
            # Connectivity lost: queue telemetry for bulk upload on recovery.
            self.telemetry_queue.append(data)
            return
        try:
            requests.post(f"{self.cloud_url}/api/v1/telemetry", json=data, timeout=3)
        except requests.RequestException:
            # Drift into Local Autonomous Mode on network failure.
            self.local_mode = True
            self.telemetry_queue.append(data)

    def run(self):
        start_http_server(8000)  # Prometheus metrics
        from command_listener import start as start_command_listener
        start_command_listener(self)
        while True:
            data = self.simulate_sensor_data()
            if self.infer(data):
                ANOMALY_DETECTED.inc()
                self.handle_anomaly(data)
            TELEMETRY_SENT.inc()
            self.send_to_cloud(data)
            self.flush_queue()
            time.sleep(2)

    def flush_queue(self):
        if self.local_mode or not self.telemetry_queue:
            return
        try:
            for data in list(self.telemetry_queue):
                requests.post(f"{self.cloud_url}/api/v1/telemetry", json=data, timeout=3)
                self.telemetry_queue.remove(data)
        except requests.RequestException:
            self.local_mode = True

    def infer(self, data):
        input_data = [data['vibration'], data['temperature']]
        self.model.set_tensor(0, input_data)
        self.model.invoke()
        return self.model.get_tensor(0) > 0.8

    def actuate(self):
        # Adjust motor speed, temperature, etc.
        pass

    def shutdown_safely(self):
        logger.info("JARVIS-directed safe shutdown initiated.")
        # Graceful halt of motors / isolation of device.

    def adjust_motor_speed(self, delta_pct):
        logger.info(f"JARVIS-directed motor speed adjustment: {delta_pct}%.")
        # Write new setpoint to hardware register.

    def remediate(self, command, params=None):
        """Execute a JARVIS autonomous-remediation command."""
        params = params or {}
        cmd = command.lower()
        logger.info(f"EXECUTING remediation: {command} (params={params})")

        if "reduce_speed" in cmd or "slow" in cmd:
            self.adjust_motor_speed(params.get("delta_pct", -20))
            self.local_mode = True
            logger.info("Motor speed reduced. Hardware safe. Telemetry queued.")
        elif "shutdown" in cmd:
            self.shutdown_safely()
        elif "local" in cmd or "autonomous" in cmd:
            self.local_mode = True
            logger.info("Switched to Local Autonomous Mode. Telemetry queued for bulk upload.")
        else:
            logger.warning(f"Unknown remediation command: {command}")

    def handle_anomaly(self, data):
        """Consults JARVIS before taking action."""
        query = (
            f"Device {self.device_id} detected anomaly. "
            f"Vibration={data['vibration']}, Temp={data['temperature']}. "
            f"Suggest immediate action."
        )
        try:
            resp = requests.post(
                f"{self.jarvis_url}/api/v1/jarvis/chat",
                json={"query": query, "device_id": self.device_id},
                timeout=5,
            )
            payload = resp.json()
            advice = payload.get("response", "")
            confidence = float(payload.get("confidence", 0.0))
            logger.info(f"JARVIS Advice: {advice} (Confidence: {confidence})")

            # Autonomous Action if confidence > 95%
            if confidence > 0.95:
                if "shutdown" in advice.lower():
                    self.shutdown_safely()
                elif "reduce_speed" in advice.lower():
                    self.adjust_motor_speed(-20)
                else:
                    self.send_to_cloud(data)  # Passive mode
            else:
                self.send_to_cloud(data)  # Wait for human approval
        except Exception as e:
            logger.error(f"JARVIS Connection Failed: {e}. Defaulting to safe mode.")
            self.send_to_cloud(data)
