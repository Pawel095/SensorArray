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
    ></calendar>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  data() {
    return {
      sid: this.$route.params.sId,
      start: new Date(+new Date() - 3600 * 1000),
      end: new Date(),
    };
  },
  mounted() {
    this.$http
      .get("http://localhost:8000/api/log_data/" + this.sid + "/")
      .then((data) => {
        console.log(data.data);
      });
  },
});
</script>

<style></style>
