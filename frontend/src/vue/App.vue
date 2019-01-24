<template>
  <div class="container">
    <div class="row">
      <div class="col-2">IP</div>
      <div class="col-3">Start Date</div>
      <div class="col-3">End Date</div>
      <div class="col-2">HTTP Method</div>
    </div>
    <form class="form row">
      <input
        class="form-control col-2 search-input"
        type="text"
        placeholder="IP"
        id="ip"
        v-model="ip"
      >
      <input
        class="form-control col-3 search-input"
        type="datetime-local"
        placeholder="Date"
        id="startDate"
        v-model="startDate"
      >
      <input
        class="form-control col-3 search-input"
        type="datetime-local"
        placeholder="Date"
        id="endDate"
        v-model="endDate"
      >
      <select
        class="form-control col-2 search-input"
        type="text"
        placeholder="HTTP Method"
        id="httpMethod"
        v-model="httpMethod"
      >
        <option value>All</option>
        <option value="GET">GET</option>
        <option value="POST">POST</option>
        <option value="HEAD">HEAD</option>
        <option value="PUT">PUT</option>
        <option value="DELETE">DELETE</option>
        <option value="CONNECT">CONNECT</option>
        <option value="TRACE">TRACE</option>
        <option value="OPTIONS">OPTIONS</option>
      </select>
      <button class="col-1 btn btn-primary" @click="searchRequest">Search</button>
    </form>
  </div>
</template>

<style>
.container {
  margin-top: 5%;
}
.search-input {
  padding-right: 4px;
}
</style>

<script>
export default {
  data: function() {
    return {
      ip: "",
      startDate: "",
      endDate: "",
      httpMethod: "",
      table: []
    };
  },
  mounted: function() {

  },
  methods: {
    searchRequest: function(event) {
      event.preventDefault();
      var ipInput = document.getElementById("ip");
      if (
        this.ip != "" &&
        !/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(
          this.ip
        )
      ) {
        ipInput.classList.add("is-invalid");
      } else if (ipInput.classList.contains("is-invalid")) {
        ipInput.classList.remove("is-invalid");
      }
      this.table = [];
    }
  }
};
</script>

