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
            <span class="page-link" @click="switchPage(-1)">First</span>
          </li>
          <li class="page-item" v-if="$parent.paging.previous">
            <span class="page-link" @click="switchPage($parent.paging.previous)">{{ $parent.paging.previous }}</span>
          </li>
          <li class="page-item active">
            <span class="page-link">
              {{ $parent.paging.current }}
              <span class="sr-only">(current)</span>
            </span>
          </li>
          <li class="page-item" v-if="$parent.paging.next">
            <span class="page-link" @click="switchPage($parent.paging.next)">{{ $parent.paging.next }}</span>
          </li>
          <li class="page-item">
            <span class="page-link" @click="switchPage($parent.paging.last)">Last</span>
          </li>
        </ul>
      </nav>
      <div class="offset-10 col-2">
        <a class="btn btn-primary" :href="'/api/download_logs?' + $parent.searchArguments">Download logs</a>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
export default {
  methods: {
    switchPage: function(page_num) {
      this.$parent.loadLogs(page_num);
    }
  }
}
</script>
