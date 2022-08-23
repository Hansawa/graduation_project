<template>
    <el-container class="content-wrapper">
      <Header/>
      <Main/>
    </el-container>
</template>

<script setup>
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