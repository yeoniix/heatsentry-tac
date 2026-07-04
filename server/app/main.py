from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HeatSentry Monitoring Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorPayload(BaseModel):
    soldier_id:str
    timestamp: Optional[str] = None

    heart_rate:int
    skin_temp: float

    acc_x: float
    acc_y: float
    acc_z: float

    gyro_x: Optional[float] = 0.0
    gyro_y: Optional[float] = 0.0
    gyro_z: Optional[float] = 0.0

    latitude: float
    longitude: float
    altitude: Optional[float] = 0.0
    gps_accuracy: Optional[float] = 0.0

    battery: Optional[int] = 100
    signal_strength: Optional[int] = -60

soldier_states: Dict[str, dict] = {}

def calculate_readiness(payload: SensorPayload) -> dict:
    score = 100
    reasons = []

    acc_mag = (payload.acc_x**2 + payload.acc_y**2 + payload.acc_z**2)**0.5

    if payload.heart_rate >= 150:
        score -= 25
        reasons.append("심박수 과상승")
    
    if payload.skin_temp >= 37.0:
        score -= 20
        reasons.append("피부온도 상승")

    if acc_mag < 0.2 and payload.heart_rate >=140:
        score -= 25
        reasons.append("저활동 상태에서 심박 회복 지연")

    if payload.battery is not None and payload.battery<20:
        score -=10
        reasons.append("배터리 부족")

    if payload.signal_strength is not None and payload.signal_strength < -85:
        score -=10
        reasons.append("통신 신호 약화")

    score = max(0, min(100, score))

    if score >= 80:
        level = "normal"
    elif score >= 60:
        level = "caution"
    elif score >= 40:
        level = "warning"
    else:
        level = "critical"
    
    return {
        "readiness_score": score,
        "risk_level": level, 
        "risk_reasons": reasons,
        "acc_mag": round(acc_mag, 3),
    }


@app.get("/")
def root():
    return{
        "message": "HeatSentry monitoring server is running",
        "time": datetime.now().isoformat(),
    }

@app.post("/api/sensor")
def receive_sensor_data(payload: SensorPayload):
    received_at = datetime.now().isoformat()
    risk = calculate_readiness(payload)

    state = {
        **payload.model_dump(),
        "server_received_at": received_at,
        "readiness_score": risk["readiness_score"],
        "risk_level": risk["risk_level"],
        "risk_reasons": risk["risk_reasons"],
        "acc_mag": risk["acc_mag"],
    }

    soldier_states[payload.soldier_id] = state

    return{
        "status": "ok",
        "soldier_id": payload.soldier_id,
        "readiness_score": risk["readiness_score"],
        "risk_level": risk["risk_level"],
        "risk_reasons": risk["risk_reasons"],
    }

@app.get("/api/soldiers")
def get_soldiers():
    return list(soldier_states.values())

@app.get("/api/soldiers/{soldier_id}")
def get_soldier(soldier_id: str):
    if soldier_id not in soldier_states:
        return {"error": "soldier not found"}
    
    return soldier_states[soldier_id]