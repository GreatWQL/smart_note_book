<template>
  <div class="sidebar">
    <!-- 品牌区域 -->
    <div class="sidebar-header">
      <div class="brand-container" @click="handleBrandClick">
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
            @click="handleNavClick"
          >
            <div class="nav-icon dashboard">
              <span class="icon">📊</span>
            </div>
            <span class="nav-text">{{ t('nav.dashboard') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
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
            @click="handleNavClick"
          >
            <div class="nav-icon notes">
              <span class="icon">📝</span>
            </div>
            <span class="nav-text">{{ t('nav.notes') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
          </router-link>
          
          <router-link 
            to="/tasks" 
            class="nav-item"
            :class="{ active: isActive('/tasks') }"
            @click="handleNavClick"
          >
            <div class="nav-icon tasks">
              <span class="icon">✅</span>
            </div>
            <span class="nav-text">{{ t('nav.tasks') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
          </router-link>
          
          <router-link 
            to="/calendar" 
            class="nav-item"
            :class="{ active: isActive('/calendar') }"
            @click="handleNavClick"
          >
            <div class="nav-icon calendar">
              <span class="icon">📅</span>
            </div>
            <span class="nav-text">{{ t('nav.calendar') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
          </router-link>
          
          <router-link 
            to="/chat" 
            class="nav-item"
            :class="{ active: isActive('/chat') }"
            @click="handleNavClick"
          >
            <div class="nav-icon chat">
              <span class="icon">🤖</span>
            </div>
            <span class="nav-text">{{ t('nav.chat') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
          </router-link>
          
          <router-link 
            to="/focus" 
            class="nav-item"
            :class="{ active: isActive('/focus') }"
            @click="handleNavClick"
          >
            <div class="nav-icon focus">
              <span class="icon">⏰</span>
            </div>
            <span class="nav-text">{{ t('nav.focus') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
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
            @click="handleNavClick"
          >
            <div class="nav-icon settings">
              <span class="icon">⚙️</span>
            </div>
            <span class="nav-text">{{ t('nav.settings') }}</span>
            <div class="nav-indicator"></div>
            <div class="ripple-effect"></div>
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
    
    // 处理导航点击动效
    const handleNavClick = (event) => {
      const navItem = event.currentTarget
      const ripple = navItem.querySelector('.ripple-effect')
      
      // 移除之前的动画类
      ripple.classList.remove('ripple-active')
      
      // 获取点击位置
      const rect = navItem.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top
      
      // 设置波纹位置
      ripple.style.left = x + 'px'
      ripple.style.top = y + 'px'
      
      // 触发动画
      setTimeout(() => {
        ripple.classList.add('ripple-active')
      }, 10)
      
      // 添加点击反馈
      navItem.classList.add('nav-item-clicked')
      setTimeout(() => {
        navItem.classList.remove('nav-item-clicked')
      }, 200)
    }
    
    // 处理品牌区域点击
    const handleBrandClick = (event) => {
      const brandContainer = event.currentTarget
      brandContainer.classList.add('brand-clicked')
      setTimeout(() => {
        brandContainer.classList.remove('brand-clicked')
      }, 300)
    }
    
    return {
      activeMenu,
      isActive,
      t,
      handleNavClick,
      handleBrandClick
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.1) 0%, 
    rgba(118, 75, 162, 0.08) 25%,
    rgba(240, 147, 251, 0.06) 50%,
    rgba(67, 233, 123, 0.08) 75%,
    rgba(79, 172, 254, 0.1) 100%);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-right: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
    rgba(102, 126, 234, 0.03) 0%,
    rgba(240, 147, 251, 0.02) 25%,
    rgba(67, 233, 123, 0.03) 50%,
    rgba(79, 172, 254, 0.02) 75%,
    rgba(156, 39, 176, 0.03) 100%);
  pointer-events: none;
  animation: gradientShift 8s ease-in-out infinite;
}

/* 品牌区域 */
.sidebar-header {
  padding: var(--spacing-8) var(--spacing-6);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  position: relative;
  z-index: 2;
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.08) 0%, 
    rgba(240, 147, 251, 0.06) 100%);
}

.brand-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  cursor: pointer;
  padding: var(--spacing-2);
  border-radius: var(--border-radius-lg);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.brand-container:hover {
  background: rgba(102, 126, 234, 0.08);
  transform: scale(1.02);
}

.brand-container.brand-clicked {
  transform: scale(0.98);
  background: rgba(102, 126, 234, 0.15);
}

.brand-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--border-radius-xl);
  background: linear-gradient(135deg, 
    #667eea 0%, 
    #764ba2 25%,
    #f093fb 50%,
    #43e97b 75%,
    #4facfe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
  animation: iconGlow 3s ease-in-out infinite;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.brand-container:hover .brand-icon {
  transform: rotate(10deg) scale(1.1);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
}

.brand-container.brand-clicked .brand-icon {
  transform: rotate(-5deg) scale(0.95);
}

.brand-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shimmer 4s infinite;
}

.icon-gradient {
  font-size: 1.5rem;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.brand-text {
  flex: 1;
}

.brand-title {
  font-size: var(--font-size-xl);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #43e97b 75%, #4facfe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
  animation: textGlow 4s ease-in-out infinite;
}

.brand-subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: var(--spacing-1) 0 0 0;
  opacity: 0.8;
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
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin-bottom: var(--spacing-3);
  padding: 0 var(--spacing-3);
  opacity: 0.8;
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.12) 0%, 
    rgba(240, 147, 251, 0.08) 50%,
    rgba(67, 233, 123, 0.12) 100%);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item:hover {
  transform: translateX(6px) scale(1.02);
  border-color: rgba(102, 126, 234, 0.3);
  color: var(--text-primary);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
}

.nav-item.nav-item-clicked {
  transform: translateX(8px) scale(0.98);
  box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.nav-item.active {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.2) 0%, 
    rgba(240, 147, 251, 0.15) 50%,
    rgba(67, 233, 123, 0.2) 100%);
  border-color: rgba(102, 126, 234, 0.4);
  color: var(--text-primary);
  font-weight: 600;
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.25);
}

.nav-item.active::before {
  opacity: 1;
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: scaleY(1);
}

/* 波纹效果 */
.ripple-effect {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: radial-gradient(circle, 
    rgba(102, 126, 234, 0.6) 0%, 
    rgba(240, 147, 251, 0.4) 50%,
    transparent 70%);
  transform: scale(0);
  opacity: 0;
  pointer-events: none;
  z-index: 1;
}

.ripple-effect.ripple-active {
  animation: rippleAnimation 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes rippleAnimation {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  50% {
    transform: scale(2);
    opacity: 0.8;
  }
  100% {
    transform: scale(4);
    opacity: 0;
  }
}

.nav-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-base);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  z-index: 2;
}

.nav-icon .icon {
  font-size: 1.1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.nav-icon.dashboard {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.nav-icon.notes {
  background: linear-gradient(135deg, rgba(240, 147, 251, 0.25) 0%, rgba(156, 39, 176, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
}

.nav-icon.tasks {
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.25) 0%, rgba(56, 178, 172, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.3);
}

.nav-icon.focus {
  background: linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(79, 172, 254, 0.3);
}

.nav-icon.calendar {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.25) 0%, rgba(255, 152, 0, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
}

.nav-icon.chat {
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.25) 0%, rgba(103, 58, 183, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(156, 39, 176, 0.3);
}

.nav-icon.settings {
  background: linear-gradient(135deg, rgba(250, 112, 154, 0.25) 0%, rgba(254, 118, 135, 0.2) 100%);
  box-shadow: 0 2px 8px rgba(250, 112, 154, 0.3);
}

.nav-item:hover .nav-icon {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.nav-item.nav-item-clicked .nav-icon {
  transform: scale(1.05) rotate(-3deg);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.5);
}

.nav-item.active .nav-icon {
  transform: scale(1.15);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.nav-text {
  flex: 1;
  position: relative;
  z-index: 2;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover .nav-text {
  transform: translateX(2px);
}

.nav-item.nav-item-clicked .nav-text {
  transform: translateX(4px);
}

.nav-indicator {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 4px;
  height: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border-radius: var(--border-radius-full);
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
}

/* 底部装饰 */
.sidebar-footer {
  padding: var(--spacing-6);
  position: relative;
  z-index: 2;
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.05) 0%, 
    rgba(240, 147, 251, 0.03) 100%);
}

.footer-decoration {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  opacity: 0.4;
}

.decoration-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(102, 126, 234, 0.6), 
    rgba(240, 147, 251, 0.6),
    rgba(67, 233, 123, 0.6),
    transparent);
  border-radius: var(--border-radius-full);
}

.decoration-dots {
  display: flex;
  gap: var(--spacing-2);
}

.decoration-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #43e97b 100%);
  animation: pulse 2s infinite;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
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
  0%, 100% { 
    opacity: 0.4; 
    transform: scale(1); 
    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
  }
  50% { 
    opacity: 1; 
    transform: scale(1.3); 
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.5);
  }
}

@keyframes gradientShift {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

@keyframes iconGlow {
  0%, 100% { 
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
  }
  50% { 
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
  }
}

@keyframes textGlow {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.1); }
}

/* 滚动条样式 */
.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-full);
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.6) 0%, 
    rgba(240, 147, 251, 0.6) 100%);
  border-radius: var(--border-radius-full);
  transition: all 0.3s ease;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.8) 0%, 
    rgba(240, 147, 251, 0.8) 100%);
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