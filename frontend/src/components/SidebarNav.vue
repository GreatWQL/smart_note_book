<template>
  <div class="sidebar">
    <!-- 品牌区域 -->
    <div class="sidebar-header">
      <div class="brand-container">
        <div class="brand-icon">
          <div class="icon-gradient">✨</div>
        </div>
        <div class="brand-text">
          <h2 class="brand-title">智能笔记本</h2>
          <p class="brand-subtitle">Smart Notebook</p>
        </div>
      </div>
    </div>
    
    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="section-title">工作台</div>
        <div class="nav-items">
          <router-link 
            to="/dashboard" 
            class="nav-item"
            :class="{ active: isActive('/dashboard') }"
          >
            <div class="nav-icon dashboard">
              <span class="icon">📊</span>
            </div>
            <span class="nav-text">{{ t('nav.dashboard') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
        </div>
      </div>

      <div class="nav-section">
        <div class="section-title">创作工具</div>
        <div class="nav-items">
          <router-link 
            to="/notes" 
            class="nav-item"
            :class="{ active: isActive('/notes') }"
          >
            <div class="nav-icon notes">
              <span class="icon">📝</span>
            </div>
            <span class="nav-text">{{ t('nav.notes') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
          
          <router-link 
            to="/tasks" 
            class="nav-item"
            :class="{ active: isActive('/tasks') }"
          >
            <div class="nav-icon tasks">
              <span class="icon">✅</span>
            </div>
            <span class="nav-text">{{ t('nav.tasks') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
          
          <router-link 
            to="/calendar" 
            class="nav-item"
            :class="{ active: isActive('/calendar') }"
          >
            <div class="nav-icon calendar">
              <span class="icon">📅</span>
            </div>
            <span class="nav-text">{{ t('nav.calendar') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
          
          <router-link 
            to="/chat" 
            class="nav-item"
            :class="{ active: isActive('/chat') }"
          >
            <div class="nav-icon chat">
              <span class="icon">🤖</span>
            </div>
            <span class="nav-text">{{ t('nav.chat') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
          
          <router-link 
            to="/focus" 
            class="nav-item"
            :class="{ active: isActive('/focus') }"
          >
            <div class="nav-icon focus">
              <span class="icon">⏰</span>
            </div>
            <span class="nav-text">{{ t('nav.focus') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
        </div>
      </div>

      <div class="nav-section">
        <div class="section-title">个人设置</div>
        <div class="nav-items">
          <router-link 
            to="/settings" 
            class="nav-item"
            :class="{ active: isActive('/settings') }"
          >
            <div class="nav-icon settings">
              <span class="icon">⚙️</span>
            </div>
            <span class="nav-text">{{ t('nav.settings') }}</span>
            <div class="nav-indicator"></div>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 底部装饰 -->
    <div class="sidebar-footer">
      <div class="footer-decoration">
        <div class="decoration-line"></div>
        <div class="decoration-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default {
  name: 'SidebarNav',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { t } = useI18n()
    
    const activeMenu = computed(() => {
      return route.path
    })
    
    const isActive = (path) => {
      return route.path === path || route.path.startsWith(path + '/')
    }
    
    return {
      activeMenu,
      isActive,
      t
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-primary);
  opacity: 0.05;
  pointer-events: none;
}

/* 品牌区域 */
.sidebar-header {
  padding: var(--spacing-8) var(--spacing-6);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 2;
}

.brand-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.brand-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--border-radius-xl);
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.brand-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 3s infinite;
}

.icon-gradient {
  font-size: 1.5rem;
  position: relative;
  z-index: 2;
}

.brand-text {
  flex: 1;
}

.brand-title {
  font-size: var(--font-size-xl);
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
}

.brand-subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: var(--spacing-1) 0 0 0;
  opacity: 0.7;
  font-weight: 500;
}

/* 导航区域 */
.sidebar-nav {
  flex: 1;
  padding: var(--spacing-4) var(--spacing-4);
  overflow-y: auto;
  position: relative;
  z-index: 2;
}

.nav-section {
  margin-bottom: var(--spacing-5);
}

.section-title {
  font-size: var(--font-size-xs);
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: var(--spacing-3);
  padding: 0 var(--spacing-3);
  opacity: 0.6;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-3) var(--spacing-3);
  border-radius: var(--border-radius-lg);
  text-decoration: none;
  color: var(--text-regular);
  font-weight: 500;
  font-size: var(--font-size-base);
  transition: var(--transition-base);
  position: relative;
  overflow: hidden;
  border: 1px solid transparent;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(102, 126, 234, 0.1);
  opacity: 0;
  transition: var(--transition-base);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item:hover {
  transform: translateX(4px);
  border-color: rgba(102, 126, 234, 0.2);
  color: var(--text-primary);
}

.nav-item.active {
  background: rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
  color: var(--text-primary);
  font-weight: 600;
}

.nav-item.active::before {
  opacity: 1;
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: scaleY(1);
}

.nav-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-base);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: var(--transition-base);
  flex-shrink: 0;
}

.nav-icon .icon {
  font-size: 1.1rem;
  transition: var(--transition-base);
}

.nav-icon.dashboard {
  background: rgba(102, 126, 234, 0.2);
}

.nav-icon.notes {
  background: rgba(240, 147, 251, 0.2);
}

.nav-icon.tasks {
  background: rgba(67, 233, 123, 0.2);
}

.nav-icon.focus {
  background: rgba(79, 172, 254, 0.2);
}

.nav-icon.calendar {
  background: rgba(255, 193, 7, 0.2);
}

.nav-icon.chat {
  background: rgba(156, 39, 176, 0.2);
}

.nav-icon.settings {
  background: rgba(250, 112, 154, 0.2);
}

.nav-item:hover .nav-icon {
  transform: scale(1.1);
}

.nav-item.active .nav-icon {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.nav-text {
  flex: 1;
  position: relative;
  z-index: 2;
}

.nav-indicator {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 3px;
  height: 20px;
  background: var(--gradient-primary);
  border-radius: var(--border-radius-full);
  opacity: 0;
  transition: var(--transition-base);
}

/* 底部装饰 */
.sidebar-footer {
  padding: var(--spacing-6);
  position: relative;
  z-index: 2;
}

.footer-decoration {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  opacity: 0.3;
}

.decoration-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--text-secondary), transparent);
}

.decoration-dots {
  display: flex;
  gap: var(--spacing-2);
}

.decoration-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--text-secondary);
  animation: pulse 2s infinite;
}

.decoration-dots span:nth-child(2) {
  animation-delay: 0.3s;
}

.decoration-dots span:nth-child(3) {
  animation-delay: 0.6s;
}

/* 动画 */
@keyframes shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* 滚动条样式 */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-full);
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .sidebar {
    width: 260px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .brand-container {
    gap: var(--spacing-3);
  }
  
  .brand-icon {
    width: 40px;
    height: 40px;
  }
  
  .brand-title {
    font-size: var(--font-size-lg);
  }
  
  .nav-item {
    padding: var(--spacing-3);
  }
  
  .nav-icon {
    width: 35px;
    height: 35px;
  }
}

@media (max-width: 480px) {
  .sidebar-header {
    padding: var(--spacing-6) var(--spacing-4);
  }
  
  .sidebar-nav {
    padding: var(--spacing-4) var(--spacing-3);
  }
  
  .nav-section {
    margin-bottom: var(--spacing-6);
  }
}
</style>