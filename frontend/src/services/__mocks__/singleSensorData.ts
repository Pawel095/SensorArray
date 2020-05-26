import IsingleSensorData from "@/types";

export default class SingleSensorData {
  lastData: IsingleSensorData[];

  mockData = {};

  constructor() {
    this.lastData = [];
  }

  makeParams(start: number, end: number) {
    let params = {};
    if (start > 0) {
      const add = { start: start / 1000 };
      params = { ...params, ...add };
    }
    if (end > 0) {
      const add = { end: end / 1000 };
      params = { ...params, ...add };
    }
    return params;
  }

  updateData(sensorId: string, start = -1, end = -1) {
    const params = this.makeParams(start, end);
  }

  parseDataForChart() {}
}
