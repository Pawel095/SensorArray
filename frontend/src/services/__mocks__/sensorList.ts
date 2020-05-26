export default class SensorListService {
  lastData = [
    {
      id: 1,
      name: "tm1xpgiizrinoxo6w2zd",
      display_name: "Sensor 1",
      description: "Data collected 2020-05-07 to 2020-05-08",
    },
    {
      id: 2,
      name: "7jisve665ybr8jbplhqz",
      display_name: "Sensor2",
      description: "Collection from 2020-05-11 to 2020-05-12",
    },
  ];
  updateData() {
    return new Promise((resolve) => {
      resolve({ data: this.lastData });
    });
  }
}
