<template>
  <div class="news-detail">
    <div class="header">
      <el-button type="info" @click="back">返回新闻列表</el-button>
    </div>
    <div class="main" style="width: 70%">
      <div class="description" style="margin-bottom: 10px">
        <h1 style="margin: 50px auto">{{ newsDetail.title }}</h1>
        <div class="datetime">发布时间：{{ newsDetail.datetime }}</div>
        <div class="website">新闻来源：{{ newsDetail.website }}</div>
        <div class="url">原网址：<a target="_blank" :href="newsDetail.url">{{ newsDetail.url }}</a></div>
      </div>
      <div class="content" style="line-height: 24px">{{ newsDetail.text }}</div>
    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'
import {get} from '/api'
import {reactive, onBeforeMount, ref} from 'vue'

const $router = useRouter()
const $route = $router.currentRoute.value


let newsDetail = ref({
  title: '',
  datetime: '',
  text: '',
  url: '',
  website: ''
})
const getNewsDetail = async () => {
  const website = $route.params.website
  const newsId = $route.params.newsId
  const news = {
    'website': website,
    'newsId': newsId
  }
  const resp = await get('/user/news/detail', news)
  if (resp === undefined) return
  newsDetail.value = resp.data['newsDetail']
  console.log(newsDetail.value.title)
}

onBeforeMount(getNewsDetail)

const back = () => {
  $router.go(-1)
}
</script>

<style lang="scss" scoped>
.news-detail {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;

  .header {
    padding-top: 10px;
    padding-right: 10px;
    display: flex;
    justify-content: end;
  }

  .main {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}
</style>