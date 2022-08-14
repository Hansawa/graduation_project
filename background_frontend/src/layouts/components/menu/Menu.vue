<template>
  <!-- 侧边栏菜单区 -->
  <el-menu
      text-color="#303133"
      active-text-color="#409eff"
      :collapse="props.isCollapse"
      :collapse-transition="false"
      :router="true"
      :default-active="activePath ? activePath : '/welcome'"
      @open="handleOpen"
      @close="handleClose"
  >
    <MenuItem :menu-list="menuList"/>
  </el-menu>
</template>

<script setup>
import {onBeforeMount, reactive, ref, defineProps} from 'vue'
import {useRouter} from 'vue-router'
import MenuItem from '/layouts/components/menu/MenuItem.vue'

const props = defineProps({
  isCollapse: {
    type: Boolean,
    required: true
  }
})

/* 菜单列表 */
const menuList = reactive([
  {id: '1', tab: '欢迎！', path: 'welcome', icon: 'StarFilled'},
  {
    id: '2', tab: '爬虫管理', path: 'crawler', icon: 'Collection', children: [
      {id: '2-1', tab: '爬虫设置', path: 'settings', icon: 'Collection'},
      {id: '2-2', tab: '配置文件', path: 'configs', icon: 'Collection'}
    ]
  },
  {id: '3', tab: '评论管理', path: 'comment', icon: 'ChatDotSquare'},
  {id: '4', tab: '用户管理', path: 'user', icon: 'User'},
  {id: '5', tab: '我的账号', path: 'admin', icon: 'Tools'}
])

const router = useRouter()
let activePath = ref('')
onBeforeMount(() => activePath = router.path)

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}
</script>

<style lang="scss" scoped>
.el-menu {
  border-right: 0;
  height: calc(100% - 50px);
}
</style>