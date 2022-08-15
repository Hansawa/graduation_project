<template>
  <div class="configs">
    <div>爬虫管理 / 配置文件</div>
    <el-table
        :data="form"
        stripe
        border
        style="width: 100%;max-height: calc(100% - 28.4px)"
        highlight-current-row
        @current-change="handleCurrentChange"
    >
      <template v-for="column in columnList">
        <el-table-column :prop="toCamel(column)" :label="column" />
      </template>
      <el-table-column  label="Operations">
        <template #default="scope">
          <el-button
              size="small"
              @click="handleEdit(scope.$index, scope.row)"
          >
            Edit
          </el-button>
          <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import {reactive, ref, onBeforeMount} from 'vue'
import {get} from '/api'
import {ElMessage} from 'element-plus'

/* 获取配置文件表的列名 */
let columnList = ref()
onBeforeMount(async () => {
  const resp = await get('/admin/crawler/configs/table/column')
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else columnList.value = resp.data.columnList
})

/* 获取配置文件表 */
let form = ref()
onBeforeMount(async () => {
  const resp = await get('/admin/crawler/configs/table')
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else form.value = resp.data.table
})
const toCamel = (column) => {
  let str = column.toString()
  return str.replace(str[0], str[0].toLowerCase())
}

const handleCurrentChange = (currentRow, oldCurrentRow) => {

}
</script>

<style scoped>
.configs {
  height: 100%;
}
</style>