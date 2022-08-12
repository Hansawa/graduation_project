<template>
  <div class="login_container">
    <p id="title">
      新闻聚合后台系统</p>
    <div class="login_box">
      <!--   头像区域   -->
      <div class="avatar_box">
        <img :src="logoImgUrl" alt="头像">
      </div>
      <p style="font-size: 20px;text-align: center">管理员登录</p>
      <!-- 登录表单区域 -->
      <!-- vue的ref属性：通过设置引用，来让script获取该元素对象 -->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="0px" class="login_form">
        <!-- 用户名 -->
        <el-form-item label="" prop="adminName">
          <el-input v-model="loginForm.adminName" prefix-icon="el-icon-s-custom" autofocus="true" placeholder="请输入登录名称"></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item label="" prop="password">
          <el-input type="password" v-model="loginForm.password" prefix-icon="el-icon-key" placeholder="请输入密码"></el-input>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item label="">
          <el-col :span="4"></el-col>
          <el-col :span="4">
            <el-button type="info" @click="resetLoginForm">重 置</el-button>
          </el-col>
          <el-col :span="4"></el-col>
          <el-col :span="4"></el-col>
          <el-col :span="4">
            <el-button type="primary" @click="login">登 录</el-button>
          </el-col>
          <el-col :span="4"></el-col>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import logoImgUrl from '/assets/logo.png'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const $router = useRouter()
import { post } from '/request'
import { ElMessage } from 'element-plus'

/* 这是登录表单的数据绑定对象 */
let loginForm = ref({
  adminName: 'admin',
  password: '123456'
})
/* 表单元素的响应式引用对象 */
const loginFormRef = ref()
/* 点击重置按钮，充值登录表单 */
const resetLoginForm = () => {
  loginFormRef.value.resetFields()
}

/* 表单的验证规则对象 */
const loginFormRules = ref({
  /* 验证用户名是否合法，具体规则对象名要与验证的数据对象名一致 */
  adminName: [
    {required: true, message: '请输入登录名称', trigger: 'blur'},
    {min: 3, max: 10, message: "长度在 3 到 10 个字符", trigger: 'blur'}
  ],
  /* 验证密码是否合法 */
  password: [
    {required: true, message: '请输入登陆密码', trigger: 'blur'},
    {min: 5, max: 15, message: "长度在 5 到 15 个字符", trigger: 'blur'}
  ]
})
const login = async () => {
  /* 表单预验证
   * validate方法对整个表单进行校验，校验结束后调用作为参数的回调函数，并传入valid参数
   *（valid取值true or false，当表单数据校验无误为true，校验有误为false）
   * 可以在这个回调函数中编写请求逻辑
   *  */
  await loginFormRef.value.validate(async (valid, fields) => {
    if (!valid) return
    /* 用了await，将返回data对象而不是promise（异步函数都返回包含返回值的promise） */
    // /* 用了解构赋值，直接将返回的对象中的data对象拿出 */
    /* 响应拦截器只返回了data对象 */
    let resp = await post('/admin/login', loginForm.value)
    if (resp.meta.status !== 200) return ElMessage.error({showClose: true, message: resp.meta.msg})
    else ElMessage.success({showClose: true, message: resp.meta.msg})
    window.sessionStorage.setItem('token', resp.token);
    window.sessionStorage.setItem('id', resp.data.adminId);
    /* 编程式导航（其实就是跳转到/home路径） */
    await $router.push('/home')
  })
}
</script>

<style lang="scss" scoped>
#title {
  color: #0cb494;
  letter-spacing: 20px;
  font-family: "Yu Mincho Light",sans-serif;
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
  transform: translate(-50%, -50%);
  width: 450px;
  height: 300px;
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

.login_form {
  position: absolute;
  /* 为什么能够向下移动 */
  bottom: 15%;
  width: 100%;
  padding: 0 20px;
  /* ? */
  box-sizing: border-box;
}
</style>