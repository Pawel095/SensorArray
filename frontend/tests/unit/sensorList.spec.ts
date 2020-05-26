import { shallowMount, createLocalVue } from "@vue/test-utils";
import VueRouter from "vue-router";
import sensorList from "@/views/sensorList.vue";
import flushPromises from "flush-promises";

import sensorListService from "../../src/services/sensorList";
import { VueConstructor } from "vue";
jest.mock("../../src/services/sensorList");

let localVue: VueConstructor<Vue>;
let router: VueRouter;
beforeEach(() => {
  localVue = createLocalVue();
  localVue.use(VueRouter);
  router = new VueRouter();
});

it("Renders a list of sensors from data in props.", async () => {
  const service = new sensorListService();
  const wrapper = shallowMount(sensorList, {
    data() {
      return {
        service,
      };
    },
    localVue,
    router,
  });
  await flushPromises();

  let tableData = wrapper
    .find("table.sensorList")
    .findAll("tr.data")
    .wrappers.map((e, index) => {
      const id = index + 1;
      const name = e.find(".name").text();
      const display_name = e.find(".display_name").text();
      const description = e.find(".description").text();
      return {
        id,
        name,
        display_name,
        description,
      };
    });
  expect(tableData).toStrictEqual(service.lastData);
});
