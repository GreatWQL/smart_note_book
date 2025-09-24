<template>
  <div class="dashboard-container">
    <!-- 动态背景效果 -->
    <div class="wave-effect"></div>
    <!-- 扫描线效果 -->
    <div class="scan-line"></div>
    
    <!-- 主体内容区域 -->
    <div class="content-wrapper">
      <!-- 顶部导航栏 -->
      <div class="topbar">
      <div class="topbar-left">
        <div class="app-logo-new">
          <!-- 优化后的现代科技风格Logo -->
          <svg width="200" height="50" viewBox="0 0 200 50" xmlns="http://www.w3.org/2000/svg" style="overflow: visible;">
            <defs>
              <!-- 主渐变 -->
              <linearGradient id="primaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#5b21b6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#ec4899;stop-opacity:1" />
              </linearGradient>
              
              <!-- 次要渐变 -->
              <linearGradient id="secondaryGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
              </linearGradient>
              
              <!-- 发光效果 -->
              <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
              
              <!-- 阴影效果 -->
              <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="1" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.2"/>
              </filter>
            </defs>
            
            <!-- 主图标 - 抽象的智能大脑/网络 -->
            <g transform="translate(10, 10)">
              <!-- 中心核心 -->
              <circle cx="15" cy="15" r="8" fill="url(#primaryGradient)" filter="url(#glow)" opacity="0.9"/>
              
              <!-- 环绕的智能节点 -->
              <circle cx="5" cy="8" r="3" fill="#00d4ff" opacity="0.7">
                <animate attributeName="r" values="3;4;3" dur="2s" repeatCount="indefinite"/>
              </circle>
              <circle cx="25" cy="6" r="2.5" fill="#5b21b6" opacity="0.8">
                <animate attributeName="r" values="2.5;3.5;2.5" dur="2.5s" repeatCount="indefinite"/>
              </circle>
              <circle cx="28" cy="20" r="3.5" fill="#ec4899" opacity="0.6">
                <animate attributeName="r" values="3.5;4.5;3.5" dur="3s" repeatCount="indefinite"/>
              </circle>
              <circle cx="8" cy="25" r="2.8" fill="#06b6d4" opacity="0.7">
                <animate attributeName="r" values="2.8;3.8;2.8" dur="2.2s" repeatCount="indefinite"/>
              </circle>
              
              <!-- 连接线网络 -->
              <path d="M 8 11 Q 15 15 22 9" stroke="url(#secondaryGradient)" stroke-width="1.5" fill="none" opacity="0.6"/>
              <path d="M 12 18 Q 20 22 25 17" stroke="url(#secondaryGradient)" stroke-width="1.5" fill="none" opacity="0.6"/>
              <path d="M 7 15 Q 15 10 23 15" stroke="url(#secondaryGradient)" stroke-width="1.5" fill="none" opacity="0.6"/>
              
              <!-- 数据流动效果 -->
              <circle r="1" fill="#00d4ff" opacity="0.8">
                <animateMotion dur="3s" repeatCount="indefinite">
                  <path d="M 8 11 Q 15 15 22 9"/>
                </animateMotion>
              </circle>
              <circle r="0.8" fill="#ec4899" opacity="0.8">
                <animateMotion dur="4s" repeatCount="indefinite">
                  <path d="M 12 18 Q 20 22 25 17"/>
                </animateMotion>
              </circle>
            </g>
            
            <!-- 几何装饰元素 -->
            <g transform="translate(50, 12)">
              <!-- 六边形 -->
              <polygon points="0,8 4,4 12,4 16,8 12,12 4,12" fill="none" stroke="url(#primaryGradient)" stroke-width="1" opacity="0.5"/>
              <!-- 三角形 -->
              <polygon points="20,6 26,6 23,12" fill="url(#secondaryGradient)" opacity="0.4"/>
              <!-- 菱形 -->
              <polygon points="30,8 34,4 38,8 34,12" fill="none" stroke="#00d4ff" stroke-width="1" opacity="0.6">
                <animateTransform attributeName="transform" type="rotate" values="0 34 8;360 34 8" dur="8s" repeatCount="indefinite"/>
              </polygon>
            </g>
            
            <!-- 文字部分 -->
            <text x="100" y="22" font-family="'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif" 
                  font-size="16" font-weight="700" fill="url(#primaryGradient)" filter="url(#glow)">
              智能笔记本
            </text>
            <text x="100" y="36" font-family="'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif" 
                  font-size="10" font-weight="400" fill="#64748b" opacity="0.8">
              AI-Powered Notebook
            </text>
            
            <!-- 右侧装饰粒子 - 调整位置确保在viewBox内 -->
            <g opacity="0.7">
              <circle cx="175" cy="10" r="1.5" fill="#00d4ff">
                <animate attributeName="cy" values="10;14;10" dur="2s" repeatCount="indefinite"/>
              </circle>
              <circle cx="180" cy="18" r="1" fill="#5b21b6">
                <animate attributeName="cx" values="180;184;180" dur="3s" repeatCount="indefinite"/>
              </circle>
              <circle cx="178" cy="30" r="1.2" fill="#ec4899">
                <animate attributeName="opacity" values="0.3;0.9;0.3" dur="2.5s" repeatCount="indefinite"/>
              </circle>
              <rect x="185" y="25" width="2" height="2" fill="#06b6d4" opacity="0.6">
                <animateTransform attributeName="transform" type="rotate" values="0 186 26;45 186 26;0 186 26" dur="4s" repeatCount="indefinite"/>
              </rect>
              
              <!-- 额外的装饰元素 -->
              <circle cx="190" cy="12" r="0.8" fill="#00d4ff" opacity="0.5">
                <animate attributeName="r" values="0.8;1.2;0.8" dur="3.5s" repeatCount="indefinite"/>
              </circle>
              <polygon points="192,35 194,32 196,35 194,38" fill="#8b5cf6" opacity="0.4">
                <animateTransform attributeName="transform" type="rotate" values="0 194 35;180 194 35;0 194 35" dur="6s" repeatCount="indefinite"/>
              </polygon>
            </g>
          </svg>
        </div>
      </div>
      
      <div class="topbar-center">
        <nav class="topbar-nav">
          <router-link to="/notes" class="nav-link">
            <i class="nav-icon">🚀</i>
            <span>笔记</span>
          </router-link>
          <router-link to="/tasks" class="nav-link">
            <i class="nav-icon">⚡</i>
            <span>任务</span>
          </router-link>
          <router-link to="/focus" class="nav-link">
            <i class="nav-icon">🎯</i>
            <span>专注</span>
          </router-link>
        </nav>
      </div>
      
      <div class="topbar-right">
        <div class="account-module">
          <div class="account-info" @click="toggleAccountMenu">
            <div class="account-avatar">
              <span>{{ user?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
            </div>
            <div class="account-details">
              <div class="account-name">{{ user?.username || '用户' }}</div>
              <div class="account-status">在线</div>
            </div>
            <i class="dropdown-icon">▼</i>
          </div>
          
          <div v-if="showAccountMenu" class="account-dropdown">
            <div class="dropdown-item" @click="switchAccount">
              <i class="item-icon">👤</i>
              <span>切换账户</span>
            </div>
            <div class="dropdown-item" @click="accountSettings">
              <i class="item-icon">⚙️</i>
              <span>账户设置</span>
            </div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item logout-item" @click="handleLogout">
              <i class="item-icon">👋</i>
              <span>退出登录</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 侧边栏导航 -->
      <SidebarNav />
      
      <div class="main-content">
      <!-- 科技感粒子背景 -->
      <div class="tech-particles">
        <div class="particle" v-for="n in 20" :key="n" :style="getParticleStyle(n)"></div>
      </div>
      

      
      <!-- 欢迎区域 -->
      <div class="welcome-section">
        <div class="welcome-content">
          <!-- 左侧文本内容 -->
          <div class="welcome-left">
            <div class="welcome-text">
              <h1 class="welcome-title">Hello，{{ user?.username || '用户' }}！</h1>
              <p class="welcome-subtitle">今天是个美好的一天，让我们开始高效工作吧 ✨</p>
            </div>
          </div>
          
          <!-- 右侧功能区域 -->
          <div class="welcome-right">
            <div class="time-display-container">
              <TimeDisplay />
            </div>
            <div class="welcome-actions">
              <!-- 三个按钮已移动到侧边栏快速操作区域 -->
            </div>
          </div>
        </div>
      </div>

      <!-- 统计卡片区域 -->
      <div class="stats-section">
        <div class="stats-grid">
          <div class="stat-card gradient-card-1 fade-in" style="animation-delay: 0.1s">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="icon-large">📚</i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.notesCount }}</div>
                <div class="stat-label">笔记总数</div>
                <div class="stat-trend">+{{ Math.floor(Math.random() * 5) + 1 }} 本周</div>
              </div>
            </div>
            <div class="stat-decoration">
              <div class="decoration-circle"></div>
              <div class="decoration-dots"></div>
            </div>
          </div>

          <div class="stat-card gradient-card-2 fade-in" style="animation-delay: 0.2s">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="icon-large">📋</i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ stats.tasksCount }}</div>
                <div class="stat-label">待办任务</div>
                <div class="stat-trend">{{ completedToday }} 今日完成</div>
              </div>
            </div>
            <div class="stat-decoration">
              <div class="decoration-circle"></div>
              <div class="decoration-dots"></div>
            </div>
          </div>

          <div class="stat-card gradient-card-3 fade-in" style="animation-delay: 0.3s">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="icon-large">🎯</i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ Math.floor(stats.focusTime / 60) }}</div>
                <div class="stat-label">专注小时</div>
                <div class="stat-trend">{{ stats.focusTime % 60 }}分钟 今日</div>
              </div>
            </div>
            <div class="stat-decoration">
              <div class="decoration-circle"></div>
              <div class="decoration-dots"></div>
            </div>
          </div>

          <div class="stat-card gradient-card-4 fade-in" style="animation-delay: 0.4s">
            <div class="stat-content">
              <div class="stat-icon">
                <i class="icon-large">🔥</i>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ streakDays }}</div>
                <div class="stat-label">连续天数</div>
                <div class="stat-trend">保持专注</div>
              </div>
            </div>
            <div class="stat-decoration">
              <div class="decoration-circle"></div>
              <div class="decoration-dots"></div>
            </div>
          </div>
        </div>
      </div>



      <!-- 最近活动区域 - 移动到上方 -->
      <div class="activity-section">
        <div class="activity-grid">
          <!-- 最近笔记 -->
          <div class="activity-card card slide-up" style="animation-delay: 0.8s">
            <div class="card-header">
              <h3>📝 最近笔记</h3>
              <router-link to="/notes" class="view-all-link">查看全部</router-link>
            </div>
            <div class="activity-content">
              <div v-if="recentNotes.length === 0" class="empty-state">
                <div class="empty-icon">📄</div>
                <p>还没有笔记，开始记录你的想法吧！</p>
                <button class="create-btn" @click="$router.push('/notes')">创建第一篇笔记</button>
              </div>
              <div v-else class="activity-list">
                <div
                  v-for="note in recentNotes.slice(0, 4)"
                  :key="note.id"
                  class="activity-item"
                  @click="$router.push(`/notes/${note.id}`)"
                >
                  <div class="item-icon">📝</div>
                  <div class="item-content">
                    <div class="item-title">{{ note.title }}</div>
                    <div class="item-meta">{{ formatTime(note.updated_at) }}</div>
                  </div>
                  <div class="item-arrow">→</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 待办任务 -->
          <div class="activity-card card slide-up" style="animation-delay: 0.9s">
            <div class="card-header">
              <h3>✅ 待办任务</h3>
              <router-link to="/tasks" class="view-all-link">查看全部</router-link>
            </div>
            <div class="activity-content">
              <div v-if="pendingTasks.length === 0" class="empty-state">
                <div class="empty-icon">✨</div>
                <p>太棒了！没有待办任务</p>
                <button class="create-btn" @click="$router.push('/tasks')">添加新任务</button>
              </div>
              <div v-else class="activity-list">
                <div
                  v-for="task in pendingTasks.slice(0, 4)"
                  :key="task.id"
                  class="activity-item"
                  @click="$router.push('/tasks')"
                >
                  <div class="item-icon" :class="`priority-${task.priority}`">
                    {{ getPriorityIcon(task.priority) }}
                  </div>
                  <div class="item-content">
                    <div class="item-title">{{ task.title }}</div>
                    <div class="item-meta">{{ getPriorityText(task.priority) }}优先级</div>
                  </div>
                  <div class="item-arrow">→</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 提醒管理 -->
          <div class="activity-card card slide-up" style="animation-delay: 1.0s">
            <div class="card-header">
              <h3>🔔 提醒中心</h3>
            </div>
            <div class="activity-content">
              <ReminderManager />
            </div>
          </div>
        </div>
      </div>


    </div>
    </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import ReminderManager from '@/components/ReminderManager.vue'
