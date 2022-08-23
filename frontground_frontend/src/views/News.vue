<template>
  <div class="news">
    <div class="main">
      <el-table
          :data="newsList"
          stripe
          border
          style="width: 100%"
          highlight-current-row
          table-layout="auto"
          @row-dblclick="handleDblClick"
      >
        <el-table-column type="index"/>
        <el-table-column prop="title" label="标题"/>
        <el-table-column prop="datetime" label="日期时间"/>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'
import {onMounted, ref} from 'vue'
import {get} from '/api'

const $router = useRouter()
const $route = $router.currentRoute.value

let newsList = ref([])
const getNewsList = async () => {
  const enName = $route.path.split('/').pop()
  const resp = await get('/user/news/all', {enName})
  if (resp === undefined) return
  newsList.value = resp.data['newsList']
}

onMounted(getNewsList)

const handleDblClick = (row, column, event) => {
  const enName = $route.params.enName
  const newsId = row['_id']
  $router.push({name: 'newsDetail', params: {newsId}})
}
</script>

<style lang="scss" scoped>
.news {
  height: 100%;
  display: flex;
  justify-content: space-evenly;

  .main {
    display: flex;
    flex-direction: column;
    width: 60%;
    height: 100%;
  }
}
</style>