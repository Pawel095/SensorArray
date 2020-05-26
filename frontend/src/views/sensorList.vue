<template>
  <div class="home">
    <table class="sensorList">
      <tr>
        <th>id</th>
        <th>Name</th>
        <th>Description</th>
        <th>Show data</th>
      </tr>
      <tr v-for="s in sensors" :key="s.id" class="data">
        <td class="name">{{ s.name }}</td>
        <td class="display_name">{{ s.display_name }}</td>
        <td class="description">{{ s.description }}</td>
        <td>
          <router-link tag="button" :to="'/sensor/' + s.name"
            >Show Data</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { SensorDescription } from "../types";
import SensorListService from "@/services/sensorList";

export default Vue.extend({
  data() {
    let obj: { sensors: SensorDescription[]; service: SensorListService } = {
      sensors: [],
      service: new SensorListService(),
    };
    return obj;
  },
  mounted() {
    this.service.updateData().then((data) => {
      this.sensors = data.data;
    });
  },
});
</script>
