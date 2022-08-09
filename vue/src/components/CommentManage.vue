<template>
  <div id="commentManage">
    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/commentmanage' }">评论管理</el-breadcrumb-item>
    </el-breadcrumb>
  </div>

  <!-- 卡片视图区域 -->
  <el-card>
    <b><p style="font-size: 18px">评论列表</p></b>
    <el-row :gutter="10">
      <el-col :span="13">
        <div>
          <!-- @也可以绑定Element的事件 -->
          <!-- 查询新闻输入框 -->
          <el-input placeholder="搜索评论" v-model="keyword" @input="queryComments(keyword, searchType)">
            <template #prepend>
              <el-select v-model="searchType" placeholder="搜索方式">
                <el-option v-for="(item, id) in searchTypeList"
                           :key="id"
                           :label="item.label"
                           :value="item.value">
                </el-option>
              </el-select>
            </template>
            <template #append>
              <el-button type="info" @click="resetQueryInput">重 置</el-button>
            </template>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <!-- 新闻列表框架 -->
    <el-table
        :data="commentList"
        style="width: 100%"
        border
        stripe
        max-height="430">
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
      <el-table-column width="170" label="操作">
        <!-- 作用域插槽，可以获取该行的全部数据 -->
        <template v-slot="scope">
          <!-- 添加按钮 -->
          <el-button
              size="mini" type="danger"
              icon="el-icon-delete"
              @click="deleteComment(scope.row.commentID)">
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import {getAllComments, queryCommentsBySearchType, deleteComment} from "request/comment";

export default {
  name: "CommentManage",
  created() {
    this.getAllComments();
  },
  data() {
    return {
      keyword: '',
      searchType: '',
      commentList: [],
      searchTypeList: [
        {label: '通过评论内容', value: '2'},
        {label: '通过用户名', value: '1'},
        {label: '通过新闻内容', value: '0'}
      ],
      listTitle: [
        {prop: 'commentContent', label: '评论内容'},
        {prop: 'commentTime', label: '评论时间'},
        {prop: 'userName', label: '用户名'},
        {prop: 'newsContent', label: '新闻内容'}
      ]
    }
  },
  methods: {

    /* 删除评论 */
    deleteComment(commentID) {
      this.$confirm('此操作将永久删除该评论, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        let meta = await deleteComment({commentID});
        if (meta.status !== 200) return this.$message.error(meta.msg);
        else {
          await this.getAllComments();
          this.$message.success('成功删除评论');
        }
      }).catch(() => this.$message.info("已经取消删除"));
    },

    /* 获取全部评论 */
    async getAllComments() {
      this.commentList = await getAllComments();
    },

    /* 根据搜索方式查询评论 */
    queryComments(keyword, searchType) {
      clearTimeout(this.timer);  //清除延迟执行
      /* 如果没有选择搜索类型不给过 */
      if (searchType === '') return;
      if (keyword !== '') {
        this.timer = setTimeout(async () => {
          let tempObj = {keyword, searchType};
          this.commentList = await queryCommentsBySearchType(tempObj);
        }, 500);
      } else this.getAllComments();

    },

    /* 重置搜索 */
    resetQueryInput() {
      if (this.keyword !== '') {
        this.keyword = '';
        this.getAllComments();
      }
    }

  }
}
</script>

<style scoped>
.el-select {
  width: 130px;
}
</style>