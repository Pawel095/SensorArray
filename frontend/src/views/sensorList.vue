<template>
  <div class="home">
    <table>
      <tr>
        <th>id</th>
        <th>Name</th>
        <th>Description</th>
        <th>Show data</th>
      </tr>
      <tr v-for="s in sensors" :key="s.id">
        <td>{{ s.name }}</td>
        <td>{{ s.display_name }}</td>
        <td>{{ s.description }}</td>
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
export default Vue.extend({
  data() {
    let obj: { sensors: SensorDescription[] } = {
      sensors: [],
    };
    return obj;
  },
  mounted() {
    this.$http.get("http://localhost:8000/api/sensors_list/").then((data) => {
      this.sensors = data.data;
    });
  },
});
</script>
