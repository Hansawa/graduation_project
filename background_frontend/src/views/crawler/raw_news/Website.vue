<template>
  <div class="website">
    <div class="header">
      <div class="title">
        <span>未加工新闻 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item>新闻网站列表</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <el-table
        :data="table.rowList"
        stripe
        border
        style="width: 100%"
        highlight-current-row
        @current-change="handleCurrentChange"
    >
      <template v-for="column in table.columnList">
        <el-table-column :prop="column" :label="toPascal(column)"/>
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
import {ElMessage} from 'element-plus'
import {get} from '/api'
import {useRouter} from 'vue-router'

/* 新闻网站表定义 */
let table = ref({
  columnList: null,
  rowList: null
})
/* 获取新闻网站表 */
const getTable = async () => {
  const resp = await get('/admin/raw_news/website/all')
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else {
    ElMessage.success(resp.msg)
    table.value.columnList = resp.data.columnList
    table.value.rowList = resp.data.rowList
  }
}
onBeforeMount(getTable)
/* table-column 元素的 label 属性的值设置为Pascal命名 */
const toPascal = (column) => {
  const str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 查看某一网站的新闻 */
const $router = useRouter()
const handleInspect = (index, row) => {
  const websiteName = row['enName']
  $router.push({name: 'rawNewsWebsiteNews', params: {websiteName}})
}

const handleCurrentChange = () => {
}
</script>

<style lang="scss" scoped>
.website {
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