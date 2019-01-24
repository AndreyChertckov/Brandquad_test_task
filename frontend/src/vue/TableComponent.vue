<template>
  <div class="main">
    <table class="table">
      <tr>
        <th>IP</th>
        <th>Date</th>
        <th>HTTP Method</th>
        <th>URI</th>
        <th>Status code</th>
        <th>Size of response</th>
      </tr>
      <tr v-for="log in this.$parent.table" :key="log['id']">
        <td>{{ log['ip'] }}</td>
        <td>{{ log['date'] }}</td>
        <td>{{ log['http_method'] }}</td>
        <td>{{ log['uri'] }}</td>
        <td>{{ log['status_code'] }}</td>
        <td>{{ log['response_size'] }}</td>
      </tr>
    </table>
    <div v-if="!this.$parent.table.length" class="offset-5">Loading...</div>
    <div v-else>
      <nav>
        <ul class="pagination">
          <li class="page-item">
            <span class="page-link">First</span>
          </li>
          <li class="page-item">
            <span class="page-link">{{ this.$parent.paging.previous }}</span>
          </li>
          <li class="page-item active">
            <span class="page-link">
              {{ this.$parent.paging.current }}
              <span class="sr-only">(current)</span>
            </span>
          </li>
          <li class="page-item">
            <span class="page-link">{{ this.$parent.paging.next }}</span>
          </li>
          <li class="page-item">
            <span class="page-link">Last</span>
          </li>
        </ul>
      </nav>
      <div class="offset-10 col-2">
        <a class="btn btn-primary" href="/api/download_logs">Download logs</a>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
</script>
