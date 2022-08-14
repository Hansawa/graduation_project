<template>
  <template v-for="item in props.menuList">
    <el-sub-menu v-if="item.children" :index="'/' + item.path">
      <template #title>
        <el-icon>
          <component :is="item.icon"/>
        </el-icon>
        <span>{{ item.tab }}</span>
      </template>
      <Menu :menu-list="item.children"/>
    </el-sub-menu>
    <el-menu-item v-else :index="'/' + item.path" :key="item.id">
      <el-icon>
        <component :is="item.icon"/>
      </el-icon>
      <span>{{ item.tab }}</span>
    </el-menu-item>
  </template>
</template>

<script setup>
import Menu from '/layouts/components/menu/MenuItem.vue'
import {defineProps} from 'vue'

const props = defineProps({
  menuList: {
    type: Object,
    required: true
  }
})
</script>

<style lang="scss" scoped>

</style>