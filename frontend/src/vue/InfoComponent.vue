<template>
  <div class="container">
    <div class="row info">
      <div class="col-3">Number of uniq IPs:</div>
      <div class="col-3">{{ this.$parent.info.num_distinct_ips }}</div>
    </div>
    <div class="row info">
      <div class="col-3">Number of uniq http_methods:</div>
      <div class="col-3">{{ this.$parent.info.num_distinct_http_methods }}</div>
    </div>
    <div class="row info">
      <div class="col-3">Sum of response size:</div>
      <div class="col-3">{{ this.$parent.info.sum_response_size }}</div>
    </div>
    <div class="info">Most common IPs:
      <table class="table info">
        <tr>
          <th>#</th>
          <th>IP</th>
        </tr>
        <tr v-for="(ip,i) in this.$parent.info.most_common_ips" :key="i">
          <td>{{ i+1 }}</td>
          <td>{{ ip }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<style>
.info {
  padding-top: 12px;
}
</style>

<script>
export default {};
</script>
