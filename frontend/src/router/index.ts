import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import sensorList from "../views/sensorList.vue";
import singleSensorView from "../views/singleSensorView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "SensorList",
    component: sensorList,
  },
  {
    path: "/sensor/:sId",
    name: "single sensor data view",
    component: singleSensorView,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
