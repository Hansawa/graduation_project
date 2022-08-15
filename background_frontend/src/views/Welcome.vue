<template>
  <div id="welcome">
    <h3>{{ adminName }}，欢迎！</h3>
  </div>
</template>

<script setup>
import {get} from '/api'
import {onBeforeMount, ref} from 'vue'
import {ElMessage} from 'element-plus'

let adminName = ref('')
onBeforeMount(async () => {
  const adminId = window.sessionStorage.getItem('adminId')
  const resp = await get('/admin/name', {adminId})
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else adminName.value = resp.data.adminName
})
</script>

<style scoped>

</style>