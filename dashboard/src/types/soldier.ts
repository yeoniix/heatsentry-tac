export type RiskLevel = "normal" | "caution" | "warning" | "critical";

export type RiskType =
  | "normal"
  | "fatigue_or_heat_stress"
  | "heat_stress_risk"
  | "fall_or_no_response"
  | "impact_detected"
  | "battery_risk"
  | "signal_loss_risk";

export type ActivityState =
  | "no_response"
  | "low_activity"
  | "normal_activity"
  | "high_activity"
  | "impact";
  
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
  risk_type: RiskType;
  activity_state: ActivityState;
}

