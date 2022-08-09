<template>
  <div id="userManage">
    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/usermanage' }">用户管理</el-breadcrumb-item>
    </el-breadcrumb>
  </div>

  <!-- 卡片视图区域 -->
  <el-card>
    <b><p style="font-size: 18px">用户列表</p></b>
    <el-row :gutter="10">
      <el-col :span="10">
        <div>
          <!-- @也可以绑定Element的事件 -->
          <!-- 查询用户输入框 -->
          <el-input placeholder="搜索用户名" v-model="keyword" @input="queryUser(keyword)" prefix-icon="el-icon-search">
            <template #append>
              <el-button type="info" @click="resetQueryInput(keyword)">重 置</el-button>
            </template>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <!-- 新闻列表框架 -->
    <el-table
        :data="userList"
        style="width: 100%"
        border
        stripe
        max-height="500">
      <el-table-column
          type="index"
          width="50"
          label="#">
      </el-table-column>
      <el-table-column
          v-for="(item, id) in listTitle"
          :key="id"
          :prop="item.prop"
          :label="item.label">
      </el-table-column>
      <el-table-column width="200" label="操作">
        <!-- 作用域插槽，可以获取该行的全部数据 -->
        <template v-slot="scope">
          <!-- 重置密码按钮按钮 -->
          <el-button
              size="mini" type="primary"
              icon="el-icon-unlock"
              @click="resetUserPwd(scope.row.userID)">
            重置密码
          </el-button>
          <el-button
              size="mini" type="danger"
              icon="el-icon-delete"
              @click="deleteUser(scope.row.userID)">
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import {getUserList, resetUserPwd, deleteUser} from "request/user";

export default {
  name: "UserManage",
  /* 创建该组件后，先查询全部的用户信息 */
  created() {
    this.queryUser(this.keyword);
  },
  data() {
    return {
      keyword: '',
      userList: [],
      listTitle: [
        {prop: 'userName', label: '用户名称'},
      ]
    }
  },
  methods: {

    /* 查询新闻方法，隔段时间才发请求 */
    async queryUser(keyword) {
      clearTimeout(this.timer);  //清除延迟执行
      if (keyword !== '')
        this.timer = setTimeout(async () => {
          this.userList = await getUserList({keyword});
        }, 500);
      else
        this.userList = await getUserList({keyword});
    },

    /* 重置查询输入框方法 */
    resetQueryInput(keyword) {
      if (keyword !== '') {
        this.queryUser(this.keyword = '');
      }
    },
    /* 重置用户密码方法 */
    resetUserPwd(userID) {
      this.$confirm('此操作将重置该用户的密码为123456, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        let newPwd = '123456';
        let tempUser = {
          userID: userID,
          userPwd: newPwd
        }
        let meta = await resetUserPwd(tempUser);
        if (meta.status !== 200) return this.$message.error(meta.msg);
        else {
          this.queryUser(this.keyword = '');
          this.$message.success('成功重置用户密码，新密码为' + newPwd);
        }
      }).catch(() => {
        this.$message.info("已经取消重置用户密码");
      });
    },
    async deleteUser(userID) {
      this.$confirm('此操作将永久删除此用户及其评论, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        let meta = await deleteUser({userID});
        if (meta.status !== 200) return this.$message.error(meta.msg);
        else {
          this.queryUser(this.keyword = '');
          this.$message.success(meta.msg);
        }
      }).catch(() => {
        this.$message.info("已经取消删除用户");
      });
    }
  }
}
</script>

<style scoped>

</style>