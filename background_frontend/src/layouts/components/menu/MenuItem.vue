<template>
  <!-- 递归创建菜单项 -->
  <template v-for="item in props.menuList">
    <el-sub-menu v-if="item.children" :index="pathCat(item)">
      <template #title>
        <el-icon>
          <component :is="item.icon"/>
        </el-icon>
        <span>{{ item.name }}</span>
      </template>
      <Menu :menu-list="item.children" :super-path="pathCat(item)"/>
    </el-sub-menu>
    <el-menu-item v-else :index="pathCat(item)" :key="item.id">
      <el-icon>
        <component :is="item.icon"/>
      </el-icon>
      <template #title>{{ item.name }}</template>
    </el-menu-item>
  </template>
</template>

<script setup>
import Menu from '/layouts/components/menu/MenuItem.vue'

const props = defineProps({
  menuList: {
    type: Array,
    required: true
  },
  superPath: {
    type: String,
    default: '/admin'
  }
})

/* 拼接上级路由与当前路由 */
function pathCat(item) {
  return props.superPath + '/' + item.path
}
</script>

<style lang="scss" scoped>

</style>