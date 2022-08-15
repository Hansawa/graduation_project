<template>
  <div id="welcome">
    <h3>欢迎！{{  }}</h3>
  </div>
</template>

<script setup>
import {get} from '/api'
import {onBeforeMount, ref} from 'vue'

let adminName = ref('')
onBeforeMount(async () => {
  // const resp = await get()
})
</script>

<style scoped>

</style>