import time
import random
from datetime import datetime
from typing import Dict, Tuple

import requests

SERVER_URL = "http://127.0.0.1:8000/api/sensor"

# 시뮬레이션 시작 위치: 예시:서울시청 근처 좌표
# 이후 수정 예정(훈련장 좌표로)
BASE_LOCATIONS: Dict[str, Tuple[float, float]] = {
    "A01": (37.5665, 126.9780),
    "A02": (37.5667, 126.9782),
    "A03": (37.5669, 126.9784),
    "A04": (37.5671, 126.9786),
}

def add_gps_noise(lat: float, lon: float, scale: float=0.00008):
    return(
        #GPS 오차를 위해 위도/경도에 작은 랜덤값을 추가함
        lat + random.uniform(-scale, scale),
        lon + random.uniform(-scale, scale),
    )

def generate_normal_soldier(soldier_id: str, tick: int):
    """
    정상상태 soldier A01 출력,
    심박, 피부온, 움직임 모두 안정적
    """
    base_lat, base_lon = BASE_LOCATIONS[soldier_id]

    lat = base_lat + tick * 0.00001
    lon = base_lon + tick * 0.00001
    lat, lon = add_gps_noise(lat, lon)

    return{
        "soldier_id": soldier_id,
        "timestamp": datetime.now().isoformat(),
        "heart_rate": random.randint(90,120),
        "skin_temp": round(random.uniform(35.5, 36.5), 1),
        "acc_x": round(random.uniform(0.2, 0.9),3),
        "acc_y": round(random.uniform(0.2, 0.9),3),
        "acc_z": round(random.uniform(0.8, 1.2),3),
        "gyro_x": round(random.uniform(-0.1, 0.1),3),
        "gyro_y": round(random.uniform(-0.1, 0.1),3),
        "gyro_z": round(random.uniform(-0.1, 0.1),3),
        "latitude": lat, 
        "longitude": lon,
        "altitude": round(random.uniform(80,120),1),
        "gps_accuracy": round(random.uniform(3,8),1),
        "battery": random.randint(75, 100), 
        "signal_strength": random.randint(-70, -50),
    }

def generate_high_activity_soldier(soldier_id: str, tick: int):
    """
    고강도 기동 상태 soldier A02 출력,
    심박은 높지만 활동량도 높아 반드시 위험은 아닌 상태
    """
    base_lat, base_lon = BASE_LOCATIONS[soldier_id]

    #정상 병사보다 빠르게 이동
    lat = base_lat + tick * 0.000018
    lon = base_lon + tick * 0.000015
    lat, lon = add_gps_noise(lat, lon)

    return{
        "soldier_id": soldier_id,
        "timestamp": datetime.now().isoformat(),
        "heart_rate": random.randint(125,155),
        "skin_temp": round(random.uniform(36.0, 36.8), 1),
        "acc_x": round(random.uniform(0.8, 1.8),3),
        "acc_y": round(random.uniform(0.8, 1.8),3),
        "acc_z": round(random.uniform(0.8, 1.8),3),
        "gyro_x": round(random.uniform(-0.5, 0.5),3),
        "gyro_y": round(random.uniform(-0.5, 0.5),3),
        "gyro_z": round(random.uniform(-0.5, 0.5),3),
        "latitude": lat, 
        "longitude": lon,
        "altitude": round(random.uniform(80,120),1),
        "gps_accuracy": round(random.uniform(3,8),1),
        "battery": random.randint(70, 100), 
        "signal_strength": random.randint(-75, -55),
    }

def generate_fatigue_risk_soldier(soldier_id: str, tick: int):
    """
    탈진/낙오 위험 soldier A03 출력,
    초반: 정상 이동
    20초 이후: 심박 상승, 피부온 상승, 활동량 감소
    35초 이후: 분대 흐름에서 이탈하는 것처럼 위치가 벌어짐
    """
    base_lat, base_lon = BASE_LOCATIONS[soldier_id]

    if tick <= 20:
        #정상 이동
        heart_rate = random.randint(100,125)
        skin_temp = round(random.uniform(35.8, 36.5),1)
        acc_x = random.uniform(0.3, 0.9)
        acc_y = random.uniform(0.3, 0.9)
        acc_z = random.uniform(0.8, 1.2)
        lat = base_lat + tick * 0.00001
        lon = base_lon + tick * 0.00001

    elif tick <= 35:
        # 위험전조: 심박/피부온 상승 + 활동량 감소
        heart_rate = random.randint(150, 170)
        skin_temp = round(random.uniform(37.0, 37.5), 1)
        acc_x = random.uniform(0.02, 0.12)
        acc_y = random.uniform(0.02, 0.12)
        acc_z = random.uniform(0.02, 0.12)
        lat = base_lat + tick * 0.000006
        lon = base_lon + tick * 0.000006

    else:
        # 낙오/고립 느낌: 위치가 분대 흐름과 벌어짐
        heart_rate = random.randint(160, 180)
        skin_temp = round(random.uniform(37.2, 38.0), 1)
        acc_x = random.uniform(0.01, 0.08)
        acc_y = random.uniform(0.01, 0.08)
        acc_z = random.uniform(0.01, 0.08)
        lat = base_lat + tick * 0.000003 - 0.0010
        lon = base_lon + tick * 0.000003 - 0.0010
    
    lat, lon = add_gps_noise(lat, lon)

    return {
        "soldier_id": soldier_id,
        "timestamp": datetime.now().isoformat(),
        "heart_rate": heart_rate,
        "skin_temp": skin_temp,
        "acc_x": round(acc_x, 3),
        "acc_y": round(acc_y, 3),
        "acc_z": round(acc_z, 3),
        "gyro_x": round(random.uniform(-0.05, 0.05), 3),
        "gyro_y": round(random.uniform(-0.05, 0.05), 3),
        "gyro_z": round(random.uniform(-0.05, 0.05), 3),
        "latitude": lat,
        "longitude": lon,
        "altitude": round(random.uniform(80, 120), 1),
        "gps_accuracy": round(random.uniform(4, 10), 1),
        "battery": random.randint(65, 95),
        "signal_strength": random.randint(-85, -60),
    }



