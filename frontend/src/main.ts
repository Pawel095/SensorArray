import Vue from "vue";
import Root from "./Root.vue";
import router from "./router";

Vue.config.productionTip = false;

// VueResource
import VueResource from "vue-resource";
Vue.use(VueResource);

// PrimeVue
import "primevue/resources/themes/nova-light/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

import Calendar from "primevue/calendar";
Vue.component("calendar", Calendar);

import Chart from "primevue/chart";
Vue.component("chart", Chart);


new Vue({
  router,
  render: (h) => h(Root),
}).$mount("#app");
