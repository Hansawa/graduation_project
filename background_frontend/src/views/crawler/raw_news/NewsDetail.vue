<template>
  <div class="news-detail">
    <el-breadcrumb separator=">">
      <el-breadcrumb-item>爬虫管理</el-breadcrumb-item>
      <el-breadcrumb-item>未处理新闻</el-breadcrumb-item>
      <el-breadcrumb-item>网站：{{ props.websiteName }}</el-breadcrumb-item>
      <el-breadcrumb-item>标题：{{ props.title }}</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script setup>
import {onBeforeMount} from 'vue'
import {useRouter} from 'vue-router'

const props = defineProps({
  websiteName: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})

const $router = useRouter()
onBeforeMount(() => {
  console.log($router.currentRoute.value.matched)
})
</script>

<style scoped>

</style>