def generate_fall_risk_soldier(soldier_id: str, tick: int):
    """
    낙상/무반응 soldier A04 출력
    초반: 정상 이동
    30초 이후: 충격 이후 거의 움직임 없음 + 심박 높음
    """

    base_lat, base_lon = BASE_LOCATIONS[soldier_id]

    if tick <= 30:
        heart_rate = random.randint(95, 125)
        skin_temp = round(random.uniform(35.7, 36.6), 1)
        acc_x = random.uniform(0.3, 1.0)
        acc_y = random.uniform(0.3, 1.0)
        acc_z = random.uniform(0.8, 1.3)
        lat = base_lat + tick * 0.000012
        lon = base_lon + tick * 0.000008

    elif tick == 31:
        # 충격 순간
        heart_rate = random.randint(140, 160)
        skin_temp = round(random.uniform(36.7, 37.2), 1)
        acc_x = 3.2
        acc_y = 2.7
        acc_z = 4.1
        lat = base_lat + 30 * 0.000012
        lon = base_lon + 30 * 0.000008

    else:
        # 충격 이후 무반응
        heart_rate = random.randint(145, 165)
        skin_temp = round(random.uniform(36.8, 37.5), 1)
        acc_x = random.uniform(0.0, 0.03)
        acc_y = random.uniform(0.0, 0.03)
        acc_z = random.uniform(0.0, 0.03)
        lat = base_lat + 30 * 0.000012
        lon = base_lon + 30 * 0.000008

    lat, lon = add_gps_noise(lat, lon, scale=0.00003)

    return {
        "soldier_id": soldier_id,
        "timestamp": datetime.now().isoformat(),
        "heart_rate": heart_rate,
        "skin_temp": skin_temp,
        "acc_x": round(acc_x, 3),
        "acc_y": round(acc_y, 3),
        "acc_z": round(acc_z, 3),
        "gyro_x": round(random.uniform(-0.05, 0.05), 3),
        "gyro_y": round(random.uniform(-0.05, 0.05), 3),
        "gyro_z": round(random.uniform(-0.05, 0.05), 3),
        "latitude": lat,
        "longitude": lon,
        "altitude": round(random.uniform(80, 120), 1),
        "gps_accuracy": round(random.uniform(4, 10), 1),
        "battery": random.randint(60, 95),
        "signal_strength": random.randint(-80, -55),
    }

def generate_payload(soldier_id: str, tick: int):
    if soldier_id == "A01":
        return generate_normal_soldier(soldier_id, tick)
    
    if soldier_id == "A02":
        return generate_high_activity_soldier(soldier_id, tick)
    
    if soldier_id == "A03":
        return generate_fatigue_risk_soldier(soldier_id, tick)
    
    if soldier_id == "A04":
        return generate_fall_risk_soldier(soldier_id, tick)
    
    raise ValueError(f"Unknown soldier_id : {soldier_id}")

def main():
    tick = 0
    soldiers = ["A01", "A02", "A03", "A04"]
    print("HeatSentry tactical scenario simulator started.")
    print(f"Sending data to: {SERVER_URL}")
    print("Press Ctrl+C to stop.\n")

    while True:
        for soldier_id in soldiers:
            payload = generate_payload(soldier_id, tick)

            try:
                response = requests.post(SERVER_URL, json=payload, timeout=3)
                result = response.json()

                print(
                    f"[tick={tick:03d}] "
                    f"{soldier_id} | "
                    f"HR={payload['heart_rate']} | "
                    f"Temp={payload['skin_temp']} | "
                    f"Score={result.get('readiness_score')} | "
                    f"Level={result.get('risk_level')}"
                )

            except requests.exceptions.ConnectionError:
                print("Server connection failde. FastAPI 서버가 켜져있는지 확인하십시오. ")
                return
            
            except Exception as e:
                print(f"Error while sending {soldier_id} : {e}")
        
        tick += 1
        time.sleep(1)

if __name__ == "__main__":
    main()