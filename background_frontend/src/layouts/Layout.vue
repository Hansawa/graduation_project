<template>
  <div class="layout-box">
    <el-container>
      <Aside/>
      <el-container>
        <Header/>
        <!-- 右侧内容主题 -->
        <Main/>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import Aside from '/layouts/components/Aside.vue'
import Header from '/layouts/components/Header.vue'
import Main from '/layouts/components/Main.vue'

</script>

<style scoped>
.layout-box {
  height: 100%;
}
</style>