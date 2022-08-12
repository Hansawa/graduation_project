<template>
  <template>
    <el-container class="home-container">
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px': '200px'">
        <!-- 菜单的折叠与展开 -->
        <div class="toggle-button" @click="isCollapse = !isCollapse">
          <el-icon><Expand /></el-icon>
        </div>
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
            <el-icon><component :is="item.icon" /></el-icon>
            <template #title>{{ item.tab }}</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- 页面主题区 -->
      <el-container>
        <!-- 头部区域 -->
        <el-header>
          <div>
            <img :src="logoImgUrl" width="50" alt="">
            <span>新闻聚合后台系统</span>
          </div>
          <el-button type="info" @click="logout">退出</el-button>
        </el-header>
        <!-- 右侧内容主题 -->
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </template>