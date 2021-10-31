<template>
  <div id="app">
    <Map class="main-map" />
    <el-table class="table" :data="region_info['data']">
      <el-table-column prop="region" label="Район города" width="400" />
      <el-table-column
        prop="problem"
        label="Самая распространённая проблема"
        width="400"
      />
      <el-table-column prop="num" label="Колличество" width="200" />
    </el-table>
  </div>
</template>

<script>
import Map from "@/components/map.vue";

export default {
  name: "App",
  components: {
    Map,
  },
  data() {
    return {
      region_info: {},
    };
  },
  async mounted() {
    await fetch("http://127.0.0.1:5000/get_info", {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: {}, // body data type must match "Content-Type" header
    })
      .then((response) => response.json())
      .then((data) => {
        this.region_info = data;
      })
      .catch(() => {});
  },
};
</script>

<style>
.table {
  width: 700px;
  margin: 30px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.el-header,
.el-footer {
  background-color: #ebebeb57;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 60px;
}
.el-main {
  background-color: #e9eef3;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 160px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
}
</style>
