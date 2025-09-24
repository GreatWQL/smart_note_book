<template>
  <div class="theme-toggle">
    <el-dropdown @command="handleThemeChange">
      <el-button circle>
        <el-icon>
          <component :is="currentThemeIcon" />
        </el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item 
            command="light" 
            :class="{ active: currentTheme === 'light' }"
          >
            <el-icon><Sunny /></el-icon>
            浅色主题
          </el-dropdown-item>
          <el-dropdown-item 
            command="dark" 
            :class="{ active: currentTheme === 'dark' }"
          >
            <el-icon><Moon /></el-icon>
            深色主题
          </el-dropdown-item>
          <el-dropdown-item 
            command="auto" 
            :class="{ active: currentTheme === 'auto' }"
          >
            <el-icon><Monitor /></el-icon>
            跟随系统
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { Sunny, Moon, Monitor } from '@element-plus/icons-vue'

export default {
  name: 'ThemeToggle',
  components: {
    Sunny,
    Moon,
    Monitor
  },
  setup() {
    const currentTheme = ref('light')
    const systemTheme = ref('light')
    
    const currentThemeIcon = computed(() => {
      if (currentTheme.value === 'auto') {
        return systemTheme.value === 'dark' ? Moon : Sunny
      }
      return currentTheme.value === 'dark' ? Moon : Sunny
    })
    
    const actualTheme = computed(() => {
      if (currentTheme.value === 'auto') {
        return systemTheme.value
      }
      return currentTheme.value
    })
    
    const applyTheme = (theme) => {
      const html = document.documentElement
      
      // 移除所有主题类
      html.classList.remove('light-theme', 'dark-theme')
      
      // 添加对应主题类
      html.classList.add(`${theme}-theme`)
      
      // 设置CSS变量
      if (theme === 'dark') {
        html.style.setProperty('--el-bg-color', '#1a1a1a')
        html.style.setProperty('--el-bg-color-page', '#0a0a0a')
        html.style.setProperty('--el-text-color-primary', '#e5eaf3')
        html.style.setProperty('--el-text-color-regular', '#cfd3dc')
        html.style.setProperty('--el-text-color-secondary', '#a3a6ad')
        html.style.setProperty('--el-text-color-placeholder', '#8d9095')
        html.style.setProperty('--el-border-color', '#4c4d4f')
        html.style.setProperty('--el-border-color-light', '#414243')
        html.style.setProperty('--el-border-color-lighter', '#363637')
        html.style.setProperty('--el-border-color-extra-light', '#2b2b2c')
        html.style.setProperty('--el-fill-color', '#303133')
        html.style.setProperty('--el-fill-color-light', '#262727')
        html.style.setProperty('--el-fill-color-lighter', '#1d1e1f')
        html.style.setProperty('--el-fill-color-extra-light', '#191a1b')
        html.style.setProperty('--el-fill-color-blank', '#141414')
        html.style.setProperty('--el-color-primary', '#409eff')
        html.style.setProperty('--el-color-success', '#67c23a')
        html.style.setProperty('--el-color-warning', '#e6a23c')
        html.style.setProperty('--el-color-danger', '#f56c6c')
        html.style.setProperty('--el-color-info', '#909399')
      } else {
        // 恢复默认浅色主题
        html.style.removeProperty('--el-bg-color')
        html.style.removeProperty('--el-bg-color-page')
        html.style.removeProperty('--el-text-color-primary')
        html.style.removeProperty('--el-text-color-regular')
        html.style.removeProperty('--el-text-color-secondary')
        html.style.removeProperty('--el-text-color-placeholder')
        html.style.removeProperty('--el-border-color')
        html.style.removeProperty('--el-border-color-light')
        html.style.removeProperty('--el-border-color-lighter')
        html.style.removeProperty('--el-border-color-extra-light')
        html.style.removeProperty('--el-fill-color')
        html.style.removeProperty('--el-fill-color-light')
        html.style.removeProperty('--el-fill-color-lighter')
        html.style.removeProperty('--el-fill-color-extra-light')
        html.style.removeProperty('--el-fill-color-blank')
        html.style.removeProperty('--el-color-primary')
        html.style.removeProperty('--el-color-success')
        html.style.removeProperty('--el-color-warning')
        html.style.removeProperty('--el-color-danger')
        html.style.removeProperty('--el-color-info')
      }
    }
    
    const detectSystemTheme = () => {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        systemTheme.value = 'dark'
      } else {
        systemTheme.value = 'light'
      }
    }
    
    const handleThemeChange = (theme) => {
      currentTheme.value = theme
      localStorage.setItem('theme', theme)
    }
    
    const loadSavedTheme = () => {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme && ['light', 'dark', 'auto'].includes(savedTheme)) {
        currentTheme.value = savedTheme
      }
    }
    
    // 监听系统主题变化
    const setupSystemThemeListener = () => {
      if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        mediaQuery.addEventListener('change', detectSystemTheme)
        
        // 返回清理函数
        return () => {
          mediaQuery.removeEventListener('change', detectSystemTheme)
        }
      }
    }
    
    // 监听主题变化并应用
    watch(actualTheme, (newTheme) => {
      applyTheme(newTheme)
    }, { immediate: true })
    
    onMounted(() => {
      detectSystemTheme()
      loadSavedTheme()
      setupSystemThemeListener()
    })
    
    return {
      currentTheme,
      currentThemeIcon,
      handleThemeChange
    }
  }
}
</script>

<style scoped>
.theme-toggle {
  display: inline-block;
}

:deep(.el-dropdown-menu__item.active) {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>

<style>
/* 全局主题样式 */
.dark-theme {
  color-scheme: dark;
}

.light-theme {
  color-scheme: light;
}

/* 深色主题下的自定义样式 */
.dark-theme .dashboard-container,
.dark-theme .main-content {
  background-color: var(--el-bg-color-page);
  color: var(--el-text-color-primary);
}

.dark-theme .el-card {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
}

.dark-theme .sidebar-nav {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
}

.dark-theme .el-menu {
  background-color: var(--el-bg-color);
}

.dark-theme .el-menu-item {
  color: var(--el-text-color-regular);
}

.dark-theme .el-menu-item:hover {
  background-color: var(--el-fill-color-light);
}

.dark-theme .el-menu-item.is-active {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

/* 滚动条样式 */
.dark-theme ::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.dark-theme ::-webkit-scrollbar-track {
  background: var(--el-fill-color-lighter);
}

.dark-theme ::-webkit-scrollbar-thumb {
  background: var(--el-fill-color);
  border-radius: 4px;
}

.dark-theme ::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color);
}
</style>