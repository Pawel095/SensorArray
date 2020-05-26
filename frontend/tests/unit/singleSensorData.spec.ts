import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from "vue-router";

import { VueConstructor } from "vue";
jest.mock("../../src/services/sensorList");

let localVue: VueConstructor<Vue>;
let router: VueRouter;

beforeEach(() => {
  localVue = createLocalVue();
  localVue.use(VueRouter);
  router = new VueRouter();
});

// czy się załadował,
// czy się zamontował,
// czy zainicjalizował elementy
describe("SensorList", () => {
  it("Renders a list of sensors from data in props.", async () => {});
});
