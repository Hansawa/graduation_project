<template>
  <div class="news">
    <el-breadcrumb separator=">">
      <el-breadcrumb-item>爬虫管理</el-breadcrumb-item>
      <el-breadcrumb-item>未处理新闻</el-breadcrumb-item>
      <el-breadcrumb-item>网站：{{ props.websiteName }}</el-breadcrumb-item>
    </el-breadcrumb>
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
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {get} from '/api'

const props = defineProps({
  websiteName: {
    type: String,
    required: true
  }
})

/* 新闻表定义 */
let table = ref({
  columnList: null,
  rowList: null
})
/* 获取新闻表 */
const getTable = async () => {
  const websiteName = props.websiteName
  const resp = await get('/admin/raw_news/website/news/all', {websiteName})
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else {
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

/* 查看新闻细节 */
const $router = useRouter()
const handleInspect = (index, row) => {
  const params = {
    websiteName: props.websiteName,
    title: row['title'].join()
  }
  $router.push({name: 'rawNewsWebsiteNewsDetail', params})
}

const handleCurrentChange = () => {
}
</script>

<style scoped>
  .news {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
</style>