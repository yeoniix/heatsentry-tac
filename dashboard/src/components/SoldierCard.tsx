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