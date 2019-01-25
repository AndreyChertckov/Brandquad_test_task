<template>
  <div class="container">
    <form class="form row">
      <div class="form-group col-5">
        <label for="ip">IP</label>
        <br>
        <input
          class="form-control search-input"
          type="text"
          placeholder="IP"
          id="ip"
          v-model="searching.ip"
        >
      </div>
      <div class="form-group col-5">
        <label for="uri">URI</label>
        <input
          class="form-control search-input"
          type="text"
          placeholder="URI"
          id="uri"
          v-model="searching.uri"
        >
      </div>
      <div class="form-group col-5">
        <label for="startDate">Start date</label>
        <input
          class="form-control search-input"
          type="datetime-local"
          placeholder="Date"
          id="startDate"
          v-model="searching.start_date"
        >
      </div>
      <div class="form-group col-5">
        <label for="endDate">End Date</label>
        <input
          class="form-control search-input"
          type="datetime-local"
          placeholder="Date"
          id="endDate"
          v-model="searching.end_date"
        >
      </div>
      <div class="form-group col-3">
        <label for="httpMethod">HTTP method</label>
        <select
          class="form-control search-input"
          type="text"
          placeholder="HTTP Method"
          id="httpMethod"
          v-model="searching.http_method"
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
      </div>
      <div class="form-group col-3">
        <label for="statusCode">Status code</label>
        <input type="number" id="statusCode" class="form-control search-input" v-model="searching.status_code">
      </div>
      <div class="form-group col-10">
        <button class="btn btn-primary" @click="searchRequest">Search</button>
      </div>
    </form>
    <table-component></table-component>
    <info-component></info-component>
  </div>
</template>

<style>
.container {
  margin-top: 5%;
}
</style>

<script>
import TableComponent from "./TableComponent.vue";
import InfoComponent from "./InfoComponent.vue";
export default {
  components: {
    TableComponent: TableComponent,
    InfoComponent: InfoComponent
  },
  data: function() {
    return {
      searching: {
        ip: "",
        start_date: "",
        end_date: "",
        status_code: "",
        uri: "",
        http_method: ""
      },
      table: [
        {
          ip: "192.168.0.1",
          date: "utseaohut",
          http_method: "GET",
          uri: "asoteuh",
          status_code: 100,
          response_size: 100
        }
      ],
      isNoData: false,
      info: {
        num_distinct_ips: 0,
        num_distinct_http_methods: 0,
        sum_response_size: 0,
        most_common_ips: []
      },
      paging: {
        current: 1,
        last: 4,
        previous: 1,
        next: 3
      },
      searchArguments: ""
    };
  },
  mounted: function() {
    this.loadLogs(-1);
  },
  methods: {
    searchRequest: function(event) {
      event.preventDefault();
      var ipInput = document.getElementById("ip");
      var reg = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
      if (
        this.searching.ip != "" &&
        !reg.test(
          this.searching.ip
        )
      ) {
        ipInput.classList.add("is-invalid");
        return;
      } else if (ipInput.classList.contains("is-invalid")) {
        ipInput.classList.remove("is-invalid");
      }
      var queryString = Object.keys(this.searching).map(key => {
        if (this.searching[key]) {
          return (
            encodeURIComponent(key) +
            "=" +
            encodeURIComponent(this.searching[key])
          );
        }
      });
      queryString = queryString
        .filter(function(el) {
          return el != null;
        })
        .join("&");
      console.log(queryString);
      this.searchArguments = queryString;
      this.table = [];
      this.isNoData = false;
      this.loadLogs(-1);
    },
    loadLogs: function(page) {
      var query = this.searchArguments;
      if (page != -1) {
        query = "page=" + page + "&" + this.searchArguments;
        this.paging.current = page;
      } else {
        this.paging.current = 1;
      }
      this.$http
        .get("/api/get_page?" + query)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.table = data["logs"];
          this.isNoData = !this.table.length;
          this.paging.next = data["next"];
          this.paging.last = data["last"];
          this.paging.previous = data["previous"];
        });
      this.$http
        .get("/api/get_info?" + query)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.info = data;
        });
    }
  }
};
</script>

