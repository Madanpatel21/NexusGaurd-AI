# cloud/microservices/analytics/src/main.py
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analytics import (
    TelemetryWindow,
    describe,
    vibration_temperature_correlation,
    health_score,
    estimate_rul,
    risk_score,
    recommend,
)

app = FastAPI(title="NexusGuard Analytics", version="1.0.0")

# In-memory sliding windows per device (would be Redis-backed in production).
windows: dict[str, TelemetryWindow] = {}


class Reading(BaseModel):
    device_id: str
    vibration: float
    temperature: float
    predicted_failure: bool = False


@app.post("/api/v1/analytics/ingest")
async def ingest(r: Reading):
    w = windows.setdefault(r.device_id, TelemetryWindow())
    w.push(r.dict())
    return {"status": "ok"}


@app.get("/api/v1/analytics/device/{device_id}")
async def device_analytics(device_id: str):
    w = windows.get(device_id)
    if not w or not w.snapshot():
        raise HTTPException(status_code=404, detail="no data for device")
    return {"device_id": device_id, **w.analyze()}


@app.post("/api/v1/analytics/batch")
async def batch(series: list[Reading]):
    if not series:
        raise HTTPException(status_code=400, detail="empty series")
    s = [r.dict() for r in series]
    return {
        "describe": describe(s).__dict__,
        "correlation": vibration_temperature_correlation(s),
        "health_score": health_score(s),
        "rul": estimate_rul(s),
        "risk_score": risk_score(s),
        "recommendation": recommend(s),
    }


@app.get("/health")
async def health():
    return {"status": "Analytics Online"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8095")))
