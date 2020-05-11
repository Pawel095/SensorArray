<template>
  <div class="singleSensorView">
    <calendar
      v-model="start"
      selectionMode="single"
      :showButtonBar="true"
      :showTime="true"
    ></calendar>
    <calendar
      v-model="end"
      selectionMode="single"
      :showButtonBar="true"
      :showTime="true"
      @date-select="updateChart($event)"
    ></calendar>
    <chart type="line" :data="chartData" :options="chartOptions"></chart>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import SingleSensorData from "../services/singleSensorData";

export default Vue.extend({
  data() {
    return {
      sid: this.$route.params.sId,
      start: new Date(+new Date() - 3600 * 1000),
      end: new Date(),
      chartData: {},
      chartOptions: {
        hoverMode: "index",
        stacked: false,
        scales: {
          yAxes: [
            {
              type: "linear",
              display: true,
              position: "left",
              id: "temp-axis",
            },
            {
              type: "linear",
              display: true,
              position: "right",
              id: "humid-axis",
              gridLines: {
                drawOnChartArea: false,
              },
            },
          ],
        },
      },
      ssd: new SingleSensorData(),
    };
  },
  mounted() {
    this.ssd.updateData(this.sid, +this.start, +this.end).then((data) => {
      console.log(data.data);
    });
  },
  methods: {
    updateChart() {
      this.ssd.updateData(this.sid, +this.start, +this.end).then((data) => {
        this.chartData = this.ssd.parseDataForChart();
      });
    },
  },
});
</script>

<style></style>
