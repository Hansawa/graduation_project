<template>
  <div id="newsManage">
    <!-- 面包屑导航 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/newsmanage' }">新闻管理</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区域 -->
    <el-card>
      <b><p style="font-size: 18px">新闻列表</p></b>
      <el-row :gutter="10">
        <el-col :span="10">
          <div>
            <!-- @也可以绑定Element的事件 -->
            <!-- 查询新闻输入框 -->
            <el-input placeholder="搜索新闻内容" v-model="keyword" @input="queryNews(keyword)" prefix-icon="el-icon-search">
              <template #append>
                <el-button type="info" @click="resetQueryInput(keyword)">重 置</el-button>
              </template>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="showAddNewsDiag">添加新闻</el-button>
        </el-col>
      </el-row>
      <!-- 新闻列表框架 -->
      <el-table
          :data="newsList"
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
            prop="newsContent"
            label="新闻内容">
        </el-table-column>
        <el-table-column
            prop="newsType"
            label="新闻类型">
        </el-table-column>
        <el-table-column
            prop="newsTime"
            label="发布时间">
        </el-table-column>
        <el-table-column width="170" label="操作">
          <!-- 作用域插槽，可以获取该行的全部数据 -->
          <template v-slot="scope">
            <!-- 修改按钮 -->
            <el-button size="mini" type="primary" icon="el-icon-edit"
                       @click="showEditDialog(scope.row.newsId)"></el-button>
            <!-- 添加按钮 -->
            <el-button size="mini" type="danger" icon="el-icon-delete"
                       @click="deleteNews(scope.row.newsId)"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加新闻对话框 -->
    <el-dialog
        title="添加新闻"
        v-model="addDialogVisible"
        width="50%"
        @close="resetAddNewsForm">
      <!-- 监听添加用户对话框的关闭事件 -->
      <!--  内容主体区  -->
      <!-- 表单需要设置表单对象，表单数据对象 -->
      <!-- 添加新闻表单 -->
      <el-form :model="addNewsForm" :rules="addNewsFormRules" ref="addNewsFormRef" label-width="100px">
        <el-form-item label="新闻内容" prop="newsContent">
          <el-input type="textarea" :autosize="{minRows: 5}" v-model="addNewsForm.newsContent"></el-input>
        </el-form-item>
        <el-form-item label="新闻类型" prop="newsType">
          <el-input v-model="addNewsForm.newsType"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <!--  底部区域  -->
        <span class="dialog-footer">
      <el-button @click="addDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="addNews">确 定</el-button>
    </span>
      </template>
    </el-dialog>

    <!-- 修改新闻对话框 -->
    <el-dialog
        title="修改新闻"
        v-model="editDialogVisible"
        width="50%">
      <!-- 修改新闻表单 -->
      <el-form :model="editNewsForm" :rules="editNewsFormRules" ref="editNewsFormRef" label-width="100px">
        <!-- prop属性值对应的是数据校验规则对象中的数据属性名 -->
        <el-form-item label="新闻内容" prop="newsContent">
          <el-input type="textarea" :autosize="{minRows: 5}" v-model="editNewsForm.newsContent"></el-input>
        </el-form-item>
        <el-form-item label="新闻类型" prop="newsType">
          <el-input v-model="editNewsForm.newsType"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
    <span class="dialog-footer">
      <el-button @click="editDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="editNews">确 定</el-button>
    </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import {getNewsList, addNews, queryNewsByNewsId, editNews, deleteNews} from "request/news";

export default {
  name: "NewsManage",

  /* 创建该组件后，先查询所有新闻 */
  created() {
    this.queryNews(this.keyword, this.pageSize);
  },

  data() {
    return {
      /* 控制添加新闻对话框的显示与隐藏 */
      addDialogVisible: false,
      /* 控制修改新闻对话框的显示与隐藏 */
      editDialogVisible: false,
      /* 查询关键字，空串时为查询全部新闻 */
      keyword: '',
      /* 存放查询后的新闻 */
      newsList: [],
      /* 添加新闻的表单数据 */
      addNewsForm: {
        newsContent: '',
        newsType: ''
      },
      /* 修改新闻的表单数据 */
      editNewsForm: {
        newsContent: '',
        newsType: '',
      },
      /* 添加新闻的表单数据校验规则 */
      addNewsFormRules: {
        newsContent: [
          {required: true, message: '请输入新闻内容', trigger: 'blur'}
        ],
        newsType: [
          {required: true, message: '请输入新闻类型', trigger: 'blur'}
        ]
      },
      /* 修改新闻的表单数据校验规则 */
      editNewsFormRules: {
        newsContent: [
          {required: true, message: '请输入新闻内容', trigger: 'blur'}
        ],
        newsType: [
          {required: true, message: '请输入新闻类型', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {

    /* 添加新新闻方法 */
    /* 预校验 */
    async addNews() {
      let valid = await this.$refs.addNewsFormRef.validate();
      if (valid === true) {
        let meta = await addNews(this.addNewsForm);
        if (meta.status !== 200)
          return this.$message.error(meta.msg);
        else {
          this.$message.success(meta.msg);
          this.newsList = await this.queryNews(this.keyword);
          this.addDialogVisible = false;
        }
      }
    },

    /* 显示添加新闻对话框方法 */
    showAddNewsDiag() {
      this.addDialogVisible = !this.addDialogVisible;
    },

    /* 重置添加新闻表单方法 */
    resetAddNewsForm() {
      this.$refs.addNewsFormRef.resetFields();
    },

    /* 删除新闻方法 */
    deleteNews(newsId) {
      this.$confirm('此操作将永久删除该新闻, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        let meta = await deleteNews({newsId});
        if (meta.status !== 200)
          return this.$message.error(meta.msg);
        else {
          await this.queryNews(this.keyword = '');
          this.$message.success('成功删除新闻');
        }
      }).catch(() => this.$message.info("已经取消删除"));
    },

    /* 查询新闻方法，隔段时间才发请求 */
    async queryNews(keyword) {
      clearTimeout(this.timer);  //清除延迟执行
      if (keyword !== '')
        this.timer = setTimeout(async () => {
          this.newsList = await getNewsList({keyword});
        }, 500);
      else
        this.newsList = await getNewsList({keyword});
    },

    /* 重置查询输入框方法 */
    resetQueryInput(keyword) {
      if (keyword !== '')
        this.queryNews(this.keyword = '');
    },

    /* 编辑新闻方法 */
    async editNews() {
      let valid = await this.$refs.editNewsFormRef.validate();
      if (valid === true) {
        let meta = await editNews(this.editNewsForm);
        if (meta.status !== 200)
          return this.$message.error(meta.msg);
        else {
          this.$message.success(meta.msg);
          await this.queryNews(this.keyword = '');
          this.editDialogVisible = !this.editDialogVisible;
        }
      }
    },

    /* 显示编辑新闻对话框与获取该行新闻数据方法 */
    async showEditDialog(newsId) {
      this.editNewsForm = await queryNewsByNewsId({newsId});
      this.editDialogVisible = !this.editDialogVisible;
    }
  }
}
</script>

<style lang="less" scoped>
</style>