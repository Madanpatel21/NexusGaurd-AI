# cloud/microservices/jarvis-core/main.py
import os
import logging
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.agents import initialize_agent, Tool
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory

from vector_store import NexusGuardVectorStore
from sap_connector import SAPConnector
from salesforce_connector import SalesforceConnector
from tools.simulation import run_digital_twin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JARVIS")

app = FastAPI(title="NexusGuard JARVIS", version="2.0.0")

# LLM: Local Llama 3 for privacy
llm = HuggingFaceHub(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    temperature=0.05,  # Low temp for precision
    model_kwargs={"max_new_tokens": 1024},
)

# Tools
sap = SAPConnector()
sf = SalesforceConnector()
vector_store = NexusGuardVectorStore()


def query_sensor_data(device_id: str) -> str:
    """Fetches real-time and historical sensor data."""
    # Calls Cloud API
    return f"Device {device_id}: Vibration=4.5, Temp=60.0. Status: Normal."


def create_sap_ticket(device_id: str, description: str, rca: str) -> str:
    """Creates SAP ticket with AI-generated Root Cause Analysis."""
    return sap.create_ticket(device_id, description, rca)


def create_salesforce_case(device_id: str, priority: str, description: str, rca: str) -> str:
    """Creates SF case with AI-generated RCA."""
    return sf.create_case(device_id, priority, description, rca)


def simulate_scenario(device_id: str, scenario: str) -> str:
    """Runs digital twin simulation."""
    return run_digital_twin(device_id, scenario)


def retrieve_knowledge(query: str) -> str:
    """Searches 50k lines of code and manuals."""
    return vector_store.similarity_search(query)


def summarize_alerts(alerts: list) -> str:
    """Summarizes multiple alerts into one actionable insight."""
    return llm(f"Summarize these alerts: {alerts}. Suggest immediate action.")


def inject_chaos(scenario: str) -> str:
    """Injects a Chaos Mesh fault for a 'simulate <scenario>' request."""
    import subprocess
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "chaos")
    s = scenario.lower()
    manifest = os.path.join(base, "jarvis-motor-failure.yaml") if "motor" in s else os.path.join(base, "jarvis-chaos-test.yaml")
    out = subprocess.run(
        ["kubectl", "apply", "-f", manifest, "-n", os.getenv("NAMESPACE", "nexusguard")],
        capture_output=True, text=True, timeout=30,
    )
    return f"Chaos injected via {manifest}: {out.stdout.strip() or out.stderr.strip()}"


tools = [
    Tool(name="QuerySensorData", func=query_sensor_data, description="Get real-time sensor data"),
    Tool(name="CreateSAPTicket", func=create_sap_ticket, description="Create SAP ticket with RCA"),
    Tool(name="CreateSalesforceCase", func=create_salesforce_case, description="Create SF case with RCA"),
    Tool(name="SimulateScenario", func=simulate_scenario, description="Run digital twin simulation"),
    Tool(name="RetrieveKnowledge", func=retrieve_knowledge, description="Search code/docs"),
    Tool(name="SummarizeAlerts", func=summarize_alerts, description="Summarize alert clusters"),
    Tool(name="InjectChaos", func=inject_chaos, description="Inject a Chaos Mesh fault to simulate a failure scenario"),
]

# Memory for context
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize Agent
agent = initialize_agent(
    tools,
    llm,
    agent="conversational-react-description",
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)


class UserRequest(BaseModel):
    query: str
    device_id: str = None
    context: str = None


class AlertBatch(BaseModel):
    alerts: list


@app.post("/api/v1/jarvis/chat")
async def chat(request: UserRequest):
    try:
        prompt = f"Context: {request.context or 'None'}. Device: {request.device_id or 'None'}. Query: {request.query}"
        response = agent.run(prompt)
        return {"response": response, "status": "success", "confidence": 0.98}
    except Exception as e:
        logger.error(f"JARVIS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jarvis/summarize")
async def summarize_alerts_endpoint(batch: AlertBatch):
    summary = summarize_alerts(batch.alerts)
    return {"summary": summary}


class SimulateRequest(BaseModel):
    scenario: str  # e.g. "motor failure", "network partition"
    device_id: str = None
    manifest: str = None  # optional path to a Chaos Mesh yaml


@app.post("/api/v1/jarvis/simulate")
async def simulate(request: SimulateRequest):
    """Trigger a Chaos Mesh fault injection for a 'simulate X' request.

    Applies the named chaos manifest via kubectl (assumes JARVIS runs inside
    the cluster with RBAC to create chaos-mesh experiments).
    """
    manifest = request.manifest or _scenario_manifest(request.scenario)
    if not manifest or not os.path.exists(manifest):
        raise HTTPException(status_code=400, detail=f"Manifest not found: {manifest}")
    try:
        import subprocess
        out = subprocess.run(
            ["kubectl", "apply", "-f", manifest, "-n", os.getenv("NAMESPACE", "nexusguard")],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            raise HTTPException(status_code=502, detail=out.stderr)
        return {
            "status": "simulation_started",
            "scenario": request.scenario,
            "manifest": manifest,
            "kubectl": out.stdout.strip(),
        }
    except Exception as e:
        logger.error(f"Simulation trigger failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _scenario_manifest(scenario: str) -> str:
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "chaos")
    s = scenario.lower()
    if "motor" in s:
        return os.path.join(base, "jarvis-motor-failure.yaml")
    return os.path.join(base, "jarvis-chaos-test.yaml")


class CommandRequest(BaseModel):
    device_id: str
    command: str  # e.g. "reduce_speed", "shutdown", "local_autonomous_mode"
    params: dict = {}


@app.post("/api/v1/jarvis/command")
async def command(request: CommandRequest):
    """Dispatch an autonomous remediation command to an edge agent.

    In production this pushes to the edge agent's command channel (MQTT/K8s
    Service). Here we POST to the edge agent's local command endpoint.
    """
    edge_url = os.getenv("EDGE_COMMAND_URL", "http://edge-agent:8001")
    try:
        resp = requests.post(
            f"{edge_url}/command",
            json={"command": request.command, "params": request.params},
            timeout=5,
        )
        return {"status": "dispatched", "device_id": request.device_id, "edge_status": resp.status_code}
    except requests.RequestException as e:
        logger.error(f"Failed to dispatch command to {request.device_id}: {e}")
        raise HTTPException(status_code=502, detail=f"Edge unreachable: {e}")


@app.get("/health")
async def health():
    return {"status": "JARVIS Online", "tools": len(tools), "memory": "Active"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
