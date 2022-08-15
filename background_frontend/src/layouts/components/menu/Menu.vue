<template>
  <!-- 侧边栏菜单区 -->
  <el-menu
      text-color="#303133"
      active-text-color="#409eff"
      :collapse="props.isCollapse"
      :collapse-transition="false"
      :router="true"
      :default-active="activePath ? activePath : '/admin/welcome'"
      default-active=""
      @open="handleOpen"
      @close="handleClose"
  >
    <MenuItem :menu-list="menuList"/>
  </el-menu>
</template>

<script setup>
import MenuItem from '/layouts/components/menu/MenuItem.vue'
import {onBeforeMount, reactive, ref} from 'vue'
import {useRouter} from 'vue-router'
import {get} from '/api'
import {ElMessage} from 'element-plus'

const props = defineProps({
  isCollapse: {
    type: Boolean,
    required: true
  }
})

/* 菜单列表 */
let menuList = ref([])
onBeforeMount(async () => {
  const resp = await get('/admin/menu')
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  menuList.value = resp.data.menuList
})

const router = useRouter()
let activePath = ref('')
onBeforeMount(() => activePath = router.path)

const handleOpen = (key, keyPath) => {
}
const handleClose = (key, keyPath) => {
}
</script>

<style lang="scss" scoped>
.el-menu {
  border-right: 0;
  height: calc(100% - 50px);
}
</style>