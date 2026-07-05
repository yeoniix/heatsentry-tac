import { useEffect, useState } from "react";
import "./App.css";
import { fetchSoldiers } from "./api/soldier";
import SoldierCard from "./components/SoldierCard";
import type { Soldier } from "./types/soldier";

function App() {
  const [soldiers, setSoldiers] = useState<Soldier[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>("");

  async function loadSoldiers() {
    try {
      const data = await fetchSoldiers();
      setSoldiers(data);
      setLastUpdated(new Date().toLocaleTimeString());
      setError(null);
    } catch (err) {
      console.error(err);
      setError("서버에서 병사 데이터를 가져오지 못했습니다.");
    }
  }

  useEffect(() => {
    //loadSoldiers();

    const intervalId = window.setInterval(() => {
      loadSoldiers();
    }, 1000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, []);

  const normalCount = soldiers.filter((s) => s.risk_level === "normal").length;
  const cautionCount = soldiers.filter((s) => s.risk_level === "caution").length;
  const warningCount = soldiers.filter((s) => s.risk_level === "warning").length;
  const criticalCount = soldiers.filter((s) => s.risk_level === "critical").length;

  return (
    <main className="app">
      <section className="hero">
        <div>
          <p className="eyebrow">HeatSentry Tactical Dashboard</p>
          <h1>전술훈련 생체위험 관제 대시보드</h1>
          <p className="description">
            웨어러블 센서와 GPS 데이터를 기반으로 병사의 전투지속능력과 위험 상태를 실시간으로 표시합니다.
          </p>
        </div>

        <div className="status-panel">
          <div>
            <span>정상</span>
            <strong>{normalCount}</strong>
          </div>
          <div>
            <span>주의</span>
            <strong>{cautionCount}</strong>
          </div>
          <div>
            <span>경고</span>
            <strong>{warningCount}</strong>
          </div>
          <div>
            <span>위험</span>
            <strong>{criticalCount}</strong>
          </div>
        </div>
      </section>

      <section className="toolbar">
        <span>연결 서버: http://127.0.0.1:8000</span>
        <span>마지막 갱신: {lastUpdated || "-"}</span>
      </section>

      {error && <div className="error">{error}</div>}

      <section className="grid">
        {soldiers.length === 0 && !error ? (
          <div className="empty">
            아직 수신된 병사 데이터가 없습니다. FastAPI 서버와 simulator.py를 실행하세요.
          </div>
        ) : (
          soldiers.map((soldier) => (
            <SoldierCard key={soldier.soldier_id} soldier={soldier} />
          ))
        )}
      </section>
    </main>
  );
}

export default App;