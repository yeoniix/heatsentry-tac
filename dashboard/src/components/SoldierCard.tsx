import type { Soldier } from "../types/soldier";

interface SoldierCardProps{
    soldier: Soldier;
}

function getRiskLabel(level:Soldier["risk_level"]){
    switch(level){
        case "normal":
            return "정상";
        case "caution":
            return "주의";
        case "warning":
            return "경고";
        case "critical":
            return "위험";
        default:
            return "알 수 없음";
    }
}

function getRiskClass(level: Soldier["risk_level"]){
    switch(level){
         case "normal":
            return "card normal";
        
        case "caution":
            return "card caution";
            
        case "warning":
            return "card warning";
        
        case "critical":
            return "card critical";
        
        default:
            return "card";
    }
}

function getRiskTypeLabel(type: Soldier["risk_type"]) {
  switch (type) {
    case "normal":
      return "정상";
    case "fatigue_or_heat_stress":
      return "탈진/열스트레스 위험";
    case "heat_stress_risk":
      return "열스트레스 위험";
    case "fall_or_no_response":
      return "낙상/무반응 위험";
    case "impact_detected":
      return "충격 감지";
    case "battery_risk":
      return "배터리 위험";
    case "signal_loss_risk":
      return "통신 위험";
    default:
      return "알 수 없음";
  }
}

function getActivityLabel(activity: Soldier["activity_state"]) {
  switch (activity) {
    case "no_response":
      return "무반응";
    case "low_activity":
      return "저활동";
    case "normal_activity":
      return "정상 활동";
    case "high_activity":
      return "고강도 활동";
    case "impact":
      return "충격";
    default:
      return "알 수 없음";
  }
}

export default function SoldierCard({ soldier }: SoldierCardProps) {
  return (
    <div className={getRiskClass(soldier.risk_level)}>
      <div className="card-header">
        <div>
          <h2>{soldier.soldier_id}</h2>
          <p className="subtitle">{getRiskLabel(soldier.risk_level)}</p>
        </div>

        <div className="score">
          {soldier.readiness_score}
          <span>/100</span>
        </div>

      </div>
      <div className="metrics">
        <div>
          <span>심박</span>
          <strong>{soldier.heart_rate} bpm</strong>
        </div>
        <div>
          <span>피부온도</span>
          <strong>{soldier.skin_temp} ℃</strong>
        </div>
        <div>
          <span>활동량</span>
          <strong>{soldier.acc_mag}</strong>
        </div>
        <div>
          <span>배터리</span>
          <strong>{soldier.battery}%</strong>
        </div>
        <div>
            <span>활동 상태</span>
            <strong>{getActivityLabel(soldier.activity_state)}</strong>
        </div>
        <div>
            <span>위험 유형</span>
            <strong>{getRiskTypeLabel(soldier.risk_type)}</strong>
        </div>
    </div>

      <div className="location">
        <span>GPS</span>
        <p>
          {soldier.latitude.toFixed(5)}, {soldier.longitude.toFixed(5)}
        </p>
      </div>

      {soldier.risk_reasons.length > 0 && (
        <div className="reasons">
          <span>위험 원인</span>
          <ul>
            {soldier.risk_reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

