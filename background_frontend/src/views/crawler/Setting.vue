<template>
  <div class="setting">
    <div class="header">
      爬虫设置
    </div>
    <el-row>
      <el-button type="primary" @click="runCrawler">爬取已配置的网站</el-button>
      <el-button type="primary" @click="stopCrawler">停止爬取</el-button>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-button type="primary" @click="runProxy">开启代理爬取</el-button>
      <el-button type="primary" @click="stopProxy">关闭代理爬取</el-button>
    </el-row>
    {{ message }}
  </div>
</template>

<script setup>
import {get} from '/api'
import {ElMessage} from 'element-plus'
import {ref} from "vue";


/* 声明计时器，用来轮询是否完成爬取 */
let timer = null
/* 轮询方法 */
const polling = async () => {
  const resp = await get('/admin/crawler/setting/polling')
  if (resp.status === 201) return ElMessage.warning(resp.headers.msg)
  clearInterval(timer)
}
const runCrawler = async () => {
  get('/admin/crawler/setting/crawl/all')
  timer = setInterval(polling, 2000)
}

const stopCrawler = async () => {
  clearInterval(timer)
}

let message = ref('')
const runProxy = () => {
  const resp = get('/admin/proxy/run')
}
const stopProxy = () => {
  const resp = get('/admin/proxy/stop')
}
</script>

<style scoped>

</style>