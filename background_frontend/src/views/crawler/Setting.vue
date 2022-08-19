<template>
  <div class="setting">
    <div class="header">
      爬虫设置
    </div>
    <el-row>
      <el-col :span="4">
        <el-button type="primary" @click="runCrawler">Primary</el-button>
      </el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
    </el-row>
  </div>
</template>

<script setup>
import {get} from '/api'
import {ElMessage} from 'element-plus'

const runCrawler = async () => {
  const env = 'dev'
  const resp = get('/admin/crawler/run', {env})
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else ElMessage.success(resp.msg)
}
</script>

<style scoped>

</style>