<template>
  <div class="test">
    <div class="header">
      <div class="title">
        <span>爬虫配置 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item>{{ $router.currentRoute.value.meta.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    <div>
      <el-button
          type="primary"
          size="small"
          auto-insert-space
          @click="dialogVisible = true"
      >
        上传文件
      </el-button>
      <el-button
          type="primary"
          size="small"
          auto-insert-space
          @click="downloadTemplate"
      >
        下载模板
      </el-button>
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
              @click="handleEditTest(scope.$index, scope.row)"
          >
            编辑与测试
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
          <el-button
              size="small"
              type="success"
              @click="handleSubmit(scope.$index, scope.row)"
          >
            提交
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <!-- 上传文件对话框 -->
  <el-dialog
      v-model="dialogVisible"
      title="Tips"
      width="30%"
      :before-close="handleClose"
  >
    <!-- 上传文件区域 -->
    <el-upload
        class="upload-area"
        action="#"
        drag
        multiple
        ref="uploadRef"
        :auto-upload="false"
        accept=".json"
        :http-request="uploadConfig"
        :on-change="handleChange"
    >
      <el-icon class="el-icon--upload">
        <upload-filled/>
      </el-icon>
      <div class="el-upload__text">
        Drop json file here or <em>click to upload</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
        </div>
      </template>
    </el-upload>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="success" @click="submitUpload">Upload</el-button>
      </span>
    </template>
  </el-dialog>
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
  const resp = await get('/admin/crawler/config/test/all')
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
  const resp = await downloadFile('/admin/crawler/config/test/download', {_id})
  if (resp === undefined) return
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

  ElMessage.success('Save this config successful')
}

/* 对话框 */
let dialogVisible = ref(false)
const handleClose = async (done) => {
  await getTable()
  done()
}

/* 上传配置文件 */
const uploadRef = ref()
let fileList = ref()
/* 上传按钮点击事件 */
const submitUpload = () => {
  uploadRef.value.submit()
}
/* 自定义上传请求 */
const uploadConfig = async (option) => {
  const resp = await uploadFile('/admin/crawler/config/test/upload', option.file)
}

/* 编辑与测试 */
const handleEditTest = (index, row) => {
  const _id = row['_id']
  $router.push({name: 'crawlerEditTest', params: {_id}})
}
const handleDblClick = (row, column, event) => {
  const index = 0
  handleEditTest(index, row)
}

/* 下载模板 */
const downloadTemplate = async () => {
  const resp = await downloadFile('/admin/crawler/config/test/download', {'_id': '62ff74c0a85533fa5bcfc976'})
  if (resp === undefined) return
  // 用从后端传来的原始二进制数据构造 blob
  const blob = new Blob([resp.data], {type: 'application/json'})
  const link = document.createElement('a')
  link.download = 'universal' // a标签添加属性
  link.style.display = 'none'
  link.href = URL.createObjectURL(blob)
  document.body.appendChild(link)
  link.click() // 执行下载
  URL.revokeObjectURL(link.href)  // 释放 blob 对象
  document.body.removeChild(link)

  ElMessage.success('Save config template successful')
}

/* 删除某配置 */
const handleDelete = async (index, row) => {
  const _id = row['_id']
  const resp = get('/admin/crawler/config/test/delete', {_id})
  await getTable()
}

/* 禁止上传文件名称为 universal 的文件 */
const handleChange = (UploadFile, UploadFiles) => {
  if (UploadFile.name === 'universal.json') {
    uploadRef.value.handleRemove(UploadFile)
    ElMessage.error('Can not upload file named universal.json')
  }
}

/* 提交 */
const handleSubmit =async (index, row) => {
  if (row['websiteCnName'] === '' || row['websiteEnName'] === '')
    return ElMessage.warning('Website name can not null!')
  const config = row
  const resp = await post('/admin/crawler/config/test/submit', config)
}
</script>

<style lang="scss" scoped>
.test {
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