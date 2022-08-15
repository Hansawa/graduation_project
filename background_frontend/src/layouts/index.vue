<template>
  <el-container class="layout-container">
    <!-- 侧边栏菜单区 -->
    <Aside/>
    <el-container class="content-wrapper">
      <Header/>
      <!-- 右侧内容主题 -->
      <Main/>
    </el-container>
  </el-container>
</template>

<script setup>
import Aside from '/layouts/components/Aside.vue'
import Header from '/layouts/components/Header.vue'
import Main from '/layouts/components/Main.vue'

</script>

<style lang="scss" scoped>
.layout-container {
  height: 100%;
}

.content-wrapper {
  flex-direction: column;
  height: 100%;
  width: 100%;
}
</style>