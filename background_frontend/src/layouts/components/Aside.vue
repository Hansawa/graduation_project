<template>
  <el-aside>
    <!-- 菜单的折叠与展开 -->
    <div class="logo-box">
      <div class="website-name" v-show="!isCollapse">NewsAggregator</div>
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
</template>

<script setup>
import {ref, onBeforeMount, reactive} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()

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
const menuList = reactive([
  {id: 1, tab: '欢迎！', path: 'welcome', icon: 'StarFilled'},
  {id: 2, tab: '新闻管理', path: 'newsmanage', icon: 'Notebook'},
  {id: 3, tab: '评论管理', path: 'commentmanage', icon: 'ChatDotSquare'},
  {id: 4, tab: '用户管理', path: 'usermanage', icon: 'User'},
  {id: 5, tab: '我的账号', path: 'selfaccount', icon: 'Tools'}
])

let activePath = ref('')
onBeforeMount(() => activePath = router.path)
</script>

<style scoped>
.logo-box {
  height: 50px;
  box-sizing: border-box;
  padding: 10px;
  display: flex;
  justify-content: space-around;
  align-items: center;

.website-name {
  color: #409eff;
  font-weight: bolder;
  line-height: 25px;
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
</style>