import SidebarNav from '@/components/SidebarNav.vue'
import WeatherWidget from '@/components/WeatherWidget.vue'
import SimpleWeather from '@/components/SimpleWeather.vue'
import TimeDisplay from '@/components/TimeDisplay.vue'
import request from '@/utils/request'
import { getUser, clearAuth } from '@/utils/auth'

export default {
  name: 'DashboardPage',
 components: {
    ReminderManager,
    WeatherWidget,
    SimpleWeather,
    TimeDisplay
  },
  setup() {
    const router = useRouter()
    const user = ref(getUser())
    
    const stats = reactive({
      notesCount: 0,
      tasksCount: 0,
      focusTime: 0
    })
    
    const recentNotes = ref([])
    const pendingTasks = ref([])
    const completedToday = ref(0)
    const streakDays = ref(7) // 模拟连续天数
    
    const loadDashboardData = async () => {
      try {
        // 加载笔记数据
        const notesResponse = await request.get('/notes')
        const notes = notesResponse.notes || []
        stats.notesCount = notes.length
        recentNotes.value = notes.slice(0, 5)
        
        // 加载任务数据
        const tasksResponse = await request.get('/tasks')
        const tasks = tasksResponse.tasks || []
        const todoTasks = tasks.filter(task => task.status === 'todo')
        stats.tasksCount = todoTasks.length
        pendingTasks.value = todoTasks.slice(0, 5)
        
        // 加载专注时长数据
        const focusResponse = await request.get('/focus-sessions')
        const sessions = focusResponse.focus_sessions || []
        stats.focusTime = sessions.reduce((total, session) => total + session.duration_minutes, 0)
        
      } catch (error) {
        console.error('加载仪表盘数据失败:', error)
      }
    }
    
    const handleLogout = async () => {
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        clearAuth()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 用户取消
      }
    }
    
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
    
    const getPriorityText = (priority) => {
      const map = {
        low: '低',
        medium: '中',
        high: '高'
      }
      return map[priority] || '中'
    }
    
    const getPriorityIcon = (priority) => {
      const map = {
        low: '🟢',
        medium: '🟡',
        high: '🔴'
      }
      return map[priority] || '🟡'
    }
    
    onMounted(() => {
      loadDashboardData()
    })
    
    // 账户模块相关数据和方法
    const showAccountMenu = ref(false)
    
    const toggleAccountMenu = () => {
      showAccountMenu.value = !showAccountMenu.value
    }
    
    const switchAccount = () => {
      ElMessage.info('切换账户功能开发中...')
      showAccountMenu.value = false
    }
    
    const accountSettings = () => {
      router.push('/settings')
      showAccountMenu.value = false
    }
    
    // 科技感效果相关方法
    const getParticleStyle = (index) => {
      const size = Math.random() * 4 + 2
      const left = Math.random() * 100
      const top = Math.random() * 100
      const duration = Math.random() * 10 + 5
      const delay = Math.random() * 5
      
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        top: `${top}%`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`
      }
    }
    

    
    return {
      user,
      stats,
      recentNotes,
      pendingTasks,
      completedToday,
      streakDays,
      showAccountMenu,
      handleLogout,
      formatTime,
      getPriorityText,
      getPriorityIcon,
      toggleAccountMenu,
      switchAccount,
      accountSettings,
      getParticleStyle
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(-45deg, 
    #ffecd2 0%, 
    #fcb69f 25%, 
    #ffecd2 50%, 
    #a8edea 75%, 
    #fed6e3 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
}

.dashboard-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
    rgba(255, 182, 193, 0.3) 0%,
    rgba(173, 216, 230, 0.3) 25%,
    rgba(255, 218, 185, 0.3) 50%,
    rgba(221, 160, 221, 0.3) 75%,
    rgba(255, 182, 193, 0.3) 100%);
  background-size: 300% 300%;
  animation: gradientShift 20s ease infinite reverse;
  z-index: 0;
}

.dashboard-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, 
    rgba(255, 192, 203, 0.4) 0%,
    transparent 50%),
  radial-gradient(circle at 80% 20%, 
    rgba(173, 216, 230, 0.4) 0%,
    transparent 50%),
  radial-gradient(circle at 40% 40%, 
    rgba(255, 218, 185, 0.3) 0%,
    transparent 50%);
  animation: floatingBubbles 25s ease-in-out infinite;
  z-index: 0;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes floatingBubbles {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
    opacity: 0.9;
  }
  66% {
    transform: translateY(10px) rotate(240deg);
    opacity: 0.8;
  }
}

@keyframes sparkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes wave {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}



/* 添加光波效果 */
.dashboard-container .wave-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, 
    transparent 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%);
  animation: wave 8s ease-in-out infinite;
  z-index: 0;
}

.content-wrapper {
  display: flex;
  flex: 1;
  position: relative;
  z-index: 1;
  flex-direction: column;
}

.content-area {
  display: flex;
  flex: 1;
  position: relative;
}

/* 顶部导航栏样式 */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 var(--spacing-6);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  position: relative;
}

.topbar-left {
  display: flex;
  align-items: center;
}

.app-logo {
  display: flex;
  align-items: center;
  height: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.app-logo:hover {
  transform: scale(1.02);
  filter: brightness(1.1);
}

.app-logo svg {
  height: 100%;
  width: auto;
  max-width: 120px;
}

.topbar-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.topbar-nav {
  display: flex;
  gap: var(--spacing-1);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--border-radius-base);
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: var(--transition-base);
  position: relative;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: rgba(102, 126, 234, 0.15);
}

.nav-icon {
  font-size: 1.5rem;
}

.topbar-right {
  display: flex;
  align-items: center;
}

/* 账户模块样式 */
.account-module {
  position: relative;
}

.account-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-2) var(--spacing-3);
  border-radius: var(--border-radius-base);
  cursor: pointer;
  transition: var(--transition-base);
  border: 1px solid transparent;
}

.account-info:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.2);
}

.account-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: var(--font-size-sm);
}

.account-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.account-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  line-height: 1.2;
}

.account-status {
  font-size: var(--font-size-xs);
  color: var(--success-color);
  line-height: 1.2;
}

.dropdown-icon {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  transition: var(--transition-base);
}

.account-info:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 账户下拉菜单 */
.account-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: var(--spacing-2);
  min-width: 200px;
  background: var(--bg-color-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-base);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  animation: dropdownFadeIn 0.2s ease-out;
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  padding: var(--spacing-3) var(--spacing-4);
  cursor: pointer;
  transition: var(--transition-base);
  color: var(--text-primary);
}

.dropdown-item:hover {
  background: rgba(102, 126, 234, 0.1);
}

.dropdown-item.logout-item {
  color: var(--danger-color);
}

.dropdown-item.logout-item:hover {
  background: rgba(250, 112, 154, 0.1);
}

.item-icon {
  font-size: var(--font-size-base);
}

.dropdown-divider {
  height: 1px;
  background: var(--border-color);
  margin: var(--spacing-2) 0;
}

.main-content {
  width: 100%;
  padding: var(--spacing-6);
  overflow-y: auto;
  margin-top: 0; /* 移除顶部边距，因为现在有topbar */
  background: transparent;
  position: relative;
  z-index: 1;
  flex: 1;
}

/* 简化天气信息样式 */
.simple-weather-section {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: var(--spacing-8);
}

.welcome-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-6) var(--spacing-8);
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-radius: var(--border-radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
              0 4px 16px rgba(255, 255, 255, 0.2) inset;
  gap: var(--spacing-6);
  max-width: 1400px;
  margin: 0 auto;
  height: 180px;
  position: relative;
  z-index: 2;
}

.welcome-left {
  flex: 1;
  display: flex;
  align-items: center;
  height: 100%;
}

.welcome-text {
  text-align: left;
}

.welcome-title {
  font-size: var(--font-size-4xl);
  font-weight: 700;
  font-family: 'SF Pro Display', 'Helvetica Neue', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--spacing-3);
  line-height: 1.3;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.welcome-title:hover {
  transform: translateY(-1px);
  filter: brightness(1.1);
}

.welcome-subtitle {
  font-size: var(--font-size-lg);
  color: var(--text-regular);
  margin: 0;
  opacity: 0.8;
}

.welcome-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--spacing-6);
  flex-shrink: 0;
  height: 100%;
}

.time-display-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  background: rgba(250, 112, 154, 0.1);
  color: var(--text-primary);
  border: 1px solid rgba(250, 112, 154, 0.3);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition-bounce);
  backdrop-filter: blur(10px);
}

.logout-btn:hover {
  background: rgba(250, 112, 154, 0.2);
  border-color: rgba(250, 112, 154, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
}

.logout-btn .icon {
  font-size: var(--font-size-base);
}

.welcome-actions {
  display: flex;
  gap: var(--spacing-3);
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 400px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-3) var(--spacing-5);
  border-radius: var(--border-radius-full);
  font-weight: 600;
  font-size: var(--font-size-sm);
  transition: var(--transition-bounce);
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.action-btn.primary {
  background: var(--gradient-primary);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.action-btn.secondary {
  background: var(--gradient-secondary);
  color: white;
  box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
}

.action-btn.tertiary {
  background: var(--gradient-success);
  color: white;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  padding: var(--spacing-3) var(--spacing-4);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-full);
  color: var(--text-regular);
  font-weight: 500;
  font-size: var(--font-size-sm);
  transition: var(--transition-base);
  cursor: pointer;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.icon {
  font-size: var(--font-size-base);
}

/* 统计卡片区域 */
.stats-section {
  margin-bottom: var(--spacing-6);
}

.welcome-section {
  margin-bottom: var(--spacing-6);
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-6);
  margin-bottom: var(--spacing-6);
}



.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
  position: relative;
  z-index: 5;
}

.card-header h3 {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: var(--spacing-2);
  position: relative;
  z-index: 10;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-base);
  border: none;
  background: rgba(102, 126, 234, 0.1);
  color: var(--primary-color);
  cursor: pointer;
  transition: var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-base);
  position: relative;
  z-index: 11;
}

.icon-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}



.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

/* 天气卡片区域 */
.weather-section {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-6);
}

.weather-card {
  padding: var(--spacing-6);
  max-width: 400px;
  width: 100%;
}

/* 最近活动区域 */
.activity-section {
  margin-bottom: var(--spacing-6);
}



.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-6);
}

.activity-card {
  padding: var(--spacing-6);
}

.view-all-link {
  color: var(--primary-color);
  font-weight: 500;
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: var(--transition-base);
}

.view-all-link:hover {
  color: var(--primary-light);
  transform: translateY(-1px);
}

.activity-content {
  margin-top: var(--spacing-4);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-4);
}

.empty-state p {
  margin-bottom: var(--spacing-4);
  font-size: var(--font-size-base);
}

.create-btn {
  padding: var(--spacing-3) var(--spacing-6);
  background: var(--gradient-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius-full);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-bounce);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  padding: var(--spacing-4);
  border-radius: var(--border-radius-base);
  transition: var(--transition-base);
  cursor: pointer;
  border: 1px solid transparent;
}

.activity-item:hover {
  background: rgba(102, 126, 234, 0.05);
  border-color: rgba(102, 126, 234, 0.2);
  transform: translateX(4px);
}

.item-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-base);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-lg);
  background: rgba(102, 126, 234, 0.1);
  flex-shrink: 0;
}

.item-icon.priority-high {
  background: rgba(250, 112, 154, 0.2);
}

.item-icon.priority-medium {
  background: rgba(67, 233, 123, 0.2);
}

.item-icon.priority-low {
  background: rgba(79, 172, 254, 0.2);
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.item-arrow {
  color: var(--text-placeholder);
  font-weight: bold;
  transition: var(--transition-base);
}

.activity-item:hover .item-arrow {
  color: var(--primary-color);
  transform: translateX(4px);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar-section {
    flex-direction: row;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }
  
  .main-content {
    padding: var(--spacing-4);
  }
  
  .welcome-content {
    flex-direction: column;
    gap: var(--spacing-6);
    text-align: center;
    height: 160px;
    padding: var(--spacing-6);
  }
  
  .welcome-left {
    align-items: center;
  }
  
  .welcome-text {
    text-align: center;
  }
  
  .welcome-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-3);
  }
  
  .stat-card {
    height: 120px;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .activity-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar-section {
    flex-direction: column;
  }
  

  
  .welcome-title {
    font-size: var(--font-size-3xl);
  }
}

@media (max-width: 480px) {
  .welcome-content {
    height: 140px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-3);
  }
  
  .stat-card {
    height: 100px;
  }
  
  .stat-number {
    font-size: 1.2rem;
  }
  
  .stat-label {
    font-size: var(--font-size-xs);
  }
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-4);
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  position: relative;
  padding: var(--spacing-4);
  border-radius: var(--border-radius-xl);
  color: white;
  overflow: hidden;
  transition: var(--transition-base);
  cursor: pointer;
  height: 140px;
  display: flex;
  align-items: center;
}

.stat-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-2);
  width: 100%;
  text-align: center;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-xl);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  margin-bottom: var(--spacing-2);
}

.icon-large {
  font-size: 1.8rem;
}

.stat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: var(--spacing-1);
}

.stat-label {
  font-size: var(--font-size-sm);
  font-weight: 600;
  opacity: 0.9;
  margin-bottom: var(--spacing-1);
}

.stat-trend {
  font-size: var(--font-size-xs);
  opacity: 0.8;
  font-weight: 500;
}

.stat-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.decoration-circle {
  position: absolute;
  top: -50px;
  right: -50px;
  width: 150px;
  height: 150px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.decoration-dots {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 2px, transparent 2px);
  background-size: 15px 15px;
}

.stat-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: var(--box-shadow-hover);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-4);
  }
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-height: auto;
    height: auto;
    padding: var(--spacing-5);
  }
  
  .welcome-left {
    min-height: auto;
    margin-bottom: var(--spacing-4);
  }
  
  .welcome-right {
    flex-direction: column;
    gap: var(--spacing-4);
    width: 100%;
  }
  
  .welcome-actions {
    justify-content: center;
    max-width: none;
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-3);
  }
  
  .stat-card {
    height: 120px;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .activity-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar-section {
    flex-direction: column;
  }
  
  .welcome-title {
    font-size: var(--font-size-3xl);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-3);
  }
  
  .stat-card {
    height: 100px;
  }
  
  .stat-number {
    font-size: 1.2rem;
  }
  
  .stat-label {
    font-size: var(--font-size-xs);
  }
}

/* 科技感效果样式 */
.tech-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.particle {
  position: absolute;
  background: radial-gradient(circle, #00d4ff 0%, #0099cc 50%, transparent 70%);
  border-radius: 50%;
  opacity: 0.6;
  animation: particleFloat infinite linear;
  box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 30px #00d4ff;
}

@keyframes particleFloat {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) scale(1);
    opacity: 0;
  }
}







/* 为主要元素添加科技感发光效果 */
.welcome-content {
  border: 1px solid rgba(0, 212, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
              0 4px 16px rgba(255, 255, 255, 0.2) inset,
              0 0 20px rgba(0, 212, 255, 0.1);
  transition: all 0.3s ease;
}

.welcome-content:hover {
  border-color: rgba(0, 212, 255, 0.5);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 
              0 4px 16px rgba(255, 255, 255, 0.2) inset,
              0 0 30px rgba(0, 212, 255, 0.2);
}

.stat-card {
  border: 1px solid rgba(0, 255, 136, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: rgba(0, 255, 136, 0.4);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15),
              0 0 20px rgba(0, 255, 136, 0.1);
  transform: translateY(-2px);
}

/* 为时间显示添加科技感效果 */
.time-display {
  border: 1px solid rgba(0, 212, 255, 0.3);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3),
              0 0 20px rgba(0, 212, 255, 0.1);
  transition: all 0.3s ease;
}

.time-display:hover {
  border-color: rgba(0, 212, 255, 0.5);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3),
              0 0 30px rgba(0, 212, 255, 0.2);
}

/* 为导航链接添加科技感效果 */
.nav-link {
  transition: all 0.3s ease;
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  border-color: rgba(0, 212, 255, 0.3);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
  background: rgba(0, 212, 255, 0.05);
}

.nav-link.router-link-active {
  border-color: rgba(0, 212, 255, 0.5);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
  background: rgba(0, 212, 255, 0.1);
  animation: activePulse 2s infinite;
}

@keyframes activePulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
  }
}



/* 为按钮添加科技感效果 */
.btn-primary {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(0, 212, 255, 0.5);
  background: linear-gradient(135deg, 
    rgba(0, 212, 255, 0.1) 0%, 
    rgba(102, 126, 234, 0.1) 100%);
  transition: all 0.3s ease;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.3), 
    transparent);
  transition: left 0.6s ease;
}

.btn-primary:hover::before {
  left: 100%;
}

.btn-primary:hover {
  border-color: rgba(0, 212, 255, 0.8);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
  transform: translateY(-1px);
}

/* 为卡片添加简洁边框效果 */
.recent-notes, .pending-tasks {
  position: relative;
  border: 1px solid rgba(0, 255, 136, 0.2);
  transition: all 0.3s ease;
}

.recent-notes:hover, .pending-tasks:hover {
  border-color: rgba(0, 255, 136, 0.4);
  box-shadow: 0 4px 20px rgba(0, 255, 136, 0.1);
}

/* 为文本添加打字机效果 */
.welcome-title {
  position: relative;
  overflow: hidden;
}



/* 为统计数字添加数字滚动效果 */
.stat-number {
  position: relative;
  overflow: hidden;
  background: linear-gradient(45deg, #00d4ff, #00ff88);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: numberGlow 2s ease-in-out infinite alternate;
}

@keyframes numberGlow {
  0% {
    filter: brightness(1);
  }
  100% {
    filter: brightness(1.3);
  }
}

/* 天气信息区域 */
.weather-info-section {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
  pointer-events: auto;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--border-radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-4);
  min-width: 280px;
}

/* 为主容器添加科技感背景 */
.dashboard-container {
  position: relative;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(0, 255, 136, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(255, 0, 128, 0.02) 0%, transparent 50%);
}

/* 响应式调整天气信息区域 */
@media (max-width: 768px) {
  .weather-info-section {
    top: 10px;
    right: 10px;
    min-width: 240px;
    padding: var(--spacing-3);
  }
}

@media (max-width: 480px) {
  .weather-info-section {
    position: relative;
    top: auto;
    right: auto;
    margin: var(--spacing-4) auto;
    min-width: auto;
    width: calc(100% - 2 * var(--spacing-4));
  }
}
</style>