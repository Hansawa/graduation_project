<template>
  <el-container class="layout-box">
    <el-aside>
      <!-- 菜单的折叠与展开 -->
      <div class="logo-box">
        <div class="website-name" v-if="!isCollapse">NewsAggregator</div>
        <el-icon :size="25" color="#409eff" @click="onCollapse">
          <Expand class="expand"/>
        </el-icon>
      </div>
      <!-- 侧边栏菜单区 -->
      <el-menu
          text-color="#303133"
          active-text-color="#409eff"
          :collapse="isCollapse"
          :collapse-transition="false"
          router
          :default-active="activePath ? activePath : '/welcome'">
        <el-menu-item
            v-for="item in menuList"
            :index="'/'+item.path"
            :key="item.id">
          <el-icon>
            <component :is="item.icon"/>
          </el-icon>
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
import {ref, onBeforeMount} from 'vue'
import {useRouter} from 'vue-router'

const $router = useRouter()

/* 菜单栏折叠所需 */
let isCollapse = ref(true)
let menuWidth = ref('64px')
let iconDeg = ref(0)
const onCollapse = () => {
  isCollapse.value = !isCollapse.value
  menuWidth.value = isCollapse.value ? '64px' : '260px'
  iconDeg.value = isCollapse.value? 0: '180deg'
}

/* 菜单列表 */
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

let activePath = ref('')
onBeforeMount(() => activePath = $router.path)
</script>

<style lang="scss" scoped>
.layout-box {
  height: 100%;
}

.logo-box {
  height: 50px;
  box-sizing: border-box;
  padding: 10px;
  display: flex;
  justify-content: space-around;
  align-items: center;

  .website-name {
    color: #409eff;
    padding-left: 4px;
    font-weight: 600;
    cursor: default;
  }

  .expand {
    transition: transform 300ms ease;
    transform: rotateY(v-bind(iconDeg));
  }
}

.el-aside {
  transition: width 300ms ease;
  width: v-bind(menuWidth);

  .el-menu {
    border-right: 0;
    height: calc(100% - 50px);
  }
}

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