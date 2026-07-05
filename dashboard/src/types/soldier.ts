export type RiskLevel = "normal" | "caution" | "warning" | "critical";

export interface Soldier {
  soldier_id: string;
  timestamp: string;
  heart_rate: number;
  skin_temp: number;
  acc_x: number;
  acc_y: number;
  acc_z: number;
  gyro_x: number;
  gyro_y: number;
  gyro_z: number;
  latitude: number;
  longitude: number;
  altitude: number;
  gps_accuracy: number;
  battery: number;
  signal_strength: number;
  server_received_at: string;
  readiness_score: number;
  risk_level: RiskLevel;
  risk_reasons: string[];
  acc_mag: number;
}