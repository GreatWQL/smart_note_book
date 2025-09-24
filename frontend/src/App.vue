<template>
  <div id="app" class="page-container">
    <!-- 护眼背景组件 -->
    <EyeCareBackground />
    <div class="page-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import EyeCareBackground from '@/components/EyeCareBackground.vue'

export default {
  name: 'App',
  components: {
    EyeCareBackground
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  height: 100vh;
}
</style>