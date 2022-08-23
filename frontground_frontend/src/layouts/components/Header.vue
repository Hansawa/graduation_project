<template>
  <el-header>
    <el-menu
        :default-active="$route.path"
        class="el-menu"
        mode="horizontal"
        router
        @select="handleSelect"
    >
      <el-menu-item class="website-name" :index="'/user/welcome'">NewsAggregator</el-menu-item>
      <el-menu-item v-for="website in websiteList" :index="'/user/' + website.enName">{{ website.cnName }}</el-menu-item>
    </el-menu>
  </el-header>
</template>

<script setup>
import {useRouter} from 'vue-router'
import {onBeforeMount, ref} from 'vue'
import {get} from '/api'

const $router = useRouter()
const $route = $router.currentRoute.value

let websiteList = ref([])
const getWebsiteList = async () => {
  const resp = await get('/user/news/website/all')
  if (resp === undefined) {
    websiteList.value = null
  }
  websiteList.value = resp.data['websiteList']
  if ($route.path === '/user/welcome') {
    window.document.title = 'NewsAggregator | 欢迎'
  }
  const cnName = '';
  const enName = $route.path.split('/').pop()
  for (let i = 0; i < websiteList.value.length; i++) {
    if (websiteList.value[i].enName === enName) {
      window.document.title = 'NewsAggregator | ' + websiteList.value[i].cnName
    }
  }
}
onBeforeMount(getWebsiteList)

const handleSelect = (index, indexPath, item, routeResult) => {
  if (index === '/user/welcome') {
    window.document.title = 'NewsAggregator | 欢迎'
  }
  const cnName = '';
  const enName = index.split('/').pop()
  for (let i = 0; i < websiteList.value.length; i++) {
    if (websiteList.value[i].enName === enName) {
      window.document.title = 'NewsAggregator | ' + websiteList.value[i].cnName
    }
  }
}
</script>

<style lang="scss" scoped>
.el-header {
  //display: flex;
  //justify-content: flex-start;
  padding-left: 0;
  align-items: center;
  font-size: 20px;

  .website-name {
    color: #409eff;
    font-weight: bolder;
    font-size: 20px;
  }

  .el-menu {
    border-bottom: none;
  }
}
</style>