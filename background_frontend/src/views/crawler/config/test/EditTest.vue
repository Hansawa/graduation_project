<template>
  <div class="edit-test">
    <div class="header">
      <div class="title">
        <span>爬虫配置 |&nbsp;</span>
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{name: 'crawlerTestConfig'}">测试配置表</el-breadcrumb-item>
          <el-breadcrumb-item>测试配置id：{{ $route.params._id }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <div class="main">
      <div class="config-area">
        <el-scrollbar>
          <el-form :model="form" label-position="top">
            <el-form-item label="配置名称">
              <el-input v-model="form.configName" />
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
        <el-button type="primary" @click="save">保存</el-button>
        <el-button type="success" @click="run">运行</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useRouter} from 'vue-router'
import {onBeforeMount, ref} from 'vue'
import {get, post} from '/api'
import {ElMessage} from 'element-plus'

const $router = useRouter()
const $route = $router.currentRoute.value

/* 配置内容定义 */
let form = ref({
  configName: '',
  configContent: ''
})
/* 获取配置内容 */
const getConfigContent = async () => {
  const configName = $route.params.configName
  const resp = await get('/admin/crawler/config/test/content', {configName})
  if (resp.status !== 200) {
    ElMessage.error(resp.msg)
    await $router.push({name: 'crawlerTestConfig'})
  } else {
    form.value = resp.data
    ElMessage.success(resp.msg)
  }
}
onBeforeMount(async () => {
  await getConfigContent()
})


/* 保存测试配置 */
const save = async () => {
  const data = {
    configName: form.value.configName,
    configContent: form.value.configContent
  }
  const resp = await post('/admin/crawler/config/test/content', data)
  if (resp.status !== 200) return ElMessage.error(resp.msg)
  else ElMessage.success(resp.msg)
}

/* 运行测试配置 */
const run = () => {

}
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
    }
  }
}
</style>