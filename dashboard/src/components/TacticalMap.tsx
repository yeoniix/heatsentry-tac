import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import type { Soldier } from "../types/soldier";

interface TacticalMapProps {
  soldiers: Soldier[];
}

function getMarkerColor(level: Soldier["risk_level"]) {
  switch (level) {
    case "normal":
      return "#22c55e";
    case "caution":
      return "#eab308";
    case "warning":
      return "#f97316";
    case "critical":
      return "#ef4444";
    default:
      return "#94a3b8";
  }
}

function createSoldierIcon(soldier: Soldier) {
  const color = getMarkerColor(soldier.risk_level);

  return L.divIcon({
    className: "soldier-marker-wrapper",
    html: `
      <div class="soldier-marker" style="border-color: ${color}; box-shadow: 0 0 18px ${color};">
        <div class="soldier-marker-dot" style="background: ${color};"></div>
        <span>${soldier.soldier_id}</span>
      </div>
    `,
    iconSize: [64, 42],
    iconAnchor: [32, 21],
    popupAnchor: [0, -22],
  });
}

function getMapCenter(soldiers: Soldier[]): [number, number] {
  if (soldiers.length === 0) {
    return [37.5665, 126.978];
  }

  const latSum = soldiers.reduce((sum, soldier) => sum + soldier.latitude, 0);
  const lonSum = soldiers.reduce((sum, soldier) => sum + soldier.longitude, 0);

  return [latSum / soldiers.length, lonSum / soldiers.length];
}

function getRiskLabel(level: Soldier["risk_level"]) {
  switch (level) {
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

export default function TacticalMap({ soldiers }: TacticalMapProps) {
  const center = getMapCenter(soldiers);

  return (
    <section className="map-panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">GPS Tactical Map</p>
          <h2>실시간 위치 관제</h2>
        </div>
        <span>{soldiers.length}명 추적 중</span>
      </div>

      <div className="map-container">
        <MapContainer
          center={center}
          zoom={16}
          scrollWheelZoom={true}
          className="leaflet-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {soldiers.map((soldier) => (
            <Marker
              key={soldier.soldier_id}
              position={[soldier.latitude, soldier.longitude]}
              icon={createSoldierIcon(soldier)}
            >
              <Popup>
                <div className="map-popup">
                  <strong>{soldier.soldier_id}</strong>
                  <p>상태: {getRiskLabel(soldier.risk_level)}</p>
                  <p>전투지속능력: {soldier.readiness_score}/100</p>
                  <p>심박: {soldier.heart_rate} bpm</p>
                  <p>피부온도: {soldier.skin_temp} ℃</p>
                  <p>활동량: {soldier.acc_mag}</p>
                  <p>활동 상태: {soldier.activity_state}</p>
                  <p>위험 유형: {soldier.risk_type}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </section>
  );
}