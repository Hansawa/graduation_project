<template>
  <div class="final">
    <div class="header">
      <div class="title">
        <span>爬虫配置 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item>{{ $router.currentRoute.value.meta.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div>
      </div>
    </div>
    <el-table
        :data="table.rowList"
        stripe
        border
        style="width: 100%"
        highlight-current-row
        @row-dblclick="handleDblClick"
        table-layout="auto"
    >
      <el-table-column type="index"/>
      <template v-for="column in table.columnList">
        <el-table-column :prop="column" :label="toPascal(column)"/>
      </template>
      <el-table-column label="Operations">
        <template #default="scope">
          <el-button
              size="small"
              auto-insert-space
              @click="handleInspect(scope.$index, scope.row)"
          >
            查看
          </el-button>
          <el-button
              type="primary"
              size="small"
              auto-insert-space
              @click="handleDownload(scope.$index, scope.row)"
          >
            下载文件
          </el-button>
          <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import {ref, onBeforeMount} from 'vue'
import {get, post, downloadFile, uploadFile} from '/api'
import {ElMessage, ElNotification} from 'element-plus'
import {useRouter} from 'vue-router'

const $router = useRouter()

/* 配置文件表定义 */
let table = ref({
  columnList: null,
  rowList: null
})
/* 获取配置文件表 */
const getTable = async () => {
  const resp = await get('/admin/crawler/config/final/all')
  if (resp === undefined) {
    table.value.columnList = null
    table.value.rowList = null
    return
  }
  table.value.columnList = resp.data.columnList
  table.value.rowList = resp.data.rowList
}
onBeforeMount(getTable)
/* table-column 元素的 label 属性的值设置为Pascal命名 */
const toPascal = (column) => {
  let str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 下载配置文件 */
const handleDownload = async (index, row) => {
  const _id = row['_id']
  const resp = await downloadFile('/admin/crawler/config/final/download', {_id})
  if (resp === undefined) return ElMessage.error('Fail to download this config')
  // 用从后端传来的原始二进制数据构造 blob
  const blob = new Blob([resp.data], {type: 'application/json'})
  const link = document.createElement('a')
  link.download = row['configName'] // a标签添加属性
  link.style.display = 'none'
  link.href = URL.createObjectURL(blob)
  document.body.appendChild(link)
  link.click() // 执行下载
  URL.revokeObjectURL(link.href)  // 释放 blob 对象
  document.body.removeChild(link)

  ElMessage.success('Download this config successful')
}

/* 配置查看 */
const handleInspect = (index, row) => {
  const _id = row['_id']
  $router.push({name: 'crawlerInspect', params: {_id}})
}
const handleDblClick = (row, column, event) => {
  const index = 0
  handleInspect(index, row)
}

/* 删除某配置 */
const handleDelete =async (index, row) => {
  const _id = row['_id']
  const resp = await get('/admin/crawler/config/final/delete', {_id})
  if (resp === undefined) return ElMessage.error('Fail to delete this config')
  await getTable()
}
</script>

<style lang="scss" scoped>
.final {
  height: 100%;
  display: flex;
  flex-direction: column;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      display: flex;
      justify-content: flex-start;
      align-items: flex-end;

      .el-breadcrumb {
        margin-bottom: 0;
      }
    }
  }
}
</style>