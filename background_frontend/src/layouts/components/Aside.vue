<template>
  <el-aside>
    <!-- 菜单的折叠与展开 -->
    <div class="logo-box">
      <div class="website-name" v-show="!isCollapse">NewsAggregator</div>
      <el-icon :size="25" color="#409eff" @click="onCollapse">
        <Expand class="expand"/>
      </el-icon>
    </div>
    <Menu :isCollapse="isCollapse"/>
  </el-aside>
</template>

<script setup>
import Menu from '/layouts/components/menu/Menu.vue'
import {onBeforeMount, ref} from 'vue'

/* 菜单栏折叠所需 */
let isCollapse = ref(true)
let menuWidth = ref('')
let iconDeg = ref('')
let logoBoxJustifyContent = ref('')

function switchAsideStyle(isCollapse) {
  menuWidth.value = isCollapse ? '64px' : '260px'
  iconDeg.value = isCollapse ? '0' : '180deg'
  logoBoxJustifyContent.value = isCollapse ? 'center' : 'space-between'
}
onBeforeMount(() => {
  switchAsideStyle(isCollapse.value)
})
const onCollapse = () => {
  isCollapse.value = !isCollapse.value
  switchAsideStyle(isCollapse.value)
}
</script>

<style lang="scss" scoped>
.logo-box {
  height: 50px;
  box-sizing: border-box;
  padding: 13.5px;
  display: flex;
  justify-content: v-bind(logoBoxJustifyContent);
  align-items: center;

  .website-name {
    color: #409eff;
    font-weight: bolder;
    font-size: 20px;
    line-height: 25px;
    cursor: default;
  }

  .expand {
    transition: transform 300ms ease;
    transform: rotateY(v-bind(iconDeg));
  }
}

.el-aside {
  transition: width 300ms ease;
  width: v-bind(menuWidth);
}
</style>