<template>
  <div class="news-detail">
    <div class="header">
      <div class="title">
        <span>未加工新闻 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{name: 'rawNewsWebsite'}">新闻网站列表</el-breadcrumb-item>
          <el-breadcrumb-item :to="{name: 'rawNewsWebsiteNews'}">新闻网站：{{
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
          @current-change="handleCurrentChange"
      >
        <template v-for="column in columnList">
          <el-table-column show-overflow-tooltip :prop="column" :label="toPascal(column)"/>
        </template>
        <el-table-column label="Operations">
          <template #default="scope">
            <el-button
                type="primary"
                size="small"
                @click="handleWash(scope.$index, scope.row)"
            >
              清洗
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
  <!-- 清洗对话框  -->
  <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="30%"
      :before-close="handleClose"
  >
    <span>This is a message</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {useRoute} from 'vue-router'
import {ref, onBeforeMount} from 'vue'
import {get} from '/api'
import {ElMessage} from 'element-plus'

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
  const resp = await get('/admin/raw_news/website/news', params)
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else ElMessage.success(resp.msg)

  const items = resp.data
  itemNameList.value = Object.keys(items)
  itemContentList.value = Object.values(items)

  const inl = itemNameList.value
  const icl = itemContentList.value
  console.log(inl)
  console.log(icl)
  for (let i = 0; i < inl.length; i++) {
    table.value.push({itemName: inl[i], itemContent: icl[i]});
  }
  console.log(table.value)
}
/* table-column 元素的 label 属性的值设置为Pascal命名 */
const toPascal = (column) => {
  const str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 内容清洗 */
let regexList = ref([])
let dialogTitle = ref('')
let dialogContent = ref('')
let dialogVisible = ref(false)
const handleWash = (index, row) => {
  dialogVisible.value = true
  dialogTitle.value = row['itemName']
  dialogContent.value = row['itemContent']
}
const handleClose = () => {
}

onBeforeMount(async () => {
  await getNews()
})

const handleCurrentChange = () => {
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