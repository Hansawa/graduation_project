<template>
  <div class="news">
    <div class="header">
      <div class="title">
        <span>新闻管理 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{name: 'newsWebsite'}">新闻网站列表</el-breadcrumb-item>
          <el-breadcrumb-item>新闻网站：{{ $route.params.websiteName }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <el-table
        :data="table.rowList"
        stripe
        border
        style="width: 100%"
        highlight-current-row
        @row-dblclick="handleDblClick"
    >
      <el-table-column type="index"/>
      <template v-for="column in table.columnList">
        <el-table-column show-overflow-tooltip :prop="column" :label="toPascal(column)"/>
      </template>
      <el-table-column label="Operations">
        <template #default="scope">
          <el-button
              size="small"
              @click="handleInspect(scope.$index, scope.row)"
          >
            查看
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
import {onBeforeMount, ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {get} from '/api'

const $router = useRouter()
const $route = $router.currentRoute.value

/* 新闻表定义 */
let table = ref({
  columnList: null,
  rowList: null
})
/* 获取新闻表 */
const getTable = async () => {
  const websiteName = $route.params.websiteName
  const resp = await get('/admin/news/final/all', {websiteName})
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
  const str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 查看新闻细节 */
const handleInspect = (index, row) => {
  const params = {
    websiteName: $route.params.websiteName,
    _id: row['_id']
  }
  $router.push({name: 'newsWebsiteNewsDetail', params})
}

/* 删除 */
const handleDelete = async (index, row) => {
  const websiteName = $route.params.websiteName
  const _id = row['_id']
  const params = {
    websiteName,
    _id
  }
  const resp = await get('/admin/news/final/delete', params)
  await getTable()
}

/* 双击 */
const handleDblClick = (row, column, event) => {
  handleInspect(0, row)
}
</script>

<style lang="scss" scoped>
.news {
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