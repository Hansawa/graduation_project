<template>
  <div class="login_container">
    <p id="title">新闻聚合后台系统</p>
    <div class="login_box">
      <!--   头像区域   -->
      <div class="avatar_box">
        <img :src="logoImgUrl" alt="Avatar">
      </div>
      <p style="font-size: 20px;text-align: center">管理员登录</p>
      <!-- 登录表单区域 -->
      <!-- vue的ref属性：通过设置引用，来让script获取该元素对象 -->
      <el-form ref="formRef" :model="form" :rules="rules" @keyup.enter="onSubmit(formRef)" class="login-form">
        <!-- 用户名 -->
        <el-form-item prop="adminName">
          <el-input v-model="form.adminName" size="large" autofocus="true" clearable
                    :placeholder="adminNameMessage">
            <template #prefix>
              <el-icon>
                <Avatar/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" size="large" clearable show-password
                    :placeholder="passwordMessage">
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="rememberMe">
          <el-checkbox v-model="form.rememberMe" label="记住我"/>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item>
          <el-button type="primary" size="large" round style="width: 100%" @click="onSubmit(formRef)">登 录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import logoImgUrl from '/assets/logo.svg'
import {ref, reactive} from 'vue'
import {useRouter} from 'vue-router'
import {post} from '/api'
import {ElMessage} from 'element-plus'

/* 这是登录表单的数据绑定对象 */
let form = reactive({
  adminName: 'admin',
  password: '123456',
  /* 是否自动登录开关 */
  rememberMe: false
})

/* 表单的验证规则对象 */
const adminNameMessage = '请输入账号'
const passwordMessage = '请输入密码'
const rules = reactive({
  /* 验证用户名是否合法，具体规则对象名要与验证的数据对象名一致 */
  adminName: [
    {required: true, message: adminNameMessage, trigger: 'blur'},
    {min: 3, max: 10, message: "长度在 3 到 10 个字符", trigger: 'blur'}
  ],
  /* 验证密码是否合法 */
  password: [
    {required: true, message: passwordMessage, trigger: 'blur'},
    {min: 5, max: 15, message: "长度在 5 到 15 个字符", trigger: 'blur'}
  ]
})

/* 表单元素的响应式引用对象 */
const formRef = ref()
const router = useRouter()
const onSubmit = async (formEl) => {
  if (!formEl) return

  await formEl.validate(async (valid) => {
    if (!valid) return

    /* 查询登录信息是否正确 */
    let resp = await post('/admin/login', form)
    if (resp.status !== 200) return ElMessage.error(resp.msg)

    /* 允许自动登录，则在当地存储保存用户 id，下次直接用 id 获取用户资料 */
    if (form.rememberMe) window.localStorage.setItem('adminId', resp.data.adminId)
    else window.localStorage.clear()
    window.sessionStorage.setItem('adminId', resp.data.adminId)

    /* 显示成功登录 Message */
    ElMessage.success(resp.msg)
    await router.push(resp.data.routePath)
  })
}
</script>

<style lang="scss" scoped>
#title {
  color: #0cb494;
  letter-spacing: 20px;
  font-family: /*"Yu Mincho Light",*/
      sans-serif;
  font-size: 40px;
  margin: 0;
  padding-top: 40px;
  text-align: center;
}

.login_container {
  height: 100%;
  background: url("/assets/login_background.png") repeat;
}

.login_box {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -40%);
  width: 450px;
  height: 350px;
  background-color: #fff;
  border-radius: 10px;

  .avatar_box {
    position: absolute;
    left: 100%;
    /* translate设置成%时是根据元素自身的大小的 */
    transform: translate(-50%, -50%);
    width: 100px;
    height: 100px;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #eee;
    border-radius: 50%;
    box-shadow: 0 0 10px #ddd;

    img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #eee;
      transition: 0.3s;
    }

    img:hover {
      transform: rotate(360deg);
      transition: transform 0.5s linear 0s;
    }
  }
}

.login-form {
  position: absolute;
  /* 为什么能够向下移动 */
  bottom: 5%;
  width: 100%;
  padding: 0 40px;
  /* ? */
  box-sizing: border-box;
}
</style>