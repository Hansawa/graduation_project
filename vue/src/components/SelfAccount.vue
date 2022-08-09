<template>
  <div id="selfAccount">
    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/selfaccount' }">我的账号</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
      <div style="width: 400px">
        <!-- 个人信息显示区 -->
        <el-descriptions class="margin-top" :column="1" border>
          <template #title>
            <p style="font-size: 18px">账号信息</p>
          </template>
          <el-descriptions-item>
            <template #label>
              <i class="el-icon-s-custom"></i>
              账号名
            </template>
            {{ adminForm.adminName }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <i class="el-icon-time"></i>
              年龄
            </template>
            {{ adminForm.adminAge }}
          </el-descriptions-item>
        </el-descriptions>
        <div id="buttonErea"
             style="display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-between; margin-top: 20px">
          <el-button type="primary" size="small" @click="showEditAdminDialog">修改信息</el-button>
          <el-button type="primary" size="small" @click="showEditAdminPasswordDialog">修改密码</el-button>
        </div>
      </div>
    </el-card>
  </div>

  <!-- 修改个人信息对话框 -->
  <el-dialog
      title="修改信息"
      v-model="editAdminDialogVisible"
      width="30%"
      @close="resetEditAdminForm">
    <!-- 修改个人信息表单 -->
    <el-form :rules="editAdminFormRules" ref="editAdminFormRef" :model="editAdminForm" label-width="80px">
      <el-form-item label="账号名" prop="adminName">
        <el-input v-model="editAdminForm.adminName" prefix-icon="el-icon-s-custom"></el-input>
      </el-form-item>
      <el-form-item label="年龄" prop="adminAge">
        <el-input v-model.number="editAdminForm.adminAge" prefix-icon="el-icon-time"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
    <span class="dialog-footer">
      <el-button @click="editAdminDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="editAdminInfo">确 定</el-button>
    </span>
    </template>
  </el-dialog>

  <!-- 修改管理员密码对话框 -->
  <el-dialog
      title="修改密码"
      v-model="editAdminPasswordDialogVisible"
      width="30%"
      @close="resetEditAdminPasswordForm">
    <!-- 修改管理员密码表单 -->
    <el-form :rules="editAdminPasswordFormRules" ref="editAdminPasswordFormRef" :model="editAdminPasswordForm"
             label-width="auto">
      <el-form-item label="原密码" prop="originPassword">
        <el-input type="password" v-model="editAdminPasswordForm.originPassword"
                  prefix-icon="el-icon-key"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input type="password" v-model="editAdminPasswordForm.newPassword"
                  prefix-icon="el-icon-key"></el-input>
      </el-form-item>
      <el-form-item label="再次输入新密码" prop="newPassword_again">
        <el-input type="password" v-model="editAdminPasswordForm.newPassword_again"
                  prefix-icon="el-icon-key"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
    <span class="dialog-footer">
      <el-button @click="editAdminPasswordDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="editAdminPassword">确 定</el-button>
    </span>
    </template>
  </el-dialog>
</template>

<script>
import {queryAdminByAdminId, editAdminInfo, editAdminPassword} from 'request/admin'

export default {
  name: "SelfAccount",
  async mounted() {
    this.adminForm = await queryAdminByAdminId({'adminId': window.sessionStorage.getItem('id')});
  },

  data() {
    /* 年龄校验规则 */
    let checkAdminAge = (rule, value, callback) => {
      if (!Number.isInteger(value)) {
        callback(new Error('请输入数字值'));
      } else {
        if (value <= 0) {
          callback(new Error('年龄必须大于0'));
        } else {
          callback();
        }
      }
    };
    /* 原密码校验规则 */
    let checkOriginPassword = (rule, value, callback) => {
      if (value !== this.adminForm.password) {
        return callback(new Error('原密码错误'));
      } else {
        callback();
      }
    };
    /* 新密码校验规则 */
    let checkNewPassword_again = (rule, value, callback) => {
      if (value !== this.editAdminPasswordForm.newPassword) {
        return callback(new Error('新密码错误'));
      } else {
        callback();
      }
    };
    return {
      editAdminDialogVisible: false,
      editAdminPasswordDialogVisible: false,
      /* 管理员信息表单 */
      adminForm: {
        adminId: '',
        adminName: '',
        adminAge: '',
        password: ''
      },
      /* 修改管理员信息表单 */
      editAdminForm: {
        adminId: '',
        adminName: '',
        adminAge: ''
      },
      /* 修改管理员密码表单 */
      editAdminPasswordForm: {
        originPassword: '',
        newPassword: '',
        newPassword_again: ''
      },
      /* 修改管理员信息表单校验对象 */
      editAdminFormRules: {
        adminName: [
          {required: true, message: '请输入账号名', trigger: 'blur'},
          {min: 3, max: 10, message: "长度在 3 到 10 个字符", trigger: 'blur'}
        ],
        adminAge: [
          {required: true, message: '请输入年龄', trigger: 'blur'},
          {validator: checkAdminAge, trigger: 'blur'}
        ]
      },
      /* 修改管理员密码表单校验对象 */
      editAdminPasswordFormRules: {
        originPassword: [
          {required: true, message: '原密码不能为空', trigger: 'blur'},
          {validator: checkOriginPassword, trigger: 'blur'},
          {min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur'}
        ],
        newPassword: [
          {required: true, message: '新密码不能为空', trigger: 'blur'},
          {min: 5, max: 15, message: "长度在 5 到 15 个字符", trigger: 'blur'}
        ],
        newPassword_again: [
          {required: true, message: '请再次输入新密码', trigger: 'blur'},
          {validator: checkNewPassword_again, trigger: 'blur'},
        ]
      }
    }
  },
  methods: {

    /* 显示修改管理员对话框方法 */
    async showEditAdminDialog() {
      this.editAdminForm = await queryAdminByAdminId({'adminId': this.adminForm.adminId});
      this.editAdminDialogVisible = !this.editAdminDialogVisible;
    },

    /* 修改管理员信息方法 */
    async editAdminInfo() {
      let valid = await this.$refs.editAdminFormRef.validate();
      if (valid === true) {
        let meta = await editAdminInfo(this.editAdminForm);
        if (meta.status !== 200)
          return this.$message.error(meta.msg);
        else {
          this.$message.success(meta.msg);
          this.editAdminDialogVisible = !this.editAdminDialogVisible;
          this.adminForm = await queryAdminByAdminId({adminId: this.editAdminForm.adminId});
        }
      }
    },

    /* 修改管理员密码方法 */
    async editAdminPassword() {
      let valid = this.$refs.editAdminPasswordFormRef.validate();
      if (valid === true) {
        let tempAdmin = {
          adminId: this.adminForm.adminId,
          password: this.editAdminPasswordForm.newPassword
        }
        let meta = await editAdminPassword(tempAdmin);
        if (meta.status !== 200)
          return this.$message.error(meta.msg);
        else this.$message.success(meta.msg);
        this.editAdminPasswordDialogVisible = !this.editAdminPasswordDialogVisible;
        await queryAdminByAdminId({adminId: this.adminForm.adminId});
      }
    },

    /* 显示修改管理员密码对话框方法 */
    showEditAdminPasswordDialog() {
      this.editAdminPasswordDialogVisible = !this.editAdminPasswordDialogVisible;
    },

    /* 重置修改管理员表单方法 */
    resetEditAdminForm() {
      this.$refs.editAdminFormRef.resetFields();
    },

    /* 重置修改管理员密码表单 */
    resetEditAdminPasswordForm() {
      this.$refs.editAdminPasswordFormRef.resetFields();
    }
  }
}
</script>

<style lang="less" scoped>
</style>