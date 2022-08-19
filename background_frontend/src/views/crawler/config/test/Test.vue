<template>
  <div class="test">
    <div class="header">
      <div class="title">
        <span>爬虫配置 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item>{{ $router.currentRoute.value.meta.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <el-button
          type="primary"
          size="small"
          auto-insert-space
          @click="dialogVisible = true"
      >
        上传文件
      </el-button>
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
import {get, downloadFile, uploadFile} from '/api'
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
  let str = column.toString()
  return str.replace(str[0], str[0].toUpperCase())
}

/* 下载配置文件 */
const handleDownload = async (index, row) => {
  const configName = row['configName']
  const resp = await downloadFile('/admin/crawler/config/test', {configName})

  if (resp == null) return ElMessage.error('fail to download config file')
  else {
    // 用从后端传来的原始二进制数据构造 blob
    const blob = new Blob([resp], {type: 'application/json'})
    const link = document.createElement('a')
    link.download = row['configName'] // a标签添加属性
    link.style.display = 'none'
    link.href = URL.createObjectURL(blob)
    document.body.appendChild(link)
    link.click() // 执行下载
    URL.revokeObjectURL(link.href)  // 释放 blob 对象
    document.body.removeChild(link)

    ElMessage.success('download config file successful')
  }
}

/* 对话框 */
let dialogVisible = ref(false)
const handleClose = (done) => {
  getTable()
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
  const resp = await uploadFile('/admin/crawler/config/test', option.file)
  if (resp.status !== 200) return ElNotification.error({message: resp.msg})
  else ElNotification.success({message: resp.msg})
}

/* 编辑与测试 */
const handleEditTest = (index, row) => {
  const configName = row['_id']
  $router.push({name: 'crawlerEditTest', params: {configName}})
}

const handleCurrentChange = (currentRow, oldCurrentRow) => {

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