<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <div>
        <img src="~assets/logo.png" width="50" alt="">
        <span>校园新闻咨询后台系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
    <!-- 页面主题区 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px': '200px'">
        <!-- 菜单的折叠与展开 -->
        <div class="toggle-button" @click="isCollapse = !isCollapse">|||</div>
        <!-- 侧边栏菜单区 -->
        <el-menu
            background-color="#333744"
            text-color="#fff"
            active-text-color="#ffd04b"
            :collapse="isCollapse"
            :collapse-transition="false"
            router
            :default-active="activePath ? activePath : '/welcome'">
          <el-menu-item
              v-for="item in menuList"
              :index="'/'+item.path"
              :key="item.id">
            <i :class="item.icon"></i>
            <template #title>{{ item.tab }}</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- 右侧内容主题 -->
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      isCollapse: false,
      menuList: [
        {id: 1, tab: '欢迎！', path: 'welcome', icon: 'el-icon-star-on'},
        {id: 2, tab: '新闻管理', path: 'newsmanage', icon: 'el-icon-notebook-2'},
        {id: 3, tab: '评论管理', path: 'commentmanage', icon: 'el-icon-s-comment'},
        {id: 4, tab: '用户管理', path: 'usermanage', icon: 'el-icon-user'},
        {id: 5, tab: '我的账号', path: 'selfaccount', icon: 'el-icon-s-tools'}
      ],
      activePath: ''
    }
  },
  created() {
    this.activePath = this.$route.path;
  },
  methods: {
    logout() {
      window.sessionStorage.clear();
      this.$router.push('/login');
    }
  },
}
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 0;

  //.el-menu-item {
  //  display: flex;
  //  justify-content: center;
  //}
}

.home-container {
  height: 100%;
}

.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;

  div {
    display: flex;
    align-items: center;

    span {
      margin-left: 15px;
    }
  }
}

.el-aside {
  background-color: #333744;
}

.el-main {
  background-color: #eaedf1;
}

.toggle-button {
  background-color: #6b7486;
  color: #eee;
  font-size: 10px;
  line-height: 24px;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
</style>