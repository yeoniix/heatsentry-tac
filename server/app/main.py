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

"""
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
"""
def classify_activity(acc_mag: float, payload: SensorPayload) -> str:
    """
    IMU 기반 단순 활동 상태 분류
    나중에 ML/DL 모델로 대체 가능
    """
    gyro_mag = (
        payload.gyro_x**2 + payload.gyro_y**2 + payload.gyro_z**2
    ) ** 0.5

    if acc_mag < 0.08 and gyro_mag < 0.08:
        return "no_response"

    if acc_mag < 0.25:
        return "low_activity"

    if acc_mag >= 2.8:
        return "impact"

    if acc_mag >= 1.6:
        return "high_activity"

    return "normal_activity"


def calculate_readiness(payload: SensorPayload) -> dict:
    score = 100
    reasons = []

    acc_mag = (payload.acc_x**2 + payload.acc_y**2 + payload.acc_z**2) ** 0.5
    activity_state = classify_activity(acc_mag, payload)

    risk_type = "normal"

    # 1. 기본 생체 위험
    high_heart_rate = payload.heart_rate >= 150
    high_skin_temp = payload.skin_temp >= 37.0
    very_low_activity = acc_mag < 0.2

    if high_heart_rate:
        score -= 20
        reasons.append("심박수 과상승")

    if high_skin_temp:
        score -= 20
        reasons.append("피부온도 상승")

    # 2. 저활동 + 고심박 = 회복 지연 또는 탈진 위험
    if very_low_activity and high_heart_rate:
        score -= 25
        reasons.append("저활동 상태에서 심박 회복 지연")
        risk_type = "fatigue_or_heat_stress"

    # 3. 피부온 상승 + 고심박 = 열스트레스 위험
    if high_skin_temp and high_heart_rate:
        score -= 10
        reasons.append("탈진 또는 열스트레스 위험")
        risk_type = "heat_stress_risk"

    # 4. 충격 감지
    if activity_state == "impact":
        score -= 35
        reasons.append("강한 충격 감지")
        risk_type = "impact_detected"

    # 5. 무반응 상태
    if activity_state == "no_response" and high_heart_rate:
        score -= 30
        reasons.append("무반응 상태에서 심박수 과상승")
        risk_type = "fall_or_no_response"

    # 6. 배터리/통신 상태
    if payload.battery is not None and payload.battery < 20:
        score -= 10
        reasons.append("배터리 부족")
        if risk_type == "normal":
            risk_type = "battery_risk"

    if payload.signal_strength is not None and payload.signal_strength < -85:
        score -= 10
        reasons.append("통신 신호 약화")
        if risk_type == "normal":
            risk_type = "signal_loss_risk"

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
        "risk_type": risk_type,
        "risk_reasons": reasons,
        "acc_mag": round(acc_mag, 3),
        "activity_state": activity_state,
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
    "risk_type": risk["risk_type"],
    "risk_reasons": risk["risk_reasons"],
    "activity_state": risk["activity_state"],
    "acc_mag": risk["acc_mag"],
    }

    soldier_states[payload.soldier_id] = state

    return {
    "status": "ok",
    "soldier_id": payload.soldier_id,
    "readiness_score": risk["readiness_score"],
    "risk_level": risk["risk_level"],
    "risk_type": risk["risk_type"],
    "activity_state": risk["activity_state"],
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