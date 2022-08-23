<template>
  <div class="news-detail">
    <div class="header">
      <div class="title">
        <span>新闻管理 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{name: 'newsWebsite'}">新闻网站列表</el-breadcrumb-item>
          <el-breadcrumb-item :to="{name: 'newsWebsiteNews'}">新闻网站：{{
              $route.params.websiteName
            }}
          </el-breadcrumb-item>
          <el-breadcrumb-item>新闻id：{{ $route.params._id }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <div class="main">
      <el-table
          :data="table"
          stripe
          border
          style="width: 100%"
          highlight-current-row
          @cell-dblclick="handleDblClick"
      >
        <template v-for="column in columnList">
          <el-table-column show-overflow-tooltip :prop="column" :label="toPascal(column)"/>
        </template>
      </el-table>
    </div>
  </div>
  <el-dialog
      v-model="dialogVisible"
      :title="title"
      :before-close="handleClose"
  >
    <el-input
        v-model="content"
        autosize
        type="textarea"
        placeholder="Please input"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {useRoute} from 'vue-router'
import {ref, onBeforeMount} from 'vue'
import {get} from '/api'

const $route = useRoute()

/* 获取新闻内容 */
let table = ref([])

let columnList = ref([
  'itemName', 'itemContent'
])

let itemNameList = ref([])
let itemContentList = ref([])

const getNews = async () => {
  const params = {
    websiteName: $route.params.websiteName,
    _id: $route.params._id
  }
  const resp = await get('/admin/news/final', params)
  if (resp === undefined) {
    table.value = null
    return
  }
  const items = resp.data['rowList'][0]
  itemNameList.value = Object.keys(items)
  itemContentList.value = Object.values(items)

  const inl = itemNameList.value
  const icl = itemContentList.value
  for (let i = 0; i < inl.length; i++) {
    table.value.push({itemName: inl[i], itemContent: icl[i]});
  }
}
/* table-column 元素的 label 属性的值设置为Pascal命名 */
const toPascal = (column) => {
  const str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}
onBeforeMount(async () => {
  await getNews()
})

/* 显示细节 */
let dialogVisible = ref(false)
let title = ref('')
let content = ref('')
const handleDblClick = (row, column, cell, event) => {
  title.value = column['property']
  content.value = row[column['property']]
  dialogVisible.value = true
}
const handleClose = (done) => {
  done()
}
</script>

<style lang="scss" scoped>
.news-detail {
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

  .main {
    overflow: hidden;
  }
}
</style>