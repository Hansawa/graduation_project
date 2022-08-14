<template>
  <el-header>
    <div>
      <span>新闻聚合后台系统</span>
    </div>
    <el-button type="info" @click="logout">退出</el-button>
  </el-header>
</template>

<script setup>
import {useRouter} from 'vue-router'

const router = useRouter()
/* 清除自动登录 */
const logout = () => {
  window.localStorage.clear()
  window.sessionStorage.clear()
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.el-header {
  height: 50px;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  font-size: 20px;

  div {
    display: flex;
    align-items: center;

    span {
      margin-left: 15px;
    }
  }
}
</style>