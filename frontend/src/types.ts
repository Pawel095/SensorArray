export interface SensorDescription {
  id: number;
  name: string;
  display_name: string;
  description: string;
}
export default interface IsingleSensorData {
  temperature: number;
  humidity: number;
  timestamp: string;
}
