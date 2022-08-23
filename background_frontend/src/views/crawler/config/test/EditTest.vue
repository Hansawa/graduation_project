<template>
  <div class="edit-test">
    <div class="header">
      <div class="title">
        <span>爬虫配置 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{name: 'crawlerTestConfig'}">测试配置表</el-breadcrumb-item>
          <el-breadcrumb-item>编辑与测试</el-breadcrumb-item>
          <el-breadcrumb-item>配置id：{{ $route.params._id }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <div class="main">
      <div class="config-area">
        <el-scrollbar>
          <el-form :model="form" label-position="top">
            <el-form-item label="配置名称">
              <el-input v-model="form.configName"/>
            </el-form-item>
            <el-form-item label="网站中文">
              <el-input v-model="form.websiteCnName"/>
            </el-form-item>
            <el-form-item label="网站英文">
              <el-input v-model="form.websiteEnName"/>
            </el-form-item>
            <el-form-item label="配置内容">
              <el-input
                  v-model="form.configContent"
                  autosize
                  type="textarea"
                  placeholder="Please input"
              />
            </el-form-item>
          </el-form>
        </el-scrollbar>
      </div>
      <el-divider direction="vertical"/>
      <div class="news-area">
        <div class="control-box">
          <el-button type="primary" @click="format">格式化配置文本</el-button>
          <el-button type="primary" @click="save">保存测试配置</el-button>
          <el-button type="success" @click="run">运行测试配置</el-button>
        </div>
        <el-table
            :data="table.rowList"
            stripe
            border
            @cell-dblclick="handleDblClick"
            style="width: 100%"
            highlight-current-row
        >
          <el-table-column type="index"/>
          <template v-for="column in table.columnList">
            <el-table-column show-overflow-tooltip :prop="column" :label="toPascal(column)"/>
          </template>
        </el-table>
      </div>
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
import {useRouter} from 'vue-router'
import {onBeforeUnmount, onBeforeMount, ref} from 'vue'
import {get, post} from '/api'
import {ElMessage} from "element-plus";

const $router = useRouter()
const $route = $router.currentRoute.value

/* 配置内容定义 */
let form = ref({
  _id: '',
  configName: '',
  websiteCnName: '',
  websiteEnName: '',
  configContent: ''
})
/* 获取配置内容 */
const getConfigContent = async () => {
  const _id = $route.params._id
  const resp = await get('/admin/crawler/config/test/content', {_id})
  if (resp === undefined) await $router.push({name: 'crawlerTestConfig'})
  else form.value = resp.data
}
onBeforeMount(async () => {
  await getConfigContent()
})


/* 保存测试配置 */
const save = async () => {
  const data = form.value
  await post('/admin/crawler/config/test/content', data)
}

/* 获取测试数据 */
let table = ref({
  rowList: [],
  columnList: []
})
const getNews = async () => {
  const _id = form.value._id
  const resp = await get('/admin/news/test/all', {_id})
  if (resp === undefined) {
    table.value.columnList = null
    table.value.rowList = null
    return
  }
  table.value.columnList = resp.data.columnList
  table.value.rowList = resp.data.rowList
}
/* table-column 元素的 label 属性的值设置为Pascal命名 */
const toPascal = (column) => {
  let str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 运行测试 */
/* 声明计时器，用来轮询是否完成爬取 */
let timer = null
/* 轮询方法 */
const polling = async () => {
  const resp = await get('/admin/crawler/config/test/polling')
  if (resp.status === 201) return ElMessage.warning(resp.headers.msg)
  clearInterval(timer)
  await getNews()
}
const run = async () => {
  const _id = form.value._id
  get('/admin/crawler/config/test/run', {_id})
  timer = setInterval(polling, 2000)
}

/* 格式化 */
const format = () => {
  let configContent = form.value.configContent
  form.value.configContent = JSON.stringify(JSON.parse(configContent), null, 2)
}

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

onBeforeUnmount(async () => {
  const _id = form.value._id
  const resp = await get('/admin/crawler/config/test/temp/delete', {_id})
})
</script>

<style lang="scss" scoped>
.edit-test {
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
    display: flex;
    overflow-y: auto;
    box-sizing: content-box;
    padding: 5px 0 0 0;

    .config-area {
      flex: 1;
    }

    .el-divider {
      height: 100%;
    }

    .news-area {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
  }
}
</style>