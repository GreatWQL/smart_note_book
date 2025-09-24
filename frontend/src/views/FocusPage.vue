<template>
  <div class="focus-container">
    <SidebarNav />
    <div class="main-content">
      <div class="content-header">
        <h1>专注模式</h1>
        <el-button @click="showHistory = !showHistory">
          <el-icon><Clock /></el-icon>
          {{ showHistory ? '隐藏历史' : '查看历史' }}
        </el-button>
      </div>
      
      <div class="focus-content">
        <div class="focus-main">
          <FocusTimer />
        </div>
        
        <div v-if="showHistory" class="focus-history">
          <el-card>
            <template #header>
              <h3>专注历史</h3>
            </template>
            
            <div class="history-filters">
              <el-date-picker
                v-model="selectedDate"
                type="date"
                placeholder="选择日期"
                @change="loadHistory"
              />
              <el-select v-model="historyFilter" @change="loadHistory">
                <el-option label="全部" value="all" />
                <el-option label="已完成" value="completed" />
                <el-option label="未完成" value="incomplete" />
              </el-select>
            </div>
            
            <div class="history-stats">
              <div class="stat-card">
                <div class="stat-number">{{ historyStats.totalSessions }}</div>
                <div class="stat-label">总会话</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ historyStats.completedSessions }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ formatDuration(historyStats.totalTime) }}</div>
                <div class="stat-label">总时长</div>
              </div>
              <div class="stat-card">
                <div class="stat-number">{{ historyStats.completionRate }}%</div>
                <div class="stat-label">完成率</div>
              </div>
            </div>
            
            <div class="history-list">
              <div v-if="focusHistory.length === 0" class="empty-state">
                <el-empty description="暂无专注记录" />
              </div>
              <div v-else>
                <div
                  v-for="session in focusHistory"
                  :key="session.id"
                  class="history-item"
                >
                  <div class="session-info">
                    <div class="session-time">
                      {{ formatTime(session.created_at) }}
                    </div>
                    <div class="session-duration">
                      {{ session.duration }}分钟
                    </div>
                  </div>
                  <div class="session-status">
                    <el-tag :type="session.completed ? 'success' : 'warning'">
                      {{ session.completed ? '已完成' : '未完成' }}
                    </el-tag>
                  </div>
                  <div class="session-actions">
                    <el-button
                      type="text"
                      size="small"
                      @click="deleteSession(session)"
                    >
                      删除
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import SidebarNav from '@/components/SidebarNav.vue'
import FocusTimer from '@/components/FocusTimer.vue'
import request from '@/utils/request'

export default {
  name: 'FocusPage',
  components: {
    SidebarNav,
    FocusTimer
  },
  setup() {
    const showHistory = ref(false)
    const selectedDate = ref(new Date())
    const historyFilter = ref('all')
    const focusHistory = ref([])
    
    const historyStats = reactive({
      totalSessions: 0,
      completedSessions: 0,
      totalTime: 0,
      completionRate: 0
    })
    
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    }
    
    const formatDuration = (minutes) => {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      if (hours > 0) {
        return `${hours}h ${mins}m`
      }
      return `${mins}m`
    }
    
    const loadHistory = async () => {
      try {
        const dateStr = selectedDate.value.toISOString().split('T')[0]
        const response = await request.get(`/focus-sessions?date=${dateStr}`)
        let sessions = response.sessions || []
        
        // 应用过滤器
        if (historyFilter.value === 'completed') {
          sessions = sessions.filter(s => s.completed)
        } else if (historyFilter.value === 'incomplete') {
          sessions = sessions.filter(s => !s.completed)
        }
        
        focusHistory.value = sessions
        
        // 计算统计数据
        const allSessions = response.sessions || []
        historyStats.totalSessions = allSessions.length
        historyStats.completedSessions = allSessions.filter(s => s.completed).length
        historyStats.totalTime = allSessions.reduce((total, s) => {
          return total + (s.completed ? s.duration : 0)
        }, 0)
        historyStats.completionRate = historyStats.totalSessions > 0 
          ? Math.round((historyStats.completedSessions / historyStats.totalSessions) * 100)
          : 0
      } catch (error) {
        console.error('加载专注历史失败:', error)
      }
    }
    
    const deleteSession = async (session) => {
      try {
        await ElMessageBox.confirm('确定要删除这条专注记录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.delete(`/focus-sessions/${session.id}`)
        ElMessage.success('删除成功')
        loadHistory()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除专注记录失败:', error)
        }
      }
    }
    
    onMounted(() => {
      loadHistory()
    })
    
    return {
      showHistory,
      selectedDate,
      historyFilter,
      focusHistory,
      historyStats,
      formatTime,
      formatDuration,
      loadHistory,
      deleteSession
    }
  }
}
</script>

<style scoped>
.focus-container {
  display: flex;
  height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-header h1 {
  color: #303133;
  font-size: 24px;
  margin: 0;
}

.focus-content {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.focus-main {
  flex: 1;
  max-width: 500px;
}

.focus-history {
  flex: 1;
  min-width: 400px;
}

.history-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.history-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.history-list {
  max-height: 400px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.history-item:last-child {
  border-bottom: none;
}

.session-info {
  flex: 1;
}

.session-time {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.session-duration {
  font-size: 12px;
  color: #909399;
}

.session-status {
  margin: 0 16px;
}

.session-actions {
  flex-shrink: 0;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

@media (max-width: 768px) {
  .focus-content {
    flex-direction: column;
  }
  
  .focus-history {
    min-width: auto;
  }
  
  .history-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>