import axios from "axios";
import IsingleSensorData from "./IsingleSensorData";

export default class SingleSensorData {
  url = "http://localhost:8000/api/log_data/";
  lastData: IsingleSensorData[];
  constructor() {
    this.lastData = [];
  }

  updateData(sensorId: string, start = -1, end = -1) {
    let params = {};
    if (start > 0) {
      const add = { start: start / 1000 };
      params = { ...params, ...add };
    }
    if (end > 0) {
      const add = { end: end / 1000 };
      params = { ...params, ...add };
    }
    return axios
      .get(this.url + sensorId + "/", { params: params })
      .then((data) => {
        this.lastData = data.data;
        return data;
      });
  }

  parseDataForChart() {
    const dates = this.lastData.map((e) => {
      return new Date(e.timestamp);
    });

    const temperatures = this.lastData.map((e) => {
      return e.temperature;
    });
    const humidities = this.lastData.map((e) => {
      return e.humidity;
    });
    let ret = {
      labels: dates,
      datasets: [
        {
          label: "Temperature",
          fill: false,
          backgroundColor: "#2f4860",
          borderColor: "#2f4860",
          yAxisID: "temp-axis",
          data: temperatures,
        },
        {
          label: "Humidity",
          fill: false,
          backgroundColor: "#00bb7e",
          borderColor: "#00bb7e",
          yAxisID: "humid-axis",
          data: humidities,
        },
      ],
    };
    console.log(ret);
    return ret;
  }
}
