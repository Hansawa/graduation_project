<template>
  <el-container class="home-container">
    <el-aside width="auto">
      <!-- 菜单的折叠与展开 -->
      <div style="height: 50px;">
        <el-icon :size="25" @click="isCollapse = !isCollapse">
          <Expand />
        </el-icon>
      </div>
      <!-- 侧边栏菜单区 -->
<!--      background-color="#333744"-->
      <el-menu
          class="el-menu-container"
          text-color="#303133"
          active-text-color="#409eff"
          :collapse="isCollapse"
          :collapse-transition="true"
          router
          :default-active="activePath ? activePath : '/welcome'">
        <el-menu-item
            v-for="item in menuList"
            :index="'/'+item.path"
            :key="item.id">
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.tab }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div>
          <span>新闻聚合后台系统</span>
        </div>
        <el-button type="info" @click="logout">退出</el-button>
      </el-header>
      <!-- 右侧内容主题 -->
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
const $router = useRouter()

const isCollapse = ref(false)

const menuList = ref([
  {id: 1, tab: '欢迎！', path: 'welcome', icon: 'StarFilled'},
  {id: 2, tab: '新闻管理', path: 'newsmanage', icon: 'Notebook'},
  {id: 3, tab: '评论管理', path: 'commentmanage', icon: 'ChatDotSquare'},
  {id: 4, tab: '用户管理', path: 'usermanage', icon: 'User'},
  {id: 5, tab: '我的账号', path: 'selfaccount', icon: 'Tools'}
])

const logout = () => {
  window.sessionStorage.clear()
  $router.push('/login')
}

let activePath =  ref('')
onBeforeMount(() => activePath = $router.path)
</script>

<style lang="scss" scoped>
.el-menu-container:not(.el-menu--collapse) {
  width: 200px;
}

.el-menu {
  border-right: solid 1px;
  border-color: #dcdfe6;
  height: calc(100% - 50px);
}

.home-container {
  height: 100%;
}

.el-header {
  height: 50px;
  //background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  //color: #fff;
  font-size: 20px;

  div {
    display: flex;
    align-items: center;

    span {
      margin-left: 15px;
    }
  }
}

.el-aside {
  //background-color: #333744;
}

.el-main {
  background-color: #eaedf1;
}

.toggle-button {
  background-color: #6b7486;
  color: #eee;
  //font-size: 10px;
  line-height: 24px;
  text-align: center;
  //letter-spacing: 0.2em;
  cursor: pointer;
}
</style>