import axios from "axios";
import IsingleSensorData from "@/types";

export default class SensorListService {
  url = "http://localhost:8000/api/sensors_list/";
  lastData: IsingleSensorData[];
  constructor() {
    this.lastData = [];
  }

  getData() {
    return axios.get(this.url).then((data) => {
      this.lastData = data.data;
      return data;
    });
  }
}
